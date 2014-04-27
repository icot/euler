#!/usr/bin/python

from math import sqrt

if __name__ == "__main__":
    b = 85 
    n = 120
    while n < int(1e12): 
        b1 = 3*b + 2*n -2
        n1 = 4*b + 3*n -3
        b = b1
        n = n1
        print b,n
