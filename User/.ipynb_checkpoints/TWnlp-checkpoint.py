import spacy
import ast
import pandas as pd
import sqlite3
import time # time measure
import os
import sys
import glob # for reading multi files
import re # for number finding
#import the phrase matcher
from numerizer import numerize
from spacy.matcher import PhraseMatcher
from pint import UnitRegistry
#load a model and create nlp object
nlp = spacy.load("zh_core_web_sm")
#initilize the matcher with a shared vocab
matcher = PhraseMatcher(nlp.vocab)
# aside from english, chinese need some changes

# 1. a word segmentation before token classify(must)
from ckiptagger import data_utils, construct_dictionary, WS, POS, NER
start = time.time()
ws = WS("./data")   # word segmentation need 4 seconds
pos = POS("./data")
ner = NER("./data")

end = time.time()
print("loading time: ", end-start)
# 2. a special use of quantity managing(chosen)

#======= function readDB() ========
# in this function, program read files at the path "./dict/enUS/alias/"
# files data will be stored in dictionary: aliasDict
# aliasDict can be parsed by spaCy nlp()
# matcher() add the nlp() object, and give each key the match id
# no parameter, no return value is needed

def readDB():
    #create the list of alias to match
    path = r"dict/zhTW/alias/"                          #  path for alias
    all_files = glob.glob(os.path.join(path , "*.txt"))
    aliasDict={}                                        # create a dictionary of alias A/D/F/V/U

    # read all file at once
    for filename in all_files:
        sublist = []
        df = pd.read_csv(filename)
        for column in df.columns:
            sublist = sublist+list(df[column])             # read all elements in one file, stored as list
        sublist = [x for x in sublist if str(x) != 'nan']  # filter all NAN element in the list
        aliasDict[filename[21]] = sublist                  # key: filename[21] means A/D/F/V in "dict/enUS/alias/*.txt"


    #obtain doc object for each word in the list and store it in a list
    A = [nlp(a) for a in aliasDict['A']]
    D = [nlp(d) for d in aliasDict['D']]
    F = [nlp(f) for f in aliasDict['F']]
    V = [nlp(v) for v in aliasDict['V']]


    #add the pattern to the matcher
    matcher.add("A", A)
    matcher.add("D", D)
    matcher.add("F", F)
    matcher.add("V", V)

    
    return aliasDict.values()

# ========= chinese number redirection(word) ========
def chinese_numredirection(wordlist):
    df = pd.read_csv("dict/zhTW/num_zh.txt")
    for idx in range(len(wordlist)):
        zh_df = df.loc[(df['text1'] == wordlist[idx]) | (df['text2'] == wordlist[idx]) ]
        if(len(zh_df.index)>0):
            print("[chinese] number", wordlist[idx])
            wordlist[idx] = str(zh_df.iloc[0]['value'])
            print("number redirection", wordlist[idx])
    return wordlist

def spellCorrection(sentence):
    df = pd.read_csv("dict/zhTW/correction/correction.txt")
    wrongwordlist = list(df['wrong'])
    print(wrongwordlist)
    for wrongword in wrongwordlist:
        if (wrongword in sentence):
            correctdf = df.loc[(df['wrong'] == wrongword)]
            correctword = correctdf.iloc[0]['correct']
            sentence = sentence.replace(wrongword, correctword)
            print("[correct process]: ", wrongword,"->", correctword)
    print("[correction]: ", sentence)
    return sentence
    
    
# ============  function textParse(sentence) ============
# main function of the parsing subsystem, do the following:
# 1. read Database
# 2. match the token(tokenclassifier)
# 3. handle value
# 4. alias redirection
# 5. token counter validation(contain rule lookup)
# 6. token support check
# 7. token value check
# sentence(string) as input parameter, return value is device_queries
    

def textParse(sentence):
    # in chinese, do word segmentation before nlp
    
    sentence = spellCorrection(sentence)
    
    alias_list_dict = readDB() # read database
    dict_for_CKIP = {}
    #store keywords in dictionary
    for alias_list in alias_list_dict:
        dict_for_CKIP.update( dict((el,1) for el in alias_list) )

    dict_for_CKIP = construct_dictionary(dict_for_CKIP)
    word_list = ws([sentence], coerce_dictionary=dict_for_CKIP) # wordlist for chinese number detection

    
    # do chinese number redirection before sentence is joined
    wordlist = word_list[0]
    print("old [wordlist]", wordlist)
