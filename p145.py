#!/usr/bin/python

def reverse(num):
    b = list(str(num))
    b.reverse()
    return int(''.join(b))

def reversible(n):
    r = reverse(n)
    if len(str(r)) == len(str(n)):
        if all(map( lambda x: (int(x) % 2 == 1) , str(n+r))):
            return True
        else:
            return False
    else:
        return False

if __name__ == "__main__":
    count = 0
    limit = 1e7
    for n in xrange(int(limit+1)):
        if reversible(n):
            count += 1
        if (n % 100000) == 0:
            print "Count: %d, Progress: %f %%" % (count, n*100.0/limit)


