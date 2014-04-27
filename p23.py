#!/usr/bin/python

from utils import FastPrimeSieve, divisors

def test_abundant(num):
    return sum(divisors(num)) > num

if __name__ == "__main__":
    print "Calculando primos"
    primes = FastPrimeSieve(30000)
    print "Calculando numeros abundantes"
    na = [i for i in xrange(2,28124) if i not in primes and test_abundant(i)]
    print "Calculando combinaciones"
    sums = []
    for x in na:
        for y in na:
            s = x + y
            if s < 28124:
                sums.append(s)
    np = (set(sums))
    n = set(range(1,28124))
    n = n - n.intersection(np)
    print sum(list(n))
     




