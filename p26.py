#!/usr/bin/python

from mpmath import *
from math import log10

def nextn(num, obj):
    buf = num
    c = -1 
    while buf < obj:
        buf *= 10
        c += 1
    return (buf,c)

def zeros(n):
    return [0 for i in xrange(n)]

def pad(xs, n):
    return zeros(n) + xs[:len(xs)-n]

def gensequence(num, l):
    buf, c = nextn(1, num)
    seq = []
    while len(seq) < l+100:
        r = buf % num
        if r:
            q = buf / num
            if q:
                buf = r * 10
                seq.append(r)
            else:
                buf = r * 10
                seq.append(0)
        else:
            break
    return seq

def issequence(xs):
    for pos1 in xrange(len(xs)):
        seq = xs[:pos1]
        buf = xs[pos1:2*len(seq)]
        buf2 = seq
        if buf and buf == buf2:
            return (len(seq), seq)
    return (0, None)

def issequence2(xs):
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


if __name__ == "__main__":
    maxl = 0
    maxn = 0
    mp.dps = 1000
    for n in xrange(900, 1001):
        s2 = gensequence(n, 2000)
        l1, seq1 = issequence(s2[100:])
        l2, seq2 = issequence2(s2[100:])
        print ">> ", n, l1, l2 
        if l2 > maxl:
            maxn = n
            maxl = l2
    print "Maxn: %d, maxl: %d" % (maxn, maxl)
