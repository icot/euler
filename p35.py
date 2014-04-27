#!/usr/bin/python

import utils

primes = utils.FastPrimeSieve(1000000)


if __name__ == "__main__":
    cprimes = []
    p = {}
    print "Generating rotations"
    for prime in primes:
        p[prime] = utils.rotations(prime)
    
    print "Computing circular primes"
    for n, rots in p.items():
        circular = True
        for item in rots:
            try:
                p[item]
            except KeyError:
                circular = False
                break
        if circular:
            cprimes.append(prime)

    print len(cprimes)


