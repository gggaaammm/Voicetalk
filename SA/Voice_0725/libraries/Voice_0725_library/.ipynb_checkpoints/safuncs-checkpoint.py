from typing import List
from iottalkpy.dan import NoData

Language = 'en-US'
sentence = 'set fan 2 fan speed to high'
valuetopush = 4

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
name = fan1fanspeed
type = idf
var_setup = 'self.A = 'fan'\nself.D = 'fan 1'\nself.F = 'fan speed'\nself.V = {'high':5, 'medium':3, 'low': 1}\nself.F';
var_setup_start_line = 4
lines = 15
ro_lines = [1, 2, 3, 4, 5, 7, 9, 10, 13]
'''

class Fan1Fanspeed_I(IdfFunction):
    def __init__(self):
        # Variable Setup will be inserted here.
        self.A = 'fan'
        self.D = 'fan 1'
        self.F = 'fan speed'
        self.V = {'high':5, 'medium':3, 'low': 1}
        self.F
        # End of Variable Setup block.
        
        return

    def runs(self)-> List[int, ]:
        value = [0, ]
        if(self.D in sentence and self.F in sentence):
            value = valuetopush
        return value

'''
name = fan1switch
type = idf
var_setup = 'self.A = 'fan'\nself.D = 'fan 1'\nself.F = {'open':1, 'close':0}\nself.V = {'high':5, 'medium':3, 'low': 1}\nself.F';
var_setup_start_line = 4
lines = 15
ro_lines = [1, 2, 3, 4, 5, 7, 9, 10, 13]
'''

class Fan1Switch_I(IdfFunction):
    def __init__(self):
        # Variable Setup will be inserted here.
        self.A = 'fan'
        self.D = 'fan 1'
        self.F = {'open':1, 'close':0}
        self.V = {'high':5, 'medium':3, 'low': 1}
        self.F
        # End of Variable Setup block.
        
        return

    def runs(self)-> List[int, ]:
        value = [0, ]
        if(self.D in sentence and self.F in sentence):
            value = valuetopush
        return value

'''
name = fan2fanspeed
type = idf
var_setup = 'self.A = 'fan'\nself.D = 'fan 2'\nself.F = 'fan speed'\nself.V = {'high':8, 'medium':4, 'low': 1}';
var_setup_start_line = 4
lines = 15
ro_lines = [1, 2, 3, 4, 5, 7, 9, 10, 13]
'''

class Fan2Fanspeed_I(IdfFunction):
    def __init__(self):
        # Variable Setup will be inserted here.
        self.A = 'fan'
        self.D = 'fan 2'
        self.F = 'fan speed'
        self.V = {'high':8, 'medium':4, 'low': 1}
        # End of Variable Setup block.
        
        return

    def runs(self)-> List[int, ]:
        value = [0, ]
        print("self.D", self.D)
        if(self.D in sentence and self.F in sentence):
            print("yes")
            value = valuetopush
        else:
            print("no")
        return value

'''
name = fan2switch
type = idf
var_setup = 'self.A = 'fan'\nself.D = 'fan 2'\nself.F = {'open':1, 'close':0}';
var_setup_start_line = 4
lines = 15
ro_lines = [1, 2, 3, 4, 5, 7, 9, 10, 13, 15]
'''

class Fan2Switch_I(IdfFunction):
    def __init__(self):
        # Variable Setup will be inserted here.
        self.A = 'fan'
        self.D = 'fan 2'
        self.F = {'open':1, 'close':0}
        # End of Variable Setup block.
        
        return

    def runs(self)-> List[int, ]:
        value = [0, ]
        if(self.D in sentence and self.F in sentence):
            value = valuetopush
        return value

'''
name = light1luminance
type = idf
var_setup = 'self.A = 'light'\nself.D = 'light 1'\nself.F = 'brightness'\nself.V = {'high':100, 'medium':50, 'low': 10}';
var_setup_start_line = 4
lines = 15
ro_lines = [1, 2, 3, 4, 5, 7, 9, 10, 13]
'''

class Light1Luminance_I(IdfFunction):
    def __init__(self):
        # Variable Setup will be inserted here.
        self.A = 'light'
        self.D = 'light 1'
        self.F = 'brightness'
        self.V = {'high':100, 'medium':50, 'low': 10}
        # End of Variable Setup block.
        
        return

    def runs(self)-> List[int, ]:
        value = [0, ]
        if(self.D in sentence and self.F in sentence):
            value = valuetopush
        return value

'''
name = light1switch
type = idf
var_setup = 'self.A = 'light'\nself.D = 'light 1'\nself.F = {'open':1, 'close':0}';
var_setup_start_line = 4
lines = 14
ro_lines = [1, 2, 3, 4, 5, 7, 9, 10, 12, 14]
'''

class Light1Switch_I(IdfFunction):
    def __init__(self):
        # Variable Setup will be inserted here.
        self.A = 'light'
        self.D = 'light 1'
        self.F = {'open':1, 'close':0}
        # End of Variable Setup block.
        
        return

    def runs(self)-> List[int, ]:
        value = [0, ]
        
        return value

