import random

from iottalkpy.dan import NoData

import libraries.Voice_004_library.safuncs as safuncs

### The registeration api url, you can use IP or Domain.
api_url = 'https://test.iottalk2.tw/csm/'

### [OPTIONAL] If not given or None, server will auto-generate.
device_name = 'Voice_004'
device_addr = '3d0c5ab9-d0d3-41ad-b6f1-42569301a2ab'

### [OPTIONAL] If the device_addr is set as a fixed value, user can enable
### this option and make the DA register/deregister without rebinding on GUI
persistent_binding = True

### The Device Model in IoTtalk, please check IoTtalk document.
device_model = 'VoiceContorl'

### The input/output device features, please check IoTtalk document.
idf_list = ['Luminance-I1', 'Switch-I1']
odf_list = []

### Set the push interval, default = 1 (sec)
### Or you can set to 0, and control in your feature input function.
push_interval = 3  # global interval



Luminance_I1_object = safuncs.Luminance_I1()
Switch_I1_object = safuncs.Switch_I1()


def on_register(dan):
    Luminance_I1_object.setup()
    Switch_I1_object.setup()
    
    
    if safuncs.daemon_list:
        for thread_object in safuncs.daemon_list:
            try:
                thread_object.dan = dan
                thread_object.start()
            except:
                pass
    print('register successfully')

def on_deregister(dan):
    if safuncs.daemon_list:
        for thread_object in safuncs.daemon_list:
        	try:
        		thread_object.stop()
        	except:
        		pass


def Luminance_I1():
    return Luminance_I1_object.runs()
def Switch_I1():
    return Switch_I1_object.runs()

