#!/usr/bin/env python3

import sys

def produce_data(limit):
    for n in range(2,limit + 1):
        for m in range(2, n//2 + 1):
            if n%m == 0:
                yield (m,n)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {prg} limit".format(prg=sys.argv[0]))
        sys.exit()

    limit = int(sys.argv[1])
    for (m,n) in produce_data(limit):
        print (m,n)
