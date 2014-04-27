#!/usr/bin/python

import utils

if __name__ == "__main__":
    n = 1
    fib = utils.fib()
    num = fib.next()
    l = len(str(num))
    while l < 1000:
        n = n + 1
        num = fib.next()
        l = len(str(num))
    print n
        
