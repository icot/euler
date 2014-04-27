#!/usr/bin/python2.7

from utils import gcd

def coprimes(n):
    return [k for k in xrange(2, (n/2) +1) if gcd(k, n) == 1]

def rpf(d):
    ns = coprimes(d)
    rpf = [ (1.0*n)/d for n in ns if (1.0*n)/d < 3.0/7 and (1.0*n)/d > 0.4284]
    return rpf

def closer(ns, N):
    c = None
    diff = 1
    for n in ns:
        d = N - n
        if abs(d) < diff and n<N:
            c = n
            diff = d
    return c, diff

if __name__ == "__main__":
    limit = 10000 
    print "Computing RPFs"
    c = 0
    diff = 1
    A = 0
    for a in xrange(1, limit +1):
        cands = rpf(a)
        cc, diffc = closer(cands, 3.0/7) 
        if diffc < diff:
            c = cc
            diff = diffc
            A = a
        if a % 1000 == 0:
            print "rpf(%d): , c: %lf, diff: %lf, a: %d" % (a, c, diff, A)
