#!/usr/bin/python

from utils import phi, memoize
from sieve import eratosthenes

@memoize
def phichain(n):
    buf = phi(n)
    nl = 1
    while buf > 1:
        buf = phi(buf)
        nl += 1
    return nl

if __name__ == "__main__":
    maxp = 400000
    print "Computing primes"
    primes = eratosthenes(maxp)
    lp = len(primes)
    acc = 0
    count = 0
    for p in primes:
        progress = float(count)/lp
        print "progress: %.4f" % (progress)
        length = phichain(p)
        if length == 25:
            acc += p
        count += 1
    print acc
            
