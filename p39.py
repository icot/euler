#!/usr/bin/python

from math import sqrt

def check_triangle(a,b,c):
    return ((a*a + b*b) == c*c)

def check_c(c, th = 1e-6):
    return (abs(c-int(c)) <= th)

if __name__ == "__main__":
    As = xrange(1,1000)
    Bs = xrange(1,1000)
    candidates = []
    for a in As:
        for b in Bs:
            c = sqrt(a*a +b*b)
            if check_c(c) and (a+b+c) <= 1000:
                candidates.append((a,b,c, a+b+c))
    print len(candidates)
    count = {}
    for item in candidates:
        try:
            count[item[3]] += 1
        except KeyError:
            count[item[3]] = 1
    for k,v in count.items():
        print k,v





