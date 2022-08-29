from typing import List
from iottalkpy.dan import NoData



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
name = Luminance-I
type = idf
var_setup = '';
var_setup_start_line = 4
lines = 14
ro_lines = [1, 2, 3, 4, 5, 7, 9, 10, 12]
'''

class Luminance_I(IdfFunction):
    def __init__(self):
        # Variable Setup will be inserted here.
        
        # End of Variable Setup block.
        
        return

    def runs(self)-> List[int, ]:
        value = [0, ]
        
        return value

'''
name = Switch-I
type = idf
var_setup = '';
var_setup_start_line = 4
lines = 14
ro_lines = [1, 2, 3, 4, 5, 7, 9, 10, 12]
'''

class Switch_I1(IdfFunction):
    def __init__(self):
        # Variable Setup will be inserted here.
        
        # End of Variable Setup block.
        
        return

    def runs(self)-> List[int, ]:
        value = [0, ]
        
        return value

'''
name = Luminance-O
type = odf
var_setup = '';
var_setup_start_line = 4
lines = 13
ro_lines = [1, 2, 3, 4, 5, 7, 9, 11]
'''

class Luminance_O(OdfFunction):
    def __init__(self):
        # Variable Setup will be inserted here.
        
        # End of Variable Setup block.
        
        return

    def runs(self, value: List[int, ])-> None:
        
        return

'''
name = Switch-O
type = odf
var_setup = '';
var_setup_start_line = 4
lines = 13
ro_lines = [1, 2, 3, 4, 5, 7, 9, 11]
'''

class Switch_O1(OdfFunction):
    def __init__(self):
        # Variable Setup will be inserted here.
        
        # End of Variable Setup block.
        
        return

    def runs(self, value: List[int, ])-> None:
        
        return