#     wordlist = chinese_numredirection(wordlist)
    
#     print("new [wordlist]", wordlist)
#     sentence_nozh = ''.join(wordlist)
#     print("[segmentation]", sentence_nozh)
    
    
    
    tokendict = {'A':'', 'D':'', 'F':'', 'V':''}  # new a dict: token dict, default key(A/D/F/V/U) is set with empty string
    
    # new a list: token
    tokenlist = ['','','','',''] #token[4] store rule/error bits, 
    
    device_queries = [[0]*5]*1 # init a device query(ies) which will send to devicetalk at the end of function
    
    
    # ====================   tokenclassifier start===================================
    # user matcher(doc) to classify words to tokens
    # unclassified word will be thrown away
    # token classifier need space
    
    #user mather to tokenize
    sentence_space = ' '.join(wordlist)
    tokendict, tokenlist = tokenClassifier(sentence_space)
    # ====================   tokenclassifier end ===================================
    
    
    # ===========================  value handling start=================================
    # check if sentence contains number, before sentence redirecting
    # first remove other tokens(i.e, '1' in sentence: "set fan 1 speed to 3")
    # use the non-space version to do number detection

    sentence = sentence.replace(tokendict['D'], "")
    
    
    
# ========================== we detect the quantity =========================
# for chinese number, we use ckip entity to detect number
    
    quantity = quantityDetect(sentence , dict_for_CKIP)

    
    
    sentence_feature = tokendict['F']     # save feature name before alias redirect
    sentence_device_name = tokendict['D'] if tokendict['D'] != '' else tokendict['A'] # save device name before alias redirect
    sentence_value = tokendict['V'] + quantity
    
    
    # ============================ alias redirection ================================
    # A,D,F,V alias should be redirect to device_model, device_name, device_feature individually
    tokenlist = aliasRedirection(tokendict, tokenlist)

    #============================ alias redirection end =================================

    # eliminate A if both AD exist
    if(tokenlist[0] != '' and tokenlist[1] != ''):
        tokenlist[0] = ''
        print('[elimination] list of token after A/D elimination:', tokenlist)

    # =========================== number of token validation  =======================================
    # check if number of tokens is enough.
    # if not enough, tokenlist[4] will record error id
      
    tokenlist[4] = tokenValidation(tokenlist)
    # =========================== number of token validation end =======================================    
    
    
    
    #============================ support check =================================
    # if token has correct number, check if A/D support F
    if(tokenlist[4] > 0):                  # if error/rule bit records rules
        tokenlist[4] = supportCheck(tokenlist) # support check
    else:                              # if error/rule bit records errors
        print("[error]not enough token!") # break
    
    
    #============================ Value check =================================
    # if token has correct number and A/D support F, check if V is valid
    if(tokenlist[4] > 0): 
        device_queries = valueCheck(tokenlist, sentence_feature, quantity) # value check and get device queries
    else: # <0 because not support
        device_queries = tokenlist

    saveLog(sentence, tokenlist)   # save logs
    print("[final] before send to iottalk,", "\ndevice query", device_queries)
    return sentence_device_name, sentence_feature,sentence_value, device_queries
        
# ======== tokenClassifer(tokendict, token) ============
# use matcher() to match each word to the token 
# token that cannot be matched will be thrown away
# input parameter: sentence, tokendict, token
# return: tokendict, token

def tokenClassifier(sentence):
    tokendict = {'A':'', 'D':'', 'F':'', 'V':[]}  # new a dict of token, default key(A/D/F/V) is set with empty string/list
    tokenlist = ['','','','',''] # new a list: token,token[0~3] store A/D/F/V token[4] store rule/error bits
    doc = nlp(sentence)
    matches = matcher(doc)
    for match_id, start, end in matches:
        token_id = nlp.vocab.strings[match_id]  # get the token ID, i.e. 'A', 'D', 'F', 'V'
        span = doc[start:end]                   # get the object of word insentence
        print("[token]", token_id, ':', span.text)
        if(token_id == 'V'):
            tokendict[token_id].append(span.text)
        elif(tokendict[token_id] == '' or tokendict[token_id] in span.text):   # if tokendict is undefined
            tokendict[token_id] = span.text     # insert key and value in tokendict
        else:
            print("too much element in one token!") # error message #1: too much token
            tokenlist[4] = -1
    return tokendict, tokenlist
    
    
