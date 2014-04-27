#!/usr/bin/pypy

from math import sqrt, floor

def ntiles(n):
    return (4*n -4)

def main(limit):
    N = int((limit + 4) / 4.0)
    outer = {}
    for n in xrange(3, N+1):
        outer[n] = 4*n -4 # ntiles
    cont = 0
    vals = outer.values()
    fvals1 = [vals[i] for i in xrange(0,len(vals),2)]
    fvals2 = [vals[i] for i in xrange(1,len(vals),2)]
    for n in range(3,5):
        if n % 2 == 1:
            fvals = fvals1
        else:
            fvals = fvals2
        for pos1 in xrange(len(fvals)+1):
            for pos2 in xrange(pos1, len(fvals)+1):
                buf = [fvals[i] for i in xrange(pos1, pos2)]
                s = sum(fvals[pos1:pos2])
                print n, pos1, pos2, buf
                if s and s <= limit:
                    cont +=1
    print cont

def main2(limit):
    N = int((limit + 4) / 4.0)
    outer = {}
    for n in xrange(3, N+1):
        outer[n] = 4*n -4 # ntiles
    cont = 0
    vals = outer.values()
    fvals1 = [vals[i] for i in xrange(0,len(vals),2)]
    fvals2 = [vals[i] for i in xrange(1,len(vals),2)]
    for n in range(3,5):
        if n % 2 == 1:
            fvals = fvals1
        else:
            fvals = fvals2
        for pos1 in xrange(len(fvals)+1):
            for pos2 in xrange(pos1, len(fvals)+1):
                buf = [fvals[i] for i in xrange(pos1, pos2)]
                s = sum(fvals[pos1:pos2])
                #print n, pos1, pos2, buf, s > limit
                if s and s <= limit:
                    cont +=1
                else:
                    if s > limit:
                        break
    print cont
        
if __name__ == "__main__":
    main2(1000000)
