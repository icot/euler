#!/usr/bin/python

import astar

with open('triangle2.txt') as fp:
    lines = fp.readlines()
    triangle = map(lambda x:map(lambda x: int(x), x[:-1].split()), lines)

if __name__== "__main__":
    for r in range(len(triangle)):
        row = triangle[r]
        #print row
    print "Top limit: ", sum(map(lambda x: max(x), triangle))
    nid = 0
    
    graph = {}
    nids = []
    grows = []
    for r in range(len(triangle)):
        row = triangle[r]
        nidr = []
        if r < len(triangle)-1:
            for pos in range(len(row)):
                value = row[pos]
                left = triangle[r+1][pos]
                right = triangle[r+1][pos+1]
                #print "#ID: %d  (%d) <-- (%d) --> (%d)" % (nid, left, value, right)
                graph[nid] = astar.Node(nid, value)
                nidr.append(nid)
                nid += 1
        else:
            for pos in range(len(row)):
                value = row[pos]
                #print "#ID: %d (%d)" % (nid, value)
                graph[nid] = astar.Node(nid, value)
                nidr.append(nid)
                nid += 1
        nids.append(nidr)
    
    for r in range(len(nids)):
        row = nids[r]
        if r < len(triangle) -1:
            for pos in range(len(row)):
                nid = row[pos]
                left = nids[r+1][pos]
                right = nids[r+1][pos+1]
                neighs = {left:graph[nid].value, right:graph[nid].value}
                graph[nid].neighbours = neighs
    
    for id, node in graph.items():
        if node.neighbours == {}:
            node.cvalue = (node.value, node.value)

    for pos in xrange(len(nids)-2,-1,-1):
        row = nids[pos]
        for nid in row:
            val = graph[nid].value
            neighs = graph[nid].neighbours
            left, right = neighs.keys()
            mcvleft = max(graph[left].cvalue)
            mcvright = max(graph[right].cvalue)
            cval = (val + mcvleft, val + mcvright)
            graph[nid].cvalue = cval
            #print "Node (%d) : %s " % (nid,str(cval))

    print "Max sum: ", max(graph[0].cvalue)

