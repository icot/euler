#!/usr/bin/python

import utils
from math import sqrt

def test_pent(num, th = 1e-6):
    r = sqrt(1 + 24 * num)
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
    r = sqrt(1 + 8 * num)
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

if __name__ == "__main__":
    tg = utils.triangle_gen()
    cont = 0
    while cont < 3:
        n = tg.next()
        if test_pent(n):
            if test_hex(n):
                print n
                cont = cont +1




