import random

from iottalkpy.dan import NoData

import libraries.Voice_0725_library.safuncs as safuncs

### The registeration api url, you can use IP or Domain.
api_url = 'https://test.iottalk2.tw/csm/'

### [OPTIONAL] If not given or None, server will auto-generate.
device_name = 'Voice_0725'
device_addr = 'd45efe8e-30c4-49aa-8d83-9d537641a8d2'

### [OPTIONAL] If the device_addr is set as a fixed value, user can enable
### this option and make the DA register/deregister without rebinding on GUI
persistent_binding = True

### The Device Model in IoTtalk, please check IoTtalk document.
device_model = 'VoiceContorl'

### The input/output device features, please check IoTtalk document.
idf_list = ['Fan1Fanspeed-I', 'Fan1Switch-I', 'Fan2Fanspeed-I', 'Fan2Switch-I', 'Light1Luminance-I', 'Light1Switch-I']
odf_list = []

### Set the push interval, default = 1 (sec)
### Or you can set to 0, and control in your feature input function.
push_interval = 10  # global interval



Fan1Fanspeed_I_object = safuncs.Fan1Fanspeed_I()
Fan1Switch_I_object = safuncs.Fan1Switch_I()
Fan2Fanspeed_I_object = safuncs.Fan2Fanspeed_I()
Fan2Switch_I_object = safuncs.Fan2Switch_I()
Light1Luminance_I_object = safuncs.Light1Luminance_I()
Light1Switch_I_object = safuncs.Light1Switch_I()


def on_register(dan):
    Fan1Fanspeed_I_object.setup()
    Fan1Switch_I_object.setup()
    Fan2Fanspeed_I_object.setup()
    Fan2Switch_I_object.setup()
    Light1Luminance_I_object.setup()
    Light1Switch_I_object.setup()
    
    
    print('register successfully')


def Fan1Fanspeed_I():
    return Fan1Fanspeed_I_object.runs()
def Fan1Switch_I():
    return Fan1Switch_I_object.runs()
def Fan2Fanspeed_I():
    return Fan2Fanspeed_I_object.runs()
def Fan2Switch_I():
    return Fan2Switch_I_object.runs()
def Light1Luminance_I():
    return Light1Luminance_I_object.runs()
def Light1Switch_I():
    return Light1Switch_I_object.runs()

