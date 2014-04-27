#!/usr/bin/python

import math

def test_pandigital(num):
    cad = str(num)
    s = set(map(lambda x: int(x), str(num)))
    return ((len(s) == len(cad) == 9) and 0 not in s)

def concatenated_product(num):
    p = 1
    l = 0
    prod = ''
    while l < 9:
        prod += str(num * p)
        l = len(prod)
        p = p + 1
    return (n, p-1, int(prod))


if __name__ == "__main__":
    prods = []
    limit = 1000000
    ns = xrange(1, limit)
    for n in ns:
        prod = concatenated_product(n)
        if test_pandigital(prod[2]):
            print prod
