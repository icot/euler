#!/usr/bin/python3.2

from fractions import Fraction
from utils import factors

class DegeneratePower:
    
    def __init__(self, exp, base, add):
        self.exp = exp
        self.base = base
        self.add = add
        self.exp_factors = factors(self.exp)
        self.algebraic_factors = None

    def __repr__(self):
        return repr((self.base, self.exp, self.add))

    def toFrac(self):
        return pow(self.base, self.exp) + self.add

    def algebraic_factorization(self):
        if self.exp_factors:
            alg_factors = []
            if self.add == -1:
                nexp = self.exp//self.exp_factors[0]
                if self.exp_factors[0] == 2:
                    alg_factors.append(DegeneratePower(nexp, self.base, -1))
                    alg_factors.append(DegeneratePower(nexp, self.base, 1))
                else:
                    alg_factors.append(DegeneratePower(nexp, self.base, self.add))
                    alg_factors.append(sum([pow(self.base, r * nexp) for r in range(self.exp_factors[0])]))
                return alg_factors
            elif self.add == 1:
                alg_factors.append(DegeneratePower(nexp, self.base, self.add))
                alg_factors.append(sum([pow(self.base, r * nexp)*pow(-1, r) for r in range(self.exp_factors[0])]))
                return alg_factors
            else:
                return None
        else:
            return None

class Repunit(DegeneratePower):

    def __init__(self, exp, base = 10, factorize = False):
        super().__init__(exp, base, -1)
        if factorize:
            self.algebraic_factors = self.algebraic_factorization()

    def toFrac(self):
        return Fraction(super().toFrac(), self.base + self.add)

def main():
    for a in range(1, 20):
        r = Repunit(a, factorize = True)
        n = r.toFrac()
        ks = r.exp_factors
        print(n, ks, r.algebraic_factors)

if __name__ == "__main__":
    main()
