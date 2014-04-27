#!/usr/bin/python


from math import log

with open('base_exp.txt') as fp:
    lines = fp.readlines()
    lines = map(lambda x: tuple(map(int, x.split(','))), map(lambda x: x[:-2], lines))

def test(a,b):
    return a[1]*log(a[0]) > b[1]* log(b[0])


if __name__ == "__main__":
    maxn = (1.0, 0.0)
    for item in lines:
        if test(item, maxn):
            maxn = item
    print maxn
