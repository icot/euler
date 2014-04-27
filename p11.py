#!/usr/bin/python

import numpy, sys

with open("11.txt") as fp:
    buf = fp.readlines()
    buf = map(lambda x: x[:-1], buf)
    grid_list = [map(lambda x: int(x), item.split()) for item in buf]

def products(xs, size):
    products = []
    for x in xs:
        for pos in range(len(x) - size ):
            buf =  x[pos:pos + size]
            products.append(reduce(lambda x,y: x*y, buf))
    return products

if __name__ == "__main__":
    lines = []
    grid_list_t = []

    m1 = numpy.matrix(grid_list)

    print "Rows: "
    for r in range(20):
        #print "Row (%d)" % (r), grid_list[r]
        lines.append(grid_list[r])

    print "Columns: "
    for c in range(20):
        col = [item[c] for item in grid_list]
        #print "Col (%d)" % (c), col
        lines.append(col)
        grid_list_t.append(col)

    m2 = numpy.matrix(grid_list_t)
    print "Diagonals Right: "
    print m1
    print ""
    print m2
    print ""
    print numpy.diagonal(m1,0,1,0)
    print numpy.diagonal(m2,0,1,0)

    for s in range(20):
        lines.append(numpy.diagonal(m1, s).tolist())
        lines.append(numpy.diagonal(m2, s).tolist())
        lines.append(numpy.diagonal(m1, -s).tolist())
        lines.append(numpy.diagonal(m2, -s).tolist())

    for r in range(20):
        rows = range(r,-1,-1)
        cols = range(r+1)
        d = []
        for pos in range(len(rows)):
            d.append(m1.item(rows[pos], cols[pos]))
        lines.append(d)

    p = products(lines, 4)
    print "Max: ", max(p)




    
