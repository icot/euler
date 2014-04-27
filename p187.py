#!/usr/bin/python

from utils import FastPrimeSieve
from bisect import bisect_left

limit = 100000000
N = int(limit/2+1)
ns = FastPrimeSieve(N)
primes = ns

def phi(n):
    global primes
    return bisect_left(primes, n)
    
if __name__ == "__main__":
    cont = 0
    for pos, p in enumerate(ns):
        a1 = phi(limit*1.0/p)
        a2 = phi(p)
        if a1 <= a2:
            break
        cont += (a1 - a2)
        primes = filter(lambda x: x < limit*1.0/p, primes)
        print p, len(primes)
    print cont 


