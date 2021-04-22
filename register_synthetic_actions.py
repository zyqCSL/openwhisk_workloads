import os
import sys
import subprocess
from pathlib import Path

top_dir = Path.cwd() / 'functions'

apps = 119 # apps in the function trace

def register_copy_function(func_dir, func_prefix, func_src, image_prefix, apps, memory_mb):
    os.chdir(str(func_dir))
    for i in range(0, apps):
        cmd = 'wsk action create %s-%d %s --docker %s-%d --web raw -i --memory %d' %(
            func_prefix, i, func_src, image_prefix, i, memory_mb)
        subprocess.call(cmd, shell=True)

register_copy_function(func_dir = top_dir / 'synthetic', 
    func_prefix='synthetic', func_src='synthetic.py',
    image_prefix='sailresearch/synthetic_openwhisk', apps=apps, 
    memory_mb=256)

os.chdir(str(top_dir / 'synthetic'))
cmd = 'wsk action create synthetic synthetic.py --docker sailresearch/python3_openwhisk -i --memory 256'
subprocess.call(cmd, shell=True)