#!/usr/bin/python

if __name__ == "__main__":
    n = 1
    p2 = range(2,7)
    while 1:
        cifs = set(str(n))
        prods = map(lambda x: set(str(n*x)), p2)
        p = filter(lambda x: x == cifs, prods)
        if len(p) == 5:
            print n
            break
        n = n + 1


    
