#!/usr/bin/env python

import sys
import copy

def partitions(n):
    def h_f(ns):
        if len(ns) == 1:
            return ns
        if len(ns) == 2:
            return [ns[0] + ns[1]]
        else:
            new_partitions = [ns]
            for pos1 in range(0, len(ns) - 1):
                for pos2 in range(pos1 + 1, len(ns)):
                    seed = copy.copy(ns)
                    new =  ns[pos1] + ns[pos2]
                    seed.remove(ns[pos1])
                    seed.remove(ns[pos2])
                    seed.append(new)
                    seed.sort() 
                    seed.reverse()
                    if seed not in new_partitions:
                        new_partitions.append(seed)
            return new_partitions
    seed = map(lambda x: 1, range(0, n))
    partition_list = [seed]
    used_seeds = []
    for seedp in partition_list:
        if seedp not in used_seeds:
            try:
                nps = h_f(seedp)
                for np in nps:
                    if np not in partition_list:
                        partition_list.append(np)
                used_seeds.append(seedp)
            except TypeError:
                pass
    return partition_list

def parts(N):
    def pnk(n,k):
        if k >= n and (n > 1 or k > 1):
            return 0
        else:
            if n <= 1 or k == 1:
                return 1
            else:
                try:
                    return parts.cache[(n,k)]
                except KeyError:
                    res = parts.cache[(n-k, k)] + parts.cache[n, k -1]
                    parts.cache[(n,k)] = res
                    return res
    parts.cache = {}
    for n in xrange(0,N+1):
        for k in xrange(1,N+1):
            parts.cache[(n,k)] = pnk(n,k)
    return parts.cache[(N,N)]

if __name__ == "__main__":
    N = int(sys.argv[1])
    parts = partitions(N)
    for p in parts:
        print p
