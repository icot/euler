#!/usr/bin/env python

from utils import isprime, factors
import math

K = 200
m = [ 0 for k in range(0, K+1) ]

def fill():
    # k == 2^i
    for i in range(0, 8):
        m[int(math.pow(2,i))] = i
    # 
    for k in range(0, 8):
        m[int(math.pow(2,i)) + 1] = i + 1
    # general case
    m[47] = 8
    for k in range(0, K+1):
        if m[k] == 0:
            m[k] = M(k)

def load():
    with open('mk.txt') as fp:
        lines = fp.readlines()
        lines = [line[:-1] for line in lines]
        ks = map(lambda x: int(x.split()[1]), lines)
        return ks

def M(k):
    if k <= 1:
        return 0
    else:
        if isprime(k):
            return (M(k-1) + 1)
        else:
            ds = factors(k)
            ks = map(lambda x: m[x], ds)
            # print k, ds, ks
            return sum(ks)

def printm(ms):
    for k in range (1, K + 1,10):
        print k, ms[ k: k + 10]
    print "sum: ", sum(ms)

def main():
    fill()
    printm(m)
    printm(load())

if __name__ == "__main__":
    main()
    m2 = load()
    m2 = [0] + m2
    for k in range(201):
        if m[k] != m2[k] : print k, m[k], m2[k]
