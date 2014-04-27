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
    for k in range(0, K+1):
        if m[k] == 0:
            m[k] = M(k)

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

def printm():
    for k in range (1, K + 1,10):
        print k, m[ k: k + 10] 

def main():
    fill()
    printm()

if __name__ == "__main__":
    main()
    print sum(m[:11])
    print sum(m[:21])
    print m[1:20]
    print m[1:128]
    for k in range(128):
       if m[k] > 9: print k, m[k], M(k), factors(k)
