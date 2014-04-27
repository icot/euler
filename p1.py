#!/usr/bin/python

if __name__ == "__main__":
    n = range(1000)
    x3 = filter(lambda x: (x % 3) == 0, n)  
    x5 = filter(lambda x: (x % 5) == 0, n)
    x = x3
    x.extend(x5)
    xf = list(set(x))
    print len(x), len(xf), sum(xf)
