#/usr/bin/python2.7

import sys
from math import sqrt
from itertools import chain, izip
from multiprocessing import Pool

TH = 1e-9

def flatten(listOflists):
    items = chain.from_iterable(listOflists)
    fl = []
    try:
        while 1:
            fl.append(items.next())
    except StopIteration:
        return fl
    except TypeError:
        return fl

def compress(data, selectors):
    return (d for d, s in izip(data, selectors) if s)

def test(num):
    return abs(num - round(num)) < TH

def test2(num):
    return (apply_mask(num) == 1234567890)

def genNum(c1, buf):
    num = zip(c1, buf)
    num = map(str, flatten(num))+['0']
    return int(''.join(num))

c1 = range(1, 10)

minn = genNum(c1, [0,0,0,0,0,0,0,0,0])
maxn = genNum(c1, [9,9,9,9,9,9,9,9,0])

MASK = [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1]

def apply_mask(num, mask = MASK):
    items = compress(str(num), mask)
    cifs = []
    try:
        while 1:
            cifs.append(items.next())
    except StopIteration:
        return int(''.join(cifs))

if __name__ == "__main__":
    nprocs = int(sys.argv[1])
    packetsize = int(sys.argv[2])
    stop = int(round(sqrt(maxn)))
    start = int(round(sqrt(minn)))
    print start
    print stop
    tot = stop - start
    print "Testing %d - %d, %d items " % (start, stop, tot)
    cont = 0
    pool = Pool(processes = nprocs)
    for n in xrange(start, stop + 1, packetsize):
        ns = [k for k in xrange(n, n + packetsize)]
        res = pool.map(test2, ns)
        if any(res):
            for i in ns:
                if test2(i):
                    print "Number: ", i
            break
        if cont % 10000 == 0:
            print "Progress: %.3f %%" % (100.0*cont/tot)
        cont += len(res) 
