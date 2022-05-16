import os
import sys
import pandas as pd
import json

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

        response = ''
        if(tokenlist[4] == -1):
            response =  'I\'m sorry, try again.' if language == 'en-US' else '很抱歉，聽不懂請重講'
            tokenlist = []
        else:
            response = 'OK, ' if language == 'en-US' else '收到，'
            tokenlist[2] = feature
            if(tokenlist[4] == 1): tokenlist[3] = ''

    return render_template("index.html",tokenlist=tokenlist, response = response)# response message add here


@app.route('/ProcessSentence', methods = ['POST','GET'])
def ProcessSentence():
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
    
    response = ''
    if(tokenlist[4] == -1):
        response =  'I\'m sorry, try again.' if language == 'en-US' else '很抱歉，聽不懂請重講'
        tokenlist = []
    else:
        response = 'OK, ' if language == 'en-US' else '收到，'
        tokenlist[2] = feature
        if(tokenlist[4] == 1): tokenlist[3] = ''
    print("source from voice", response, tokenlist)
    
    entry2Value = request.args.get('entry2_id')
    entry1Value = request.args.get('entry1_id')

    var1 = int(entry2Value) + int(entry1Value)
    var2 = 10
    var3 = 15
    return jsonify({ 'var1': var1, 'var2': var2, 'var3': var3 , 'tokenlist': tokenlist, 'response': response})
#     return response# response message add here



    
# def registerIottalk():
    

    





    

if __name__ == "__main__":
    register.registerIottalk()
    app.run(host='0.0.0.0',debug=True, port=19453)
    