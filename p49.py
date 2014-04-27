#!/usr/bin/python

import utils

if __name__ == "__main__":
    primes = filter(lambda x: x > 1000, utils.FastPrimeSieve(9999))
    candidates = []
    for pos1 in xrange(len(primes)):
        serie = [primes[pos1]]
        for pos2 in xrange(len(primes)):
            s1 = set(map(lambda x: int(x), str(primes[pos1])))
            s2 = set(map(lambda x: int(x), str(primes[pos2])))
            if s1 == s2 and primes[pos2] not in serie:
                serie.append(primes[pos2])

        if len(serie) > 1:
            candidates.append(serie)
    for serie in candidates:
        for pos1 in xrange(len(serie)):
            for pos2 in xrange(pos1, len(serie)):
                diff = serie[pos2] - serie[pos1]
                if (serie[pos2] + diff) in serie and diff:
                    print serie[pos1], serie[pos2], serie[pos2] + diff







