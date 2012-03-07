#!/usr/bin/python

import sys

from utils import isprime

def partitions(N):
    def new_partitions(seed):
        newps = []
        if len(seed) > 1:
            for pos in xrange(1, len(seed) ):
                newp = seed[0:pos-1] + [sum(seed[pos-1:pos+1])] + seed[pos+1:]
                newp.sort()
                newp.reverse()
                if newp not in newps:
                    newps.append(newp)
            return newps
        else:
            return [seed]
    parts = []
    # Initial seeding
    for n in xrange(1,N):
        parts.append( [n] + [1 for item in xrange(N - n)] )
    for p in parts:
        newps = new_partitions(p)
        for newp in newps:
            if newp not in parts:
                parts.append(newp)
    return parts

def nparts(N):
    nparts.rparts = {}
    def restParts(n,k):
        if k == 0 or k ==1:
            nparts.rparts[(n,k)] = 1
            return 1
        else:
            if k > n:
                return 0
            else:
                try:
                    return nparts.rparts[(n,k)]
                except KeyError:
                    buf = restParts(n-k, k) + restParts(n, k-1)
                    nparts.rparts[(n,k)] = buf
                    return buf
    for n in xrange(N+1):
        for k in xrange(N+1):
            restParts(n,k)
            #print n,k, nparts.rparts[(n,k)]
    return nparts.rparts[(N,N)]


if __name__ == "__main__":
    pass
