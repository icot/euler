#!/usr/bin/python

import utils

primes = utils.FastPrimeSieve(1000000)

def test(num, pn):
    candidates = filter(lambda x: x < num, pn)
    candidates.reverse()
    maxl = 0
    for pos in range(len(candidates)):
        if sum(candidates[pos:]) < num:
            return maxl 
        delta = 1 
        sl = 1 
        bufl = candidates[pos]
        while bufl < num:
            if pos+delta < len(candidates):
                np = candidates[pos+delta]
                sl += 1
                bufl += candidates[pos+delta]
                delta += 1
            else:
                break
        if bufl == num:
            l = sl
            if l > maxl:
                maxl = l
    return maxl

def main1():
    maxl = 1
    primesr = utils.FastPrimeSieve(1000000)
    primesr.reverse()
    maxprime = 0
    for prime in primesr:
        if prime > 987979:
            continue
        l = test(prime, primes)
        if l > maxl:
            maxl = l
            maxprime = prime
            print prime, l, maxl, maxprime


def main2():
    serie = []
    for prime in primes:
        serie.append(prime)
        s = sum(serie)
        if s > 1e6:
            break
        if s in primes:
            continue
        else:
            serie.remove(serie[0])
        print s, len(serie)
    print sum(serie), len(serie)


if __name__ == "__main__":
    main2()





