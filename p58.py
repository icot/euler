#!/usr/bin/python

import utils
import math

def isprime(num):
    for div in xrange(2, int(math.sqrt(num)) + 1):
        if (num % div)==0:
            return False
    return True

def main1(primes):
    order = 1 
    limit = 5
    cont = 1
    r = 1
    diags = [1]
    np = [1]
    while True:
        buf = range(pow(r,2), pow(r+2,2)+1, 2)
        pos = range(cont, len(buf), cont) 
        cont = cont + 1
        newitems = [buf[p] for p in pos]
        diags.extend(newitems)
        np += [item for item in newitems if item in primes]
        perc = (float(len(np))/len(diags))
        print r, len(np), len(diags), "%.3f" % perc
        if perc <= 0.1:
            break
        r += 2

def main2():
    x = 3
    N = 1 
    np = 0 
    while True:
        d1 = x*x
        d2 = d1 -x + 1
        d3 = d1 -2*x + 2
        d4 = d1 -3*x + 3
        if isprime(d2):
            np += 1
        if isprime(d3):
            np += 1
        if isprime(d4):
            np += 1
        N += 4
        print "Rank: %d, Np: %d, N:%d, ratio: %f" % (x, np, N, float(np)/N)
        if 10 * np < N:
            break
        x += 2


if __name__ == "__main__":
    print "Computing spiral vertex"
    main2()
