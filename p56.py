#!/usr/bin/python

def sumdigs(num):
    return sum(map(lambda x: int(x), str(num)))

if __name__ == "__main__":
    m = 0
    for a in xrange(1,100):
        for b in xrange(1,100):
            num = pow(a,b)
            s = sumdigs(num)
            if s > m:
                print a,b,s
                m = s


