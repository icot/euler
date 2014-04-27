#!/usr/bin/python


if __name__ == "__main__":
    cont = 0
    for n in xrange(1,10):
        for exp in xrange(1, 1000):
            num = pow(n, exp)
            if len(str(num)) == exp:
                print n, exp, num, len(str(num))
                cont += 1
    print cont


