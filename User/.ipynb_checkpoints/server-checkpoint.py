import os
import sys
import time
import pandas as pd
import json

import time, random, requests
import DAN
import unitconversion, enspacy, zhckip, register

# ========iottalk================
ServerURL = 'http://140.113.199.246:9999'      #with non-secure connection
#ServerURL = 'https://DomainName' #with SSL connection
# for D+F






#===========ckiptagger(tensorflow)==========
# Suppress as many warnings as possible
# this code hide the warning meesage
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
from tensorflow.python.util import deprecation
deprecation._PRINT_DEPRECATION_WARNINGS = False
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

from ckiptagger import data_utils, construct_dictionary, WS, POS, NER

#=========read ckiptagger model========
start = time.time()
ws = WS("./data", disable_cuda=False)
pos = POS("./data", disable_cuda=False)
ner = NER("./data", disable_cuda=False)
end = time.time()
print("loading time: ", end-start)

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
            feature,tokenlist = textParse(text,ws,pos,ner) # ckiptagger function

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
        feature,tokenlist = textParse(sentence,ws,pos,ner) # ckiptagger function
    
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
    

    
    
def sendiot(tokenlist):
    #tokenlist contains: 1.device model   2.device name 3. device feature 4.device return value 5. rule/valid 
    print("ready to send to iottalk")
    rule = tokenlist[4]
    
    if(tokenlist[1]!=""): # D+F
        #search for real iottalk device name
        df = pd.read_csv('dict/ADF.txt')
        print('df info:', df)
        df = df.loc[df['D']==tokenlist[1]]
        deviceName = df.iloc[0]['D_en']
        deviceModel = df.iloc[0]['A_en']
        dfList = df.iloc[0]['DFlist']
        Regaddr = df.iloc[0]['Regaddr']
        dfList = eval(dfList)
        print(type(dfList))
        returnValue = tokenlist[3]
        deviceFeature = tokenlist[2]
        print("device name: ",deviceName,"device model: ", deviceModel )
        Reg_addr = Regaddr
        DAN.profile['d_name']= deviceName # search for device name 
        DAN.profile['dm_name']=deviceModel # use specific device model 
        DAN.profile['df_list']=dfList
        DAN.device_registration_with_retry(ServerURL, Reg_addr)
        DAN.push(deviceFeature, int(returnValue))
        
    if(tokenlist[0]!="" and tokenlist[4]!=-1): #  A+F
        df = pd.read_csv('dict/ADF.txt')
        df = df.loc[df['A']==tokenlist[0]]
        print('df info:',df)
        for ind in df.index:
            print(df['D_en'][ind], df['A_en'][ind], df['DFlist'][ind], df['Regaddr'][ind])
            deviceName = df['D_en'][ind]
            deviceModel = df['A_en'][ind]
            dfList = df['DFlist'][ind]
            Regaddr = df['Regaddr'][ind]
            dfList = eval(dfList)
            returnValue = tokenlist[3]
            deviceFeature = tokenlist[2]
            print("device name: ",deviceName,"device model: ", deviceModel )
            Reg_addr = Regaddr
            DAN.profile['d_name']= deviceName # search for device name 
            DAN.profile['dm_name']=deviceModel # use specific device model 
            DAN.profile['df_list']=dfList
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
            DAN.push(deviceFeature, int(returnValue))
            


    
    
def dictionaryLookup(word,A_dict, D_dict, F_dict, V_dict):
    key = 4
    if word in A_dict:
        key = 0
    if word in D_dict: #if word in both A/D, word will be recognized as D
        key = 1
    if word in F_dict:
        key = 2
    if word in V_dict:
        key = 3
    return key
    
def num_there(s): # check if any digit exist in any word
    return any(i.isdigit() for i in s)

def ruleLookup(feature):
    df = pd.read_csv('dict/rule.txt')
    df = df.loc[df['feature']==feature]
    rule = df.iloc[0]['rule']
    if(rule == 1):
        return 1
    else:
        return 2
    
    return 0
    
