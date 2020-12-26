import sys
import os
import subprocess
import argparse
from minio import Minio
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--minio-config', dest='minio_config', type=str, required=True)
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
    print("Bucket '%s' does not exist" %bucket_name)
else:
    print("Bucket '%s' already exists" %bucket_name)
    print(minio_client.list_objects(bucket_name=bucket_name))
