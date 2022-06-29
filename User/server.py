import os
import sys
import pandas as pd
import json
from threading import Thread
import time, random, requests
import DAN
import unitconversion, enspacy, register
import zhckip #uncomment later

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
        if(language == 'cmn-Hant-tw'): #English
            enspacy.readDB()
            value,name, feature, device_queries = enspacy.textParse(text) #spacy function
        else:  # chinese
            value,name, feature, device_queries = zhckip.textParse(text,zhckip.ws,zhckip.pos,zhckip.ner) # ckiptagger function
            print("chinese not yet")
        
        
        #get all device query(ies) from the tokenlist
        print("[ProcessSentence] is multiple device: ", isinstance(device_queries[0], list))
        
        print("[ProcessSentence] how long:",len(device_queries))
        thread = Thread(target=sendIot, args=(device_queries,))
        thread.daemon = True
        thread.start()
        
        if(isinstance(device_queries[0], list) == False):
            returnlist = device_queries
            valid = device_queries[4]    # only 1 device, get valid/rule bits
        else:
            for device_query in device_queries:
                if(device_query[4] < 0):
                    valid = device_query[4]
                    returnlist = device_query
                    break
                else:
                    valid = device_query[4]
                    device_query[2] = 0
                    returnlist = device_query
        
        print("[valid]message bit:", valid)
        print("[response]response info:",returnlist)
        response = ''
        if(valid < 0):
            response =  'I\'m sorry, try again.' if language == 'en-US' else '很抱歉，聽不懂請重講'
            returnlist = []
        else:
            response = 'OK, ' if language == 'en-US' else '收到，'
            #returnlist[2] = feature
            #if(returnlist[4] == 1): returnlist[3] = ''

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
        value,name, feature, device_queries = enspacy.textParse(sentence) #spacy function
    else:  # chinese
        value,name, feature, device_queries = zhckip.textParse(text,zhckip.ws,zhckip.pos,zhckip.ner) # ckiptagger function
        print("chinese not yet")
    
    #get all device query(ies) from the tokenlist
    #get all device query(ies) from the tokenlist
    print("[ProcessSentence] is multiple device: ", isinstance(device_queries[0], list))    
    print("[ProcessSentence] how long:",len(device_queries,))
    thread = Thread(target=sendIot, args=(device_queries,))
    thread.daemon = True
    thread.start()
    

    if(isinstance(device_queries[0], list) == False):
        valid = device_queries[4]    # only 1 device, get valid/rule bits
        returnlist = device_queries  # show the success/error message of device D
    else:
        for device_query in device_queries:
            if(device_query[4] < 0):
                valid = device_query[4]
                returnlist = device_query # show the error message of certiain deivce in A
                name = device_query[1]
                break
            else:
                valid = device_query[4]
                returnlist = device_query # show the success message of A
            
    
    response = '' # init response
    # complete the response context
    if(valid < 0):
        response =  'I\'m sorry, try again.' if language == 'en-US' else '很抱歉，聽不懂請重講'
    else:
        response = 'OK, ' if language == 'en-US' else '收到，'
#         if(returnlist[4] == 1): returnlist[3] = ''      # rule 1: no value(token 3) need
            
    print("source from response", response,"\nreturnlist:", returnlist,"\nvalid:", valid, )
    
    
    return jsonify({ 'tokenlist': returnlist, 'response': response, 'valid':valid, 'name': name, 'feature': feature, 'value':value})




