#!/usr/bin/python

def valid_permutations(l):
    buf = map(str, l)
    valid = True
    for pos in range(len(buf)-1):
        x=buf[pos]
        y=buf[pos+1]
        for pc in range(len(x)):
            if x.count(x[pc]) != y.count(x[pc]):
                valid = False
                break
    return valid


if __name__ == "__main__":
    limit = 1e6
    cubes = [ pow(n, 3) for n in xrange(1, limit) ]
    rel = {}
    maxl = 0
    maxk = None
    for cube in cubes:
        cifs = str(cube)
        key = list(cifs)
        key.sort()
        key = (''.join(key) , len(cifs))
        try:
            rel[key].append(cube)
            l = len(rel[key])
        except KeyError:
            rel[key] = [cube]
            l = 1

    candidates = []
    for k, v in rel.items():
        if len(v) == 5 and valid_permutations(v):
            print len(v), min(v), k, v
            candidates.extend(v)
    print min(candidates)
    




