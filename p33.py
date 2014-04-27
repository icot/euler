#!/usr/bin/python

def test(a,b,th = 1e-6):
    return (abs(a-b)<th)

def simplify(num,den):
    n11 = num / 10
    n12 = num % 10
    d11 = den / 10
    d12 = den % 10
    if n12 and d12:
        if n11 == d11 and d12:
            return float(n12)/d12
        else:
            if n11 == d12 and d11:
                return float(n12)/d11
            else:
                if n12 == d11 and d12:
                    return float(n11)/d12
                else:
                    if n12 == d12 and d11:
                        return float(n11)/d11
                    else:
                        return 0
    else:
        return 0

if __name__ == "__main__":
    num = xrange(11,100)
    for n in num:
        den = xrange(n,100)
        for d in den:
            s = simplify(n,d)
            if test(float(n)/d, s) and (s < 1) and s:
                print "(#) %d/%d, %.6f, %.6f" % ( n, d, float(n)/d, s)
            
