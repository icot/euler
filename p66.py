#!/usr/bin/python

from math import floor, sqrt
from fractions import Fraction

def frac(cfrepr):
    cfr = [cfrepr[0]]
    tail = cfrepr[1:]
    if len(tail) % 2 == 0:
        cfr.extend(tail[:-1])
    else:
        tail = tail + tail[:-1]
        cfr.extend(tail)
    # Reduce cfr
    fr = Fraction(cfr.pop())
    try:
        while 1:
            buf = cfr.pop()
            fr = 1 / fr
            fr += buf
    except IndexError:
        return (fr.numerator, fr.denominator)

def contfrac(N):
    r = Fraction(sqrt(N))
    p = r.numerator
    q = r.denominator
    while q:
        n = p // q
        yield n
        q, p = p - q * n, q

def cfrepr(N):
    gen = contfrac(N)
    a = [gen.next()]
    cont = True
    try:
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
    for D in range(3, 20):
        a = cfrepr(D)
        if len(a) > 1:
            xy = frac(a)
            x, y = xy
            if x >= maxx:
                maxx = x
                maxd = D
            print "D: %d Maxx: %d MaxD: %d, X: %d Y: %d" % (D, maxx, maxd, x,y)
            print "cfrep: ", a, "k:", len(a[1:]), "\n"

if __name__ == "__main__":
    main()
