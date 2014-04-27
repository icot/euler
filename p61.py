#!/usr/bin/env python

from itertools import product, permutations

def test_chain(num1, num2):
    return str(num1)[-2:] == str(num2)[0:2]

def test_nss(nss):
    candidates = [[n1,n2] for n1 in nss[0] for n2 in nss[1] if test_chain(n1,n2)]
    for pos in xrange(2,6):
        ns = nss[pos]
        buf = []
        for n in ns:
            for candidate in candidates:
                if test_chain(candidate[-1], n):
                    buf.append(candidate+[n])
        candidates = buf
    for candidate in candidates:
        if test_chain(candidate[-1], candidate[0]):
            return (candidate, sum(candidate))
    return None

if __name__ == "__main__":
    limit = 200 

    nss = []
    nss.append(filter(lambda x: len(str(x)) == 4, [n*(n+1)/2 for n in xrange(1, limit)]))
    nss.append(filter(lambda x: len(str(x)) == 4, [n*n for n in xrange(1, limit)]))
    nss.append(filter(lambda x: len(str(x)) == 4, [n*(3*n -1)/2 for n in xrange(1, limit)]))
    nss.append(filter(lambda x: len(str(x)) == 4, [n*(2*n -1) for n in xrange(1, limit)]))
    nss.append(filter(lambda x: len(str(x)) == 4, [n*(5*n -3)/2 for n in xrange(1, limit)]))
    nss.append(filter(lambda x: len(str(x)) == 4, [n*(3*n -2) for n in xrange(1, limit)]))

    gen = permutations(range(6))
    try:
        while 1:
            order = gen.next()
            buf = [nss[pos] for pos in order]
            t = test_nss(buf)
            if t:
                print order, t
    except StopIteration:
        pass



