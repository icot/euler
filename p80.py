#!/usr/bin/python

from mpmath import *

def testint(num, th = 1e-9):
    return abs(num-round(num)) < th

def sum_digits(x):
    decs = ''.join(str(x).split('.'))[0:100]
    return reduce(lambda x, y : x+y, map(int, decs))
    

if __name__ == "__main__":
    mp.dps = 1000
    ns = range(1,101)
    print len(ns)
    buf = filter(lambda x: testint(sqrt(x)), ns)
    print buf
    #ns = filter(lambda x: not testint(sqrt(x)), ns)
    tot = 0
    for n in ns:
        if not testint(sqrt(n)):
            tot += sum_digits(sqrt(n))
        else:
            pass
    print tot
    print sum_digits(sqrt(2))
    cad = str(sqrt(2)).split('.')[1][:100]
    print len(cad), cad
