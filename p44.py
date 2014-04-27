#!/usr/bin/python

from utils import test_pent as test

if __name__ == "__main__":
    limit = 10000
    print "Generating pentagonal numbers"
    a = [ x*(3*x -1)/2 for x in xrange(1,limit) ]
    b = [ x*(3*x -1)/2 for x in xrange(1,limit) ]
    print "Generating pairs"
v v v v v v v
    pairs = [(a[i],b[j], abs(a[i]-b[j])) for i in xrange(1,len(a)) for j in xrange(1,len(b)) if test(abs(a[i]-b[j])) and test(a[i]+b[j])]
    for pair in pairs:
        print pair
*************
    pairs = []
    minr = 1e6
    for i in xrange(1, limit):
        p1 = i*(3*i -1)/2
        for k in xrange(i+1, limit):
            p2 = k*(3*k -1)/2  
            sik = (p1+p2)
            rik = abs(p1 -p2)
            if rik < minr:
                if rik in p and sik in p:
                    pairs.append((p1, p2, rik))
                    minr = rik
            print i, k, p1, p2, sik, rik, minr
    print pairs

^ ^ ^ ^ ^ ^ ^




