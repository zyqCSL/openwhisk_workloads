import sys
import os
import subprocess
from pathlib import Path

apps = 119

def copy_images(src, targ, apps):
    for i in range(0, apps):
        cmd = 'docker tag sailresearch/%s sailresearch/%s' %(src, targ + '-' + str(i))
        subprocess.run(cmd, shell=True)

        cmd = 'docker push sailresearch/%s' %(targ + '-' + str(i))
        subprocess.run(cmd, shell=True)

copy_images(src='python3_openwhisk', targ='synthetic_openwhisk', apps=apps)