#!/usr/bin/python

import math
import utils

def test_pandigital(num, n = 9):
    cad = str(num)
    c = map(lambda x: int(x), str(num))
    l = len(filter(lambda x: x > n, c))
    if l == 0:
        s = set(map(lambda x: int(x), str(num)))
        return ((len(s) == len(cad) == n))
    else:
        return False

def extract(num, ps):
    ps = map(lambda x: x-1, ps)
    cad = str(num)
    return int(''.join([cad[pos] for pos in ps]))

def test(num):
    subs = []
    for k in xrange(1,len(ns) + 1):
        subs.append(extract(num, range(k+1,k+4)))
    res = map(lambda x,y: x % y == 0, subs, ns)
    return all(res)
        
def test_cif(num1, num2):
    c1 = "%.3d" % num1
    c2 = "%.3d" % num2
    return c1[1:] == c2[0:2]

if __name__ == "__main__":
    ns = [2, 3, 5, 7, 11, 13, 17] 
    
    ds = []
    for n in ns:
        buf = [i for i in xrange(1000) if i % n == 0]
        buf = filter(lambda x: len(str(x)) == len(set(str(x))), buf)
        ds.append(buf)
   
    pan = []
    for d8910 in ds[6]: 
        c1 = "%.3d" % d8910
        d789s = filter(lambda x: test_cif(x, d8910), ds[5])
        for d789 in d789s:
            c2 = "%.3d" % d789
            c2 = c2[0] + c1 
            d678s = filter(lambda x: test_cif(x, d789), ds[4])
            for d678 in d678s:
                c3 = "%.3d" % d678
                c3 = c3[0] + c2
                d567s = filter(lambda x: test_cif(x, d678), ds[3])
                for d567 in d567s:
                    c4 = "%.3d" % d567
                    c4 = c4[0] + c3
                    d456s = filter(lambda x: test_cif(x, d567), ds[2])
                    for d456 in d456s:
                        c5 = "%.3d" % d456
                        c5 = c5[0] + c4
                        d345s = filter(lambda x: test_cif(x, d456), ds[1])
                        for d345 in d345s:
                            c6 = "%.3d" % d345
                            c6 = c6[0] + c5
                            d234s = filter(lambda x: test_cif(x, d345), ds[0])
                            for d234 in d234s:
                                c7 = "%.3d" % d234
                                c7 = c7[0] + c6
                                if len(c7) == len(set(c7)):
                                    for a in xrange(1,9):
                                        num = str(a) + c7
                                        if test_pandigital(num,10):
                                            print num
                                            pan.append(int(num))
    pan = list(set(pan))
    print pan
    print sum(pan)





