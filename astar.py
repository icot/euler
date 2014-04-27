#!/usr/bin/python
#

class Node:
    def __init__(self, name, value, n = {}):
        self.name = name
        self.value = value
        self.neighbours=n
        self.cvalue = None
    def __repr__(self):
        return str((self.name, self.value, self.cvalue, self.neighbours))

class Astar:
    def __init__(self, g = [], start = "", end = ""):
        self.graph = g
        self.startNode = self.graph[start]
        self.endNode = self.graph[end]
        self.path = [self.startNode]
        self.paths = []

    def cost(self,origin,dest):
        print "Costs:  Origin: %d, Dest: %d" % (origin.name, dest.name)
        if origin == dest:
            return 1e9
        else: 
            if dest.name in origin.neighbours.keys():
                print "Path cost: ", origin.neighbours[dest.name]
                return origin.neighbours[dest.name]
            else:
                return None

    def pathcost(self, path):
        origin = self.startNode
        cost = 0.0
        for node in path:
            cost += self.cost(origin,node)
            origin = node
        return cost

    def run(self):
        print "\n\nStart node: %s\nEnd Node: %s" % (self.startNode,self.endNode)
        
        while self.path[-1].name != self.endNode.name:
            node = self.path[-1]
            p = 0
            pt = 0
            candidate = None
            print "+++ Node: %s, Neighbours: %s" % (node.name, str(node.neighbours.keys()))
            for n in node.neighbours.keys():
                buf = self.graph[n]
                if buf in self.path:
                    print "> Skipping Node %s, already in path" % buf.name
                    pass
                else:
                    print "> Checking Node %s" % buf.name
                    if len(self.path) == 1:
                        g = self.cost(self.startNode,buf)
                        h = self.cost(buf,self.endNode)
                    else:
                        g = self.pathcost(self.path)
                        h = self.cost(buf,self.endNode)
                    if g and h:
                        pt = g + h
                        print ">> Temp node: %s, Pt: %f " % (buf.name, pt)
                        print ">> g: %f, h: %f" % (g,h)
                        if pt >= p:
                            candidate = buf
                            p = pt
            if candidate:
                self.path.append(candidate)
            cad = ''
            pvalue = 0
            for item in self.path:
                cad += repr(item.name) + ' '
                pvalue += item.value
            print "\n>>> path { %s}, cost: %d" % (cad, pvalue)
            
if __name__=="__main__":
    graph = { "A": Node( "A", { "B":1, "C":1 } ),
            "B": Node( "B", { "A":1, "D":1, "E": 2.24 } ),
            "C": Node( "C", { "A":1, "D":1, "E":1 } ),
            "D": Node( "D", { "B":1, "C":1, "F":1 } ),
            "F": Node( "F", { "D":1, "E":1 } ),
            "E": Node( "E", { "B":2.24, "C":1, "F":1} ) }

    a = Astar(graph,"A","E")
    
    #print a.cost(graph["A"],graph["A"])
    #print a.cost(graph["A"],graph["B"])
    #print a.cost(graph["A"],graph["E"])

    a.run()


    
