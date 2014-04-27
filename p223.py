#!/usr/bin/python3.2

from math import sqrt
from utils import memoize

@memoize
def intsqrt(n2):
    n = sqrt(n2)
    if n == int(n):
        return int(n)
    else:
        return None

def triangles(P):
    perimeter = 0
    while perimeter <= P:
        for a in range(1,P):
            a2 = a*a
            for b in range(a,P-a):
                b2 = b*b
                c2 = a2 + b2
                c = intsqrt(c2)
                if c and c >= b:
                    yield(a, b, c)

def main():
    gen = triangles(1000)
    for t in gen:
        print(t)

if __name__ == "__main__":
    main()
