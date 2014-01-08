#!/usr/bin/python

value = {}
value['M'] = 1000
value['D'] = 500
value['C'] = 100
value['L'] = 50
value['X'] = 10
value['V'] = 5
value['I'] = 1

def roman_to_int(roman):
    vals = [value[x] for x in roman]
    res = [vals[0]]
    for pos in xrange(1, len(vals)):
        new = vals[pos]
        if new <= res[-1]:
            res.append(new)
        else:
            res[-1] = new - res[-1]
    return sum(res) 

def int2roman(number):
    numerals = { 1 : "I", 4 : "IV", 5 : "V", 9 : "IX", 10 : "X", 40 : "XL",
            50 : "L", 90 : "XC", 100 : "C", 400 : "CD", 500 : "D", 900 : "CM", 1000 : "M" }
    result = ""
    for value, numeral in sorted(numerals.items(), reverse=True):
        while number >= value:
            result += numeral
            number -= value
    return result

if __name__ == "__main__":
    with open('roman.txt') as fp:
        romans = fp.readlines()
        romans = [number[:-1] for number in romans[:-1]]
    numbers_int = [roman_to_int(number) for number in romans]
    numbers_rom = [int2roman(number) for number in numbers_int]
    l1 = sum([len(number) for number in romans])
    l2 = sum([len(number) for number in numbers_rom])
    print l1, l2, l1 - l2