# ===== quantityDetect =========
def quantityDetect(sentence, dict_for_CKIP):
    quantity = [] 
    word_list = ws([sentence], coerce_dictionary=dict_for_CKIP) # wordlist for chinese number detection
    word_list[0] = chinese_numredirection(word_list[0])
    pos_list = pos(word_list)
    entity_list = ner(word_list, pos_list)
    # in entity list , we only find out 1. cardianl 2. quanity 3. time 4. ORDINAL
    entity_list = list(entity_list)
    for entity in entity_list[0]:
        entity = list(entity)
        if(entity[2] == 'QUANTITY' or entity[2] == 'TIME' or entity[2] == 'CARDINAL' or entity[2] == 'ORDINAL' ):
            quantity.append(handleEntity(entity[2],entity[3]))
    return quantity


# == read entity
def readEntity():
    df = pd.read_csv("dict/zhTW/entity.txt")
    return df



# == handle entity, we need to change chienese entity into english entity
# for Quantity and Time search for aliasU and redirect to english ver
# for Cardinal and Ordinal, do nothing

def handleEntity(Type, Context):
    #Context might contain number(s)+unit(s)
    #extract all units
    #change all unit to english ver
    print("entity is", Context)
    if(Type == 'QUANTITY' or Type == 'TIME'):# get all the units in loop
        df = readEntity()
        for n in re.findall(r'[\u4e00-\u9fff]+', Context):
            # for each unit, get the absolute name
            df_abs = df.loc[((df['alias1'] == n) | (df['alias2'] == n) | (df['alias3'] == n))]
            eng_txt =df_abs.iloc[0][0]
            print(n, " to ", eng_txt)
            # change n to absolute name
            Context = Context.replace(n, " "+df_abs.iloc[0][0]+" ")
        print("[Entity change result]", Context)

    
    return Context.rstrip()
    
# === aliasRedirection(tokendict, tokenlist)

def aliasRedirection(tokendict, tokenlist):
    path = r"dict/zhTW/alias/" #  path for synonym
    all_files = glob.glob(os.path.join(path , "*.txt"))
    for filename in all_files:
        sublist = []
        df = pd.read_csv(filename)
        if(filename[21] == 'V'): # V is a special with a list
            V_list = list(tokendict[filename[21]])
            for idx, V_word in enumerate(V_list):
                for column in df.columns:
                    df_abs = df.loc[(df[column])== V_word]
                    if(len(df_abs.index)>0):
                        V_list[idx] = df_abs.iloc[0][0] 
            tokendict['V'] = V_list
        #redirect A,D,F to device_model, device_name, device_feature individually
        else:
            for column in df.columns:
                df_abs = df.loc[(df[column] == tokendict[filename[21]])]
                if(len(df_abs.index)>0):
                    tokendict[filename[21]] = df_abs.iloc[0][0]              
    tokenlist = [tokendict['A'], tokendict['D'], tokendict['F'], tokendict['V'], tokenlist[4]]
    print("[alias Redirect] Result:", tokenlist)
    return tokenlist





# ======= tokenValidation(tokenlist)  ========
# check if the number of token is valid
# token[4] will record rule if number of each token is enough
# token[4] will record error if number of each token is not enough
def tokenValidation(tokenlist):
    if(bool(tokenlist[0]!="") ^ bool(tokenlist[1]!="")): # check either A or D exist
        if(tokenlist[2]!=""):                        # check if F exist
            rule = ruleLookup(tokenlist[2])          # lookup rule by F
            tokenlist[4] = rule                      # token[4] record rule
        else:
            tokenlist[4]=-3                       # error message #3: no feature found in sentence 
    else:
        tokenlist[4]=-2                           # error message #2: no device found in sentence
        
    return tokenlist[4]
    
# ======= ruleLookup(feature) =======
# read the Table: DevicefeatureTable.txt
# look up the rule of the device feature and return rule number
# input parameter: feature(device_feature_name)
# return: rule id, 1 for rule 1, 2 for rule 2, 0 for not found
    
