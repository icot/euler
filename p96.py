#!/usr/bin/pypy

import re
from itertools import permutations
import copy

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
    
def valid_candidate(row, ref, c_used_values):
    for i, elem in enumerate(ref):
        if elem > 0 and row[i] != elem:
            return False
        else:
            buf = c_used_values[i]
            if row[i] in c_used_values[i]:
                return False
    return True

def valid_permutations(ref, c_used_values):
    gen = permutations(range(1, 10))
    # used_values
    used_values = copy.deepcopy(c_used_values)
    for pos, item in enumerate(ref):
        if item in used_values[pos]:
            used_values[pos].remove(item)
    for item in gen:
        if valid_candidate(item, ref, used_values):
            yield item
        else:
            continue

def test_cube(center, sudoku):
    r, c = center
    cube = [sudoku[i,j] for i in range(r-1,r+2) for c in range(c-1, c+2)]
    cube = list(set(cube))
    if len(cube) == 9 and cube == range(1,10):
        return True
    else:
        return False


for sid, sudoku in data.items()[:1]:

    values = {}
    for r in range(9):
        for c in range(9):
            if sudoku[r][c]:
                values[(r,c)] = (sudoku[r][c], None)
            else:
                candidates = set([n for n in range(1,10)])
                values[(r,c)] = (sudoku[r][c], candidates)
        # Filtrado en filas
        used_r = set([sudoku[r][c] for c in range(9) if sudoku[r][c]])
        for c in range(9):
            cell, cands = values[(r,c)]
            if cands:
                values[(r,c)] = (cell, cands - used_r)

    # Filtrado en columnas
    for c in range(9):
        used_c = set([sudoku[r][c] for r in range(9) if sudoku[r][c]])
        for r in range(9):
            cell, cands = values[(r,c)]
            if cands:
                values[(r,c)] = (cell, cands - used_c)


    for k,v in values.items():
        if k[0] == 7:
            print k, v

