import random

from iottalkpy.dan import NoData

import libraries.voicelibrary.safuncs as safuncs

### The registeration api url, you can use IP or Domain.
api_url = 'https://test.iottalk2.tw/csm/'

### [OPTIONAL] If not given or None, server will auto-generate.
device_name = 'Voice_D1'
device_addr = 'd3a5dc8e-5816-4141-9765-8baffc7e7dca'

### [OPTIONAL] If the device_addr is set as a fixed value, user can enable
### this option and make the DA register/deregister without rebinding on GUI
persistent_binding = True

### The Device Model in IoTtalk, please check IoTtalk document.
device_model = 'Dummy_Device'

### The input/output device features, please check IoTtalk document.
idf_list = ['DummySensor-I']
odf_list = ['DummyControl-O']

### Set the push interval, default = 1 (sec)
### Or you can set to 0, and control in your feature input function.
push_interval = 10  # global interval
value = 0

DummySensor_I_object = safuncs.DummySensor_I()
DummyControl_O_object = safuncs.DummyControl_O()

def on_register(dan):
    DummySensor_I_object.setup()
    DummyControl_O_object.setup()
    
    print('register successfully')


def DummySensor_I():
    return DummySensor_I_object.runs()


def DummyControl_O(data):
    DummyControl_O_object.runs(data)