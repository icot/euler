#!/usr/bin/python

import sys
import copy
from math import exp,sqrt, floor,ceil
from utils import memoize

def ngen():
    m = 1
    ref = pow(5,6)
    while 1:
        cand = 5*m + 4
        if (((24*cand) % ref) == 1):
            if ((cand - 5) % 7) != 0 or ((cand - 6) % 11) != 0:
                yield cand
        m += 1

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
    cont = 0
    candidate = 1
    sys.setrecursionlimit = 10000
    while cont < 50:
        p = nparts(candidate)
        if p % 64 == 0:
            print candidate, p
            cont +=1
        candidate += 1

