import math
import random
from time import time

def compute(duration):
    r = int(10000000 / 1.7 * duration)
    start = time()
    ctr = 0
    i = 0
    while i < r:
        ctr += 187 * 133
        i += 1
    latency = time() - start
    return latency, ctr

def main(params):
    duration = float(params['duration'])
    ret_val = {}
    lat, ctr = compute(duration)
    ret_val['latency'] = lat
    ret_val['counter'] = ctr
    return ret_val