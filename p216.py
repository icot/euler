#!/usr/bin/python 

from utils import isprime, ndivisors

if __name__ == "__main__":
    limit = int(10e7)
    cont = 0
    nd1 = 0
    for n in xrange(2, limit):
        nd2 = ndivisors(n)
        if nd2 == nd1:
            cont += 1
        nd1 = nd2
        if n % 10000 == 0:
            print n, cont
    print cont

