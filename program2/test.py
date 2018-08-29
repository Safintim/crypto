# h = int(input())
# a = int(input())
# b = int(input())
# h0 = h-a
# shag = a - b
# print(1+h0//shag+(h0 % shag+shag-1)//shag)

import hashlib
import inspect
a = inspect.getsource(hashlib)
with open('/home/timur/source/program3/has.py', 'w') as f:
    for i in a:
        f.write(i)