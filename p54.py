#!/usr/bin/python

from goopy import functional as func

with open('poker.txt') as fp:
    deals = map(lambda x:x[:-2], fp.readlines())

val = {'2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        'T': 10,
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14}

def test_straight(l):
    l = list(set(l))
    l.sort()
    difs = func.first_difference(l)
    cond = sum(difs) == len(difs)
    if cond:
        return (cond, max(l))
    else:
        return (cond, None)

def test_pair(values, play):
    cond = len(set(values)) == 4
    if cond:
        for k, v in play.items():
            if v == 2:
                return (cond, k)
    else:
        return (cond, None)

def test_twopairs(values, play):
    cond = (len(set(values)) == 3 and max(play.values()) == 2)
    if cond:
        vs = []
        for k, v in play.items():
            if v == 2:
                vs.append(v)
        return (cond, vs)
    else:
        return (cond, None)

def test_threeofakind(values, play):
    cond = len(set(values)) == 3 and max(play.values()) == 3
    if cond:
        for k, v in play.items():
            if v == 3:
                return (cond, k)
    else:
        return (cond, None)

def test_fullhouse(values, play):
    cond = len(set(values)) == 2 and max(play.values()) == 3
    if cond:
        vs = []
        for k, v in play.items():
            vs.append(v)
        vs.sort()
        return (cond, vs)
    else:
        return (cond, None)

def test_quad(values, play):
    cond = len(set(values)) == 2 and max(play.values()) == 4
    if cond:
        for k, v in play.items():
            if v == 4:
                return (cond, k)
    else:
        return (cond, None)

def evalh(h, vals = val):
    values = map(lambda x: x[0], h)
    values = [vals[item] -1 for item in values]
    suits = map(lambda x: x[1], h)
    play = {}
    for item in list(set(values)):
        play[item] = values.count(item)
    #Pair
    hand = 0
    test, card = test_pair(values, play)
    if test:
        return 1 *card 
    #Two Pairs
    test, card = test_twopairs(values, play)
    if test:
        return 10 * card[0] +10*card[1]
    #Three of a Kind
    test, card = test_threeofakind(values, play)
    if test:
        return 100 * card
    #Straight
    test, card = test_straight(values)
    if test and len(set(suits)) > 1:
        return 1000 * card
    #Flush
    if len(set(suits)) == 1 and not test:
        return 10000 * max(values)
    #Full House
    test, card = test_fullhouse(values, play)
    if test:
        return 100000 * card[0] + 10000 * card[1]
    #Four of a kind
    test, card = test_quad(values, play)
    if test:
        return 1000000 * card
    #Royal flush
    test, card = test_straight(values)
    if test and len(set(suits)) == 1:
        return 10000000 * card
    return 0
    

def compare(h1, h2, vals = val):
    v1 = [vals[item] -1 for item in map(lambda x: x[0], h1)]
    v1.sort()
    v1.reverse()
    v2 = [vals[item] -1 for item in map(lambda x: x[0], h2)]
    v2.sort()
    v2.reverse()
    for pos in range(len(h1)):
        if v1[pos] > v2[pos]:
            return True
        else:
            if v2[pos] > v1[pos]:
                return False
            else:
                return None


if __name__ == "__main__":
    t1 = 0
    t2 = 0
    for deal in deals:
        h1 = deal.split(' ')[0:5]
        h2 = deal.split(' ')[5:]
        e1 = evalh(h1)
        e2 = evalh(h2)
        if e1 > e2:
            t1 += 1
        else:
            if e2 > e1:
                t2 += 1
            else:
                v = compare(h1, h2)
                if v:
                    t1 +=1
                else:
                    t2 +=1
                print h1, e1, h2, e2, v
    print len(deals), t1, t2

