
def generator(x0, y0, PQK, RSL):
    P, Q, K, = PQK 
    R, S, L = RSL
    xn, yn = x0, y0
    while 1:
        xn1 = P*xn + Q*yn + K
        yn1 = R*xn + S*yn + L
        yield (xn1, yn1)
        xn, yn = xn1, yn1

def main():
    Ls = []
    a = 1
    gen1 = generator(0,-1, (-9,-8,-8), (-10,-9,-8))
    gen2 = generator(0,1, (-9,-8,8), (-10,-9,8))
    while len(Ls) < 12:
        b1, l1 = gen1.next()
        b2, l2 = gen2.next()
        if (abs(l1)) > 2:
            Ls.append(abs(l1))
            print l1,l2, l1+l2

    for pos, k in enumerate(Ls):
        print pos,k
    print sum(Ls)

if __name__ == "__main__":
    main()
