import sys
import os
import subprocess
import argparse
from minio import Minio
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--minio-config', dest='minio_config', type=str, required=True)
# data_top_dir =  Path.home() / 'openwhisk_workloads' / 'openwhisk_locust' / 'faas_data'
data_top_dir =  Path.cwd() / '..' / 'openwhisk_locust' / 'faas_data'
image_dir = data_top_dir / 'image_process'
video_dir = data_top_dir / 'video_process'
# -----------------------------------------------------------------------
# parse args
# -----------------------------------------------------------------------
args = parser.parse_args()
minio_config_f = args.minio_config
with open(minio_config_f ,'r') as f:
    minio_config = json.load(f)
    endpoint = minio_config['endpoint']
    access_key = minio_config['access_key']
    secrete_key = minio_config['secret_key']

minio_client = Minio(endpoint=endpoint,
                     access_key=access_key,
                     secret_key=secrete_key,
                     secure=False)

bucket_name = "openwhisk"
found = minio_client.bucket_exists(bucket_name)
if not found:
    minio_client.make_bucket(bucket_name)
else:
    print("Bucket '%s' already exists" %bucket_name)

for img in os.listdir(str(image_dir)):
    img_path = image_dir / img
    minio_client.fput_object(bucket_name=bucket_name,
                       object_name=img,
                       file_path=str(img_path))

for vid in os.listdir(str(video_dir)):
    vid_path = video_dir / vid
    minio_client.fput_object(bucket_name=bucket_name,
                       object_name=vid,
                       file_path=str(vid_path))