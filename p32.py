#!/usr/bin/python

import math

def test_pandigital(num):
    cad = str(num)
    s = set(map(lambda x: int(x), str(num)))
    return ((len(s) == len(cad) == 9) and 0 not in s)

if __name__ == "__main__":
    prods = []
    limit = 10000
    xs = xrange(1, limit)
    ys = xrange(1, limit)
    for x in xs:
        lx = len(str(x))
        for y in xrange(x, limit) :
            ly = len(str(y))
            mlp = 9 - lx -ly
            maxp = pow(10, mlp) -1
            p = x*y
            lp = len(str(p))
            if p <= maxp and ((lp+lx+ly) == 9):
                if test_pandigital(int(str(x) + str(y) + str(p))):
                    print x, y, p
                    prods.append(p)
    print set(prods)
    print sum(list(set(prods)))
