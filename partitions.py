#!/usr/bin/python

import sys
import copy
from math import exp, sqrt, floor, ceil, log
from utils import memoize
from itertools import product, chain

def partitions_gen(n):
    # base case of recursion: zero is the sum of the empty list
    if n == 0:
        yield []
        return
        
    # modify partitions of n-1 to form partitions of n
    for p in partitions_gen(n-1):
        yield [1] + p
        if p and (len(p) < 2 or p[1] > p[0]):
            yield [p[0] + 1] + p[1:]

def ngen():
    m = 1
    ref = pow(5,6)
    while 1:
        cand = 5*m + 4
        if (((24*cand) % ref) == 1):
            if ((cand - 5) % 7) != 0 or ((cand - 6) % 11) != 0:
                yield cand
        m += 1

def gen5():
    n = 1
    while 1:
        yield 5*n + 4
        n += 1


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

def flatten(listOfLists):
    "Flatten one level of nesting"
    return chain.from_iterable(listOfLists)

@memoize
def partitions(n):
    if n <=1 :
        return 1
    elif n == 2:
        return 2
    else:
        j1 = [ (3*pow(k,2) -k)/2 for k in range(1, n)]
        j2 = [ (3*pow(k,2) +k)/2 for k in range(1, n)]
        js = [j for j in flatten(zip(j1,j2)) if j <= n]
        p = 0
        cpos = 0
        for pos, j in enumerate(js):
            if pos % 2 == 0:
                cpos += 1
            p += pow(-1, cpos - 1) * partitions(n-j)
        return p

def main2():
    # Last tested: 2358724
    g = 1
    n = 1
    while n<12:
        n += 1
        np = partitions(n)
        print n, np

def sigma_gen():
    exps = range(20)
    abc = product(exps, repeat=3)
    for item in abc:
        a,b,c = item
        n = pow(5,a) * pow(7,b) * pow(11,c)
        print a,b,c,n, n % (int(1e6))

if __name__ == "__main__":
    main2()

