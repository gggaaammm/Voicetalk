import pandas as pd
import re

def checkUnit(feature, entity, word_sentence):
    print("check unit")
    df = pd.read_csv('dict/quantity.txt')
    #select only row for unit conversion
    df = df.loc[df['F_zh']==feature]
    print("feature", feature, 'u1=', df.iloc[0]['u1'])
    if(df.iloc[0]['u1'] in entity):#exist a unit(need conversion) in expression
        if(feature == '溫度'):
            temperature_unit(entity)
        elif(feature == '旋轉'):
            rotation_unit(entity)
    elif(df.iloc[0]['default'] in entity):
        print("default unit")
    
    
    
    
def rotation_unit(entity): # % -> degree
    print("rotation:")
    
    

def temperature_unit(entity): # F -> C
    print("temperature")
    num = re.findall(r'\d+', entity)
    print('num exist as', num)
    
    