#!/usr/bin/python

from utils import ndivisors, trial_division, FastPrimeSieve
from math import sqrt
import cPickle, multiprocessing
import gzip

from pymongo import Connection

global progress
progress = 0

def worker_load(data):
    con = Connection('localhost')
    db = con['integers']
    col = db['misc']
    col.insert(data)
    con.disconnect()


def cb(result):
    global progress
    progress += result
    if progress % int(1e5) == 0:
        print "Progress: %f" % ((float(progress) / 1e9)*100)

def worker_file(a,b, primes):
    with gzip.open('dump.bin', 'ab', compresslevel = 3) as fp:
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
        cPickle.dump(buf, fp, protocol = 2)
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
        pool.apply_async(worker_file, [a, b, primes], callback=cb)
        a = b  
        b = a + jobsize
    pool.close()
    pool.join()

if __name__ == "__main__":
    main(int(1e9), 5000)

