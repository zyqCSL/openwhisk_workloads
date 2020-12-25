import sys
import os
import subprocess
from pathlib import Path

copies = 20

def change_image_org(img_name):
    cmd = 'docker pull  yz2297/%s:latest' %img_name
    subprocess.run(cmd, shell=True)

    cmd = 'docker tag yz2297/%s sailresearch/%s' %(img_name, img_name)
    subprocess.run(cmd, shell=True)

    cmd = 'docker push sailresearch/%s' %img_name
    subprocess.run(cmd, shell=True)

images = [
    'chameleon_openwhisk',
    'python3_openwhisk',
    'pyaes_openwhisk',
    'video_process_openwhisk',
    'lr_review_openwhisk',
    'mobilenet_openwhisk'
]

for img in images:
    change_image_org(img)

def copy_images(src, targ, copies):
    for i in range(0, copies):
        cmd = 'docker tag sailresearch/%s sailresearch/%s' %(src, targ + '-' + str(i))
        subprocess.run(cmd, shell=True)

        cmd = 'docker push sailresearch/%s' %(targ + '-' + str(i))
        subprocess.run(cmd, shell=True)

copy_images(src='chameleon_openwhisk', targ='chameleon_openwhisk', copies=copies)
copy_images(src='python3_openwhisk', targ='image_processing', copies=copies)
copy_images(src='python3_openwhisk', targ='matmult', copies=copies)
copy_images(src='python3_openwhisk', targ='linpack', copies=copies)
copy_images(src='pyaes_openwhisk', targ='pyaes_openwhisk', copies=copies)
copy_images(src='video_process_openwhisk', targ='video_process_openwhisk', copies=copies)
copy_images(src='lr_review_openwhisk', targ='lr_review_openwhisk', copies=copies)
copy_images(src='mobilenet_openwhisk', targ='mobilenet_openwhisk', copies=copies)