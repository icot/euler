#!/usr/bin/python3.2

from fractions import Fraction
from utils import factors

class CunninghamNumber:
    
    def __init__(self, exp, base, add):
        self.exp = exp
        self.base = base
        self.add = add
        self.exp_factors = factors(self.exp)
        self.algebraic_factors = self.algebraic_factorization()

    def __repr__(self):
        return repr((self.base, self.exp, self.add))

    def toFrac(self):
        return pow(self.base, self.exp) + self.add

    def algebraic_factorization(self):
        if self.exp_factors:
            alg_factors = []
            nexp = self.exp//self.exp_factors[0]
            if self.add == -1:
                if self.exp_factors[0] == 2:
                    alg_factors.append(CunninghamNumber(nexp, self.base, -1))
                    alg_factors.append(CunninghamNumber(nexp, self.base, 1).toFrac())
                else:
                    alg_factors.append(CunninghamNumber(nexp, self.base, self.add))
                    alg_factors.append(sum([pow(self.base, r * nexp) for r in range(self.exp_factors[0])]))
                return alg_factors
            elif self.add == 1:
                alg_factors.append(CunninghamNumber(nexp, self.base, self.add))
                if self.exp_factors[0] % 2 == 1:
                    alg_factors.append(sum([pow(self.base, r * nexp)*pow(-1, r) for r in range(self.exp_factors[0])]))
                else:
                    alg_factors.append(sum([pow(self.base, r * nexp)*pow(-1, r+1) for r in range(self.exp_factors[0])]))
                return alg_factors
            else:
                return []
        else:
            return []

class Repunit(CunninghamNumber):

    def __init__(self, exp, base = 10):
        super().__init__(exp, base, -1)
        self.algebraic_factors = self.algebraic_factorization()
        self.rfactors = None
        self.factors = None

    def toFrac(self):
        return Fraction(super().toFrac(), self.base + self.add)

    def full_algebraic_factorization(self):
        acc = [item for item in self.algebraic_factors]
        cond = [True for item in acc if isinstance(item, CunninghamNumber)]
        while any(cond):
            #print("Acc: ", acc)
            buf = [] 
            for item in acc:
                #print(type(item),item)
                if isinstance(item, CunninghamNumber):
                    if not item.algebraic_factors:
                        buf.append(item.toFrac())
                    else:
                        buf.extend(item.algebraic_factors)
                else:
                    buf.append(item)
            acc = buf
            cond = [True for item in acc if isinstance(item, CunninghamNumber)]
        self.rfactors = acc

    def full_factorization(self):
        self.factors = []
        First = True
        if self.rfactors:
            for item in self.rfactors:
                buf = None
                elem = None
                if First and (item % (self.base + self.add) == 0):
                    elem = item//(self.base + self.add)
                    First = False
                else:
                    elem = item
                buf = factors(elem)
                if buf:
                    self.factors.extend(buf)
                else:
                    self.factors.append(elem)
        else:
            self.factors = factors(self.toFrac())
        self.factors.sort()

def main():
    
    for a in range(1,10):
        r = Repunit(a)
        r.full_algebraic_factorization()
        r.full_factorization()
        print(a, r.rfactors, r.factors)

if __name__ == "__main__":
    main()
