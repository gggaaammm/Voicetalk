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
# 1: rule1, 2: rule2, -1: error
# -2 error: no device in sentence
# -3 error: no device feature in sentence
# -4 error: device feature need value
# -5 error: D not support F

def readDB():
    # ver. 0620: update database
    # we shoud read all the synonym in to dictionary for tokenize words
    
    #create the list of synonyms to match
    
    
    path = r"dict/enUS/alias/" #  path for synonym
    all_files = glob.glob(os.path.join(path , "*.txt"))
    synonymlist={}

    # read all file at once
    for filename in all_files:
        sublist = []
        df = pd.read_csv(filename)
        for column in df.columns:
            sublist = sublist+list(df[column])
        sublist = [x for x in sublist if str(x) != 'nan']  # filter all NAN element
        synonymlist[filename[21]] = sublist

    

    #number synonym is special, read individually
    path_num_dict = r"dict/enUS/num_en.txt"
    num_dict = pd.read_csv(path_num_dict, usecols= ['text'])
    num_dict.columns = ['num']
    num_list = list(num_dict['num'])

    #obtain doc object for each word in the list and store it in a list
    # synonymlist(A),  synonymlist(D),  synonymlist(F),  synonymlist(V),
    A = [nlp(a) for a in synonymlist['A']]
    D = [nlp(d) for d in synonymlist['D']]
    F = [nlp(f) for f in synonymlist['F']]
    V = [nlp(v) for v in synonymlist['V']]
    unit = [nlp(unit) for unit in synonymlist['U']]
    num =  [nlp(num) for num in num_list]

    #add the pattern to the matcher
    matcher.add("A", A)
    matcher.add("D", D)
    matcher.add("F", F)
    matcher.add("V", V)
    matcher.add("U", unit)
    matcher.add("num", num)
    #======

def numberHandle(word):
    print("need to be handled word",word)
    df = pd.read_csv(r"dict/enUS/num_en.txt")
    df = df.loc[df['text'] == word]
    value = df.iloc[0]['value']
    return value
    

    

def textParse(sentence):
    # read database
    readDB()
    
    sentence = sentence.lower() # lower all the chracter in sentence
    
    tokenlist = ['','','','',''] # init token as empty
    tokendict = {'A':'', 'D':'', 'F':'', 'V':'', 'U':'',}
    unit = ''
    feature = ''
    rule = 0
    valid = 0
    
    quantity = {}  # pairs of n+u(number+unit)
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
            print("too much element in one token!") #error 1: wrong number of token==================
            valid = -1
        # (issue=====================================)
        #(issue: number and unit)
        if(token_id == 'num'):
            value = numberHandle(span.text)
            print('text means value:', value)
            tokenlist[3] = int(value)
        elif(token_id == 'U'): # might more than 1 unit!
            unit = span.text
            print("unit discovered:", unit)
            # pair up with value-unit
    
    # check if sentence contains number, before sentence redirecting
    # (issue)first check other token contains number(especially D: fan 1)
    # remove ADF keyword which might contain digit
    sentence = sentence.replace(tokendict['D'], "")
    
    pattern = '[0-9]+'
    numlist = re.findall(pattern, sentence)
    if(len(numlist) >= 1): # default : set last num as return value V(in case that device name contains number)
        tokenlist[3] = int(numlist[len(numlist)-1])
        
    
    print("debug now after number finding token list", tokenlist,"token dict",tokendict, "value pair", quantity)
    if(tokendict['V'] != ''):
        pass
    else:
        value_doc = nlp(sentence)    
        print(value_doc._.numerize()) # for number and unit conversion , use  numberize and pint module
        if(len(value_doc._.numerize())== 1):
            quantity = list(value_doc._.numerize())
            tokendict['V'] = handleValue(str(quantity[0]))
        
    
    #(issue) check V has unit and need conversion
#     if(unit != ''):
#         token[3] = unitConversion(token[2], token[3], unit)
#     else:
#         print('no unit conversion required')
    # (issue=====================================)
    
    
    sentence_feature = tokendict['F'] # save before synonym redirect
    sentence_device_name = tokendict['D'] 
    
    #check the synonym, redirect to iottalk ver================================
    # A,D,F,V synonym should be redirect
    path = r"dict/enUS/alias/" #  path for synonym
    all_files = glob.glob(os.path.join(path , "*.txt"))
    # read all file at once or read indvidually?
    for filename in all_files:
        sublist = []
#         print("file name:", filename)
        df = pd.read_csv(filename)
