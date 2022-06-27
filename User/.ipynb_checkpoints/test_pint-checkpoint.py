from pint import UnitRegistry
ureg = UnitRegistry()
ureg.load_definitions('my_def.txt') 

ureg.default_system = 'iottalk'
# ureg = UnitRegistry('my_def.txt') 

print(ureg.default_system)
# print(dir(ureg.sys))

Q_ = ureg.Quantity
value1 = Q_(100, ureg.fahrenheit)

value2 = Q_(100, ureg.percent)

value3 = Q_(100, ureg.second)

print(value1.to_base_units())
print(value2.to_base_units())
print(value3.to_base_units())


rows, cols = (10, 4)
arr = [[0]*cols]*rows
print(arr)
