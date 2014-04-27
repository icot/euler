#!/usr/bin/env python

from utils import gcd

def Z(N):
    """ Returns Z_N Cyclic group """ 
    return [n for n in range(0, N)]

def Zps(N):
    """ Returns Z_p^* """
    return [n for n in range(0, N) if gcd(n, N) == 1]

def main():
    z = Z(23)
    res = {a:(a*a) % 23 for a in z}
    for k,v in res.items():
        print k,v

if __name__ == "__main__":
    main()

