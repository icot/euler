#!/usr/bin/python3.2

import timeit
import math
from utils import FastPrimeSieve
from itertools import chain

def eratosthenes(n):
    cands = [(item+1, item+5) for item in range(0,n,6)]
    g = chain.from_iterable(cands)
    candidates = [item  for item in g if item < n]
    candidates.insert(1,2)
    candidates.insert(2,3)
    candidates = candidates[1:]
    spos = 0
    cpos = 1
    while cpos < len(candidates) :
        if candidates[cpos] % candidates[spos] == 0:
            candidates[cpos] = 0
        else:
            spos = cpos
            for pos1, c in enumerate(candidates):
                if pos1 > cpos and c % candidates[spos] == 0:
                    candidates[pos1] = 0
        cpos += 1
    return [item for item in candidates if item > 0]

def sundaram(n):
    m = n // 2
    P = [True for item in range(m+1)]
    for i in range(1, m + 1):
        for j in range(i, ((m-i)//(2*i +1))+1 ):
            P[i + j + (2 * i * j)] = False
    primes = [ 2*k + 1 for k,v in enumerate(P) if v and 2*k+1 < n]
    return [2] + primes[1:]

def FastPrimeSieve(max):
    possible_primes = [n for n in range(3,max+1, 2)]
    curr_index = -1
    max_index = len(possible_primes)
    for latest_prime in possible_primes:
        curr_index +=1
        if not latest_prime : continue
        for index_variable_not_named_j in range((curr_index+latest_prime),max_index, latest_prime): 
            possible_primes[index_variable_not_named_j]=0
    possible_primes.insert(0,2)
    return [x for x in possible_primes if x > 0]

MAXPRIME = 1000

if __name__ == "__main__":
    N = 100
    t = timeit.Timer("eratosthenes(MAXPRIME)", "from __main__ import eratosthenes, MAXPRIME")
    print("Sieve1: %.2f usec/pass " % (1e6 * t.timeit(number=N)/float(N)))
    t = timeit.Timer("FastPrimeSieve(MAXPRIME)", "from __main__ import FastPrimeSieve, MAXPRIME")
    print("Sieve2: %.2f usec/pass" % (1e6 * t.timeit(number=N)/float(N)))
    t = timeit.Timer("sundaram(MAXPRIME)", "from __main__ import sundaram, MAXPRIME")
    print("Sieve3: %.2f usec/pass" % (1e6 * t.timeit(number=N)/float(N)))
    print(len(eratosthenes(MAXPRIME)))
    print(len(FastPrimeSieve(MAXPRIME)))
    print(len(sundaram(MAXPRIME)))
