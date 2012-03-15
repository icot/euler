#!/usr/bin/python3.2

import utils
from itertools import izip
import math

def solutions(n):
    divs = utils.divisors(n*n)
    divs += map(lambda x: -x, divs)
    xys = []
    for d in divs:
        x = n - d
        y = n - ((n*n)/(n-x))
        if x > 0 and y >0:
            xys.append((d,(x,y)))
    sols = set()
    for xy in xys:
        tup = xy[1]
        rev = (tup[1], tup[0])
        if rev not in sols: 
            sols.add(tup)
    sols = list(sols)
    sols.sort()
    return sols

def main1():
    ts = []
    n = 2
    estim = 0
    maxestim = 0
    maxn = 0
    while estim < 1000:
        #ts = solutions(n)
        ndivs = utils.ndivisors(n*n)
        estim = ndivs/2 +1
        if estim > maxestim :
            maxestim = estim
            maxn = n
            print maxn,maxestim
        #print("N: %d, estim: %d, sols: %d, ndivs(n2): %d" % (n, estim, len(ts), ndivs))
        n += 1
        

def main2():
    ndivs2 = 1998
    n2 = gennum(ndivs2)
    print math.sqrt(n2)


def gennum(ndivs):
    exps = utils.factors(ndivs)
    exps.reverse()
    exps = [exp - 1 for exp in exps]
    primes = utils.prime_sieve(100)
    g = izip(primes, exps)
    n = [pow(item[0], item[1]) for item in g]
    return reduce(lambda x, y: x * y, n)

if __name__ == "__main__":
    main1()

