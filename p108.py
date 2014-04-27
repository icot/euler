#!/usr/bin/python3.2

import utils
from itertools import izip
import math

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

def gen2(primes, limit):
    k = math.ceil(math.log(limit)/math.log(3))
    return k

if __name__ == "__main__":
    solutions = 4000000*4000000
    primes = utils.prime_sieve(1000)
    print gen2(primes, solutions)
