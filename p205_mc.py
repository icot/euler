#!/usr/bin/python

from random import randint

if __name__ == "__main__":
    cont = 0
    prev = 10.0 
    total = 0
    while 1:
        total += 1
        t4 = sum([randint(1,4) for dice in xrange(9)])
        t6 = sum([randint(1,6) for dice in xrange(6)])
        if t4 > t6:
            cont += 1
        ratio = (cont * 1.0)/total
        diff = abs(ratio - prev)
        if total % 10000 == 0:
            print total, cont, ratio, diff
        if diff < 1e-7:
            break
        prev = ratio
    print cont, ratio 
    
