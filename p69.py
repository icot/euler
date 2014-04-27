#!/usr/bin/python

import sys
from utils import phi
from multiprocessing import Pool

def main():
    maxq = 0
    maxn = 0
    maxtot = 0
    Phi = {}
    for n in xrange(2, 1000000):
        factors = utils.factors(n)
        fs = list(set(factors))
        if fs:
            if len(fs) < len(factors) :
                pairs = {}
                for factor in factors:
                    pairs[factor] = factors.count(factor)
                try:
                    phis = [Phi[pow(p,k)] for p,k in pairs.items()]
                    Phi[n] = reduce(lambda x, y: x*y, phis)
                    tot = Phi[n]
                except KeyError:
                    Phi[n] = n * reduce(lambda x,y: x*y, map(lambda x: 1.0 - (1.0/x), fs))
                    tot = Phi[n]
            else:
                try:
                    phis = [Phi[f] for f in fs]
                    tot = reduce(lambda x, y: x*y, phis)
                except KeyError:
                    Phi[n] = n * reduce(lambda x,y: x*y, map(lambda x: 1.0 - (1.0/x), fs))
                    tot = Phi[n]
        else:
            Phi[n] = n - 1
            tot = Phi[n]
        q = (n*1.0)/tot
        print n, tot, q
        if q > maxq:
            maxq = q
            maxn = n
            maxtot = tot
            print " ",  maxn, maxtot, maxq
    
    print ""
    print maxn, maxtot, maxq


def worker(n):
    return (n, n/phi(n))

if __name__ == "__main__":
    packetsize = int(sys.argv[2])
    nprocs = int(sys.argv[1])
    maxq = 1
    maxitem = None
    pool = Pool(processes = nprocs)
    for pos in xrange(1, 1000000, packetsize):
        print "\nComputing %d-%d" % (pos, pos + packetsize)
        ns = range(pos, pos + packetsize)
        result = pool.map(worker, ns)
        for item in result:
            if item[1] > maxq:
                maxitem = item
                maxq = item[1]
        print " Maxitem: ", maxitem
    print maxitem
