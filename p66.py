#!/usr/bin/python

from math import floor, sqrt
from fractions import Fraction
from copy import copy


def pell (D):
    """Return the smallest integer set solving Pell equation
    x^2-D*y^2=1 where x, D and y are positive integers. If there are no
    solution (D is a square), return None.

    >>> pell(3)
    (2, 1)"""
    a0 = int (D**0.5)
    if a0*a0 == D: return None
    gp = [0, a0]
    gq = [1, D-a0**2]
    a = [a0, int((a0+gp[1])/gq[1])]
    p = [a[0], a[0]*a[1]+1]
    q = [1, a[1]]
    maxdepth = None
    n = 1
    while maxdepth is None or n < maxdepth:
        if maxdepth is None and a[-1] == 2*a[0]:
            r = n-1
            if r % 2 == 1: return p[r], q[r]
            maxdepth = 2*r+1
        n += 1
        gp.append (a[n-1]*gq[n-1]-gp[n-1])
        gq.append ((D-gp[n]**2)//gq[n-1])
        a.append (int ((a[0]+gp[n])//gq[n]))
        p.append (a[n]*p[n-1]+p[n-2])
        q.append (a[n]*q[n-1]+q[n-2])
    return p[2*r+1], q[2*r+1]

def reduce_frac(cfr):
    cfrepr = copy(cfr)
    cfrepr.reverse()
    fr = Fraction(cfrepr.pop())
    try:
        while 1:
            buf = cfrepr.pop()
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
        yield a0
        if a1:
            buf = a1
        else:
            break

def convergents(N):
    def step(r):
        a0 = int(floor(r))
        a1 = r - a0
        if a1:
            return (a0, 1.0 / a1)
        else:
            return (a0, None)
    start = sqrt(N)
    cf = []
    h = []
    k = []
    a0, r = step(start)
    if not r:
        return (a0, 1)
    cf.append(a0)
    h.append(a0)
    k.append(1)
    a1, r = step(r)
    h.append(a1*a0+1)
    k.append(a1)
    cf.append(a1)
    x = y = 0
    j = 1
    x = h[-1]
    y = k[-1]
    maxdepth = None
    while maxdepth is None or j < maxdepth:
        if maxdepth is None and cf[-1] == 2*cf[0]:
            R = j - 1
            if R % 2 == 1: 
                return h[R], k[R]
            else:
                maxdepth = 2 * R + 1
        aj, r = step(r)
        cf.append(aj)
        h.append(aj * h[j] + h[j-1])
        k.append(aj * k[j] + k[j-1])
        print j,cf,h,k
        j += 1
    return (h[maxdepth], k[maxdepth])

def cfrepr(N, generator_method = continued_fraction):
    gen = generator_method(N)
    a = []
    cont = True
    try:
        a = [gen.next()]
        while cont:
            elem = gen.next()
            a.append(elem)
            if elem == 2 * a[0]:
                body = a[1:-1]
                if body == body[::-1]:
                    return a
                break
    except StopIteration:
        return a
    return a

def test_solution(x,y,D):
    return ((x*x - y*y*D))

def main():
    maxx = 0
    maxd = 0
    for D in range(3, 1001):
        a = cfrepr(D)
        if len(a) > 1:
            xy = frac(a)
            x, y = xy
            if x >= maxx:
                maxx = x
                maxd = D
            print("D: %d MaxD: %d, X: %d Y: %d " % (D, maxd, x,y)), pell(D)

def main2():
    maxx = 0
    maxd = 0
    cont = 0
    errors = []
    squares = [n*n for n in range(1, 34)]
    Ds = [n for n in range(3,1001) if n not in squares]
    for D in Ds:
        x, y = convergents(D)
        print "D: %d, x: %d, y: %d Test: %d " % (D, x, y, test_solution(x,y,D)) 
        if (test_solution(x,y,D) != 1):
            cont += 1
            errors.append(D)
        if x > maxx:
            maxd = D
            maxx = x
    print "MaxD: %d, Maxx: %d, Errors: %d" % (maxd, maxx,cont)
    print errors


if __name__ == "__main__":
    main2()
