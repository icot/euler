#!/usr/bin/env python

import itertools

sums = {}
sums[1] = 1 
sums[2] = 1

def flatten(listOfLists):
    return itertools.chain.from_iterable(listOfLists)

def combs(n):
    if n == 1:
        combs = [1]
    else: 
        if n == 2:
            combs = [1, 1]
        else:
            combs = [] 
            for k in xrange(1,int(round(n/2.0))): 
                combs.append([k, n-k])
    return combs

def Sums(n):
    c = combs(n)
    res = [item for item in flatten(c)]
    res = sum(map(lambda x: sums[x], res)) 
    return res

def bruteforce(n):
    gen = itertools.product(range(n), repeat=n)
    cont = 0
    while 1:
        try:
            if sum(gen.next()) == n:
                cont += 1
        except StopIteration:
            break
    return cont

if __name__ == "__main__":
    for a in range(3, 10):
        s = Sums(a)
        sums[a] = s
        print a, s 

