import sys
import os
from pathlib import Path
import time

stat = Path('/proc/stat')
interval = 1

total_time = 0
idle_time = 0
prev_record = []

def update():
	global idle_time
	global total_time
	with open(str(stat), 'r') as f:
		lines = f.readlines()
		data = [int(k) for k in lines[0].split(' ') if k != '' and k != '\n' and k != 'cpu']
		prev_record = list(data)
		print(data)
		total = sum(data)
		idle = data[3]
		print('total = %d, idle = %d' %(total, idle))
		util = 1 - (idle - idle_time) / (total - total_time)
		total_time = total
		idle_time = idle
		print('util = %.3f' %util)
		print()

update()
while True:
	time.sleep(1)
	update()
