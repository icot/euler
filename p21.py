#!/usr/bin/python

import utils

if __name__ == "__main__":
    primes = utils.FastPrimeSieve(10001)
    n = [i for i in range(1,10001) if i not in primes]
    pairs = []
    for number in n:
        s1 = sum(utils.divisors(number))
        if s1 <= 10000:
            s2 = sum(utils.divisors(s1))
            if s2 == number and s1 != number:
                pairs.append((number, s1))
    print pairs
    sums = map(lambda x: x[0] + x[1], pairs)
    usums = list(set(sums))
    print pairs
    print sums
    print usums
    print sum(usums)




