import random
import threading
import time
from iottalkpy.dan import Client
# from iottalkpy.dan import NoData

### The registeration api url, you can use IP or Domain.
api_url = 'https://test.iottalk2.tw/csm/'  # default
url2='https://test.iottalk2.tw/csm/'
# api_url = 'http://localhost/csm'  # with URL prefix
# api_url = 'http://localhost:9992/csm'  # with URL prefix + port

### [OPTIONAL] If not given or None, server will auto-generate.
device_name =  'Voice_D1'

### [OPTIONAL] If not given or None, DAN will register using a random UUID.
### Or you can use following code to use MAC address for device_addr.
# from uuid import getnode
device_addr = 'd3a5dc8e-5816-4141-9765-8baffc7e7dca'
# device_addr = "..."

### [OPTIONAL] If the device_addr is set as a fixed value, user can enable
### this option and make the DA register/deregister without rebinding on GUI
persistent_binding = True

### [OPTIONAL] If not given or None, this device will be used by anyone.
# username = 'myname'

### The Device Model in IoTtalk, please check IoTtalk document.
device_model = 'Dummy_Device'

### The input/output device features, please check IoTtalk document.
idf_list = ['DummySensor-I']
odf_list = ['DummyControl-O']

device_queries = ['A', 'D', 'F', 'V']
### Set the push interval, default = 1 (sec)
### Or you can set to 0, and control in your feature input function.
push_interval = 10  # global interval
interval = {
    'Dummy_Sensor': 3,  # assign feature interval
}


dan1 = Client()
dan1.register(url=url2,on_signal= None, on_data=None, name='Voice66', idf_list=idf_list,  odf_list=odf_list, 
              id_= 'd3a5dc8e-5816-4141-9765-8baffc7e4466', 
              profile={'model': device_model,'u_name': 'hscli',}
             )


dan2 = Client()
dan2.register(url=url2, on_signal= None, on_data=None, name='Voice88', idf_list=idf_list,  odf_list=odf_list, 
              id_= 'd3a5dc8e-5816-4141-9765-8baffc7e4488', 
              profile={'model': device_model,'u_name': 'hscli',}
             )


def sendDevicetalk(queries):
    if(queries % 4 == 0 ):
        dan1.push('DummySensor-I', 0)
    elif(queries % 4 == 1 ):
        dan1.push('DummySensor-I', 1)
    elif(queries % 4 == 2 ):
        dan2.push('DummySensor-I', 2)
    elif(queries % 4 == 3 ):
        dan2.push('DummySensor-I', 3)

for i in range(30):
    print(i)
    sendDevicetalk(i)
    time.sleep(1)



# class func_thread:
#     dan = None

#     def __init__(self, func, args, daemonlize):
#         self.thread = threading.Thread(target=func, args=args, daemon=daemonlize)

#     def start(self):
#         if self.thread:
#             self.thread.start()

#     def stop(self):
#         if self.thread:
#             self.thread.stop()

#     def push(self, device_feature, data):
#         if self.dan:
#             self.dan.push(device_feature, data)
            
            
            
            
            



# def on_register(dan):
#     t2.dan = dan
#     t2.start()
#     print('register successfully')

# def ps(device_queries):
#     for i in range(30):
#         if(i%3 == 0):
#             time.sleep(1)
#             print("ps1", device_queries)
#             t2.push('DummySensor-I', 16)

#         elif(i%3 ==1):
#             time.sleep(1)
#             print('t2',t2.dan)
# #                 t2.dan.deregister()
#             print('t2 dereg',t2.dan)
#         else:
#             time.sleep(1)
#             print('what is dan', dan)
#             t2.dan = dan.register(url=api_url, name='Voice2', idf_list=idf_list,  odf_list=odf_list, id_= 'd3a5dc8e-5816-4141-9765-8baffc7e4466')
# #                 t2.dan.on_register()
# #                 url=api_url, name='Voice1', device_model=device_model, idf_list=idf_list,  odf_list=odf_list, 
# #                                 id_= 'd3a5dc8e-5816-4141-9765-8baffc7e4466'




    
    
# # def DummySensor_I():
# #     return random.randint(0, 100)

#     # Or you want to return nothing.
#     # Note that the object `None` is treated as normal data in IoTtalk
#     #
#     # return NoData


# def DummyControl_O(data: list):
#     print(str(data[0]))

# t2 = func_thread(func=ps,args=(device_queries,), daemonlize=True) 