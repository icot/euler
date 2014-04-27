#!/usr/bin/env python

def r(a, n):
    return (pow(a-1, n) + pow(a+1, n)) % pow(a, 2)

if __name__ == "__main__":
    tot = 0
    for a in xrange(3,101):
        maxr = 0
        maxn = 0
        for n in xrange(1,1001):
            bufr = r(a, n)
            if bufr > maxr:
                maxr = bufr
                maxn = n
        if a % 4 == 3:
            print a, a % 4, maxn, maxr
        tot += maxr
    print tot