#         print("df now:\n", df)
        #redirect A,D,F to device model, device name, device feature individually
        for column in df.columns:
            df_abs = df.loc[(df[column] == tokendict[filename[21]])]
            if(len(df_abs.index)>0):
                tokendict[filename[21]] = df_abs.iloc[0][0]

    # new a list: token
    token = ['','','','',''] #token[4] store rule and valid bits
    token[0] = tokendict['A']
    token[1] = tokendict['D']
    token[2] = tokendict['F']
    token[3] = tokendict['V']
    token[4] = valid
    #(issues should be tokendict['V'], and do conversion before this)
    #token[3] = tokenlist[3]
    print("=======new token list after redirect token======\n", tokenlist)
    


    # eliminate A if both AD exist
    if(token[0] != '' and token[1] != ''):
        token[0] = ''
        print('list of token after A/D elimination:', token)


    

    
    #check if enoght token A/D+F
    #when loop end, calculate token number and check if valid.
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
        
    #now token has correct number, check if A/D support F
    if(token[4] > 0):
        token = supportCheck(token) #when support check, use DevicefeatureTable.txt
    else:
        print("not enough token!") # break
    if(token[4] > 0): # <0 because not support
        token = valueCheck(token, rule, sentence_feature) # check value is in range(rule2) or give it a value(rule1)
    

    print("last before send to iottalk", tokenlist,"token\n", token)
    
    saveLog(sentence, tokenlist)
    print("voice input feature: ", sentence_feature)
    return sentence_feature, token
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
    print("support check", tokenlist)
    A = tokenlist[0]
    D = tokenlist[1]
    F = tokenlist[2]

    #check if D supports F
    # in DeviceTable.txt
    if(D!=''):
        df = pd.read_csv('dict/DeviceTable.txt')
        df = df.loc[df['device_name']== D]
        feature_list = ast.literal_eval(df.iloc[0]['device_feature_list'])
        
        if(F not in feature_list):
            print('D not support F')
            tokenlist[4] = -5   #error #5: Device not support such feature
            
    
    #check if A support F
    if(A!=''):
        allsupport = 1
        df = pd.read_csv('dict/DeviceTable.txt')
        df_A = df.loc[df['device_model'] == A]
        print("df in support check:", df)
        # d_id = 0
        # while (d_id < len(df.index)):
        #     feature_list = ast.literal_eval(df.iloc[d_id]['device_feature_list'])
        #     print("feature list for",d_id, feature_list)
        #     if(F not in feature_list):
        #         allsupport = 0
        #         break
        #     d_id = d_id+1
        device_list =  list(df_A['device_name'])     # get the device name list which device_model is A
        for device in device_list:
            feature_list = ast.literal_eval(df.loc[(df['device_name'] == device)]['device_feature_list'])
            print("feature list for",device, feature_list)
            if(F not in feature_list):
                allsupport = 0
                break





        if(allsupport == 0):
            print("some device not support")
            tokenlist[4] = -5 #error message #5: Device not support such feature
        else:
            print("all support")
            
    return tokenlist

