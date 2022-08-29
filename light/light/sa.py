import random

from iottalkpy.dan import NoData

import libraries.light_library.safuncs as safuncs

### The registeration api url, you can use IP or Domain.
api_url = 'https://test.iottalk2.tw/csm/'

### [OPTIONAL] If not given or None, server will auto-generate.
device_name = 'light'
device_addr = '204a72a8-0cdb-4c31-976e-6cff1f3a223b'

### [OPTIONAL] If the device_addr is set as a fixed value, user can enable
### this option and make the DA register/deregister without rebinding on GUI
persistent_binding = True

### The Device Model in IoTtalk, please check IoTtalk document.
device_model = 'Light'

### The input/output device features, please check IoTtalk document.
idf_list = ['Luminance-I', 'Switch-I1']
odf_list = ['Luminance-O', 'Switch-O1']

### Set the push interval, default = 1 (sec)
### Or you can set to 0, and control in your feature input function.
push_interval = 10  # global interval



Luminance_I_object = safuncs.Luminance_I()
Switch_I1_object = safuncs.Switch_I1()

Luminance_O_object = safuncs.Luminance_O()
Switch_O1_object = safuncs.Switch_O1()

def on_register(dan):
    Luminance_I_object.setup()
    Switch_I1_object.setup()
    
    Luminance_O_object.setup()
    Switch_O1_object.setup()
    
    print('register successfully')


def Luminance_I():
    return Luminance_I_object.runs()
def Switch_I1():
    return Switch_I1_object.runs()


def Luminance_O(data):
    Luminance_O_object.runs(data)
def Switch_O1(data):
    Switch_O1_object.runs(data)