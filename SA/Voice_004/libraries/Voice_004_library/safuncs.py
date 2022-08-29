from typing import List
from iottalkpy.dan import NoData

daemon_list = []
from ..VoiceTalk_library.voicetalk import VoiceTalk
voicetalk = VoiceTalk()
# Language Set = {'en-US', 'cmn-Hant-TW'}
daemon_list.append(voicetalk)
Language = 'en-US'



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
name = luminance
type = idf
var_setup = 'self.A = 'device'\nself.D = 'device 1'\nself.F = 'brightness'\nself.V = {'bright':5, 'medium':3, 'dark':1}\n';
var_setup_start_line = 5
lines = 25
ro_lines = [0, 2, 3, 4, 5, 6, 7, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 25]
'''
# Using `luminance` from `VoiceTalk_library`

class Luminance_I1(IdfFunction):
    def __init__(self):
        # Variable Setup will be inserted here.
        self.A = 'light'
        self.D = 'light 1'
        self.F = 'brightness'
        self.V = {'bright':5, 'medium':3, 'dark':1}

        # End of Variable Setup block.
        voicetalk.update_table(type(self).__name__ ,self.A, self.D, self.F, self.V)
        
        return

    def runs(self)-> List[int, ]:
        value = [0, ]
        Token = voicetalk.get_info(type(self).__name__)
        print("Token[luminance]:", Token)
        if( (Token['A'] == self.A or Token['D'] ==self.D) and Token['F'] == self.F):
            print("luminance 1 runs")
            if(Token['V'] in self.V):
                value = self.V[Token['V']]
            else:
                value = voicetalk.get_data(type(self).__name__)
            return value
        else:
            return NoData
        
        return value

'''
name = switch
type = idf
var_setup = 'self.A = 'fan'\nself.D = 'fan 1'\nself.F = {'open':1, 'close':0}\nself.V = None\n';
var_setup_start_line = 5
lines = 22
ro_lines = [0, 2, 3, 4, 5, 6, 7, 9, 11, 12, 13, 14, 15, 16, 17, 18, 20, 22]
'''
# Using `switch` from `VoiceTalk_library`

class Switch_I1(IdfFunction):
    def __init__(self):
        # Variable Setup will be inserted here.
        self.A = 'light'
        self.D = 'light 1'
        self.F = {'open':1, 'close':0}
        self.V = None

        # End of Variable Setup block.
        voicetalk.update_table(type(self).__name__ ,self.A, self.D, self.F, self.V)
        
        return

    def runs(self)-> List[int, ]:
        value = [0, ]
        Token = voicetalk.get_info(type(self).__name__)
        print("Token[switch]:", Token)
        if( (Token['A'] == self.A or Token['D'] ==self.D) and Token['F'] in self.F):
            print("switch 1 runs")
            value = voicetalk.get_data(type(self).__name__)
            return value
        else:
            return NoData
        
        return value

