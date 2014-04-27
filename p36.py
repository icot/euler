#!/usr/bin/python

import utils

if __name__ == "__main__":
    n = range(1,1000000)
    p1 = filter(lambda x: utils.palindrome(str(x)), n)
    nb = map(lambda x: bin(x)[2:], n)
    p2 = filter(utils.palindrome, nb)
    p2f = map(lambda x: int(x, 2), p2)
    nums = set(p1).intersection(set(p2f))
    print len(nums)
    print nums
    print sum(list(nums))
