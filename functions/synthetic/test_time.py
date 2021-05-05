import math
import random
import sys
from time import time

ratio = 10000000 / 1.7

if __name__ == '__main__':
    r = int(float(sys.argv[1]) * ratio)
    # r = 100000
    ctr = 0
    i = 0
    s = time()
    while i < r:
        ctr += 187 * 133
        i += 1
    print((time() - s))