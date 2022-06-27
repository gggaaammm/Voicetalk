import spacy
import ast
import DAN
import pandas as pd
import sqlite3
import time
import os
import glob # for reading multi files
import re # for number finding
#import the phrase matcher
from numerizer import numerize
from spacy.matcher import PhraseMatcher
from pint import UnitRegistry
#load a model and create nlp object
nlp = spacy.load("en_core_web_sm")
#initilize the matcher with a shared vocab
matcher = PhraseMatcher(nlp.vocab)
ServerURL = 'http://140.113.199.246:9999'      

# define error message format:
# 1: rule1, 2: rule2, -1~-8: error
# error log id and message stored in errorlog.txt

def readDB():
    #create the list of alias to match
    path = r"dict/enUS/alias/" #  path for alias
    all_files = glob.glob(os.path.join(path , "*.txt"))
    aliasList={} # create a dictionary of alias

    # read all file at once
    for filename in all_files:
        sublist = []
        df = pd.read_csv(filename)
        for column in df.columns:
            sublist = sublist+list(df[column])
        sublist = [x for x in sublist if str(x) != 'nan']  # filter all NAN element
        aliasList[filename[21]] = sublist


    #obtain doc object for each word in the list and store it in a list
    # alias(A),  alias(D),  alias(F),  alias(V),
    A = [nlp(a) for a in aliasList['A']]
    D = [nlp(d) for d in aliasList['D']]
    F = [nlp(f) for f in aliasList['F']]
    V = [nlp(v) for v in aliasList['V']]
    U = [nlp(u) for u in aliasList['U']]


    #add the pattern to the matcher
    matcher.add("A", A)
    matcher.add("D", D)
    matcher.add("F", F)
    matcher.add("V", V)
    matcher.add("U", U)
    #======
    

def textParse(sentence):
    sentence = sentence.lower() # lower all the chracters in sentence
    
    readDB() # read database

    # new a dict: token dict
    tokendict = {'A':'', 'D':'', 'F':'', 'V':'', 'U':''}
    # new a list: token
    token = ['','','','',''] #token[4] store rule and valid bits
    
    device_queries = [[0]*5]*1 # init query:a device query(ies) ['A','D','F','V','error/rule'] which will send to devicetalk at the end of function
    
    
    # ====================   tokenclassifier start===================================
    doc = nlp(sentence)  
    matches = matcher(doc)
    for match_id, start, end in matches:
        token_id = nlp.vocab.strings[match_id]  # get the unicode ID, i.e. 'COLOR'
        span = doc[start:end]
        print("==========================before classifying:", token_id, span.text)
        # stored as sorted token list
        # if duplicate, mark tokenlist[4] as -1(invalid)
        if(tokendict[token_id] == '' or tokendict[token_id] == span.text):
            tokendict[token_id] = span.text
        else:
            print("too much element in one token!") #error 1: wrong number of token
            token[4] = -1
    # ====================   tokenclassifier end ===================================
    
    
    # ===========================  value handling start=================================
    
    # check if sentence contains number, before sentence redirecting
    # first remove other tokens(i.e, '1' in sentence: "set fan 1 speed to 3")
    sentence = sentence.replace(tokendict['D'], "")
    
    
    if(tokendict['V'] != ''):     # if token V has a string matched, pass
        pass
    else:
        value_doc = nlp(sentence)     # use spacy's sid extension: numerizer, converts numerical and quantitative words into numeric strings.
        if(len(value_doc._.numerize())== 1): # if V is recognized as numeric strings, save it as a string of quantity 
            quantity = list(value_doc._.numerize().values())
            tokendict['V'] = handleValue(str(quantity[0]))
    
    # ===========================  value handling end =================================

    sentence_feature = tokendict['F'] # save before alias redirect
    sentence_device_name = tokendict['D'] 
    
    # ============================  check the alias, redirect================================
    # A,D,F alias should be redirect to device_model, device_name, device_feature individually
    path = r"dict/enUS/alias/" #  path for synonym
    all_files = glob.glob(os.path.join(path , "*.txt"))
    for filename in all_files:
        sublist = []
        df = pd.read_csv(filename)
        #redirect A,D,F to device_model, device_name, device_feature individually
        for column in df.columns:
            df_abs = df.loc[(df[column] == tokendict[filename[21]])]
            if(len(df_abs.index)>0):
                tokendict[filename[21]] = df_abs.iloc[0][0]
                
    token = [tokendict['A'], tokendict['D'], tokendict['F'], tokendict['V'], token[4]]
    #============================================== redirect end =================================

    # eliminate A if both AD exist
    if(token[0] != '' and token[1] != ''):
        token[0] = ''
        print('[elimination] list of token after A/D elimination:', token)


    

    
    # =========================== number of token validation  =======================================
    # check if number of tokens is enough.
    if(bool(token[0]!="") ^ bool(token[1]!="")): #check either A or D exist
        if(token[2]!=""): #check if F exist
            rule = ruleLookup(token[2])
            token[4] = rule # token[4] is rule
            if(token[3]=="" and rule==2): #check if V(for rule2) exist
                token[4]=-4 # error message #4: device feature need value
        else:
            token[4]=-3     # error message #3: no feature found in sentence 
    else:
        token[4]=-2         # error message #2: no device found in sentence    
    
    # =========================== number of token validation end =======================================    
    
    
    
    
    #now token has correct number, check if A/D support F
    if(token[4] > 0):
        token = supportCheck(token) #support check
    else:
        print("[error]not enough token!") # break
    
    if(token[4] > 0): # <0 because not support
        device_queries = valueCheck(token, sentence_feature) # value check
    else:
        device_queries = token
        
    

    print("[final] before send to iottalk,", " \ntoken:", token, "\ndevice query", device_queries)
    
    saveLog(sentence, token)
    print("voice input feature: ", sentence_feature)
    return sentence_feature, device_queries
