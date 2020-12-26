# test
# python3 ./zz_profile_cpu_limit.py --min-cpus 0.5 --max-cpus 1.0 --cpus-step 0.5 --users 1 --exp-time 60s --function mobilenet --iat 1

# assume docker version >= 1.13
import sys
import os
import time
import numpy as np
import json
import math
import random
import argparse
import logging
import subprocess
from pathlib import Path
import copy
import shutil
import csv
import requests

from pathlib import Path
sys.path.append(str(Path.cwd() / 'util'))
from db_activation import *
from cpu_util import *

# from socket import SOCK_STREAM, socket, AF_INET, SOL_SOCKET, SO_REUSEADDR

random.seed(time.time())
# -----------------------------------------------------------------------
# miscs
# -----------------------------------------------------------------------
logging.basicConfig(level=logging.INFO,
					format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

parser = argparse.ArgumentParser()
# parser.add_argument('--cpus', dest='cpus', type=int, required=True)
# parser.add_argument('--stack-name', dest='stack_name', type=str, required=True)
parser.add_argument('--function', dest='function', type=str, required=True)
parser.add_argument('--users', dest='users', type=int, required=True)
parser.add_argument('--min-cpus', dest='min_cpus', type=float, required=True)
parser.add_argument('--max-cpus', dest='max_cpus', type=float, required=True)
parser.add_argument('--cpus-step', dest='cpus_step', type=float, required=True)
parser.add_argument('--exp-time', dest='exp_time', type=str, default='90s')
parser.add_argument('--warmup-time', dest='warmup_time', type=str, default='10s')
parser.add_argument('--iat', dest='iat', type=int, required=True)
args = parser.parse_args()

function = args.function
users = args.users
min_cpus = args.min_cpus
max_cpus = args.max_cpus
cpus_step = args.cpus_step
exp_time = args.exp_time
warmup_time = args.warmup_time
iat = args.iat

data_dir = Path.cwd() / 'zz_data'
locust_stats_dir = Path.home() / 'openwhisk_locust_log'

auth_str = '23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP'
USER_PASS = auth_str.strip().split(':')
NAMESPACE = '_'
APIHOST = 'https://172.17.0.1'

action_records = {}	# indexed by cpu limit
locust_records = {} # indexed by cpu limit

# openwhisk
openwhisk_invoker_log = Path('/tmp/wsklogs/invoker0/invoker0_logs.log')

if not os.path.isdir(str(data_dir)):
	os.makedirs(str(data_dir))

script = Path.cwd() / 'scripts' / ('test_action_iat_' + str(iat) + '.sh')
assert os.path.isfile(str(script))

tested_cpus = np.arange(min_cpus, max_cpus + cpus_step, cpus_step)
print('tested_cpus')
print(tested_cpus)

def change_time(time_str):
	if 'm' in time_str:
		return int(time_str.replace('m', '')) * 60
	elif 's' in time_str:
		return int(time_str.replace('s', ''))
	else:
		return int(time_str)

def update_action_limits(action_name, cpu=None, memory=None, timeout=None):
	limits = {}
	if cpu is None and memory is None and timeout is None:
		return
	if cpu is not None:
		limits['cpu'] = cpu
	if memory is not None:
		limits['memory'] = memory
	if timeout is not None:
		limits['timeout'] = timeout
	response = requests.put(url=APIHOST + '/api/v1/namespaces/' + NAMESPACE + '/actions/' + action_name,
							json={'limits': limits},
							params={'overwrite': 'true'},
							auth=(USER_PASS[0], USER_PASS[1]), verify=False)
	return response

def run_exp(test_time, user, quiet=False):
	cmd = str(script) + ' ' + str(test_time) + ' ' + str(user) + ' ' + function
	if not quiet:
		p = subprocess.Popen(cmd, shell=True)
	else:
		p = subprocess.Popen(cmd, shell=True, 
			stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	return p

def copy_locust_stats(dir_name):
	global data_dir

	full_path = data_dir / dir_name
	if os.path.isdir(str(full_path)):
		shutil.rmtree(str(full_path))
	shutil.copytree(str(locust_stats_dir), str(full_path))

# "Type","Name","Request Count","Failure Count","Median Response Time","Average Response Time","Min Response Time","Max Response Time","Average Content Size","Requests/s","Failures/s","50%","66%","75%","80%","90%","95%","98%","99%","99.9%","99.99%","99.999%","100%"

def read_locust_stats(function, cpu):
	global locust_records
	if cpu not in locust_records:
		locust_records[cpu] = {}

	locust_stats_file = locust_stats_dir / (function + '_stats.csv')
	with open(str(locust_stats_file), 'r') as f:
		lines = f.readlines()
		fields = lines[0].split(',')
		rps_idx = -1
		requests_idx = -1
		fps_idx = -1
		failures_idx = -1
		
		for (i, field) in enumerate(fields):
			# print(field)
			if 'Request Count' in field:
				requests_idx = i
			elif 'Failure Count' in field:
				failures_idx = i
			elif 'Requests/s' in field:
				rps_idx = i
			elif 'Failures/s' in field:
				fps_idx = i

		for line in lines[0:]:
			# print(line)
			if function not in line:
				# print('line skipped, ', function)
				continue
			data = line.split(',')
			# print(data)
			# print(rps_idx, requests_idx, fps_idx, failures_idx)
			if rps_idx >= 0:
				locust_records[cpu]['rps'] = float(data[rps_idx])
			else:
				locust_records[cpu]['rps'] = -1

			if requests_idx >= 0:
				locust_records[cpu]['requests'] = int(data[requests_idx])
			else:
				locust_records[cpu]['requests'] = -1

			if fps_idx >= 0:
				locust_records[cpu]['fps'] = float(data[fps_idx])
			else:
				locust_records[cpu]['fps'] = -1

			if failures_idx >= 0:
				locust_records[cpu]['failures'] = int(data[failures_idx])
			else:
				locust_records[cpu]['failures'] = -1

def clear_locust_stats():
	for fn in os.listdir(str(locust_stats_dir)):
		full_path = locust_stats_dir / fn
		os.remove(str(full_path))

def get_activation_ids():
	full_path = locust_stats_dir / 'locust_openwhisk_log.txt'
	aids = {}	# indexed by function name
	with open(str(full_path), 'r') as f:
		lines = f.readlines()
		for line in lines:
			if 'aid--' in line:
				# print(line)
				data = line.split('aid--')[-1]
				action, aid = data.split(':')
				aid = aid.replace('\n', '').strip()
				if action not in aids:
					aids[action] = []
				aids[action].append(aid)
				# print(aid)
				# print('')
	return aids

def invoker_log_length():
	l = 0
	with open(str(openwhisk_invoker_log), 'r') as f:
		lines = f.readlines()
		l = len(lines)
	return l

def grep_function_distr(tail_len, distr_file, cpu):
	global action_records
	assert cpu in action_records

	chosen = []
	with open(str(openwhisk_invoker_log), 'r') as f:
		lines = f.readlines()[-tail_len:]
		for line in lines:
			if 'cpu_util' in line:
				chosen.append(line)
				# parse the line
				data = line.split(',')
				cpu_util = -1
				exe_time = -1
				for d in data:
					if 'cpu_util' in d:
						cpu_util = float(d.split('=')[-1])
					elif 'exe_time' in d:
						exe_time = int(d.split('=')[-1])
				action_records[cpu].append((cpu_util, exe_time))

	with open(str(distr_file), 'w+') as f:
		for l in chosen:
			f.write(l + '\n')

clear_locust_stats()
time.sleep(10)
# stress test
for c in tested_cpus:
	# update action cpu limit
	r = update_action_limits(function, cpu=c)
	print(r.text)
	# sys.exit()

	action_records[c] = []

	# warm up
	pl = run_exp(test_time=warmup_time, user=users)
	pl.wait()
	consecutive_low_use = 0
	prev_idle = 0
	prev_total = 0
	while consecutive_low_use < 5:
		time.sleep(1)
		total, idle = check_proc_stat()
		util = compute_cpu_util(prev_idle, prev_total, idle, total)
		if util <= 0.1:
			consecutive_low_use += 1
		else:
			consecutive_low_use = 0
		prev_idle = idle
		prev_total = total
	print('warm up complete\n')
	
	# check log
	log_init_length = invoker_log_length()
	print('log_init_length = %d' %log_init_length)

	pl = run_exp(test_time=exp_time, user=users)
	pl.wait()

	# time.sleep(10)
	consecutive_low_use = 0
	print('waiting for system to cool down...')
	prev_idle = 0
	prev_total = 0
	while consecutive_low_use < 5:
		time.sleep(1)
		total, idle = check_proc_stat()
		util = compute_cpu_util(prev_idle, prev_total, idle, total)
		if util <= 0.1:
			consecutive_low_use += 1
		else:
			consecutive_low_use = 0
		prev_idle = idle
		prev_total = total
	print('system cooled down\n')

	log_length = invoker_log_length()
	print('log_length = %d' %log_length)

	if not os.path.isdir(str(data_dir / function)):
		os.makedirs(str(data_dir / function))

	distr_file =  data_dir / function / ('cpu_' + format(c, '.1f') + '.txt' )
	grep_function_distr(tail_len=log_length-log_init_length, distr_file=distr_file, cpu=c)

	read_locust_stats(function=function, cpu=c)

	copy_locust_stats(function + 'locust_cpu_' + format(c, '.1f'))
	clear_locust_stats()

summary_csv = data_dir / function / 'summary.csv'
with open(str(summary_csv), 'w+') as f:
	lat_writer = csv.writer(f, delimiter=',')
	lat_writer.writerow(['cpu_limit', 
						 # cpu time
						 'mean_cpu_time', 
						 'std_cpu_time', 
						 'max_cpu_time',
						 'min_cpu_time',
						 # cpu
						 'mean_cpu', 
						 'std_cpu', 
						 'max_cpu',
						 'min_cpu',
						 # exe_time
						 'mean_time', 
						 'std_time', 
						 'max_time',
						 'min_time',
						 #locust stats
						 'requests',
						 'failures',
						 'rps',
						 'fps'
						 ])

	# print('locust_records')
	# print(locust_records)
	for cpu_limit in action_records:
		cpu_time_arr = np.array([s*t for (s, t) in action_records[cpu_limit]])
		cpu_arr = np.array([s for (s, _) in action_records[cpu_limit]])
		exe_time_arr = np.array([t for (_, t) in action_records[cpu_limit]])
		lat_writer.writerow([cpu_limit,
							cpu_time_arr.mean(),
							cpu_time_arr.std(),
							cpu_time_arr.max(),
							cpu_time_arr.min(),
							cpu_arr.mean(),
							cpu_arr.std(),
							cpu_arr.max(),
							cpu_arr.min(),
							exe_time_arr.mean(),
							exe_time_arr.std(),
							exe_time_arr.max(),
							exe_time_arr.min(), 
							locust_records[cpu_limit]['requests'],
							locust_records[cpu_limit]['failures'],
							locust_records[cpu_limit]['rps'],
							locust_records[cpu_limit]['fps']
							])