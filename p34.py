#!/usr/bin/python

from utils import factorial

def func(num):
    cifs = map(lambda x:int(x), str(num))
    return sum(map(factorial, cifs))

if __name__ == "__main__":
    n = xrange(3,100000)
    res = []
    for num in n:
        if num == func(num):
            res.append(num)
    print res
    print sum(res)
