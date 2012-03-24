#!/usr/bin/python3.2

from functools import partial
from utils import factors
from fractions import Fraction

def Rb(b,k):
    return (pow(b, k)-1)/(b-1)

R10 = partial(Rb, 10)

def algebraic_factorization(b, k):
    kfs = factors(k)
    fs = [Fraction(1, b-1)]
    if kfs:
        n = k/kfs[0]
        fs.append(pow(b, n))
        fs.append(sum([pow(b, r) for r in range(0, k-1)]))
        return fs
    else:
         return factors(R10(k))

def main():
    for a in range(10):
        print(a, R10(a), algebraic_factorization(10, a))

if __name__ == "__main__":
    main()
