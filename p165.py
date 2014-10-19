#!/usr/bin/python

from sympy.geometry import Point, Segment

NCOORDS = 20000 
NPOINTS = NCOORDS/2
NSEGMENTS = NPOINTS/2

def blumblumshub():
    s = 290797
    while 1:
        sn = (s * s) % 50515093
        tn = sn % 500
        s = sn
        yield tn

def brute_count(sx):
    ix = []
    for pos, s in enumerate(sx):
        print "Progress: %f" % ((pos*100.0)/NSEGMENTS)
        for t in sx[pos+1:]:
            i = s.intersection(t)
            if i:
                ix.extend(i)
    return ix

def main():
    gen = blumblumshub()
    cx = [ gen.next() for a in xrange(NCOORDS) ]
    px = [ Point(cx[i], cx[i+1]) for i in range(0, NCOORDS, 2) ]
    sx = [ Segment(px[i], px[i+1]) for i in range(0, NPOINTS, 2) ]
    sxfiltered = list(set(sx))
    print "Filtering segments for duplicates: %d -> %d " % (len(sx), len(sxfiltered))
    ix = brute_count(sx)
    ixf1 = list(set(ix))
    print "Filtering intersections for duplicates: %d -> %d " % (len(ix), len(ixf1))
    ixf2 = [i for i in ixf1 if i not in px]
    print "Filtering intersections for endpoints: %d -> %d " % (len(ixf1), len(ixf2))

if __name__ == "__main__":
    main()
