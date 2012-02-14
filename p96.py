#!/usr/bin/python3.2

import re

with open('sudoku.txt') as fp:
    lines = fp.readlines()

lines = [line[:-2] for line in lines]

data = {}
sudoku_id = 0
sudoku = []

for line in lines:
    if re.search('Grid', line):
        sudoku_id = int(line.split()[1])
        if sudoku_id > 1:
            data[ sudoku_id - 1 ] = sudoku
            sudoku = []
    else:
        sudoku.append([int(c) for c in line])
        
for sid, sud in data.items():
    print( (sid,sud))
