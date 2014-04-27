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

def main2():
    result = 0
    x, y = 2, 1
    while 1:
        # b = a + 1 
        a3 = 2 * x-1
        area3 = y * (x-2)
        if a3 > 1e9:
            break
        if a3 > 0 and area3 > 0 and a3 % 3== 0 and area3 % 3 == 0:
            a = a3/3
            print a, 3*a+1
            result += 3*a+1
        # b = a - 1
        a3 = 2 * x + 1
        area3 = y * (x+2)
        if a3 > 0 and area3 > 0 and a3 % 3== 0 and area3 % 3 == 0:
            a = a3/3
            print a, 3*a-1
            result += 3*a-1
        xn = 2*x + y *3
        yn = 2*y + x
        x = xn
        y = yn
    print result


if __name__ == "__main__":
    main2()

