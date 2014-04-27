#!/usr/bin/python

import itertools

with open('cipher1.txt') as fp:
    line = map(lambda x:x[:-1], fp.readlines())
    code = line[0].split(',')
    code = map(lambda x: int(x), code)

def combinations_with_replacement(iterable, r):
    # combinations_with_replacement('ABC', 2) --> AA AB AC BB BC CC
    pool = tuple(iterable)
    n = len(pool)
    if not n and r:
        return
    indices = [0] * r
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != n - 1:
                break
        else:
            return
        indices[i:] = [indices[i] + 1] * (r - i)
        yield tuple(pool[i] for i in indices)

def encrypt(data, key):
    print len(key), key
    keygen = itertools.cycle(key)
    return [ byte^keygen.next() for byte in data ]

if __name__ == "__main__":
    alphabet = range(ord('a'), ord('z') +1)
    keys = [ (i,j,k) for i in alphabet for j in alphabet for k in alphabet]
    valid = [32] + range(ord('a'), ord('z') +1) + range(ord('A'), ord('Z') + 1)
    valid.extend(range(48,58))
    valid.append(ord("'"))
    valid = set(valid)
    cont = 0
    print " # of bytes: ", len(code)
    print " # of valid values: ", len(valid)
    ma1 = 255
    ma2 = 1
    for key in [(103, 111, 100)]: 
        res = encrypt(code, key) 
        used_values = set(res)
        if True:
            print "\nAttempting key: ", ''.join(map(lambda x: chr(x), key))
            print " Max: %d, Min: %d" % (max(res), min(res))
            print " # of used values: ", len(used_values) 
            print " Total value: ", sum(res)
            print " Result: ", ''.join(map(chr, res))
        if max(res) > ma2:
            ma2 = max(res)
        if min(res) < ma1:
            ma1 = min(res)
        cont += 1




