#!/usr/bin/python

with open('names.txt') as fp:
    names = fp.read().split(',')
    names = map(lambda x: x[1:-1], names)
    names.sort()

def value(name):
    return sum(map(lambda x: (ord(x) - ord('A')) + 1, name))

if __name__ == "__main__":
    scores = []
    for pos in range(len(names)):
        scores.append((pos+1) * value(names[pos]))
    print len(scores), sum(scores)

