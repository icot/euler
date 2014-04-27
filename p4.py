#!/usr/bin/python


def palindrome(cad):
    if (len(cad) <= 1):
        return True
    else:
        if cad[0] == cad[-1]:
            return palindrome(cad[1:-1])
        else:
            return False
        

if __name__ == "__main__":
    n = range(100, 1000)
    products = []
    for pos in range(len(n)):
        rem = n[pos:]
        buf = [n[pos] * item for item in rem]
        products.extend(buf)
    palindromes = filter(lambda x: palindrome(str(x)), products)
    palindromes.sort()
    print palindromes[-10:]

