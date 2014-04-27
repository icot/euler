#!/usr/bin/python2.7

from utils import isprime

def p(n, c):
    return n*n + c

if __name__ == "__main__":
    limit = 1000000
    cs = (3, 7, 9, 13, 27)
    print "Generating groups"
    groups = [[n, p(n, 1)] for n in xrange(limit) if isprime(p(n,1))]
    for c in cs:
        groups = [item + [p(item[0], c)] for item in groups]
        groups = filter(lambda x: isprime(x[-1]), groups)
        print "Filter: ", len(groups)
    print "Suma: ", sum(cs)

