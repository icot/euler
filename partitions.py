#!/usr/bin/python

import sys
import copy
from math import exp,sqrt, floor,ceil
from utils import memoize

def partitions(N):
    def loop(seed):
        res = copy.copy(seed)
        for p in res:
            if len(p) > 1:
                newp = p[:-2]
                newe = sum(p[-2:])
                newp.append(newe)
                newp.sort()
                newp.reverse()
                print "p: ", p, " newp: ", newp
                if newp not in res:
                    res.append(newp)
        return res

    parts = []
    # Initial seeding
    for n in xrange(1,N+1):
        parts.append( [n] + [1 for item in xrange(N - n)] )
    for p in parts:
        if len(p) > 1:
            newp = p[:-2]
            newe = sum(p[-2:])
            newp.append(newe)
            newp.sort()
            newp.reverse()
            print "p: ", p, " newp: ", newp
            if newp not in parts:
                parts.append(newp)
    return parts

def hrlimit(n):
    sqrt3 = 1.7320508075688772
    pi = 3.141592653589793
    a = 1/(4*n*sqrt3)
    b = 0.816496580927726
    ex = pi*b*sqrt(n)
    return a*exp(ex)

ps = {}

def nparts(n):
    def rp(k,n):
        global ps
        if k > n:
            return 0
        else:
            if k==n:
                return 1
            else:
                try:
                    return ps[(k,n)]
                except KeyError:
                    ps[(k,n)] = rp(k+1,n) + rp(k, n-k)
                    return ps[(k,n)]
    p = 2 
    for k in xrange(1, int(floor(n/2.0))):
        p += rp(k, n-k)
    return p

if __name__ == "__main__":
    res = 0
    print partitions(10)