def ruleLookup(feature): #check rule by feature
    # rulelookup will read DevicefeatureTable.txt
    print("token list check rule: ", feature)
    df = pd.read_csv('dict/DevicefeatureTable.csv')
    df = df.loc[(df['device_feature']==feature)]
    rule = df.iloc[0]['rule']
    if(rule == 1):
        return 1
    elif(rule == 2):
        return 2

# ======== supportCheck(tokenlist) =====
# read DeviceTable.txt, check if F exist in device_feature_list if 
# A/D match device_model/device_name
# if support, pass
# if not support, record the error bit(tokenlist[4])
# input parameter: tokenlist
# return value: tokenlist[4](error/value bit)

def supportCheck(tokenlist):
    A = tokenlist[0]
    D = tokenlist[1]
    F = tokenlist[2]
    # read device info in DeviceTable.txt
    df = pd.read_csv('dict/DeviceTable.txt')
    DeviceTable = readDeviceTable(A,D)
    
    if(D!=''):  #check if D supports F
        print("spotlight Device table check",DeviceTable )
        feature_list = ast.literal_eval(DeviceTable.iloc[0]['device_feature_list'])
        if(F not in feature_list):
            tokenlist[4] = -4   #error message#4: Device not support such feature
            
    if(A!=''): #check if A all support F
        allsupport,d_id = 1,0
        while (d_id < len(DeviceTable.index)):
            feature_list = ast.literal_eval(DeviceTable.iloc[d_id]['device_feature_list'])
            if(F not in feature_list):
                allsupport = 0
                break
            d_id = d_id+1

        if(allsupport == 0):
            tokenlist[4] = -4 #error message #4: Device not support such feature
            
    return tokenlist[4]


# ======== valueCheck(tokenlist, feature) ============

