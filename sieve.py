#!/usr/bin/python3.2

import timeit
import math

def eratosthenes(n):
    candidates = [item for item in range(3, n, 2)]
    L = len(candidates)
    for cpos, c in enumerate(candidates):
        if c:
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

def lucky(n):
    lucky = [item for item in range(1, n, 2)]
    cpos = 1
    L = len(lucky)
    while cpos < L:
        c = lucky[cpos]
        cont = 1
        for pos in range(L):
            if cont == c:
                lucky[pos] = 0
                cont = 1 
            else:
                cont += 1
        lucky = [item for item in lucky if item]
        L = len(lucky)
        cpos += 1
    return lucky

MAXPRIME = 100000

if __name__ == "__main__":
    N = 20
    t = timeit.Timer("eratosthenes(MAXPRIME)", "from __main__ import eratosthenes, MAXPRIME")
    print("Eratosthenes: %.2f usec/pass " % (1e6 * t.timeit(number=N)/float(N)))
    t = timeit.Timer("sundaram(MAXPRIME)", "from __main__ import sundaram, MAXPRIME")
    print("Sundaram: %.2f usec/pass" % (1e6 * t.timeit(number=N)/float(N)))
    #t = timeit.Timer("lucky(MAXPRIME)", "from __main__ import lucky, MAXPRIME")
    #print("Lucky: %.2f usec/pass" % (1e6 * t.timeit(number=N)/float(N)))
    print(len(eratosthenes(MAXPRIME)))
    print(len(sundaram(MAXPRIME)))