def valueCheck(tokenlist, rule, feature): #issue give value
    print("valueCheck", tokenlist,  feature)
    A = tokenlist[0]
    D = tokenlist[1]
    F = tokenlist[2]
    V = tokenlist[3]
    

    df = pd.read_csv('dict/DevicefeatureTable.txt')
    

    if(rule == 1):      #(issue): Used for value_dict in devicefaturetable.txt
        print("rule 1") #give a value for rule 1 in value_keyword list
        #read from alias F to get list
        df2 = pd.read_csv('dict/enUS/alias/aliasF.txt')
        df2 = df2.loc[ (df2['alias1']==feature) | (df2['alias2']==feature) | (df2['alias3']==feature) ]
        feature = df2.iloc[0]['alias1']
        #feature change to absolte device feature('open'/'close')
        
        #require table of dictionary, rule 1 dont care if A or D(if they pass the support check, they have same valu_dict)
        df = df.loc[(df['device_feature'] == F)]
        print("value check rule 1 df", df)
        tokenlist[3] = ast.literal_eval(df.iloc[0]['value_dict'])[feature]
        print("value check rule 1", tokenlist[3])
        
        
        
    elif(rule ==2):
        print("rule 2") # check value in range
        # 3 case to check
        # 1. a string(do nothing and pass)
        # 2. a number(check if exceed min/max)
        # 3. a quantity(check if unit support and check exceed min/max)
        
        if(D != ''):  #access the device info(which D and F are fitted)
            if(isinstance(V, int)):
                print('a number')
                tokenlist[4] = checkMinMax(D,F,V)
                # a value, check number min/max
            elif(isinstance(V,str)):
                print('a string')
                #find if string exist in value_dict
                df = findinfo(D,F)
                print("value check rule 2 df check", df)
                if(V in df.iloc[0]['value_dict']):
                    tokenlist[3] =  ast.literal_eval(df.iloc[0]['value_dict'])[V]
                    print("value check rule 2 string to int success: ", V)
                else:
                    print("value check rule 2 string bypass")
                           
                #give a value to string or bypass string
            else:
                print('a quantity')
                U = str(V).split(' ')[1] # check if unit in unit list
                if(len(df.loc[(df['device_name'] == D)&(df['unit_list'].str.contains(U))].index)>0):
                    print("value check rule 2 unit verified")
                else:
                    tokenlist[4] = -8 # unsupport unit
                    print("value check rule 2 quantity unit error!")
                
                
                
                tokenlist[3] = str(V).split(' ')[0] # split a string into list, extract 1 element                
                tokenlist[4] = checkMinMax(D,F,tokenlist[3])
                

                # already set to base unit, just extract the value 
            print("value check valid bit: ", tokenlist[4])
            
            
        elif(A != ''):
            print("A is ", A)
            df_A = pd.read_csv('dict/DeviceTable.txt')   # read DeviceTable.txt
            df_A = df_A.loc[(df_A['device_model'] == A)] # access all the dataframe which device_model equals to A
            device_list =  list(df_A['device_name'])     # get the device name list which device_model is A
            
            
            #(issue) list 3 cases
            if(isinstance(V, int)):
                print('a number')
                # in while loop check min max
                for device in device_list:
                    tokenlist[4] = checkMinMax(device, F, V)
                print('device model value check number:', tokenlist)

                # a value, check number min/max
            elif(isinstance(V,str)):
                print('a string')
                for device in device_list:
                    df = findinfo(device, F)
                    if(V in df.iloc[0]['value_dict']):
                        tokenlist[3] =  ast.literal_eval(df.iloc[0]['value_dict'])[V]
                print('device model value check string:', tokenlist)

                           
                #give a value to string or bypass string
            else:
                print('a quantity')
                for device in device_list:                    
                    U = str(V).split(' ')[1] # check if unit in unit list
                    if(len(df.loc[(df['device_name'] == D)&(df['unit_list'].str.contains(U))].index)>0):
                        print("value check rule 2 unit verified")
                    else:
                        tokenlist[4] = -8 # unsupport unit
                        print("value check rule 2 quantity unit error!")
                        
                    tokenlist[3] = str(V).split(' ')[0] # split a string into list, extract 1 element                
                    tokenlist[4] = checkMinMax(device,F,tokenlist[3])
                print('device model value check quantity:', tokenlist)

        
    return tokenlist


#follwings are sub functions of value cheeck
def findinfo(D,F):
    df = pd.read_csv('dict/DevicefeatureTable.txt')
    df = df.loc[(df['device_name'] == D) & (df['device_feature'] == F)]
    return df

def checkMinMax(D,F, V): #check min max only for rule 2, 
    print(D,F,V)
    df = pd.read_csv('dict/DevicefeatureTable.txt')
    df_D= df.loc[(df['device_name'] == D) & (df['device_feature'] == F)]
    if( (int(V) > int(df_D.iloc[0]['max'])) | ( int(V) < int(df_D.iloc[0]['min'])) ): #if value exceed range
        return -6    # return -6 as error code
    else:
        return 2     # return 2 as rule 2


    
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
        print(type(value))
        print(type(str(value)))
        return value
    else:
        print("error: is not by 2")
        return -7  # quantity error


    
    # if(len(quantitylist) == 2):
    #     print("only one value and one unit")
    #     print(Q_(int(quantitylist[0]), quantitylist[1]))
    #     value = Q_(int(quantitylist[0]), quantitylist[1])
    #     value = value.to_base_units()
    #     print("base unit value:", value)
    #     return str(value)
    # elif(len(quantitylist) > 2): #multiple pairs of number+units
    #     print("more pairs of number+unit")
    #     for q_id in range(0, len(quantitylist),2):
    #         value = value + Q_(int(quantitylist[q_id]), quantitylist[q_id+1]).to_base_units()
    #     print("base unit value changed:", value)
    #     print(type(str(value)))
    #     return str(value)
    
            

    
    return 0
    
    



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
    

