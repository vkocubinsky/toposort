#!/usr/bin/env python3
from toposort import *

if __name__ == '__main__':
    """Like unix tsort"""
    with fileinput.input(files=('divisors.data')) as f, open('toposort.sorted.data','w') as w:
        for n in sort_edges(tuple(line.split()) for line in f): 
            print(n, file=w)

