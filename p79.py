#!/usr/bin/python

with open('keylog.txt') as fp:
    lines = fp.readlines()

lines = [int(line[:-1]) for line in lines]
keylogs = [map(int, str(line)) for line in lines]

if __name__ == "__main__":
    firsts = []
    lasts = []
    for keylog in keylogs:
        print keylog
        firsts.append(keylog[0])
        lasts.append(keylog[-1])
    print set(firsts), set(lasts)