def sendIot(device_queries):
    if(isinstance(device_queries[0], list)):
        print("[F] rework:", device_queries)
        for device_query in device_queries:
            print("each query:", device_query)
            D = device_query[1]
            F = device_query[2]
            V = device_query[3]
            valid = device_query[4]
            if(valid>0):
                df = pd.read_csv('dict/DeviceTable.txt')
                df = df.loc[df['device_name'] == D]
                Regaddr = df.iloc[0]['Regaddr']
                DAN.profile['d_name']= D
                DAN.profile['dm_name'] = df.iloc[0]['device_model']
                DAN.profile['df_list'] = eval(df.iloc[0]['device_feature_list'])
                DAN.device_registration_with_retry(ServerURL, Regaddr)

                print("device name: ",D,"device model: ", df.iloc[0]['device_model'])
                print("device feature", F)
                if(F == 'Luminance-I' or F == 'ColorTemperature-I'):
                    iotvalue = int(V)*10 if int(V)<=10 else 100
                    DAN.push(F, iotvalue)
                else:
                    DAN.push(F, int(V))

            
            
    else:
        print("only 1 query", device_queries)
        device_query = device_queries
        D = device_query[1]
        F = device_query[2]
        V = device_query[3]
        valid = device_query[4]
        if(valid>0):         
            df = pd.read_csv('dict/DeviceTable.txt')
            df = df.loc[df['device_name'] == D]
            Regaddr = df.iloc[0]['Regaddr']
            DAN.profile['d_name']= D
            DAN.profile['dm_name'] = df.iloc[0]['device_model']
            DAN.profile['df_list'] = eval(df.iloc[0]['device_feature_list'])
            DAN.device_registration_with_retry(ServerURL, Regaddr)
            
            print("device name: ",D,"device model: ", df.iloc[0]['device_model'])
            if(F == 'Luminance-I' or F == 'ColorTemperature-I'):
                iotvalue = int(V)*10 if int(V)<=10 else 100
                DAN.push(F, iotvalue)
            else:
                DAN.push(F, int(V))
    
    

# def sendIot_old(A,D,F,V,valid,lang):
#     if(D !="" and valid >0 ): # D+F
#         df = pd.read_csv('dict/ADF.txt')
#         print('df info:', df, "searching", D)
#         if(lang == "en-US"):
#             df = df.loc[df['D_en']==D]
#         else:
#             df = df.loc[df['D'] == D]
#         print("remain df", df)
#         deviceName = df.iloc[0]['D_en']
#         deviceModel = df.iloc[0]['A_en']
#         dfList = df.iloc[0]['DFlist']
#         Regaddr = df.iloc[0]['Regaddr']
#         dfList = eval(dfList)
#         print(type(dfList))
#         returnValue = V
#         deviceFeature = F
#         print("device name: ",deviceName,"device model: ", deviceModel)
#         Reg_addr = Regaddr
#         DAN.profile['d_name']= deviceName # search for device name 
#         DAN.profile['dm_name']=deviceModel # use specific device model 
#         DAN.profile['df_list']=dfList
#         DAN.device_registration_with_retry(ServerURL, Reg_addr)
# #         DAN.push('Switch1', 1)
#         if(deviceFeature == 'Luminance-I' or deviceFeature == 'ColorTemperature-I'):
#             iotvalue = int(returnValue)*10 if int(returnValue)<=10 else 100
#             DAN.push(deviceFeature, iotvalue)
#         else:
#             DAN.push(deviceFeature, int(returnValue))
    
#     if(A !="" and valid >0): #  A+F
#         print("tokenlist outer loop change1?:", A,D,F,V)
#         df = pd.read_csv('dict/ADF.txt')
#         if(lang == 'en-US'):
#             df = df.loc[df['A_en']==A]
#         else:
#             df = df.loc[df['A'] == A]
#         print('df info:',df)
#         for ind in df.index:     
#             print(df['D_en'][ind], df['A_en'][ind], df['DFlist'][ind], df['Regaddr'][ind])
#             deviceName = df['D_en'][ind]
#             deviceModel = df['A_en'][ind]
#             dfList = df['DFlist'][ind]
#             Regaddr = df['Regaddr'][ind]
#             dfList = eval(dfList)
#             returnValue = V
#             deviceFeature = F
#             print("device name: ",deviceName,"device model: ", deviceModel )
#             Reg_addr = Regaddr
#             DAN.profile['d_name']= deviceName # search for device name 
#             DAN.profile['dm_name']=deviceModel # use specific device model 
#             DAN.profile['df_list']=dfList
            
#             DAN.device_registration_with_retry(ServerURL, Reg_addr)
#             if(deviceFeature == 'Luminance-I' or deviceFeature == 'ColorTemperature-I'):
#                 DAN.push(deviceFeature, int(returnValue)*10)
#             else:
#                 DAN.push(deviceFeature, int(returnValue))

    

if __name__ == "__main__":
    #register.registerIottalk()
    #register will be close for debug
    app.run(host='0.0.0.0',debug=True, port=19453)
    