#     return sentence_feature, tokenlist
        

    
def ruleLookup(feature): #check rule by feature
    # rulelookup will read DevicefeatureTable.txt
    print("token list check rule: ", feature)
    df = pd.read_csv('dict/DevicefeatureTable.txt')
    df = df.loc[(df['device_feature']==feature)]
    rule = df.iloc[0]['rule']
    if(rule == 1):
        return 1
    else:
        return 2
    return 0


def supportCheck(tokenlist):
    A = tokenlist[0]
    D = tokenlist[1]
    F = tokenlist[2]
    # read device info in DeviceTable.txt
    df = pd.read_csv('dict/DeviceTable.txt')
    DeviceTable = readDeviceTable(A,D,F)
    
    if(D!=''):  #check if D supports F
        feature_list = ast.literal_eval(DeviceTable.iloc[0]['device_feature_list'])
        if(F not in feature_list):
            tokenlist[4] = -6   #error #6: Device not support such feature
            
    if(A!=''): #check if A all support F
        allsupport,d_id = 1,0
        while (d_id < len(DeviceTable.index)):
            feature_list = ast.literal_eval(DeviceTable.iloc[d_id]['device_feature_list'])
            if(F not in feature_list):
                allsupport = 0
                break
            d_id = d_id+1

        if(allsupport == 0):
            tokenlist[4] = -6 #error message #5: Device not support such feature
            
    return tokenlist

def valueCheck(tokenlist, feature): #issue give value
    A = tokenlist[0]
    D = tokenlist[1]
    F = tokenlist[2]
    V = tokenlist[3]
    rule = tokenlist[4]
    
    device_queries = [[0]*5]*1   # create a device query as return type of function

    
    df = pd.read_csv('dict/DevicefeatureTable.txt')

    if(rule == 1):      #(issue): Used for value_dict in devicefaturetable.txt
        print("rule 1") #give a value for rule 1 in value_keyword list
        df2 = pd.read_csv('dict/enUS/alias/aliasF.txt')
        df2 = df2.loc[ (df2['alias1']==feature) | (df2['alias2']==feature) | (df2['alias3']==feature) ]
        feature = df2.iloc[0]['alias1']
        #feature change to absolute device feature('open'/'close')
        
        #require table of dictionary, rule 1 dont care if A or D(if they pass the support check, they have same value_dict)
        df = df.loc[(df['device_feature'] == F)]
        tokenlist[3] = ast.literal_eval(df.iloc[0]['value_dict'])[feature]
        
        if(D != ""):
            device_queries = [A,D,F,tokenlist[3], rule]
        if(A != ""):
            df_A = pd.read_csv('dict/DeviceTable.txt')   # read DeviceTable.txt
            df_A = df_A.loc[(df_A['device_model'] == A)] # access all the dataframe which device_model equals to A
            device_list =  list(df_A['device_name'])     # get the device name list which device_model is A
            device_queries = [[0]*5]*len(device_list)    # create a query for each device in 1 device model
            
            for idx, device in enumerate(device_list):
                device_queries[idx] = [A,device,F,tokenlist[3], rule]
        
        
    elif(rule ==2):
        # 1. a string(do nothing and pass)
        # 2. a number(check if exceed min/max)
        # 3. a quantity(check if unit support and check exceed min/max)
        
        if(D != ''):  #access the device info(which D and F are fitted)
            if(isinstance(V, int)):
                tokenlist[4] = checkMinMax(D,F,V)
                # a value, check number min/max
            elif(isinstance(V,str)):
                #find if string exist in value_dict, if yes, give value; if no, bypass string.
                df = findinfo(D,F)
                print("value check rule 2 df check", df)
                if(V in df.iloc[0]['value_dict']):
                    tokenlist[3] =  ast.literal_eval(df.iloc[0]['value_dict'])[V]
                    print("value check rule 2 string to int success: ", V)      
            else:
                print('a quantity')
                U = str(V).split(' ')[1] # check if unit in unit list
                if(len(df.loc[(df['device_name'] == D)&(df['unit_list'].str.contains(U))].index)>0):
                    print("value check rule 2 unit verified")
                    tokenlist[4] = checkMinMax(D,F,str(V).split(' ')[0])# already set to base unit, just extract the value 
                else:
                    tokenlist[4] = -8 # unsupport unit
                    print("value check rule 2 quantity unit error!")
            device_queries = tokenlist

                
                
            print("value check valid bit: ", tokenlist[4])
            
            
        elif(A != ''):
            print("A is ", A)
            df_A = pd.read_csv('dict/DeviceTable.txt')   # read DeviceTable.txt
            df_A = df_A.loc[(df_A['device_model'] == A)] # access all the dataframe which device_model equals to A
            device_list =  list(df_A['device_name'])     # get the device name list which device_model is A
            
            device_queries = [[0]*5]*len(device_list)    # create a query for each device in 1 device model
            
            
            #(issue) list 3 cases
            if(isinstance(V, int)):
                print('a number')
                # in while loop check min max
                
                for idx, device in enumerate(device_list):
                    device_queries[idx] = [A,device,F,V, checkMinMax(device, F, V)]
                print('device model value check number:', tokenlist)
                print('[device model] value check queries:', device_queries)

                # a value, check number min/max
            elif(isinstance(V,str)):
                print('a string')
                for idx, device in enumerate(device_list):
                    df = findinfo(device, F)
                    print('breakpoint #329:',type(V))
                    if(V in df.iloc[0]['value_dict']):
                        tokenlist[3] =  ast.literal_eval(df.iloc[0]['value_dict'])[V]
                    device_queries[idx] = [A,device,F,tokenlist[3],tokenlist[4]]
                        
                print('device model value check string:', tokenlist)
                print('[device model] value check queries:', device_queries)

                           
                #give a value to string or bypass string
            else:
                print('a quantity')
                for idx,device in enumerate(device_list):                    
                    U = str(V).split(' ')[1] # check if unit is in unit list
                    if(len(df.loc[(df['device_name'] == D)&(df['unit_list'].str.contains(U))].index)>0):
                        print("value check rule 2 unit verified")
                    else:
                        tokenlist[4] = -8 # unsupport unit
                        print("value check rule 2 quantity unit error!")
                        
                    V = str(V).split(' ')[0] # split a string into list, extract 1 element                
                    tokenlist[4] = checkMinMax(device,F,V)
                    device_queries[idx] = [A,device,F,V,tokenlist[4]]
                print('device model value check quantity:', tokenlist)
                print('[device model] value check queries:', device_queries)

    print("[valueCheck end] :", "device query:",device_queries, "\n tokenlist", tokenlist)    
    return device_queries


    
