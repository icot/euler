#!/usr/bin/env python

from utils import fib

def test_pandigital(num):
    s = set(num)
    return ((len(s) == 9) and '0' not in s)

if __name__ == "__main__":
    gen = fib()
    num = gen.next()
    cond = True
    k = 1
    while cond:
        if num > 1e18:
            tail = num % 1000000000
            tt = test_pandigital(str(tail))
            if tt:
                head = str(num)[:9]
                th = test_pandigital(head)
                print k
                print "> ", head, tail, th, tt
                if th:
                    cond = False
        k += 1
        num = gen.next()


