#!/usr/bin/python

from math import floor, sqrt
from fractions import Fraction

def reduce_frac(cfr):
    fr = Fraction(cfr.pop())
    try:
        while 1:
            buf = cfr.pop()
            fr = 1 / fr
            fr += buf
    except IndexError:
        return fr

def frac(cfrepr):
    cfr = [cfrepr[0]]
    tail = cfrepr[1:]
    if len(tail) % 2 == 0:
        cfr.extend(tail[:-1])
    else:
        tail = tail + tail[:-1]
        cfr.extend(tail)
    # Reduce cfr
    fr = reduce_frac(cfr)
    return (fr.numerator, fr.denominator)

def contfrac(N):
    r = Fraction(sqrt(N))
    p = r.numerator
    q = r.denominator
    while q:
        n = p // q
        print p,q
        yield n
        q, p = p - q * n, q

def continued_fraction(N):
    def step(r):
        a0 = int(floor(r))
        a1 = r - a0
        if a1:
            return (a0, 1.0 / a1)
        else:
            return (a0, None)

    buf = sqrt(N)
    while 1:
        a0, a1 = step(buf)
        if a1:
            buf = a1
        else:
            break
        yield a0

def cfrepr(N, generator_method):
    gen = generator_method(N)
    a = []
    cont = True
    try:
        a = [gen.next()]
        while cont:
            elem = gen.next()
            a.append(elem)
            if elem == 2 * a[0]:
                check = True
                buf = a[1:-1]
                for i, item in enumerate(buf):
                    if item != buf[-(i + 1)]:
                        check = False
                if check:
                    return a
                break
    except StopIteration:
        return a
    return a

def main():
    maxx = 0
    maxd = 0
    for D in range(3, 1001):
        a = cfrepr(D, continued_fraction)
        if len(a) > 1:
            xy = frac(a)
            x, y = xy
            if x >= maxx:
                maxx = x
                maxd = D
            print "D: %d MaxD: %d, X: %d Y: %d" % (D, maxd, x,y)
            print "cfrep k:", len(a[1:]), "\n"

if __name__ == "__main__":
    main()
