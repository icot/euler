#!/usr/bin/env python

import itertools

def gen_triplets(P):
    for a in xrange(3, P+1):
        for b in xrange(a+1, P-a):
            c = P - a - b
            if (a+b > c) and (a+c>b) and (b+c)>a:
                yield (a,b,c)
            else:
                continue

if __name__ == "__main__":
    
    cont = 0
    for P in xrange(12, 1000):
        tripgen = gen_triplets(P)
        pcont = 0
        try:
            while 1:
                triplet = tripgen.next()
                a,b,c = triplet
                if (c*c == (b*b + a*a)):
                    pcont += 1 
                    if pcont > 1:
                        raise StopIteration
        except StopIteration:
            if pcont == 1:
                print "> ", P
                cont +=1
    print cont
        
        

