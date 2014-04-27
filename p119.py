#!/usr/bin/env python

def cifras(num):
    return map(int, str(num))

def test(num):
    base = sum(cifras(num))
    if base > 1:
        buf = base
        exp = 1
        while buf <= num:
            buf *= base
            exp += 1
            #print buf, exp
            if buf == num:
                return (base, exp)
    return None

candidates = [(base, exp) for base in xrange(2, 100) for exp in xrange(1,10)]

if __name__ == "__main__":
    print len(candidates)
    nums = []
    for candidate in candidates:
        base, exp = candidate
        num = pow(base, exp)
        if sum(cifras(num)) == base and num > 10:
            nums.append(num)
    nums.sort()
    for p in xrange(len(nums)):
        print p, nums[p]


