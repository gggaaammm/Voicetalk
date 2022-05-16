import DAN

def registerIottalk():
    ServerURL = 'http://140.113.199.246:9999'  
    # read all the device from db and register on iottalk
    # init all the device
    print("register all device first")
    Reg_addr = '20220501sp2'
    DAN.profile['d_name']= 'spotlight' 
    DAN.profile['dm_name']='Vlight'
    DAN.profile['df_list']=['Color-I', 'Luminance-I', 'Switch1']
    DAN.device_registration_with_retry(ServerURL, Reg_addr)
    
    Reg_addr = '20220501CHTLED'
    DAN.profile['d_name']= 'CHT LED' 
    DAN.profile['dm_name']='Vlight'
    DAN.profile['df_list']=['Luminance-I', 'Switch1']
    DAN.device_registration_with_retry(ServerURL, Reg_addr)


    #different device
    Reg_addr = '20220501sp3'
    DAN.profile['d_name']= 'indirect light' 
    DAN.profile['dm_name']='Vlight'
    DAN.profile['df_list']=['Switch1',]
    DAN.device_registration_with_retry(ServerURL, Reg_addr)
    
    #different device
    Reg_addr = '20220501Lightctl'
    DAN.profile['d_name']= 'fluorescent lamp' 
    DAN.profile['dm_name']='Vlight'
    DAN.profile['df_list']=['Switch1',]
    DAN.device_registration_with_retry(ServerURL, Reg_addr)
    
    #different device
    Reg_addr = '20220501trilight'
    DAN.profile['d_name']= 'triangle light' 
    DAN.profile['dm_name']='Vlight'
    DAN.profile['df_list']=['Switch1', 'Luminance-I']
    DAN.device_registration_with_retry(ServerURL, Reg_addr)
    
    #different device
    Reg_addr = '20220501CAGLED'
    DAN.profile['d_name']= 'CAG LED'
    DAN.profile['dm_name']='Vlight'
    DAN.profile['df_list']=['Switch1', 'Luminance-I','ColorTemperature-I']
    DAN.device_registration_with_retry(ServerURL, Reg_addr)
    
    #different device
    Reg_addr = '20220501Tatungfan'
    DAN.profile['d_name']= 'tatung fan'
    DAN.profile['dm_name']='Vfan'
    DAN.profile['df_list']=['Switch1', 'Fanspeed-I']
    DAN.device_registration_with_retry(ServerURL, Reg_addr)
    
    #different device
    Reg_addr = '20220501Chimeifan'
    DAN.profile['d_name']= 'chimei fan'
    DAN.profile['dm_name']='Vfan'
    DAN.profile['df_list']=['Switch1', 'Fanspeed-I']
    DAN.device_registration_with_retry(ServerURL, Reg_addr)
    
    #different device
    Reg_addr = '20220501curtain1'
    DAN.profile['d_name']= 'curtain1'
    DAN.profile['dm_name']='Vcurtain'
    DAN.profile['df_list']=['Switch1',]
    DAN.device_registration_with_retry(ServerURL, Reg_addr)
    
    #different device
    Reg_addr = '20220501curtain2'
    DAN.profile['d_name']= 'curtain2'
    DAN.profile['dm_name']='Vcurtain'
    DAN.profile['df_list']=['Switch1',]
    DAN.device_registration_with_retry(ServerURL, Reg_addr)
    
    #different device
    Reg_addr = '20220501curtain3'
    DAN.profile['d_name']= 'curtain3'
    DAN.profile['dm_name']='Vcurtain'
    DAN.profile['df_list']=['Switch1',]
    DAN.device_registration_with_retry(ServerURL, Reg_addr)
    
    #different device
    Reg_addr = '20220501window'
    DAN.profile['d_name']= 'window'
    DAN.profile['dm_name']='Vwindow'
    DAN.profile['df_list']=['Switch1',]
    DAN.device_registration_with_retry(ServerURL, Reg_addr)
    
    #different device
    Reg_addr = '20220501airpurifier'
    DAN.profile['d_name']= 'Tatung airpurifier'
    DAN.profile['dm_name']='Vairpurifier'
    DAN.profile['df_list']=['Switch1',]
    DAN.device_registration_with_retry(ServerURL, Reg_addr)
    
    #different device
    Reg_addr = '20220501roboticarm'
    DAN.profile['d_name']= 'robotic arm'
    DAN.profile['dm_name']='Vdummy'
    DAN.profile['df_list']=['Rotation-I',]
    DAN.device_registration_with_retry(ServerURL, Reg_addr)
    
    #different device
    Reg_addr = '20220501door'
    DAN.profile['d_name']= 'door'
    DAN.profile['dm_name']='Vdoor'
    DAN.profile['df_list']=['Switch1',]
    DAN.device_registration_with_retry(ServerURL, Reg_addr)
    