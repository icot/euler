#!/usr/bin/python3.2

import timeit
import math

def eratosthenes(n):
    candidates = [item for item in range(3, n, 2)]
    L = len(candidates)
    for cpos, c in enumerate(candidates):
        if not c:
            continue
        else:
            for pos in range(cpos+c, L, c):
                candidates[pos] = 0
    candidates.insert(0,2)
    return [item for item in candidates if item > 0]

def sundaram(n):
    m = n // 2
    P = [True for item in range(m+1)]
    for i in range(1, m + 1):
        for j in range(i, ((m-i)//(2*i +1))+1 ):
            P[i + j + (2 * i * j)] = False
    primes = [ 2*k + 1 for k,v in enumerate(P) if v and 2*k+1 < n]
    return [2] + primes[1:]

MAXPRIME = 100

if __name__ == "__main__":
    N = 10
    t = timeit.Timer("eratosthenes(MAXPRIME)", "from __main__ import eratosthenes, MAXPRIME")
    print("Sieve1: %.2f usec/pass " % (1e6 * t.timeit(number=N)/float(N)))
    t = timeit.Timer("sundaram(MAXPRIME)", "from __main__ import sundaram, MAXPRIME")
    print("Sieve3: %.2f usec/pass" % (1e6 * t.timeit(number=N)/float(N)))
    print((eratosthenes(MAXPRIME)))
    print((sundaram(MAXPRIME)))
