#!/usr/bin/python2.7

from utils import factorial

def comb(n,k):
    return factorial(n)/(factorial(k)*factorial(n-k))

def cyphers(num):
    return map(int, str(num))

def isincreasing(num):
    c = cyphers(num)
    for p in xrange(len(c)-1):
        if c[p] < c[p+1]:
            return False
    return True

def isdecreasing(num):
    c = cyphers(num)
    for p in xrange(len(c)-1):
        if c[p] > c[p+1]:
            return False
    return True

def isbouncy(num):
    return not isincreasing(num) and not isdecreasing(num)

if __name__ == "__main__":
    nums = range(1,1001)
    k = 0
    ratio = 0
    n = 1
    inc = 0
    dec = 0
    for n in nums:
        if isincreasing(n):
            inc += 1
        if isdecreasing(n):
            dec += 1
        if isbouncy(n):
            k += 1
    print n, inc, dec, k
    print comb(10,2), comb(10,3)
        
