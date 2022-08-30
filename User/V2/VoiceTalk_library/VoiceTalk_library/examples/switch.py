# ***[import_string]***
# ***[var_define]***
self.A = 'device'
self.D = 'device 1'
self.F = {'open':1, 'close':0}
self.V = None
# ***[init_content]***
voicetalk.update_table(type(self).__name__ ,self.A, self.D, self.F, self.V, Language)
# ***[runs_content]***
Token = voicetalk.get_info(type(self).__name__)
if( (Token['A'] == self.A or Token['D'] ==self.D) and Token['F'] in self.F):
    value = voicetalk.get_data(type(self).__name__)
    return value
else:
    return NoData