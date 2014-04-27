#!/usr/bin/python

m = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
ml = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

dow = [0, 1, 2, 3, 4, 5, 6]

def dow_gen():
    a = 0
    while 1:
        yield a
        if a <= 5:
            a = a+1
        else:
            a = 0

def leap_year(year):
    if year % 100 == 0:
        if year % 400 == 0:
            return True
        else:
            return False
    else:
        if year % 4 == 0:
            return True

if __name__ == "__main__":
    day = 1
    firsts = []
    for year in xrange(1900, 2001):
        if leap_year(year):
            months = ml
        else:
            months = m
        for p in range(len(months)):
            M = months[p]
            for md in xrange(M):
                day = day + 1
                if md == 0 and year > 1900:
                    firsts.append(day)
    print len(filter(lambda x: ((x%7)==0), firsts))
