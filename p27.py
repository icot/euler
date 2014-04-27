#!/usr/bin/python

import utils

if __name__ == "__main__":
    print "Generating Primes"
    primes = utils.FastPrimeSieve(100000)
    aes = xrange(-1000,1001)
    bes = xrange(-1000,1001)
    print "Filtering b coeficients"
    bes = filter(lambda x: abs(x) in primes, bes)
    print "Computing, first run"
    poly = {'coefs':(0,0), 'primes':0}
v v v v v v v
    candidates = []
*************
    iters = 0
^ ^ ^ ^ ^ ^ ^
    for a in aes:
        for b in bes:
v v v v v v v
            iters += 1
            if iters > 10000:
                break
            prime = True
            n = poly['primes'] 
            while prime:
                num =  n*n + a*n + b
                if num in primes:
                    n = n + 1
                    print n, poly['primes']
                else:
                    prime = False
                    if n and (n> poly['primes']):
                        poly['coefs'] = (a,b)
                        poly['primes'] = n
                        print poly
*************
            num = 1 + a + b
            if num in primes:
                candidates.append((a,b))
    print " # of candidates:", len(candidates)
    n = 2
    while len(candidates) > 1:
        keepers = []
        for item in candidates:
            num = n*n +item[0]*n + item[1]
            if num in primes:
                keepers.append(item)
            else:
                continue
        candidates = keepers
        print "N = %d, # candidates = %d " % (n, len(candidates))
        n += 1
    print candidates

                


^ ^ ^ ^ ^ ^ ^


