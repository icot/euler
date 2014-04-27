#!/usr/bin/python

def d(i):
    n = [str(item) for item in xrange(1, i+1)]
    cad = ''.join(n)
    return int(cad[i-1])

if __name__ == "__main__":
    indices = map(lambda x: pow(10,x), range(1,7))
    cifs = []
    for i in indices:
        cifs.append(d(i))
    print cifs
    print reduce(lambda x,y: x*y, cifs)


