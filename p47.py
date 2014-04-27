#!/usr/bin/python

from utils import factors, FastPrimeSieve

if __name__ == "__main__":
    print "Generating primes"
    primes = FastPrimeSieve(1000000)
    print "Computing"
    n = 1 
    s = 1 
    while s <= 3:
        if n not in primes:
            f = set(factors(n))
            l = len(f)
            if l >= 4 :
                s = s+1
                f1 = set(factors(n-1))
                l1 = len(f1)
                if l1 >= 4 :
                    s = s+1
                    print n-1, f1, n, f, s
                else:
                    s = 1
            else:
                s = 1
        n = n + 2 
    print n-3
        
        


