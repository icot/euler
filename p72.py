#!/usr/bin/env python2.7

limit = 1000001 

with open('phi.txt') as fp:
    lines = [fp.readline()[:-1] for i in xrange(1, limit)]

if __name__ == "__main__":
    rpfs = 0
    print "Computing"
    for line in lines[1:]:
        n, phi = map(int, line.split(' '))
        rpfs += phi
    print n, rpfs


