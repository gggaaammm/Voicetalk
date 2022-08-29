from asyncore import read
import random
import threading
import time
import os
# from libraries.VoiceTalk_library.DB import DataBase
import pandas as pd
# database = DataBase()

#==========flask as backend=============
# this file will not be seen in Devicetalk
# only if download

APItext = 0
# print("startup a server")
# app.run(host='0.0.0.0',debug=True, port=19453)
# threading.Thread(target=lambda: app.run(host='0.0.0.0', port=19453, debug=True, use_reloader=False)).start()


class VoiceTalk:
    def __init__(self):
        self.data = 0
        print("init a daemon")
        self.thread = threading.Thread(target=self.daemon, daemon=True)
        print("init a daemon done")

    def get_random(self):
        return self.data

    def update_table(self,name, A, D, F, V):
        df = pd.read_csv('libraries/VoiceTalk_library/DB/TokenTable.csv')
        result_df = df.loc[(df['IDF'] == name)]
        if(len(result_df.index) == 0):
            print("update new table", name)
            df = df.append({'IDF':name , 'A': A, 'D': D, 'F': F, 'V': V}, ignore_index=True)
            df.to_csv('libraries/VoiceTalk_library/DB/TokenTable.csv', index=False)


    

    def get_data(self, name):    # read,  command  change
        # command = database.readCommand()
        # self.data = command['data']
        print("get data from certain IDF")
        df = pd.read_csv('libraries/VoiceTalk_library/DB/cmd/command.csv')
        i = df[(df.IDF == name) ].index
        print("i is:", i, type(i))
        select_df = df.loc[(df['IDF'] == name)]
        self.data = select_df['V'].iloc[0].item() 
        # print("select df", select_df, type(select_df))
        # print("self data: ", self.data, "!", type(self.data))
        df = df.drop(i)
        df.to_csv('libraries/VoiceTalk_library/DB/cmd/command.csv', index=False)
        return  self.data
    
    def get_info(self, name): # get infomation, should also think of valid value
        # command = database.readCommand()
        df = pd.read_csv('libraries/VoiceTalk_library/DB/cmd/command.csv')
        result_df = df.loc[(df['IDF'] == name)]
        if(len(result_df.index)!=0):
            print("get infomation for each IDF")
            A=df.loc[df['IDF'] == name, 'A'].iloc[0]
            D=df.loc[df['IDF'] == name, 'D'].iloc[0]
            F=df.loc[df['IDF'] == name, 'F'].iloc[0]
            V=df.loc[df['IDF'] == name, 'V'].iloc[0]
            Token ={'A':A,'D':D, 'F':F, 'V':V}
        else:
            print("get info None")
            Token = {'A':'','D':'','F':'','V':''}
        return Token

    def set_data(self, value):
        # print("set data", self.data)
        # print("set_value",  value)
        return value

    def start(self):
        if self.thread:
            print("start daemon")
            self.thread.start()

    def stop(self):
        if self.thread:
            self.thread._stop()

    def daemon(self):
        while True:
            try:
                # a protocol to send directly to chosen IDF
                self.data = random.random()
                
                print("daemon thread")
                # Push IDF data in daemon thread
                # self.dan.push(<idf_name:str>, <data:list>) 
                
                time.sleep(2)

            except:
                pass


