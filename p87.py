#!/usr/bin/python

import utils
import itertools
from math import pow

primes = utils.FastPrimeSieve(7100)

def p2num(l):
    s = 0
    for p in xrange(len(l)):
        s += pow(l[p], p +2)
    return s


if __name__ == "__main__":
    gen = itertools.product(primes, repeat=3)

    nums = {}
    try:
        while 1:
            l = gen.next()
            num = p2num(l)
            if num < 50000000:
                try:
                    nums[num] += 1
                except KeyError:
                    nums[num] = 1
    except StopIteration:
        print len(nums.keys()), max(nums.keys()), min(nums.keys())



