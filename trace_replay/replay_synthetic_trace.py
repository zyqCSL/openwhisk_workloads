# replay a syntheic trace with exact arrival timestamps
import argparse
import json
import os
import requests
from requests_futures.sessions import FuturesSession
import subprocess
import sys
import time
import threading
import logging
import numpy as np
from pathlib import Path

logging.basicConfig(level=logging.INFO)
# -----------------------------------------------------------------------
# parser args definition
# -----------------------------------------------------------------------
parser = argparse.ArgumentParser()
# parser.add_argument('--users', dest='users', type=int, required=True)
parser.add_argument('--exp-time', dest='exp_time', type=str, required=True)
parser.add_argument('--workers', dest='workers', type=int, required=True)
parser.add_argument('--func-trace', dest='func_trace', type=str, required=True)

def change_time(time_str):
    if 'm' in time_str:
        return int(time_str.replace('m', '')) * 60
    elif 's' in time_str:
        return int(time_str.replace('s', ''))
    else:
        return int(time_str)

# -----------------------------------------------------------------------
# parse args
# -----------------------------------------------------------------------
args = parser.parse_args()
# users = args.users
exp_time = change_time(args.exp_time)
num_workers = args.workers

# -----------------------------------------------------------------------
# parse function trace
# -----------------------------------------------------------------------
def check_inv_record(inv):
    r = True
    r = r and ('start_time' in inv)
    r = r and ('app' in inv)
    r = r and ('duration' in inv)
    return r

worker_traces = {}
for i in range(0, num_workers):
    worker_traces[i] = []
next_worker = 0
with open(args.func_trace, 'r') as f:
    invocations = json.load(f)
    for inv in invocations:
        if not check_inv_record(inv):
            logging.error('invalid inv record: ' + str(inv))
            sys.exit()
        worker_traces[next_worker].append(inv)
        next_worker = (next_worker + 1) % num_workers
    
# -----------------------------------------------------------------------
# openwhisk config
# -----------------------------------------------------------------------
auth_str = '23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP'
pwd_1, pwd_2 = auth_str.strip().split(':')
auth = (pwd_1, pwd_2)
api_host = 'https://172.17.0.1'
base_url = api_host + '/api/v1/namespaces/_/actions/'

def http_worker(worker_trace, base_url, auth, exp_time):
    session = FuturesSession(max_workers=30)
    start_time = time.time()
    for inv in enumerate(worker_trace):
        cur_time = time.time() - start_time
        if cur_time > exp_time:
            break
        wait_time = inv['start_time'] - cur_time
        if wait_time > 0:
            time.sleep(wait_time)
        elif wait_time <= -1:
            logging.warning('worker fall behind schedule by %.1fs' %(-wait_time))
        # inv info
        duration = float(inv['duration'])
        app = str(inv['app'])
        action = 'synthetic-' + app
        # http req
        url = base_url + action
        params = {}
        params['blocking'] = 'false'
        params['result'] = 'false'
        body = {}
        body['duration'] = duration
        future = session.post(url, params=params, auth=auth,
            json=body, verify=False)


threads = []
for worker in worker_traces:
    trace = worker_traces[worker]    

    t = threading.Thread(target=http_worker, kwargs={
                'worker_trace': trace,
                'base_url': base_url, 
                'auth': auth, 
                'exp_time': exp_time
            })
    threads.append(t)
    
logging.info("#------------- Experiment started -------------#")
for thread in threads:
    thread.start()
logging.info("#------------- Experiment ended -------------#")