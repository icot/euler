#!/usr/bin/python

from utils import ndivisors, trial_division, FastPrimeSieve
from math import sqrt
import multiprocessing
from pymongo import Connection


global progress
progress = 0

def cb(result):
    global progress
    progress += result
    if progress % int(1e5) == 0:
        print "Progress: %f" % ((float(progress) / 1e7)*100)

def worker_db(a,b, primes):
    with Connection('localhost') as con:
        db = con['integers']
        col = db['misc']
        buf = []
        for n in xrange(a, b):
            prime_factors = trial_division(n, primes)
            num_factors = len(prime_factors)
            data = {'n' : n, 
                    'factors' : prime_factors,
                    'ndivisors' : ndivisors(n, prime_factors),
                    'nfactors' : num_factors,
                    'max_factor': max(prime_factors),
                    'primality' : num_factors == 1}
            buf.append(data)
        col.insert(buf)
        con.disconnect()
    return (b-a)

def main(N, jobsize):

    global progress 
    print "Generating primes"
    maxp = int(sqrt(N)) + 1
    primes = FastPrimeSieve(maxp)
    print "Computing factors"

    pool = multiprocessing.Pool()
    
    buf = []
    a = 2
    b = a + jobsize
    while a <= N:
        pool.apply_async(worker_db, [a, b, primes], callback=cb)
        a = b  
        b = a + jobsize
    pool.close()
    pool.join()

def main2(N):
    print "Generating primes"
    maxp = int(sqrt(N)) + 1
    primes = FastPrimeSieve(maxp)
    print "Computing factors"
    prev = 0
    total = 0
    for n in xrange(2,int(1e7) +1):
        prime_factors = trial_division(n, primes)
        ndivs = ndivisors(n, prime_factors)
        if ndivs == prev:
            total += 1
        prev = ndivs
        if n % 100000 == 0:
            print n
    print total


if __name__ == "__main__":
    main2(int(1e7))
