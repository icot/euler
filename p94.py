#!/usr/bin/python

def generator(x0, y0, PQK, RSL):
    P, Q, K, = PQK 
    R, S, L = RSL
    xn, yn = x0, y0
    while 1:
        xn1 = P*xn + Q*yn + K
        yn1 = R*xn + S*yn + L
        yield (xn1, yn1)
        xn, yn = xn1, yn1

def test_triangle(h, a):
    return (h*h + a*a) == ((2*a+1)*(2*a+1))

def test_triangle2(h, a):
    return (h*h + a*a) == ((2*a-1)*(2*a-1))

def main():
    perimeters = []
    a = 1
    gen = generator(0,1, (-2,-1,-2), (-3,-2,-2))
    while 6*abs(a)+2 <= int(1e9):
        a, h = gen.next()
        if test_triangle(h,a) and a>0 and h:
            print a, h, 2*a, 2*a+1
            perimeters.append(6*a + 2)
    a = 1
    gen = generator(0,1, (-2,-1,2), (-3,-2,2))
    while 6*abs(a)-2 <= int(1e9):
        a, h = gen.next()
        if test_triangle2(h,a) and a>0 and h:
            print a, h , 2*a, 2*a-1
            perimeters.append(6*a - 2)

    perimeters = list(set(perimeters))
    perimeters.sort()
    for p in perimeters:
        print p
    print sum(perimeters)

if __name__ == "__main__":
    main()

