#!/usr/bin/python2.7

import itertools

def sumdigits(xs):
    return sum(map(len, map(str, xs)))

def test(nums):
    x1, x2, x3, x4, x5, x6, x7, x8, x9, x10 = nums
    l1 = x1 + x7 + x8
    l2 = x2 + x8 + x9
    l3 = x3 + x9 + x10
    l4 = x4 + x10 + x6
    l5 = x5 + x6 + x7
    return l1 == l2 == l3 == l4 == l5

def cad(xs):
    x1, x2, x3, x4, x5, x6, x7, x8, x9, x10 = nums
    l1 = [x1, x7, x8]
    l2 = [x2, x8, x9]
    l3 = [x3, x9, x10]
    l4 = [x4, x10, x6]
    l5 = [x5, x6, x7]
    cad = ''.join(map(str, l1 + l2 + l3 + l4 + l5))
    return len(cad)

def cads(xs):
    x1, x2, x3, x4, x5, x6, x7, x8, x9, x10 = nums
    l1 = [x1, x7, x8]
    l2 = [x2, x8, x9]
    l3 = [x3, x9, x10]
    l4 = [x4, x10, x6]
    l5 = [x5, x6, x7]
    cad = ''.join(map(str, l1 + l2 + l3 + l4 + l5))
    print cad, len(cad)
    cad =  ''.join(map(str, l2 + l3 + l4 + l5 + l1))
    print cad, len(cad)
    cad =  ''.join(map(str, l3 + l4 + l5 + l1 + l2))
    print cad, len(cad)
    cad = ''.join(map(str, l4 + l5 + l1 + l2 + l3))
    print cad, len(cad)
    cad =  ''.join(map(str, l5 + l1 + l2 + l3 + l4))
    print cad, len(cad)

if __name__ == "__main__":
    cifs = range(1,11)
    gen = itertools.combinations_with_replacement(cifs, 10)
    c = 0
    try:
        while 1:
            nums =  gen.next()
            perms = itertools.permutations(nums)
            p = 0
            used = {}
            try:
                while 1:
                    perm = perms.next()
                    buf = cad(perm)
                    if buf == 16:
                        h = ''.join(map(str,perm))
                        try:
                            used[h]
                        except KeyError:
                            if test(perm):
                                print perm, "\n"
                                cads(perm)
                            used[h] = 1
                    p += 1
            except StopIteration:
                print c
                c += 1
    except StopIteration:
        print "Total iterations: ", c

