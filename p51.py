#!/usr/bin/python

import utils
from itertools import *

def test_prime_family(n):
    cad = str(n)
    for c in xrange(len(cad)):
        print 
    for cif in range(0,9):
        pass

def compress(data, selectors):
    l = (d for d, s in izip(data, selectors) if not s)
    r = []
    try:
        while 1:
            r.append(l.next())
    except StopIteration:
        return int(str(''.join(r)))


def test(data, selectors):
    l = (d for d, s in izip(data, selectors) if s)
    r = []
    try:
        while 1:
            r.append(l.next())
    except StopIteration:
        return len(set(r)) == 1

def selectors(l):
    gen = product([0,1], repeat=l)
    s = []
    try:
        while 1:
            item = gen.next()
            if sum(item) >= 1 and sum(item) <=4:
                s.append(item)
    except StopIteration:
        return s

if __name__ == "__main__":
    print "Generating Primes"
    primes = utils.FastPrimeSieve(1000000)
    print len(primes)
    candidates = filter(lambda x: x> 50000, primes)

    pdict = {}
    for prime in candidates:
        k = len(str(prime))
        try:
            pdict[k].append(prime)
        except KeyError:
            pdict[k] = [prime]

    families = {}
    print "Generating prime families"
    for k in pdict.keys():
        ss = selectors(k)
        primes = pdict[k]
        for selector in ss:
            for prime in primes:
                try:
                    k1 = compress(str(prime), selector)
                    k2 = ''.join(map(str, selector))
                    families[(k,k1,k2)].append(prime)
                except KeyError:
                    families[(k,k1,k2)] = [prime]

    print "Looking for longest family"
    maxl = 0
    octofam = []
    for k, v in families.items():
        buf = list(set(v))
        selector = map(int, k[-1])
        buf = filter(lambda x: test(str(x), selector), buf)
        buf.sort()
        l = len(buf)
        if l > maxl:
            print k, buf
            maxl = l
        if len(buf) == 8:
            octofam.append(buf)
    print len(octofam), octofam
            



