# ***[import_string]***
# ***[var_define]***
# D = Device, A = Action, V = Value
self.D = 'device'
self.A = 'brightness'
self.V = {'bright':5, 'medium':3, 'dark':1}
# ***[init_content]***
voicetalk.update_table(type(self).__name__ ,self.A, self.D, self.F, self.V, Language)
# ***[runs_content]***
Token = voicetalk.get_info(type(self).__name__)
if( Token['D'] == self.D and Token['A'] ==self.A):
    if(Token['V'] in self.V):
        value = self.V[Token['V']]
    else:
        value = voicetalk.get_data(type(self).__name__)
    return value
else:
    return NoData