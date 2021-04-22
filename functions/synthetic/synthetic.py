import math
import random
from time import time

def compute(duration):
    start = time()
    ctr = 0
    while time() - start < duration:
        ctr += random.randint(0, 100)
    latency = time() - start
    return latency, ctr

def main(params):
    duration = float(params['duration'])
    ret_val = {}
    lat, ctr = compute(duration)
    ret_val['latency'] = lat
    ret_val['counter'] = ctr
    return ret_val