import numpy as np
import _pickle as cPickle
import codecs

a2 = np.arange(24).reshape(3,4,2)
a = [
    [[2.45,243],[3.45,128]],[[1,67],[8.6,255]]
    ]
b = cPickle.dumps(a)
print(b)
print(type(b))

s = str(b)[2:-1]
print(s)
print(type(s))

b1 = bytes(s, encoding="gbk")
print(b1)
print(type(b1))

b2 = codecs.escape_decode(b1, 'hex-escape')[0]
print(b2)
print(type(b2))

a1 = cPickle.loads(b2)
print(a1)
print(type(a1))
