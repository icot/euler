#!/usr/bin/env python

import re
from itertools import permutations
import copy

def main():
    with open('sudoku.txt') as fp:
        lines = fp.readlines()

    lines = [line[:-2] for line in lines]

    data = {}
    sudoku_id = 0
    sudoku = []

    for line in lines:
        if re.search('Grid', line):
            sudoku_id = int(line.split()[1]) - 1
            if sudoku_id >= 1:
                data[ sudoku_id ] = sudoku
                sudoku = []
        else:
            sudoku.append([int(c) for c in line])
        
    return data

if __name__ == "__main__":
    data = main()
    for sid, sud in data.items():
        print('%' + " Grid %d" % (sid))
        for line in sud:
            buf = []
            for char in line:
                if char == 0:
                    buf.append('.')
                else:
                    buf.append(str(char))
            print ''.join(buf)
        print
