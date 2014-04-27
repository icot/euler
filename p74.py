#!/usr/bin/env python

import utils

cv = map(utils.factorial, range(10))

def cifras(num):
    return map(int, str(num))

def fvalue(num):
    return sum([cv[i] for i in cifras(num)])

def serie(start):
    buf = fvalue(start)
    s = [start]
    while buf not in s:
        s.append(buf)
        buf = fvalue(buf)
    return len(s)
    
if __name__ == "__main__":
    series = {}
    for n in xrange(1, 1000000):
        s = serie(n)
        try:
            series[s] += 1
        except KeyError:
            series[s] = 1
    print series
