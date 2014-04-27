#!/usr/bin/python

def pit(a,b,c):
    if ((a**2 + b**2) == c**2):
        return True
    else:
        return False

if __name__ == "__main__":
    maximum = 1001
    for posA in range(maximum):
        a = posA
        for posB in range(posA, maximum):
            b = posB
            for posC in range(posB, maximum):
                c = posC
                if pit(a,b,c):
                    if ((a+b+c)==1000):
                        print a,b,c, a*b*c
                        break

