#!/usr/bin/python

from utils import test_triang, triangle_gen

with open('words.txt') as fp:
    words = fp.read().split(',')
    words = map(lambda x: x[1:-1], words)

def word_value(word):
    return sum(map(lambda x: (ord(x) - ord('A')) + 1, word))

if __name__ == "__main__":
    print len(words)
    triangle_words = []    
    for word in words:
        print word, word_value(word)
        if test_triang(word_value(word)):
            triangle_words.append(word)
    print len(triangle_words)






