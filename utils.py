#!/usr/bin/python

import math
import functools
from sieve import eratosthenes as prime_sieve

def memoize(f):
    cache = {}
    
    @functools.wraps(f)
    def wrapper(*args):
        try:
            return cache[args[0]]
        except KeyError:
            cache[args[0]] = f(*args)
            return cache[args[0]]
    return wrapper

def isprime(num):
    for div in xrange(2, int(math.sqrt(num)) + 1):
        if (num % div)==0:
            return False
    return True

def factors(num, primes = None):
    factors = []
    if num > 3:
        buf = num
        if primes:
            fcandidates = [prime for prime in primes if prime < (num/2) +1]
        else:
            fcandidates = prime_sieve((num/2)+1)
        for candidate in fcandidates:
            cond = True
            while cond:
                r = buf % candidate
                if r == 0:
                    factors.append(candidate)
                    buf /= candidate
                elif buf == 1:
                    break
                else:
                    cond = False
    return factors

@memoize
def phi(n, primes = None):
    f = list(set(factors(n, primes)))
    if f:
        return int(n * reduce(lambda x,y: x*y, map(lambda x: 1.0 - (1.0/x), f)))
    else:
        if n > 1:
            return (n-1)
        else:
            return 1

def gcd(a, b):
      while b: 
         a, b = b, a % b 
      return a 

def phi2(n):
    phi = [gcd(n, k) for k in xrange(1, n)]
    return sum(filter(lambda x: x== 1, phi))

def sum_digits(num):
    return reduce(lambda x,y: x+y, map(lambda x: int(x), str(num)))

def fib():
    a, b = 0, 1
    while 1:
        yield b
        a, b = b, a+b

def triangle_gen():
    x = 1
    n = 1
    while 1:
        yield x
        n = n + 1
        x = x + n

def rotate(num, shift = 1):
    N = str(num)
    if len(N) == 1:
        return num
    else:
        if len(N) == 2:
            return int(N[1] + N[0])
        else:
            return int(N[shift:] + N[0:shift])

def rotations(num):
    rots = []
    for s in xrange(1, len(str(num))):
        rot = rotate(num, s)
        rots.append(rot)
    return rots

def truncate_left(num):
    if num > 10:
        exp = int(math.log10(num))
        return num % pow(10, exp)
    else:
        return num

def truncate_right(num):
    if num > 10:
        return num/10
    else:
        return num

def test_triang(num, th = 1e-6):
    r = math.sqrt(1 + 8 * num)
    s1 = (-1+r)/2
    s2 = (-1-r)/2
    if abs(s1) > 0:
        if abs(s1 - int(s1)) < th:
            return True
        else:
            return False
    else:
        if abs(s2 - int(s2)) < th:
            return True
        else:
            return False

def test_pent(num, th = 1e-6):
    r = math.sqrt(1 + 24 * num)
    s1 = (1+r)/6
    s2 = (1-r)/6
    if abs(s1) > 0:
        if abs(s1 - int(s1)) < th:
            return True
        else:
            return False
    else:
        if abs(s2 - int(s2)) < th:
            return True
        else:
            return False
         
def test_hex(num, th = 1e-6):
    r = math.sqrt(1 + 8 * num)
    s1 = (1+r)/4
    s2 = (1-r)/4
    if abs(s1) > 0:
        if abs(s1 - int(s1)) < th:
            return True
        else:
            return False
    else:
        if abs(s2 - int(s1)) < th:
            return True
        else:
            return False

def ndivisors(num, primes = None):
    f = factors(num, primes)
    if f:
        exps = [f.count(item) for item in set(f)]
        return reduce(lambda x,y: x*y, map(lambda x: x+1, exps))
    else:
        return 2

def divisors(num):
    if num >3:
        divisors = [1]
        fcandidates = xrange(2, (num/2)+1)
        for candidate in fcandidates:
            if (num % candidate) == 0:
                divisors.append(candidate)
        if divisors:
            return divisors
        else:
            return [1, num]
    else:
        return [1, num]

def palindrome(num):
    b = map(lambda x: x, str(num))
    b.reverse()
    return (num == int(''.join(b)))

def reverse(num):
    b = map(lambda x: x, str(num))
    b.reverse()
    return int(''.join(b))

def catnums(num1, num2):
    s1 = str(num1)
    s2 = str(num2)
    return int(s1+s2)

def factorial(num):
    if num:
        r = xrange(1,num+1)
        return reduce(lambda x,y:x*y, r)
    else:
        return 1



