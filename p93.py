#!/usr/bin/python2.7

import itertools

funcs = ['+', '-', '*', '/']

def myzip(comb):
    nums = map(str, map(float, comb[0]))
    funs = comb[1]
    LP = '('
    RP = ')'
    r = []
    r.append(nums[0] + funs[0] + nums[1] + funs[1] + nums[2] + funs[2] + nums[3])
    r.append(LP + nums[0] + funs[0] + nums[1] + RP + funs[1] + nums[2] + funs[2] + nums[3])
    r.append(LP + nums[0] + funs[0] + nums[1] + funs[1] + nums[2] + RP + funs[2] + nums[3])
    r.append(LP + LP + nums[0] + funs[0] + nums[1] + RP + funs[1] + nums[2] + RP + funs[2] + nums[3])
    r.append(LP + nums[0] + funs[0] + LP + nums[1] + funs[1] + nums[2] + RP + RP + funs[2] + nums[3])
    r.append(nums[0] + funs[0] + LP + nums[1] + funs[1] + nums[2] + funs[2] + nums[3] + RP)
    r.append(nums[0] + funs[0] + nums[1] + funs[1] + LP + nums[2] + funs[2] + nums[3] + RP)
    r.append(nums[0] + funs[0] + LP + LP + nums[1] + funs[1] + nums[2] + RP + funs[2] + nums[3] + RP)
    r.append(nums[0] + funs[0] + LP + nums[1] + funs[1] + LP + nums[2] + funs[2] + nums[3] + RP + RP)
    r.append(nums[0] + funs[0] + LP + nums[1] + funs[1] + nums[2] + RP + funs[2] + nums[3])
    r.append(LP + nums[0] + funs[0] + nums[1] + RP + funs[1] + LP + nums[2] + funs[2] + nums[3] + RP)
    return map(lambda x: ''.join(x), r)

if __name__ == "__main__":

    anums = [(a,b,c,d) for a in xrange(1,6+1) for b in xrange(a+1,7+1) for c in xrange(b+1,8+1) for d in xrange(c+1, 9+1)]

    stats = {}

    print "\n%d (a,b,c,d) tuples\n" % len(anums)
    
    for nums in anums:
        key = reduce(lambda x,y: x+y, map(str, nums))
        series = {}
        pnums = itertools.permutations(nums)
        pfuncs = itertools.product(funcs,funcs, repeat=2)
        combs = [comb for comb in itertools.product(pnums, pfuncs)]
        
        for comb in combs:
            ops = myzip(comb)
            for op in ops:
                try:
                    n = eval(op)
                    if n == int(n):
                        try:
                            series[n] += 1
                        except KeyError:
                            series[n] = 1
                except ZeroDivisionError:
                    pass

        ks = series.keys()
        ks.sort()
        ol = len(ks)
        ks = filter(lambda x: x > 0, ks)
        if ks[0] == 1 and len(ks) > 2:
            cont = 1
            for pos in xrange(1, len(ks)):
                if (ks[pos] - ks[pos-1]) == 1:
                    cont += 1
                else:
                    break
            stats[key] = cont
        else:
            stats[key] = 0
        print "  Tuple: %s, # of Values: %d, # of PValues: %d, # of CValues: %d Max: %d\n" % (key, ol, len(ks), cont, max(ks))
    maxl = 0
    maxnums = 0
    keys = stats.keys()
    keys.sort()
    for k in keys:
        v = stats[k]
        if v > maxl:
            maxl = v
            maxnums = k
    print "Max: ", maxnums, maxl



