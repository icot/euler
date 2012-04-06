#!/usr/bin/python

from math import log, ceil, sqrt
from partitions import partitions_gen as partitions
from utils import prime_sieve

primes = prime_sieve(200)

def main():
    nsols = int(4000000)
    limit = 2 * nsols + 1
    K = ceil(log(2*nsols)/log(3))
    K = 100
    print K
    sols = {}
    for k in range(1,int(K)+2):
        pn = partitions(int(k)+1)
        candidates = {}
        for p in pn:
            contrib = [2*x +1 for x in p]
            ndivs = reduce(lambda x,y: x*y, contrib)
            candidates[ndivs] = (contrib, p)
        keys = candidates.keys()
        keys.sort()
        keys = [key for key in keys if key >= nsols]
        if keys:
            key = keys[0]
            contrib, a = candidates[key]
            a.reverse()
            prods = [pow(pi, ai) for pi, ai in zip(primes, a)]
            num = reduce(lambda x, y: x * y, prods)
            print k, key, prods[:7], prods[-1], num
            try:
                if num < sols[key]:
                    sols[key] = num
            except KeyError:
                sols[key] = num
    inverted = {v:k for k,v in sols.items()}
    iks = inverted.keys()
    iks.sort()
    for ik in iks:
        print ik, inverted[ik]

if __name__ == "__main__":
    main()

