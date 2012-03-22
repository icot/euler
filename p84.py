#!/usr/bin/python3.2

import random
import fractions

def chance(pos):
    c = random.randint(1,16)
    if c == 1:
        return 10
    elif c == 2:
        return 0
    else:
        return pos 

def community_chest(pos):
    global chest
    c = random.randint(1,16)
    if type(chest[c]) == type(lambda x:x):
        return chest[c](pos)
    elif chest[c]:
        return chest[c]
    else:
        return pos

def next_utility(pos):
    if pos < 12 or pos > 28: 
        return 12
    else:
        return 28

def next_railway(pos):
    if 5 < pos < 15:
        return 15
    elif 15 < pos < 25:
        return 25
    elif 25 < pos < 35:
        return 35
    else:
        return 5

def rolls():
    return random.randint(1,6) + random.randint(1,6)

def step(pos, d):
    global board
    nposition = (pos + d) % 39
    action = board[nposition]
    if not action:
        return nposition
    elif type(action) == type(lambda x:x):
        res = action(nposition)
        if res < 0:
            res =  39 - nposition + 1
        return res
    else:
        return action

board = {n:None for n in range(40)}
board[2] = community_chest
board[17] = community_chest
board[33] = community_chest
board[7] = chance
board[22] = chance
board[36] = chance
board[30] = 10

chest = {n:None for n in range(1,17)}
chest[1] = 0
chest[2] = 10
chest[3] = 11
chest[4] = 34
chest[5] = 39
chest[6] = 5
chest[7] = next_railway
chest[8] = next_railway
chest[9] = next_utility
chest[10] = lambda x: x-3 

def main():
    N = 1000000
    pos = 0
    visited = {n:0 for n in range(40)}
    for n in range(N):
        dices = rolls() 
        pos = step(pos, dices)
        visited[pos] += 1

    data = {v:k for k,v in visited.items()}
    dkeys = list(data.keys())
    dkeys.sort()
    dkeys.reverse()

    for k in dkeys:
        ratio = float(fractions.Fraction(k*100, N))
        print(data[k], ratio)

    modalstr = ''.join([str(data[k]) for k in dkeys[0:3]])
    print("Modalstr: %s" % (modalstr))
        
if __name__ == "__main__":
    main()

