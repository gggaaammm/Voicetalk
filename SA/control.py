import random

from iottalkpy.dan import NoData
import sa

device_addr = sa.device_addr
persistent_binding = sa.persistent_binding
api_url = sa.api_url
device_name = sa.device_name
device_model = sa.device_model
idf_list = sa.idf_list
odf_list = sa.odf_list
DummySensor_I_object = sa.DummySensor_I_object
DummyControl_O_object = sa.DummyControl_O_object


def on_register(dan):
    DummySensor_I_object.setup()
    DummyControl_O_object.setup()  
    print('register successfully')
