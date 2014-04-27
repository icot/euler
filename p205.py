#!/usr/bin/python

from itertools import product

def f(nf, nd):
    res = {}
    gen = product(range(1,nf+1), repeat = nd)
    cont = 0 
    while 1:
        try:
            cont += 1 
            roll = gen.next()
            tot = sum(roll)
            try:
                res[tot] += 1
            except KeyError:
                res[tot] = 1
        except StopIteration:
            break
    for k,v in res.items():
        res[k] = float(v)/cont
    return res

def P(fd, n):
    start = min(fd.keys())
    return sum([fd.get(n, 0) for n in xrange(0, n+1)])


if __name__ == "__main__":
    fp = f(4, 9)
    fc = f(6, 6)
    Pp = {}
    Pc = {}
    Ppc = {}
    for n in xrange(0, 38):
        Pp[n] = P(fp, n)
        Pc[n] = P(fc, n)
        print "%d %.7f, %.7f" % (n, Pc[n], Pp[n])
    for p in xrange(0,37):
        for c in xrange(0, 37):
            print Pp.get(p,0), Pc.get(c, 0)
            Ppc[(p,c)] = Pp.get(p,0) * Pc.get(c, 0)
    for x in xrange(0,37):
            print x,Ppc[(x,10)], Pp[x], Pc[x]

