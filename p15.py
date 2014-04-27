#!/usr/bin/python

class node:
    def __init__(self, label, x, y, right=None, down=None):
        self.label = label
        self.x = x
        self.y = y
        self.right = right
        self.down = down

    def __repr__(self):
        return self.label

if __name__ == "__main__":
    rank = 4
    grid = []
    for r in range(rank):
        for c in range(rank):
            grid.append(node(str((r,c)), r, c))
    print grid


