#!/usr/bin/env python

import utils

primes = utils.FastPrimeSieve(int(1e10))
primes = filter(lambda x: x > 1e9, primes)

def cifras(num):
    return [int(c) for c in str(num)]

def m(num):
    cifs = cifras(num)
    reps = {c:cifs.count(c) for c in set(cifs)}
    maxr = 0
    res = None
    for c, r in reps.items():
        if r > maxr:
            res = (c,r)
            maxr = r
    return res


if __name__ == "__main__":
    mdcs = {prime:m(prime) for prime in primes if m(prime)[1] > 1}
    MDCS = {}
    # Find maximun mdc's
    for c in range(10):
        ms = [item for item in mdcs.values() if item[0]==c]
        MDCS[max(ms)] = []
    for prime, mdc in mdcs.items():
        try:
            MDCS[mdc].append(prime)
        except KeyError:
            continue
    SDCS = {}
    for k, v in MDCS.items():
        SDCS[k[0]] = sum(v)
   
    tot = 0
    for k,v in SDCS.items():
        print k,v
        tot += v
    print tot


