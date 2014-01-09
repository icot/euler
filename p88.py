#!/usr/bin/env python

import itertools
from utils import factors
from sieve import eratosthenes as prime_sieve

# Reference to be found at http://oeis.org/A104173/b104173.txt

def prod(xs):
    return reduce(lambda x,y : x*y, xs)

def difference(a, b):
    res = list(a)
    for item in b:
        if item in res:
            res.remove(item)
    return res

def reduct_step(xs):
    gen = itertools.combinations(xs, 2)
    res = set()
    for comb in gen:
        others = difference(xs, comb)
        others.append(prod(comb))
        res.add(tuple(sorted(others)))
    return res

def reductions_full(n):
    fs = factors(n)
    acc = [fs]
    yss = [fs]
    zss = yss
    minl = min(map(len, zss))
    while minl > 2:
        for ys in yss:
            zss = reduct_step(ys)
        acc.append(zss)
        yss = zss
        minl = min(map(len, zss))
    return list(itertools.chain.from_iterable(acc[1:])) + [fs]

def main():
    primes = prime_sieve(1000)
    minns = [] 
    for k in range(2, 200):
        cond = True
        n = 2 
        while cond:
            if n in primes:
                n += 1
                continue
            combs = reductions_full(n)
            for item in combs:
                # pad with ones
                s = sum(item) + k - len(item)
                pr = prod(item)
                # print n, pr, s
                if s == pr:
                    print("K: %d, N: %d, pr: %d, s: %d" % (k, n, pr, s))
                    if pr not in minns:
                        minns.append(pr)
                    cond = False
                    break
            n += 1
    print sum(minns)

if __name__ == "__main__":
    main()
