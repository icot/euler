#!/usr/bin/python

def collatz(start):
    buf = start
    l = 1
    while buf != 1:
        if (buf % 2) == 0:
            buf /= 2
        else:
            buf = buf * 3 +1
        l = l +1
    return l

if __name__ == "__main__":
    M = 0
    n = range(1,1000000)
    for item in n:
        L = collatz(item)
        if L > M:
            M = L
            print item, M


