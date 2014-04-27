#!/usr/bin/python

import utils

with open('13.txt') as fp:
    lines = fp.readlines()
    lines = map(lambda x: x[:-1], lines)


if __name__ == "__main__":
    num = 0
    for item in lines:
        num += int(item)
    print "Result: ", num 

