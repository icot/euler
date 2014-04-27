#!/usr/bin/python

from utils import factorial

def comb(n,r):
    return factorial(n)/(factorial(n-r)*factorial(r))


if __name__ == "__main__":
    cont = 0
    for n in xrange(1,101):
        for r in xrange(1,n):
            if comb(n,r) > 1e6:
                cont = cont+1
    print cont


