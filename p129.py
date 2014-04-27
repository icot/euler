#!/usr/bin/python


def load_list():
    with open("Repunit60.txt") as fp:
        l = {}
        lines = fp.readlines()
        ind = 0
        lnumber = ''
        for line in lines[2:]:
            buf = line.split()
            lastn = 0
            if len(buf) > 1:
                try:
                    last = buf[-1]
                    if last == 'M':
                        factors = [eval(item) for item in buf[1:-2]]
                    elif last == '$':
                        lnumber += buf[0]
                    else:
                        factors = [eval(item) for item in buf[1:]]
                    if last != '$':
                        n = int(buf[0])
                        lnumber = ''
                    ind = n
                except ValueError:
                    # M, L
                    nums = map(eval, buf[1:])
                    for item in nums:
                        factors.append(item)
            else:
                if len(lnumber) :
                    lnumber += buf[0]
                    factors.append(eval(lnumber))
                else:
                    factors.append(eval(buf[0]))
            l[ind] = factors
        return l

def R(k):
    return (pow(10, k) -1)/9

if __name__ == "__main__":
    for a in range(1, 10):
        print(a, R(a))

