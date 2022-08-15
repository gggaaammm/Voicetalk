import random

from iottalkpy.dan import NoData

import libraries.Voice_001_library.safuncs as safuncs

### The registeration api url, you can use IP or Domain.
api_url = 'https://test.iottalk2.tw/csm/'

### [OPTIONAL] If not given or None, server will auto-generate.
device_name = 'Voice_001'
device_addr = '21be1863-f9b8-4ecf-8d42-48ccda50d8b8'

### [OPTIONAL] If the device_addr is set as a fixed value, user can enable
### this option and make the DA register/deregister without rebinding on GUI
persistent_binding = True

### The Device Model in IoTtalk, please check IoTtalk document.
device_model = 'VoiceContorl'

### The input/output device features, please check IoTtalk document.
idf_list = ['FanFanspeed-I1', 'FanFanspeed-I2', 'FanSwitch-I1', 'FanSwitch-I2']
odf_list = []

### Set the push interval, default = 1 (sec)
### Or you can set to 0, and control in your feature input function.
push_interval = 10  # global interval



FanFanspeed_I1_object = safuncs.FanFanspeed_I1()
FanFanspeed_I2_object = safuncs.FanFanspeed_I2()
FanSwitch_I1_object = safuncs.FanSwitch_I1()
FanSwitch_I2_object = safuncs.FanSwitch_I2()


def on_register(dan):
    FanFanspeed_I1_object.setup()
    FanFanspeed_I2_object.setup()
    FanSwitch_I1_object.setup()
    FanSwitch_I2_object.setup()
    
    
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


def FanFanspeed_I1():
    return FanFanspeed_I1_object.runs()
def FanFanspeed_I2():
    return FanFanspeed_I2_object.runs()
def FanSwitch_I1():
    return FanSwitch_I1_object.runs()
def FanSwitch_I2():
    return FanSwitch_I2_object.runs()