def valueCheck(tokenlist, feature, quantityV): #issue give value
    
    A = tokenlist[0]
    D = tokenlist[1]
    F = tokenlist[2]
    stringV = tokenlist[3]
    rule = tokenlist[4]
    
    device_queries = [[0]*5]*1   # create a device query as return type of function
    print("[valueCheck] begin: ", tokenlist, feature, quantityV)
    
    df = pd.read_csv('dict/ParameterTable.csv')

    if(rule == 1):      #(issue): Used for value_dict in devicefaturetable.txt
        print("rule 1") #give a value for rule 1 in value_keyword list
        df2 = pd.read_csv('dict/zhTW/alias/aliasF.txt')
        df2 = df2.loc[ (df2['alias1']==feature) | (df2['alias2']==feature) | (df2['alias3']==feature) |  (df2['alias3']==feature) | (df2['alias4']==feature)]
        feature = df2.iloc[0]['alias1']
        #feature change to absolute device feature('open'/'close')
        
        #require table of dictionary
        df = df.loc[(df['device_feature'] == F)]
        tokenlist[3] = ast.literal_eval(df.iloc[0]['param_dict'])[feature]
        
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
        print("rule 2 not done")  
        if(D != ""):
            dimension = findDimension(D,F)
            paramTable = readParameterTable(D,F)
            V, keylist = [],[]
            num_id,str_id,key_id = 0,0,0
            for p_id in paramTable.index:
                if(paramTable['type'][p_id] == 'string'):
                    try:
                        V.append(stringV[str_id])
                        str_id+=1
                    except IndexError:
                        tokenlist[4] = -5
                elif(paramTable['type'][p_id] == 'int' or paramTable['type'][p_id] == 'float'):
                    value_find = 0           # 1. check out if stringV represent value in dictionary
                    for keyword in stringV:
                        print("keyword is", keyword)
                        if keyword in paramTable['param_dict'][p_id]:
                            V.append(ast.literal_eval(paramTable['param_dict'][p_id])[keyword])
                            key_id +=1
                            value_find =1
                            if(keyword not in keylist):
                                keylist.append(keyword)
                    if(value_find == 0): # if not find
                        try:
                            unit = paramTable['unit'][p_id]       # no unit defined in parameterTable
                            if(pd.isna(unit)):
                                print("quantity length", quantityV[num_id])
                                # we want to check if pure number
                                if(isPureNumber(quantityV[num_id])):  # pure number
                                    tokenlist[4] = checkMinMax(D,F,float(quantityV[num_id]), p_id)
                                    V.append(handleValue(quantityV[num_id]))
                                else:                             # number+unit
                                    tokenlist[4] = -5
                                    print("parameter unit undefined")
                            elif(not pd.isna(unit)):              # unit defined in parameterTable
                                if(isPureNumber(quantityV[num_id])):
                                    tokenlist[4] = checkMinMax(D,F,float(quantityV[num_id]), p_id)
                                    V.append(handleValue(quantityV[num_id]))   # pure number
                                else:
                                    quantity = handleUnit(str(quantityV[num_id]), unit)   # number + unit
                                    if(quantity is None):
                                        print("handle unit error")
                                        tokenlist[4] = -5
                                    else:
                                        tokenlist[4] = checkMinMax(D,F,quantity._magnitude, p_id)
                                        V.append(quantity._magnitude)
                            num_id += 1
                        except IndexError:
                            tokenlist[4] = -5
                            print("index out of bounds")
                    #in for loop , we check the last index
                    if(p_id == paramTable.index[-1]):
                        print("[param length]", len(paramTable.index))
                        print("[check num id]", str_id, 'length of str list',  len(stringV))
                        print("[check str id]", num_id, 'length of quan list', len(quantityV))
                        print("[check key id]", key_id, 'length of keylist', len(keylist))

                        if(key_id+len(stringV)-len(keylist)+len(quantityV) != len(paramTable.index)):
                            print("[error]: param length error")
                            tokenlist[4] = -5
                        # the equalty check:
                        # if num_id+len(strinV)+len(quantityV) has exceed the parameter length
                        # for last element, we detect if stringV and quantityV has ended 
                if(dimension == 1 & len(V) == 1):
                    device_queries = [A,D,F,V[0], tokenlist[4]]
                else:
                    device_queries = [A,D,F,V, tokenlist[4]]
         # next, we handle A
        elif(A != ''):
            df_A = pd.read_csv('dict/DeviceTable.txt')   # read DeviceTable.txt
            df_A = df_A.loc[(df_A['device_model'] == A)] # access all the dataframe which device_model equals to A
            device_list =  list(df_A['device_name'])     # get the device name list which device_model is A
            device_queries = [[0]*5]*len(device_list)    # create a query for each device in 1 device model
            print("[value check] list of device:", device_list)
            for idx, device in enumerate(device_list):
                print("[A this device]", device)
                dimension = findDimension(device,F)
                paramTable = readParameterTable(device,F)
                print("[A dimension]", dimension)
                V,keylist = [], []
                num_id, str_id, key_id = 0,0,0
                for p_id in paramTable.index:
                    if(paramTable['type'][p_id] == 'string'):
                        try:
                            V.append(stringV[str_id])
                            str_id +=1
                        except IndexError:
                            tokenlist[4] = -5
                    elif(paramTable['type'][p_id] == 'int' or paramTable['type'][p_id] == 'float'):
                        value_find = 0
                        for keyword in stringV:
                            if keyword in paramTable['param_dict'][p_id]:
                                V.append(ast.literal_eval(paramTable['param_dict'][p_id])[keyword])
                                key_id+=1
                                value_find =1
                                if(keyword not in keylist):
                                    keylist.append(keyword)
                        if(value_find == 0):
                            try:
                                unit = paramTable['unit'][p_id]       # no unit defined in parameterTable
                                if(pd.isna(unit)):
                                    if(isPureNumber(quantityV[num_id])):  # pure number
                                        tokenlist[4] = checkMinMax(device,F,float(quantityV[num_id]), p_id)
                                        V.append(handleValue(quantityV[num_id]))
                                    else:                             # number+unit
                                        tokenlist[4] = -5
                                elif(not pd.isna(unit)):              # unit defined in parameterTable
                                    if(isPureNumber(quantityV[num_id])):
                                        tokenlist[4] = checkMinMax(device,F,float(quantityV[num_id]), p_id)
                                        V.append(handleValue(quantityV[num_id]))   # pure number
                                    else:
                                        quantity = handleUnit(str(quantityV[num_id]), unit)   # number + unit
                                        if(quantity is None):
                                            tokenlist[4] = -5
                                        else:
                                            tokenlist[4] = checkMinMax(device,F,quantity._magnitude, p_id)
                                            V.append(quantity._magnitude)
                            except IndexError:
                                tokenlist[4] = -5
                                print("index out of bounds")

                    if(p_id == paramTable.index[-1]):
                        print("[param length]", len(paramTable.index))
                        print("[check num id]", num_id)
                        print("[check str id]", str_id)
                        print("[check key id]", key_id)
                        
                        if(key_id+len(stringV)-len(keylist)+len(quantityV) != len(paramTable.index)):
                            print("[error]: param length error")
                            tokenlist[4] = -5
                            
                if(dimension == 1 & len(V) == 1):
                    device_queries[idx] = [A, device, F, V[0], tokenlist[4]]
                else:
                    device_queries[idx] = [A, device, F, V, tokenlist[4]]

            
    return device_queries


