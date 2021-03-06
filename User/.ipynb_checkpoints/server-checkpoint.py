import os
import sys
import pandas as pd
import json
from threading import Thread
import time, random, requests
import DAN
import unitconversion, enspacy, zhckip, register

# define error message format:
# 1: rule1, 2: rule2, <0: error
# -2 error: no device in sentence
# -3 error: no device feature in sentence
# -4 error: device feature need value
# -5 error: D not support F

# ========iottalk================
ServerURL = 'http://140.113.199.246:9999'      #with non-secure connection
#ServerURL = 'https://DomainName' #with SSL connection
# for D+F






#==========flask as backend=============
from flask import Flask, render_template, request, jsonify, url_for
app = Flask(__name__)


#======== fast test method by sending text input=============
@app.route('/',methods=['POST','GET']) 
def index():
    returnlist = []
    tokenlist = ['','','','',-1]
    response = ''
    if(request.method == 'POST'):
        text = request.values['user']
        print(text)
        language = 'en-US'
        # use text to send for demo
        # add rule to check if chinese or english
        if(language == 'en-US'): #English
            enspacy.readDB()
            feature, tokenlist = enspacy.textParse(text) #spacy function
        else:  # chinese
            feature,tokenlist = zhckip.textParse(text,zhckip.ws,zhckip.pos,zhckip.ner) # ckiptagger function
        
        
        
        A = tokenlist[0]
        D = tokenlist[1]
        F = tokenlist[2]
        V = tokenlist[3]
        valid = tokenlist[4]
        
        thread = Thread(target=sendIot, args=(A,D,F,V,valid,language))
        thread.daemon = True
        thread.start()
        
        returnlist = tokenlist
        
        print("message bit:", valid)
        response = ''
        if(returnlist[4] == -1):
            response =  'I\'m sorry, try again.' if language == 'en-US' else '很抱歉，聽不懂請重講'
            returnlist = []
        else:
            response = 'OK, ' if language == 'en-US' else '收到，'
            returnlist[2] = feature
            if(returnlist[4] == 1): returnlist[3] = ''

    return render_template("index.html",returnlist=returnlist, response = response) # response message add here


@app.route('/ProcessSentence', methods = ['POST','GET'])
# prcoess setence from the frontend
# input is {voice, lang_id}
def ProcessSentence():
    returnlist = []
    sentence = request.args.get('sentence')
    language = request.args.get('language')
    print("voice sentence: ", sentence) #data should be decoded from bytestrem to utf-8
    
    if(language == 'en-US'): #English
        feature, tokenlist = enspacy.textParse(sentence) #spacy function
    else:  # chinese
        feature,tokenlist = zhckip.textParse(sentence,zhckip.ws,zhckip.pos,zhckip.ner) # ckiptagger function
    
    #get all token from the tokenlist
    A = tokenlist[0]
    D = tokenlist[1]
    F = tokenlist[2]
    V = tokenlist[3]
    valid = tokenlist[4] # valid bit: rule1: 1, rule2: 2, error 1: -1, error2: -2, etc.

    thread = Thread(target=sendIot, args=(A,D,F,V,valid,language)) # open thread to send signal to iottalk
    thread.daemon = True
    thread.start()

    returnlist = tokenlist
    response = '' # init response
    # complete the response context
    if(returnlist[4] < 0):
        response =  'I\'m sorry, try again.' if language == 'en-US' else '很抱歉，聽不懂請重講'
        returnlist = []
    else:
        response = 'OK, ' if language == 'en-US' else '收到，'
        returnlist[2] = feature  # feature is different from F
        if(returnlist[4] == 1): returnlist[3] = ''      # rule 1: no value(token 3) need
    print("source from voice", response, returnlist)
    
    
    return jsonify({ 'tokenlist': returnlist, 'response': response, 'valid':valid})



def sendIot(A,D,F,V,valid,lang):
    if(D !="" and valid >0 ): # D+F
        df = pd.read_csv('dict/ADF.txt')
        print('df info:', df, "searching", D)
        if(lang == "en-US"):
            df = df.loc[df['D_ens']==D]
        else:
            df = df.loc[df['D'] == D]
        print("remain df", df)
        deviceName = df.iloc[0]['D_en']
        deviceModel = df.iloc[0]['A_en']
        dfList = df.iloc[0]['DFlist']
        Regaddr = df.iloc[0]['Regaddr']
        dfList = eval(dfList)
        print(type(dfList))
        returnValue = V
        deviceFeature = F
        print("device name: ",deviceName,"device model: ", deviceModel)
        Reg_addr = Regaddr
        DAN.profile['d_name']= deviceName # search for device name 
        DAN.profile['dm_name']=deviceModel # use specific device model 
        DAN.profile['df_list']=dfList
        DAN.device_registration_with_retry(ServerURL, Reg_addr)
        DAN.push('Switch1', 1)
        if(deviceFeature == 'Luminance-I' or deviceFeature == 'ColorTemperature-I'):
            iotvalue = int(returnValue)*10 if int(returnValue)<=10 else 100
            DAN.push(deviceFeature, iotvalue)
        else:
            DAN.push(deviceFeature, int(returnValue))
    
    if(A !="" and valid >0): #  A+F
        print("tokenlist outer loop change1?:", A,D,F,V)
        df = pd.read_csv('dict/ADF.txt')
        if(lang == 'en-US'):
            df = df.loc[df['A_ens']==A]
        else:
            df = df.loc[df['A'] == A]
        print('df info:',df)
        for ind in df.index:     
            print(df['D_en'][ind], df['A_en'][ind], df['DFlist'][ind], df['Regaddr'][ind])
            deviceName = df['D_en'][ind]
            deviceModel = df['A_en'][ind]
            dfList = df['DFlist'][ind]
            Regaddr = df['Regaddr'][ind]
            dfList = eval(dfList)
            returnValue = V
            deviceFeature = F
            print("device name: ",deviceName,"device model: ", deviceModel )
            Reg_addr = Regaddr
            DAN.profile['d_name']= deviceName # search for device name 
            DAN.profile['dm_name']=deviceModel # use specific device model 
            DAN.profile['df_list']=dfList
            
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
            if(deviceFeature == 'Luminance-I' or deviceFeature == 'ColorTemperature-I'):
                DAN.push(deviceFeature, int(returnValue)*10)
            else:
                DAN.push(deviceFeature, int(returnValue))

    

if __name__ == "__main__":
    register.registerIottalk()
    app.run(host='0.0.0.0',debug=True, port=19453)
    