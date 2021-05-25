import time
from bitstring import BitStream, BitArray
from bitarray import bitarray

t = BitArray(bin='10000000') # on
t = (129).to_bytes(1,'big')
tid = (11223).to_bytes(2, 'big')
p = (240).to_bytes(1,'big')
print(tid)
t = bytearray(t)
tid = bytearray(tid)
p = bytearray(p)
t.extend(tid)
t.extend(p)

print(t)
print(t[0])
print(t[1:3])
print(t[3])
# 0x80046230
# 0x80046230

trigger = True if t[0]&128 != 0 else False
id = int.from_bytes(t[1:3], byteorder='big',  signed=False)
position = t[3] >> 4
print(trigger, id, position)

