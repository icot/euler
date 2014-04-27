#!/usr/bin/python

import networkx as nx
import matplotlib.pyplot as plt

def loadFile(filename):
    matrix = []
    with open(filename) as fp:
        lines = fp.readlines()
        lines = map(lambda x: x[:-1], lines)
        for line in lines:
            row = map(int, line.split(','))
            matrix.append(row)
    return matrix

def g81(matrix):
    dg = nx.DiGraph()
    N = len(matrix)
    M = len(matrix[0])
    for r in xrange(N):
        for c in xrange(M):
            nodeName = (r,c)
            dg.add_node(nodeName, value = matrix[r][c])
    for r in xrange(N-1):
        for c in xrange(M-1):
            nodeOrigin =  (r,c)
            nodeRight = (r+1,c)
            nodeDown = (r,c+1)
            dg.add_edge(nodeOrigin, nodeRight, weight = matrix[r][c])
            dg.add_edge(nodeOrigin, nodeDown, weight = matrix[r][c])
    dg.add_edge((N-2,M-1), (N-1,M-1), weight = matrix[N-2][M-1])
    dg.add_edge((N-1,M-2), (N-1,M-1), weight = matrix[N-1][M-2])
    return dg

def g82(matrix):
    dg = nx.DiGraph()
    N = len(matrix)
    M = len(matrix[0])
    for r in xrange(N):
        for c in xrange(M):
            nodeName = (r,c)
            dg.add_node(nodeName, value = matrix[r][c])
    # First row
    for c in xrange(M-1):
        nodeOrigin = (0,c)
        nodeRight = (0,c+1)
        nodeDown = (1, c)
        dg.add_edge(nodeOrigin, nodeRight, weight = matrix[0][c])
        dg.add_edge(nodeOrigin, nodeDown, weight = matrix[0][c])
    # General Case
    for r in xrange(1, N-2):
        for c in xrange(M-1):
            nodeOrigin =  (r,c)
            nodeRight = (r+1,c)
            nodeDown = (r,c+1)
            nodeUp = (r-1,c)
            dg.add_edge(nodeOrigin, nodeRight, weight = matrix[r][c])
            dg.add_edge(nodeOrigin, nodeDown, weight = matrix[r][c])
            dg.add_edge(nodeOrigin, nodeUp, weight = matrix[r][c])
    # Last Row
    for c in xrange(M-1):
        nodeOrigin = (N-1, c)
        nodeRight = (N-1, c+1)
        nodeUp = (N-2, c)
        dg.add_edge(nodeOrigin, nodeRight, weight = matrix[N-1][c])
        dg.add_edge(nodeOrigin, nodeUp, weight = matrix[N-1][c])
    return dg

def g83(matrix):
    dg = nx.DiGraph()
    N = len(matrix)
    M = len(matrix[0])
    for r in xrange(N):
        for c in xrange(M):
            node = (r,c)
            dg.add_node(node, value = matrix[r][c])
            up = (r-1, c)
            left = (r, c-1)
            right = (r,c+1)
            down = (r+1, c)
            try:
                vleft = matrix[r][c-1]
            except IndexError:
                vleft = 1e6
            try:
                vright = matrix[r][c+1]
            except IndexError:
                vright = 1e6
            try:
                vdown = matrix[r+1][c]
            except IndexError:
                vdown = 1e6
            try:
                vup = matrix[r-1][c]
            except IndexError:
                vup = 1e6
            dg.add_edge(node, right, weight = vright)
            dg.add_edge(node, left, weight = vleft)
            dg.add_edge(node, up, weight = vup)
            dg.add_edge(node, down, weight = vdown)

    for node in dg.nodes():
        x, y = node
        if x < 0 or x > (N-1):
            dg.remove_node(node)
        if y < 0 or y > (M-1):
            dg.remove_node(node)
    return dg

matrix = loadFile("matrix.txt")

def dist(node, target):
    global matrix
    (r, c) = node
    mini = 1e6
    sumv = 0
    for row in [r-1, r, r+1]:
        for col in [c-1, c, c+1]:
            try:
                val = matrix[row][col]
                sumv += val
                if val < mini:
                    mini = val
            except IndexError:
                continue
    return sumv


def main82():
    g = g82(matrix)
    N = len(matrix)
    M = len(matrix[0])
    print "(%d) Nodes, (%d) Edges" % (len(g.nodes()), len(g.edges()))
    #print nx.dijkstra_path_length(g, (0,0), (N-1,M-1)) + g.node[(N-1, M-1)].get('value')
    minimum = 1e6
    minimum2 = 1e6
    for r in xrange(N):
        for r1 in xrange(M):
            try:
                source = (r,0)
                destiny = (r1, M-1)
                l = nx.dijkstra_path_length(g, source, destiny)
                l += g.node[destiny].get('value')
                l2 = nx.astar_path_length(g, source, destiny, dist)
                l2 += g.node[destiny].get('value')
                if l < minimum:
                    minimum = l
                if l2 < minimum2:
                    minimum2 = l2
            except:
                continue
    print minimum, minimum2    

def main83():
    g = g83(matrix)
    N = len(matrix)
    M = len(matrix[0])
    print "(%d) Nodes, (%d) Edges" % (len(g.nodes()), len(g.edges()))
    start = (0,0)
    end = (N-1, M-1)
    path_d = nx.dijkstra_path(g, start, end)
    print len(path_d), nx.dijkstra_path_length(g, start, end) + g.node[start].get('value')
    for node in path_d:
        print node, g.node[node].get('value'), g[node]

if __name__ == "__main__":
    main83()
