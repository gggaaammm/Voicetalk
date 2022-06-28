import pandas as pd
import glob
import os



## step 1: read all the synonym (and number exception handling as well)
## step 2: redirect synonym into ADFV standard word


## tokenize words 
path_dictA = r"dict/enUS/synonym/synonymA.txt"
path_dictD = r"dict/enUS/synonym/synonymD.txt"
path_dictF = r"dict/enUS/synonym/synonymF.txt"
path_dictV = r"dict/enUS/synonym/synonymV.txt"


path = r"dict/enUS/synonym/" #  path dicided
all_files = glob.glob(os.path.join(path , "*.txt"))
synonymlist={}

# read all file at once and send to nlp
for filename in all_files:
    sublist = []
    print("file name:", filename)
    df = pd.read_csv(filename)
    print("df now:", df)
    for column in df.columns:
        sublist = sublist+list(df[column])
    
    sublist = [x for x in sublist if str(x) != 'nan']
    synonymlist[filename[25]] = sublist

# read each column in token dictionary
print("result synonyn list:", synonymlist)
    
#obtain doc object for each word in the list and store it in a list
# A = [nlp(a) for a in A_list]
# D = [nlp(d) for d in D_list]
# F = [nlp(f) for f in F_list]
# V = [nlp(v) for v in V_list]
# unit = [nlp(unit) for unit in unit_list]
# num =  [nlp(num) for num in num_list]


    
##=========================== online code start========================    
#read all the A synonym    
Asyn = pd.read_csv(path_dictA)
Asyn_list = []
for column in Asyn.columns:
    Asyn_list = Asyn_list+list(Asyn[column])
print("Asyn_list", Asyn_list)
#read all the F synonym    
Fsyn = pd.read_csv(path_dictF)
Fsyn_list = []
for column in Fsyn.columns:
    Fsyn_list = Fsyn_list+list(Fsyn[column])
print("Fsyn_list", Fsyn_list)

##=========================== online code start========================    




## tokenclassifier and token 


# path_dict = r"dict/DeviceTable.txt"
# fields = ['A', 'D']
# AD_dict = pd.read_csv(path_dict,  usecols=fields)
# A_list = list(AD_dict['A'])
# D_list = list(AD_dict['D'])
# print("A:", A_list, "D:", D_list)

#feature must through synonym test
# create a synonym table
# use synonym.txt is ok?
path_sy = r"dict/Featuresynonym.txt"
F_dict = pd.read_csv(path_sy)

F_list_raw = list(F_dict['F'])+list(F_dict['syn1'])+list(F_dict['syn2'])+list(F_dict['syn3'])
F_list = [x for x in F_list_raw if str(x) != 'nan']
print(F_list)


#for U_list, V_list, read DevicefeatureTable

path_DFTable =r"dict/DevicefeatureTable.txt"
fields = ['unit_list', 'value_list']
UV_dict = pd.read_csv(path_DFTable, usecols = fields)
V_list_raw = list(UV_dict['value_list'])
U_list_raw = list(UV_dict['unit_list'])

V_list_raw = [x for x in V_list_raw if str(x) != 'nan']
U_list_raw = [x for x in U_list_raw if str(x) != 'nan']


import ast # use abstract syntax trees to convert string to list


V_list = []
print("length is",len(V_list_raw))
for y in range(len(V_list_raw)):
    V_list = V_list+ast.literal_eval(V_list_raw[y])
print(V_list)

U_list = []
for y in range(len(U_list_raw)):
    U_list = U_list+ast.literal_eval(U_list_raw[y])
print(U_list)


