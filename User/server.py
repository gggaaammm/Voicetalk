import os
import sys
import pandas as pd
import json
from threading import Thread
import time, random, requests
import DAN
import unitconversion, enspacy, zhckip, register

# ========iottalk================
ServerURL = 'http://140.113.199.246:9999'      #with non-secure connection
#ServerURL = 'https://DomainName' #with SSL connection
# for D+F






#==========flask as backend=============
from flask import Flask, render_template, request, jsonify, url_for
app = Flask(__name__)



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
        
        response = ''
        if(returnlist[4] == -1):
            response =  'I\'m sorry, try again.' if language == 'en-US' else '很抱歉，聽不懂請重講'
            returnlist = []
        else:
            response = 'OK, ' if language == 'en-US' else '收到，'
            returnlist[2] = feature
            if(returnlist[4] == 1): returnlist[3] = ''

    return render_template("index.html",returnlist=returnlist, response = response)# response message add here


@app.route('/ProcessSentence', methods = ['POST','GET'])
def ProcessSentence():
    returnlist = []
    voice = request.args.get('voice')
    sentence = voice
    language = request.args.get('lang_id')
    print("voice sentence: ", sentence) #data should be decoded from bytestrem to utf-8
    # add rule to check if chinese or english
    
    if(language == 'en-US'): #English
        enspacy.readDB()
        feature, tokenlist = enspacy.textParse(sentence) #spacy function
    else:  # chinese
        feature,tokenlist = zhckip.textParse(sentence,zhckip.ws,zhckip.pos,zhckip.ner) # ckiptagger function
        
    A = tokenlist[0]
    D = tokenlist[1]
    F = tokenlist[2]
    V = tokenlist[3]
    valid = tokenlist[4]

    thread = Thread(target=sendIot, args=(A,D,F,V,valid,language))
    thread.daemon = True
    thread.start()

    returnlist = tokenlist
    
    response = ''
    if(returnlist[4] == -1):
        response =  'I\'m sorry, try again.' if language == 'en-US' else '很抱歉，聽不懂請重講'
        returnlist = []
    else:
        response = 'OK, ' if language == 'en-US' else '收到，'
        returnlist[2] = feature
        if(returnlist[4] == 1): returnlist[3] = ''
    print("source from voice", response, returnlist)
    
    entry2Value = request.args.get('entry2_id')
    entry1Value = request.args.get('entry1_id')

    var1 = int(entry2Value) + int(entry1Value)
    return jsonify({ 'var1': var1 , 'tokenlist': returnlist, 'response': response})



def sendIot(A,D,F,V,valid,lang):
    if(D !="" and valid !=-1): # D+F
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
        DAN.push(deviceFeature, int(returnValue))
    
    if(A !="" and valid !=-1): #  A+F
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
            DAN.push(deviceFeature, int(returnValue))

    

if __name__ == "__main__":
    register.registerIottalk()
    app.run(host='0.0.0.0',debug=True, port=19453)
    