def handleValue(quantity):
    print("quantity: ",quantity)
    quantitylist = quantity.split(' ') # split a string into list
    
    if(len(quantitylist) == 1):
        print("only value")
        return int(quantitylist[0])
    else:
        return handleUnit(quantitylist)

def handleUnit(quantitylist): # use Pint package for unit hanlding 
    ureg = UnitRegistry() # new a unit module
    Q_ = ureg.Quantity    # define a quantity element quantity = (value, unit)
    
    #(issue)get base unit from iottalk define
    ureg.load_definitions('my_def.txt')
    ureg.default_system = 'iottalk'
    
    value = 0 #init value
    #(issue) When exception, catch the error message(wrong unit cannot be calculated. ex: 3 minute + 20 cm)
    if(len(quantitylist)%2 == 0):
        print("is by 2")
        for q_id in range(0, len(quantitylist),2):
            value = value + Q_(int(quantitylist[q_id]), quantitylist[q_id+1]).to_base_units()
        print("base unit value changed:", value)
        return value
    else:
        print("error: is not by 2")
        return -5  # quantity error, number of value and unit mismatch
    
    
#followings are sub functions of value check
def checkMinMax(D,F, V): #check min max only for rule 2, 
    print(D,F,V)
    df = pd.read_csv('dict/DevicefeatureTable.txt')
    df_D= df.loc[(df['device_name'] == D) & (df['device_feature'] == F)]
    if( (float(V) > float(df_D.iloc[0]['max'])) | ( float(V) < float(df_D.iloc[0]['min'])) ): #if value exceed range
        return -7    # return -6 as error code
    else:
        return 2     # return 2 as rule 2

#followings are sub functions of support check
def findinfo(D,F):
    df = pd.read_csv('dict/DevicefeatureTable.txt')
    df = df.loc[(df['device_name'] == D) & (df['device_feature'] == F)]
    return df

def readDeviceTable(A,D,F):
    df = pd.read_csv('dict/DeviceTable.txt')
    if(D != ""):
        df = df.loc[df['device_name']== D]
    elif(A != ""):
        df = df.loc[df['device_model']== A]
    return df



def saveLog(sentence, tokenlist):
    print('save log')
    connection = sqlite3.connect("db/log.db")
    crsr = connection.cursor()
    # SQL command to insert the data in the table
    sql_command = """CREATE TABLE IF NOT EXISTS log ( 
    sentence TEXT,  
    result CHAR(1)
    );"""
    crsr.execute(sql_command)

    
    crsr.execute(f'INSERT INTO log VALUES ( "{sentence}", "{tokenlist[4]}")')

    connection.commit()
    connection.close()
    

