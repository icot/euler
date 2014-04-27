#!/usr/bin/python

import utils

def test_lychrel(num):
    n = 1
    candidate = num
    while n <= 50:
        candidate += utils.reverse(candidate)
        if utils.palindrome(candidate):
            return False
        n += 1
    return True

if __name__ == "__main__":
    total = 0
    for n in xrange(1, 10001):
        if test_lychrel(n):
            total += 1
    print total