def supportCheck(tokenlist):
    print("tokenlist before support check: ", tokenlist)
    # unified synonym
    df = pd.read_csv('dict/synonym.txt')
    df = df.loc[(df['F1']==tokenlist[2]) | (df['F2'] == tokenlist[2]) | (df['F3'] == tokenlist[2])]
    print(df.iloc[0]['F'])
    feature = df.iloc[0]['F']
    
    
    #check if D supports F
    if(tokenlist[1]!=''):
        df = pd.read_csv('dict/supportlist_ADF.txt')
        print("why no D", tokenlist[1])
        print("D list:\n", df['D'])
        df = df.loc[df['D']==tokenlist[1]]
        print("= = why not parse", df, tokenlist[1])
        if(df.iloc[0]['F1']==feature or df.iloc[0]['F2']==feature or df.iloc[0]['F3']==feature ):
            print('D support F')
        else:
            print('D not support F')
            tokenlist[4] = -1
    
    #check if A support F
    if(tokenlist[0]!=''):
        allsupport = 1
        df = pd.read_csv('dict/supportlist_ADF.txt')
        df = df.loc[df['A']==tokenlist[0]]
        print("all belongs to A:", df)
        d_id = 0
        while (d_id < len(df.index)):
            if(df.iloc[d_id]['F1']!= feature and df.iloc[d_id]['F2']!=feature):
                print('one of D unsupport')
                allsupport = 0
                break
            d_id = d_id+1
    
        if(allsupport == 1):
            print('A all support F')
        else: tokenlist[4] = -1
            
    return tokenlist
    # check if F support V(only for Rule2)   
        
    
    
    
def mappingToken(wordset): #mapping token should return an array of A/D/F/V
    token = ["","","","",0]
    j=0
    path_A_dict = r"dict/A.txt"
    A_dict = pd.read_csv(path_A_dict, sep="\n", header=None)
    # 存到list
    A_dict.columns = ['A']
    A_list = list(A_dict['A'])
    
    path_D_dict = r"dict/D.txt"
    D_dict = pd.read_csv(path_D_dict, sep="\n", header=None)
    # 存到list
    D_dict.columns = ['D']
    D_list = list(D_dict['D'])
    
    path_F_dict = r"dict/F.txt"
    F_dict = pd.read_csv(path_F_dict, sep="\n", header=None)
    # 存到list
    F_dict.columns = ['F']
    F_list = list(F_dict['F'])
    
    path_V_dict = r"dict/V.txt"
    V_dict = pd.read_csv(path_V_dict, sep="\n", header=None)
    # 存到list
    V_dict.columns = ['V']
    V_list = list(V_dict['V'])
    
    while(j<len(wordset)):
        print(wordset[j])
        if(num_there(wordset[j])): #check if this word is number
            token[3] = wordset[j]
        get_token = dictionaryLookup(wordset[j],A_list,D_list, F_list,V_list)
        print("token: ",get_token)
        #if A/D/F/V already exist another value, break
        if(token[get_token]!="" and get_token<4):
            print("it should break")
            token[4]=-1
            break
        # if token belongs to A/D/F/V
        if(get_token<4):
            token[get_token] = wordset[j]
        
        j=j+1
    
    
    #when loop end, calculate token and check if valid.
    #sucess: token[4] = 1, E:token[4]=-1
    if(bool(token[0]!="") ^ bool(token[1]!="")):
        print("either A or D exist")
        #check if F exist
        if(token[2]!=""):
            print("F exist")
            rule = ruleLookup(token[2])
            token[4] = rule
            #check if V(for rule2) exist
            if(token[3]=="" and rule==2):
                print("need value")
                token[4]=-1
            elif(token[3]!="" and rule==2):
                print("V exist for rule 2")
        else:
            token[4]=-1
    else:
        token[4]=-1
        
    #now token has correct number, check if A/D support F
    if(token[4] != -1):
        token = supportCheck(token)
        
    return token
        
        
def unitConversion(feature, entity, entityType, word_sentence):
    print('unit conversion: ', entity, entityType)
    if(entityType == 'TIME'):
        print("time") # (uv)+ default as hr-min-sec //ordered
        hr, minu ,sec=0,0,0
        #find hour
        if("時" in entity):
            print("hour detect")
            if("小時" in entity):
                hr = int(entity[:-(len(entity)-entity.find("小時"))])
                entity = entity[entity.find("小時")+2:]
            else:
                hr = int(entity[:-(len(entity)-entity.find("時"))])
                entity = entity[entity.find("時")+1:]
            print("hour declare as sec:", hr, hr*3600)
            hr = hr*3600
                
        #find minute
        if("分" in entity):
            print("min detect")
            minu = int(entity[:-(len(entity)-entity.find("分"))])
            if("分鐘" in entity):
                entity = entity[entity.find("分鐘")+2:]
            else:
                entity = entity[entity.find("分")+1:]
            print("min declare as sec:", minu, minu*60)
            minu = minu*60
                
        #find second
        if("秒" in entity):
            print("sec detect")
            sec = int(entity[:-(len(entity)-entity.find("秒"))])
            print("sec declare as sec:", sec, sec*1)
            
            
        #merge together
        total_time = hr+minu+sec;
        print("total time:", total_time)
        return total_time
        
    elif(entityType == 'PERCENT'):
        print("percent") # u%
        value = entity[:-1]
        return float(value)
        
        
    elif(entityType == 'QUANTITY'):
        print("quantity") # uv
        unitconversion.checkUnit(feature, entity, word_sentence)
        
    



