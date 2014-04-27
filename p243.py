#!/usr/bin/python

def factor(n):  
        if n == 1: return [1]  
        i = 2  
        limit = n**0.5  
        while i <= limit:  
                if n % i == 0:  
                        ret = factor(n/i)  
                        ret.append(i)  
                        return ret  
                i += 1  
        return [n]  

def uniqify(seq):
        return list(set(seq))
        
def phi(x):
    t = x
    for k in uniqify(factor(x)):
        t -= t // k
    return t

def resilience(x):
    return phi(x) / (x-1.0)
    
def main2():
    lastprime = 11
    base = 2*3*5*7*11.0
    multiplier = 1.0
    print "Starting value",  base

    while (resilience(base * multiplier) > (15499.0/94744.0)):
        multiplier = multiplier +1.0
        print base*multiplier
        if (multiplier > lastprime):
            if (len(factor(multiplier)) == 1):
                lastprime = multiplier
                base = base * multiplier
                print "New starting value for search",  base
                multiplier = 1.0

    print "Answer :: ", base * multiplier

 

if __name__ == "__main__":
    main2()
