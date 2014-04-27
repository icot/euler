#!/usr/bin/python

import math
import utils

def test_pandigital(num, n = 9):
    cad = str(num)
    c = map(lambda x: int(x), str(num))
    l = len(filter(lambda x: x > n, c))
    if l == 0:
        s = set(map(lambda x: int(x), str(num)))
        return ((len(s) == len(cad) == n) and 0 not in s)
    else:
        return False

if __name__ == "__main__":
    prods = []
    limit = 10000000 
    primes = utils.FastPrimeSieve(limit) 
    for prime in primes:
        n = len(str(prime))
        if n >= 9:
            n = 9
        if test_pandigital(prime, n):
            print prime

