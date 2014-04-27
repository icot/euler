#!/usr/bin/python

if __name__ == "__main__":
    order = 1001
    #n = xrange(1, pow(order, 2) +1, 2)
    total = 1   
    cont = 1
    for r in xrange(1, order+1, 2):
        #buf = filter(lambda x: x>=pow(r,2) and x<=pow(r+2,2), n)
        buf = range(pow(r,2), pow(r+2,2)+1, 2)
        pos = range(cont, len(buf), cont) 
        #print buf, buf2, pos
        cont = cont + 1
        total = total + sum([buf[p] for p in pos])
    print total 

