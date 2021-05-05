import os
import sys
import subprocess
from pathlib import Path

top_dir = Path.cwd() / 'functions'

apps = 119 # apps in the function trace

def unregister_copy_function(func_prefix, copies):
    for i in range(0, copies):
        cmd = 'wsk -i action delete %s-%d' %(
            func_prefix, i)
        subprocess.call(cmd, shell=True)

unregister_copy_function(func_prefix = 'synthetic', 
    copies=apps)