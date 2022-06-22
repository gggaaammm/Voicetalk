import pandas as pd
import glob
import os

## tokenize words 
path_dictA = r"dict/enUS/synonym/synonymA.txt"
path_dictD = r"dict/enUS/synonym/synonymD.txt"
path_dictF = r"dict/enUS/synonym/synonymF.txt"
path_dictV = r"dict/enUS/synonym/synonymV.txt"


path = r"dict/enUS/synonym/" #  path
all_files = glob.glob(os.path.join(path , "*.txt"))
li=[]
# read all file at once
for filename in all_files:
    print("file name:", filename)
    df = pd.read_csv(filename)
    print("df now:", df)
    for column in df.columns:
        print(column)
    # read each column in token dictionary

Asyn = pd.read_csv(path_dictA)
print(Asyn)
Asyn_list = []
for column in Asyn.columns:
    Asyn_list = Asyn_list+list(Asyn[column])
print("Asyn_list", Asyn_list)




## tokenclassifier and token 


path_dict = r"dict/DeviceTable.txt"
fields = ['A', 'D']
AD_dict = pd.read_csv(path_dict,  usecols=fields)
A_list = list(AD_dict['A'])
D_list = list(AD_dict['D'])
print("A:", A_list, "D:", D_list)

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


import ast # use abstract syntax trees to convert string to list


V_list = []
for y in range(len(V_list_raw)):
    V_list = V_list+ast.literal_eval(V_list_raw[y])
print(V_list)

U_list = []
for y in range(len(U_list_raw)):
    U_list = U_list+ast.literal_eval(U_list_raw[y])
print(U_list)