def textParse(text,ws,pos,ner):
    # Download data
    # data_utils.download_data("./")
    
    
    # 用讀CSV的方式讀取前面匯出的txt
    path_A_dict = r"dict/A.txt"
    df_ner_dictA = pd.read_csv(path_A_dict, sep="\n", header=None)
    # 存到list
    df_ner_dictA.columns = ['NER']
    list_ner_dictA = list(df_ner_dictA['NER'])
    
    
    # 用讀CSV的方式讀取前面匯出的txt
    path_D_dict = r"dict/D.txt"
    df_ner_dict = pd.read_csv(path_D_dict, sep="\n", header=None)
    # 存到list
    df_ner_dict.columns = ['NER']
    list_ner_dict = list_ner_dictA+list(df_ner_dict['NER'])
    # 將list轉成dict型態，這邊每個權重都設為1
    dict_for_CKIP = dict((el,1) for el in list_ner_dict)
    # Create custom dictionary(for D)
    dictionary = construct_dictionary(dict_for_CKIP)
    print("user defined dictionary", dictionary)
    
    # Run WS-POS-NER pipeline
    sentence_list = [
        text
    ]
    # word_sentence_list = ws(sentence_list)
    #word_sentence_list = ws(sentence_list, sentence_segmentation=True)
    start = time.time()
#     word_sentence_list = ws(sentence_list, recommend_dictionary=dictionary)
    word_sentence_list = ws(sentence_list, coerce_dictionary=dictionary)
    pos_sentence_list = pos(word_sentence_list)
    entity_sentence_list = ner(word_sentence_list, pos_sentence_list)
    end  = time.time()
    
    print("execution time: ", end-start)
    
    # Release model
    del ws
    del pos
    del ner
    
    # Show results
    def print_word_pos_sentence(word_sentence, pos_sentence, entity_sentence):
        assert len(word_sentence) == len(pos_sentence)
        
        tokenlist = mappingToken(word_sentence)
        #support check
        
        
        
        print("token list: ", tokenlist)
        # if tokenlist[4] indicate R1:1, R2:2, E:-1
        rule = tokenlist[4]
        deviceFeature = tokenlist[2]
        # match F to Return value(only for Rule1)
        if(rule == 1):
            df = pd.read_csv('dict/supportlist_FV.txt')
            df = df.loc[(df['F1']==tokenlist[2]) | (df['F2'] == tokenlist[2]) | (df['F3'] == tokenlist[2])]
            return_value = df.iloc[0]['R']
            tokenlist[3] = return_value
            # change F to iottalk device feature
            tokenlist[2] = df.iloc[0]['Fiot']
            print("token list for return value:", tokenlist)
            # for A+F
            
            # for D+F
            
            
        #after getting token list, use entity recog result to do unit conversion
        #if more than 2 entity in one sentence, filter it for CARDINAL, TIME, QUANTITY, PERCENT
        print("entity:", entity_sentence)
        if(rule == 2):
            feature = tokenlist[2]
            entitylist = list(entity_sentence)
            entity = entitylist[0][3]
            entityType = entitylist[0][2]
            print("entity category and context:", entitylist[0][2], entitylist[0][3])
        
            
            if(len(entity_sentence)==0 or entitylist[0][2] == 'CARDINAL'):
                print("no unit conversion required...")
            elif(entitylist[0][2] == 'TIME' or entitylist[0][2] == 'QUANTITY' or entitylist[0][2] == 'PERCENT'):
                print("conversion requied!")
                value = unitConversion(feature, entity, entityType, word_sentence)
            
            df = pd.read_csv('dict/supportlist_FV.txt')
            df = df.loc[(df['F1']==tokenlist[2]) | (df['F2'] == tokenlist[2]) | (df['F3'] == tokenlist[2])]
            tokenlist[2] = df.iloc[0]['Fiot']
            
            
            
            
        return deviceFeature, tokenlist
        
    
    for i, sentence in enumerate(sentence_list):
        print()
#         print("sentence list")
        print(f"'{sentence}'")
        F,iotinfo = print_word_pos_sentence(word_sentence_list[i],  pos_sentence_list[i], entity_sentence_list[i])
        print("send iotinfo: ", iotinfo)
        if(iotinfo[4] != -1):
            sendiot(iotinfo)
        for entity in sorted(entity_sentence_list[i]):
            print(entity)
            
    return F,iotinfo
    

if __name__ == "__main__":
    register.registerIottalk()
    app.run(host='0.0.0.0',debug=True, port=19453)
    