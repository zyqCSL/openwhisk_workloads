import os
import sys
import subprocess
from pathlib import Path

top_dir = Path.cwd() / 'functions'

copies = 50

def register_copy_function(func_dir, func_prefix, func_src, image_prefix, copies, memory_mb):
    os.chdir(str(func_dir))
    for i in range(0, copies):
        cmd = 'wsk action create %s-%d %s --docker %s --web raw -i --memory %d' %(
            func_prefix, i, func_src, image_prefix, memory_mb)
        subprocess.call(cmd, shell=True)

# os.chdir(str(top_dir / 'chameleon'))
# cmd = 'wsk action create chameleon faas_chameleon.py --docker yz2297/chameleon_openwhisk --web raw -i --memory 256'
# subprocess.call(cmd, shell=True)
register_copy_function(func_dir = top_dir / 'chameleon', 
    func_prefix='chameleon', func_src='faas_chameleon.py',
    image_prefix='sailresearch/python3_openwhisk_unified', copies=copies, 
    memory_mb=256)

os.chdir(str(top_dir / 'float_operation'))
cmd = 'wsk action create float_op float_operation.py --docker sailresearch/python3_openwhisk_unified -i --memory 256'
subprocess.call(cmd, shell=True)

# os.chdir(str(top_dir / 'image_processing'))
# cmd = 'wsk action create image_process image_process.py --docker yz2297/python3_openwhisk --web raw -i --memory 512'
# subprocess.call(cmd, shell=True)
register_copy_function(func_dir = top_dir / 'image_processing', 
    func_prefix='image_process', func_src='image_process.py',
    image_prefix='sailresearch/python3_openwhisk_unified', copies=copies, 
    memory_mb=512)

# os.chdir(str(top_dir / 'linpack'))
# cmd = 'wsk action create linpack linpack.py --docker yz2297/python3_openwhisk --web raw --memory 512 -i'
# subprocess.call(cmd, shell=True)
register_copy_function(func_dir = top_dir / 'linpack', 
    func_prefix='linpack', func_src='linpack.py',
    image_prefix='sailresearch/python3_openwhisk_unified', copies=copies, 
    memory_mb=512)

# os.chdir(str(top_dir / 'matmult'))
# cmd = 'wsk action create matmult matmult.py --docker yz2297/python3_openwhisk --web raw --memory 512 -i'
# subprocess.call(cmd, shell=True)
register_copy_function(func_dir = top_dir / 'matmult', 
    func_prefix='matmult', func_src='matmult.py',
    image_prefix='sailresearch/python3_openwhisk_unified', copies=copies, 
    memory_mb=512)

# os.chdir(str(top_dir / 'pyaes'))
# cmd = 'wsk action create pyaes faas_pyaes.py --docker yz2297/pyaes_openwhisk --web raw -i --memory 256'
# subprocess.call(cmd, shell=True)
register_copy_function(func_dir = top_dir / 'pyaes', 
    func_prefix='pyaes', func_src='faas_pyaes.py',
    image_prefix='sailresearch/python3_openwhisk_unified', copies=copies, 
    memory_mb=256)

# os.chdir(str(top_dir / 'video_processing'))
# cmd = 'wsk action create video_process video_process.py --docker yz2297/video_process_openwhisk --web raw -i --memory 512'
# subprocess.call(cmd, shell=True)
register_copy_function(func_dir = top_dir / 'video_processing', 
    func_prefix='video_process', func_src='video_process.py',
    image_prefix='sailresearch/python3_openwhisk_unified', copies=copies, 
    memory_mb=512)

# os.chdir(str(top_dir / 'ml_inference' / 'logistic_regression_review'))
# cmd = 'wsk action create lr_review lr_review.py --docker yz2297/lr_review_openwhisk --web raw -i --memory 256'
# subprocess.call(cmd, shell=True)
register_copy_function(func_dir = top_dir / 'ml_inference' / 'logistic_regression_review', 
    func_prefix='lr_review', func_src='lr_review.py',
    image_prefix='sailresearch/python3_openwhisk_unified', copies=copies, 
    memory_mb=256)

# os.chdir(str(top_dir / 'ml_inference' / 'mobilenet'))
# cmd = 'wsk action create mobilenet mobilenet.py --docker yz2297/mobilenet_openwhisk --web raw -i --memory 1024'
# subprocess.call(cmd, shell=True)
register_copy_function(func_dir = top_dir / 'ml_inference' / 'mobilenet', 
    func_prefix='mobilenet', func_src='mobilenet.py',
    image_prefix='sailresearch/python3_openwhisk_unified', copies=copies, 
    memory_mb=1024)