# ====== handleValue(quantity) ========
# check if quantity contains value and number
# if quantity contains only number, return number
# if quantity contains number and value, return the result of handleUnit(quantitylist)
# input parameter: quantity(a string contains numeric values)
# return value: quantitylist[0] or handleUnit(quantitylist)

def handleValue(quantity):
    print("quantity: ",quantity)
    quantitylist = quantity.split(' ') # split a string into list
    
    if(len(quantitylist) == 1):
        return float(quantitylist[0])
    else:
        return handleUnit(quantitylist)

# ===== handleUnit(quantitylist) =======
# calculate the unit conversion of quantitylist
# read predefined base unit
# if number of quantitylist is even, calculate the result of unit conversion
# if number of quantitylist is 

def handleUnit(quantity, unit): # use Pint package for unit hanlding
    quantitylist = quantity.split(' ') # split a string into list
    ureg = UnitRegistry()     # new a unit module
    Q_ = ureg.Quantity        # define a quantity element quantity = (value, unit)
    
    #(issue)get base unit from iottalk define
    ureg.load_definitions('my_def.txt')
    ureg.default_system = 'iottalk'
    
    value = 0 #init value
    #(issue) When exception, catch the error message(wrong unit cannot be calculated. ex: 3 minute + 20 cm)
    if(len(quantitylist)%2 == 0):
        for q_id in range(0, len(quantitylist),2):
            try:
                value = value + Q_(int(quantitylist[q_id]), quantitylist[q_id+1]).to(unit)
#                 value = value + Q_(int(quantitylist[q_id]), quantitylist[q_id+1]).to_base_units()
            except:
                return None
        print("[base unit]:", value)
        return value
    else:
        print("Unit cannot be calculated")
        return None  # quantity error, number of value and unit mismatch
    
    
#followings are sub functions of value check
def checkMinMax(D,F, V,p_id): #check min max only for rule 2, and only in parameterTable use p_id
    print("[checkminmax]",D,F,V, p_id)
    df = pd.read_csv('dict/ParameterTable.csv')
    df_D= df.loc[(df['device_name'] == D) & (df['device_feature'] == F)]
    print(df_D)
    if( (float(V) > float(df_D['max'][p_id])) | ( float(V) < float(df_D['min'][p_id])) ): #if value exceed range
        print("exceed range")
        return -6    # return -6 as error code: exceed range
    else:
        print("in range")
        return 2     # return 2 as rule 2
    
#
def findDimension(D,F):
    df = findinfo(D,F)
    dimension = df.iloc[0]['dim']
    return dimension
    
#
def findinfo(D,F):
    df = pd.read_csv('dict/DevicefeatureTable.txt')
    df = df.loc[(df['device_name'] == D) & (df['device_feature'] == F)]
    return df

def readDeviceTable(A,D):
    df = pd.read_csv('dict/DeviceTable.txt')
    if(D != ""):
        df = df.loc[df['device_name']== D]
    elif(A != ""):
        df = df.loc[df['device_model']== A]
    return df

def readParameterTable(D,F):
    df = pd.read_csv('dict/ParameterTable.csv')
    df = df.loc[(df['device_name'] == D) & (df['device_feature'] == F)]
    return df

def isPureNumber(quantity):
    quantitylist = quantity.split(' ') # split a string into list
    if(len(quantitylist)==1):
        return True
    else:
        return False

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
    

