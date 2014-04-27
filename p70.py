#!/usr/bin/python 

import utils
import cPickle

with open('phi.txt') as fp:
    print "Reading File"
    phi = fp.readlines()
    print "Converting"
    phi = map(lambda x: tuple(map(int, x[:-1].split(' '))), phi)

def test_perm(a, b):
    ca = map(lambda x: x, str(a))
    cb = map(lambda x: x, str(b))
    sa = set(ca)
    sb = set(cb)
    if ((sa == sb) and (len(ca) == len(cb))):
        for item in tuple(sa):
            if ca.count(item) != cb.count(item):
                return False
        return True

if __name__ == "__main__":
    candidates = filter(lambda x: test_perm(x[0], x[1]), phi)
    print "Ncandidates = ", len(candidates)
    minr = 100
    minn = None
    for pair in candidates[1:]:
        n, phi = pair
        r = (n*1.0)/phi
        if r < minr:
            minn = n
            minr = r
            print n, phi, r

