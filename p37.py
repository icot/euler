#!/usr/bin/python

import utils

primes = utils.FastPrimeSieve(1000000)

def truncatable(n):
    global primes
    buf = n
    trunc = True
    while buf > 10:
        buf = utils.truncate_right(buf)
        if buf not in primes:
            trunc = False
            break
    if trunc == True:
        buf = n
        while buf > 10:
            buf = utils.truncate_left(buf)
            if buf not in primes:
                trunc = False
                break
        return trunc
    else:
        return False

def truncatables(primes):
    t = []
    for prime in primes:
        buf = prime 
        trunc = True
        while buf > 10:
            buf = utils.truncate_right(buf)
            if buf not in primes:
                trunc = False
                break
        if trunc == True:
            buf = prime
            while buf > 10:
                buf = utils.truncate_left(buf)
                if buf not in primes:
                    trunc = False
                    break
        if trunc:
            t.append(prime)
        if len(t) > 14:
            return t

if __name__ == "__main__":
    t = truncatables(primes)
    print sum(t[4:])
