#!/usr/bin/python

from math import floor, sqrt
from fractions import Fraction

def step(r):
    a0 = int(floor(r))
    a1 = r - a0
    if a1:
        return (a0, 1.0 / a1)
    else:
        return (a0, None)

def issequence(xs):
    seq = []
    for k, item in enumerate(xs):
        if item not in seq:
            seq.append(item)
        else:
            segment = xs[k:k+len(seq)]
            if segment == seq:
                return (len(seq), seq)
            else:
                seq.append(item)
    return (len(seq), seq)

def cfrepr(r):
    buf = r
    rep = []
    while len(rep) < 50:
        a0, a1 = step(buf)
        rep.append(a0)
        if a1:
            buf = a1
        else:
            break
    res = [rep[0]]
    seq = issequence(rep[1:])
    res.append(seq[1])
    return res

def contfrac(p, q):
    while q:
        n = p // q
        yield n
        q, p = p - q*n, q

def main():
    cont = 0
    for a in range(2, 47):
        rep = cfrepr(sqrt(a)) 
        print a, rep[1]
        if len(rep[1]) == 49:
            break
        if (len(rep[1]) % 2) == 1:
            cont += 1
    print cont

def main2():
    cont = 0
    for a in range(2, 14):
        r = Fraction(sqrt(a))
        rep = contfrac(r.numerator, r.denominator)
        seq = list(rep)
        l, mseq = issequence(seq[1:])
        print a, len(seq), l
        if (len(mseq) % 2) == 1:
            cont += 1
    print cont

if __name__ == "__main__":
    main2()
