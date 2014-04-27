#!/usr/bin/python2.7

from utils import gcd

def coprimes(n):
    ns = range(n)
    return filter(lambda x: gcd(x, n) == 1, ns)

def rpf(d):
    ns = coprimes(d)
    rpf = [ 1.0*n/d for n in ns if n<d ]
    return rpf

if __name__ == "__main__":
    rpfs = []
    print "Computing RPFs"
    for a in xrange(2, 12001):
        buf = filter(lambda x: x < 1.0/2 and x > 1/3.0, rpf(a)) 
        rpfs.extend(buf)
    print "Sorting"
    rpfs.sort()
    print len(set(rpfs))

