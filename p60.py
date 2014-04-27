#!/usr/bin/python

from utils import isprime, catnums, FastPrimeSieve
import sys
from itertools import combinations

def checkGroup(nums):
    pairs = combinations(nums, 2)
    try:
        while 1:
            pair = pairs.next()
            n1 = catnums(pair[0], pair[1])
            if isprime(n1):
                n2 = catnums(pair[1], pair[0])
                if not isprime(n2):
                    return False
            else:
                return False
    except StopIteration:
        return True


if __name__ == "__main__":
    limit = 5000
    print "Generating primes"
    primes = FastPrimeSieve(limit)
    print " Generated %d primes" % len(primes)

    groups = []

    print "Populating prime pairs" 
    for pos1 in xrange(len(primes)):
        g = []
        p = primes[pos1]
        for pos2 in xrange(pos1, len(primes)):
            k = primes[pos2]
            if p != k:
                g = [p,k]
                g.sort()
                g = tuple(g)
                if checkGroup(g):
                    groups.append(g)

    print " %d seed pairs" % len(groups)
    candidates = []
    for pos1 in xrange(len(groups)):
        g1 = groups[pos1]
        s1 = set(g1)
        for g2 in xrange(pos1, len(groups)):
            g2 = groups[pos2]
            s2 = set(g2)
            if len(s1.intersection(s2)) == (len(s1) -1):
                el1 = list(s1.difference(s2))[0]
                el2 = list(s2.difference(s1))[0]
                if checkGroup([el1] + list(g2)):
                    buf = list(g2) + [el1]
                    buf.sort()
                    if buf not in candidates:
                        candidates.append(buf)
                        print buf
                if checkGroup([el2] + list(g1)):
                    buf = list(g1) + [el2]
                    buf.sort()
                    if buf not in candidates:
                        candidates.append(buf)
                        print buf
    print " % expanded sets: ", (len(candidates))

    print "Checking groups"
    maxgl = 2
    oldmax = 2
    niter = 0
    candidates = [groups]
    while maxgl < 5 :
        groups = candidates[-1]
        gl = len(groups)
        new_candidates = []
        print "+++ Iteration # (%d) MaxGL: %d " % (niter, maxgl)
        for pos in range(len(groups)):
            g = groups[pos]
            for p in primes:
                if p not in g and p > max(g):
                    buf = list(g) + [p]
                    buf.sort()
                    if tuple(buf) not in new_candidates:
                        if checkGroup(buf):
                            new_candidates.append(tuple(buf)) 
                            l = len(buf)
                            if l == maxgl:
                                print "Group %d/%d %s" % (pos, gl, str(buf))
                            if l > maxgl:
                                oldmax = maxgl
                                maxgl = l
        if new_candidates != []:
            candidates.append(new_candidates)
        niter += 1
        if niter > 6:
            print oldmax, maxgl
            break
    
    for candidate in candidates[-1]:
        print list(candidate), sum(list(candidate))




