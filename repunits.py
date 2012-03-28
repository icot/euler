#!/usr/bin/python3.2

from fractions import Fraction
from utils import factors

class DegeneratePower:
    
    def __init__(self, exp, base, add):
        self.exp = exp
        self.base = base
        self.add = add

    def toFrac(self):
        return pow(self.base, self.exp) + self.add

class Repunit(DegeneratePower):

    def __init__(self, exp, base = 10, factorize = False):
        super().__init__(exp, base, -1)
        self.exp_factors = factors(self.exp)
        self.algebraic_factors = []
        if factorize:
            self.algebraic_factorization()

    def algebraic_factorization(self):
        pass

    def toFrac(self):
        return Fraction(super().toFrac(), self.base + self.add)

def main():
    for a in range(1,10):
        r = Repunit(a)
        n = r.toFrac()
        ks = r.exp_factors
        print(n, ks)

if __name__ == "__main__":
    main()
