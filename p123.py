#!/usr/bin/python

from utils import FastPrimeSieve

primes = FastPrimeSieve(10000000)

def f(pn, n):
    return (pow(pn - 1, n)+pow(pn + 1, n)) % pow(pn, 2)
    
if __name__ == "__main__":
    k=0
    for n in xrange(len(primes)):
        pn = primes[n]
        r = f(pn, n+1)
        if r > 1e10:
            print ">> ", n+1, pn, r
            break
        if (k % 1000) == 0:
            print "> ", n+1, pn, r
        k += 1

