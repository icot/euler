#!/usr/bin/python

import math
from utils import palindrome
from itertools import count
import timeit

def ssum(m):
    return m*(m+1)*(2*m+1)/6

def test_sum(num):
    limit = int(round(math.sqrt(num))) + 1
    for n1 in xrange(1,limit):
        for n2 in xrange(n1+1, limit):
            s1 = ssum(n2)
            s2 = ssum(n1-1)
            buf = s1 - s2
            if buf == num:
                return True
            if buf > num:
                break
    return False

def main1():
    #fp = open('palindromes.txt','w')
    cont = 0
    ns = count(2)
    n = ns.next()
    tot = 0
    while n <= 1000:
        if palindrome(n):
            cont+=1
            #fp.write("%d\n" % (n))
            if test_sum(n):
                print ">", n
                tot += n
        n = ns.next()
    print "total", tot
    #fp.close()

def main2():
    with open('palindromes.txt') as fp:
       lines = fp.readlines()
       ns = map(int, lines)
    tot = 0
    l = len(ns)
    for pos in xrange(l-1,-1,-1):
        n = ns[pos]
        if test_sum(n):
            tot += n
        print "N: %d, Status: %f comlete" % (n, 100*float(pos)/l)
    print "Total: ", tot


def main3():
    with open('palindromes.txt') as fp:
       lines = fp.readlines()
       ns = map(int, lines)
    t = timeit.Timer('test_sum(99999999)', "gc.enable()\nfrom __main__ import test_sum")
    print t.repeat(3,10)

if __name__ == "__main__":
    main2()
