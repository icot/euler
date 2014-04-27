#!/usr/bin/python

values = {
0:"",
1:"one",
2:"two",
3:"three",
4:"four",
5:"five",
6:"six",
7:"seven",
8:"eight",
9:"nine",
10:"ten",
11:"eleven",
12:"twelve",
13:"thirteen",
14:"fourteen",
15:"fifteen",
16:"sixteen",
17:"seventeen",
18:"eighteen",
19:"nineteen",
20:"twenty",
30:"thirty",
40:"forty",
50:"fifty",
60:"sixty",
70:"seventy",
80:"eighty",
90:"ninety",
100:"hundred",
1000: "onethousand"}

def convert(num, values=values):
    if num <= 20:
        return [values[num]]
    if num < 100:
        dec = int(num / 10)
        units = num % 10
        return [values[dec*10], values[units]]
    if num < 1000:
        cents = int(num / 100)
        rem = num % 100 
        dec = int(rem / 10)
        units = rem % 10
        if units or dec:
            if (dec*10 + units) <= 20:
                return [values[cents], values[100], "and", values[dec*10+units]]
            else:
                return [values[cents], values[100], "and", values[dec*10],values[units]]
        else:
            return [values[cents], values[100]]
    if num == 1000:
        return [values[num]]

if __name__ == "__main__":
    total = 0
    for n in range(1,1001):
        res = convert(n)
        N = ' '.join(res)
        l = sum(map(lambda x: len(x), res))
        print n, N, l
        total += l
    print total
