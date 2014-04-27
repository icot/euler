#!/usr/bin/python

import utils


if __name__ == "__main__":
    primes = utils.FastPrimeSieve(1000000)
    triangle = utils.triangle_gen()
    n = triangle.next()
    ndivisors = 1
    n = n+1
    while ndivisors <100:
        n = n+1
        if n not in primes:
            ndivisors = utils.ndivisors(n)
    print n, ndivisors

