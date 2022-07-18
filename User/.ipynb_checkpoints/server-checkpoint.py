import os
import sys
import pandas as pd
import json
from threading import Thread
import time, random, requests
import DAN, register
import TWnlp #uncomment later
import USnlp
# v2
# import managesa as SA



# define error message format:
# 1: rule1, 2: rule2, <0: error
# -2 error: no device in sentence
# -3 error: no device feature in sentence
# -4 error: device feature need value
# -5 error: D not support F

# ========iottalk================
ServerURL = 'http://140.113.199.246:9999'      #with non-secure connection


#  ==========================
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
        language = 'zh-TW'
        # use text to send for demo
        # add rule to check if chinese or english
        if(language == 'en-US'): #English
            #enspacy.readDB()
            name, feature,value, device_queries = USnlp.textParse(text) #spacy function
        else:  # chinese
#             value,name, feature, device_queries = zhckip.textParse(text,zhckip.ws,zhckip.pos,zhckip.ner) # ckiptagger function
            name, feature,value, device_queries = TWnlp.textParse(text) #spacy function
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
        name, feature,value, device_queries = USnlp.textParse(sentence) #spacy function
    else:  # chinese
        name, feature,value, device_queries = TWnlp.textParse(sentence) #spacy function
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
                #turn on the device
                DAN.push('Switch1',1)

                print("\ndevice name: ",D,"\ndevice model: ", df.iloc[0]['device_model'], "\ntype V", type(V), V)
                print("device feature", F)
                if(F == 'Luminance-I' or F == 'ColorTemperature-I'):
                    iotvalue = int(V)*10 if int(V)<=10 else 100
                    DAN.push(F, iotvalue)
                else:
                    if(isinstance(V,list)):
                        DAN.push(F,*V)
                    else:
                        DAN.push(F, V)

            
            
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
            #turn on the device
            DAN.push('Switch1',1)
            
            print("\ndevice name: ",D,"\ndevice model: ", df.iloc[0]['device_model'], "\ntype V", type(V), V)
            if(F == 'Luminance-I' or F == 'ColorTemperature-I'):
                iotvalue = int(V)*10 if int(V)<=10 else 100
                DAN.push(F, iotvalue)
            else:
                if(isinstance(V,list)):
                    DAN.push(F,*V)
                else:
                    DAN.push(F, V)


        

    

if __name__ == "__main__":
    #register.registerIottalk()
    #register will be close for debug
        

    app.run(host='0.0.0.0',debug=True, port=19453)
    