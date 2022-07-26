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
name = Voice_I1
type = idf
var_setup = '';
var_setup_start_line = 4
lines = 14
ro_lines = [1, 2, 3, 4, 5, 7, 9, 10, 12]
'''

class Ｓwitch_I(IdfFunction):
    def __init__(self):
        # Variable Setup will be inserted here.
        feature_name ='[open, close, turn on , turn off]'
        # End of Variable Setup block.
		
        return

    def runs(self, inputvalue)-> List[float, ]:
        value = [0, ]
        print("-I A", inputvalue)
        return inputvalue

'''
name = Voice_O1
type = odf
var_setup = '';
var_setup_start_line = 4
lines = 13
ro_lines = [1, 2, 3, 4, 5, 7, 9, 11]
'''

class DummyControl_O(OdfFunction):
    def __init__(self):
        # Variable Setup will be inserted here.
        
        # End of Variable Setup block.
		
        return

    def runs(self, value: List[float, ])-> None:
        print("-O A",value)
        return

