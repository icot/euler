#!/usr/bin/python

def func(num):
    buf = num
    while buf != 1 and buf != 89:
        buf = sum(map(lambda x: pow(x,2), map(int, str(buf))))
    return buf


if __name__ == "__main__":
    tot = 0
    for n in xrange(1, 1e6):
        print n
        if func(n) == 89:
            tot += 1
    print tot
