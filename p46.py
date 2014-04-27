#!/usr/bin/python

import utils
import math

def test(num, primes, maxs = 100):
    for n in primes:
        for s in xrange(1, maxs):
            buf = n + 2* pow(s,2)
            cond = (num == n + 2*pow(s,2))
            if cond:
                return cond
    return cond

if __name__ == "__main__":
    limit = 10000
    primes = utils.FastPrimeSieve(10000)
    n = 1
    cond = True
    while cond:
        n = n + 2
        if n not in primes:
            nums = filter(lambda x: x<n, primes)
            cond = test(n, nums, 1000)
            print n, cond

