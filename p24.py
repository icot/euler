#!/usr/bin/python

from itertools import permutations

def next_perm(seq):
    k = None 
    l = None
    for i in xrange(len(seq) -1):
        if seq[i] < seq[i+1]:
            k = i
    if k:
        l = k + 1
        for i in xrange(k+1, len(seq) -1):
            if seq[k] < seq[i]:
                l = i
        buf = seq[k]
        seq[k] = seq[l]
        seq[l] = buf
        bufs = seq[k+1:]
        bufs.reverse()
        #print k, l, seq, bufs, seq[:k+1] + bufs
        return seq[:k+1] + bufs
    else:
        return seq
            

if __name__ == "__main__":
    perm = permutations(range(10))
    limit = 1e6
    cont = 1
    try:
        while 1:
            buf = perm.next()
            if cont == limit:
                print ''.join(map(str, buf))
            cont += 1
    except StopIteration:
        print cont
