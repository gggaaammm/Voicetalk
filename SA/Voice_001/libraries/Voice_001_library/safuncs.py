from typing import List
from iottalkpy.dan import NoData

daemon_list = []
from ..eventdriven_ex_library.eventdriven_ex import EventDriven
event_driven = EventDriven()
daemon_list.append(event_driven)


class DfFunction:
    def setup(self):
        return None


class IdfFunction(DfFunction):
    def runs(self):
        return NoData


class OdfFunction(DfFunction):
    def runs(self, value):
        return None



'''
name = get_random
type = idf
var_setup = '';
var_setup_start_line = 5
lines = 17
ro_lines = [0, 2, 3, 4, 5, 6, 8, 10, 11, 12, 13, 15]
'''
# Using `get_random` from `eventdriven_ex_library`

class FanFanspeed_I1(IdfFunction):
    def __init__(self):
        # Variable Setup will be inserted here.
        
        # End of Variable Setup block.
        
        return

    def runs(self)-> List[int, ]:
        value = [0, ]
        result = event_driven.get_random()
        # `result` is the value of random.
        
        return value

'''
name = get_random
type = idf
var_setup = '';
var_setup_start_line = 5
lines = 17
ro_lines = [0, 2, 3, 4, 5, 6, 8, 10, 11, 12, 13, 15]
'''
# Using `get_random` from `eventdriven_ex_library`

class FanFanspeed_I2(IdfFunction):
    def __init__(self):
        # Variable Setup will be inserted here.
        
        # End of Variable Setup block.
        
        return

    def runs(self)-> List[int, ]:
        value = [0, ]
        result = event_driven.get_random()
        # `result` is the value of random.
        
        return value

'''
name = get_random
type = idf
var_setup = '';
var_setup_start_line = 5
lines = 17
ro_lines = [0, 2, 3, 4, 5, 6, 8, 10, 11, 12, 13, 15]
'''
# Using `get_random` from `eventdriven_ex_library`

class FanSwitch_I1(IdfFunction):
    def __init__(self):
        # Variable Setup will be inserted here.
        
        # End of Variable Setup block.
        
        return

    def runs(self)-> List[int, ]:
        value = [0, ]
        result = event_driven.get_random()
        # `result` is the value of random.
        
        return value

'''
name = get_random
type = idf
var_setup = '';
var_setup_start_line = 5
lines = 17
ro_lines = [0, 2, 3, 4, 5, 6, 8, 10, 11, 12, 13, 15]
'''
# Using `get_random` from `eventdriven_ex_library`

class FanSwitch_I2(IdfFunction):
    def __init__(self):
        # Variable Setup will be inserted here.
        
        # End of Variable Setup block.
        
        return

    def runs(self)-> List[int, ]:
        value = [0, ]
        result = event_driven.get_random()
        # `result` is the value of random.
        
        return value

