#!/usr/bin/python

fib = lambda xs: xs[-1] + xs[-2]

if __name__ == "__main__":
    total = 0
    ns = []
    ns.append(1)
    ns.append(1)
    value = fib(ns)
    while value < 4e6:
        ns.append(value)
        value = fib(ns)

    print ns
    nf = filter(lambda x: (x % 2) == 0, ns)
    print nf
    total = sum(nf)
    print total

