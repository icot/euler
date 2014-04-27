#!/usr/bin/env python

from numpy import polyval, polyfit

# un = 1 - n + n2 - n3 + n4 - n5 + n6 - n7 + n8 -  n9 + n10

gen = [1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1]
series = [polyval(gen, x) for x in range(11)]
test = [1,8,27,64,125,216]
test = series
bops = []
for k in range(1, len(test)):
    # fit
    x = range(1, k+1)
    y = test[:k]
    print "fiting to n^%d" % (k-1)
    pol = polyfit(x, y, k-1)
    print ">> ", pol
    pol = [int(coef) for coef in pol]
    print ">> ", pol
    # find bop's
    yts = [int(polyval(pol, x)) for x in range(1, len(test)+1)]
    print k, yts
    fits = False
    for pos, yt in enumerate(yts):
        if test[pos] != yt:
            bops.append(yt)
            fits = True
            break
    if not fits:
        break

print bops
print sum(bops)
