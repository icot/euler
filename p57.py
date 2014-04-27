#!/usr/bin/python

import decimal
import fractions

decimal.getcontext().prec = 16 

def sqrt2(d):
    seq = [1,1,2]
    if d > 1:
        for i in xrange(d-1):
            seq.extend([1,2])
    seq = map(lambda x: decimal.Decimal(x), seq)
    while len(seq) > 1:
        den = seq.pop()
        num = seq.pop()
        acc = seq.pop()
        seq.append(acc + num/den)
    return seq[0]


if __name__ == "__main__":
    t = 0
    for d in xrange(1,1001):
        x = sqrt2(d)
        f = fractions.Fraction().from_decimal(x).limit_denominator()
        ln = len(str(f.numerator))
        ld = len(str(f.denominator))
        if ln > ld:
            t += 1
        print d, sqrt2(d), f, t
    print t
    

