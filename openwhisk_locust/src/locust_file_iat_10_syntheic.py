# src files for calling all functions, including copied ones
import random
from locust import HttpUser, task, tag, between
import base64
import os
from pathlib import Path
import logging
import numpy as np
import time
import json

random.seed(time.time())

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# logging.basicConfig(level=logging.INFO,
#                     # filename='/mnt/locust_log/locust_openwhisk_log.txt',
#                     # filemode='w+',
#                     format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

logging.basicConfig(level=logging.INFO)

# minio config
minio_config = {}
minio_config_p = Path('/mnt/faas_data/minio_config.json')
with open(str(minio_config_p), 'r') as f:
    minio_config = json.load(f)
minio_endpoint = minio_config['endpoint']
minio_access_key = minio_config['access_key']
minio_secret_key = minio_config['secret_key']
minio_bucket = minio_config['bucket']

data_dir  = Path('/mnt/faas_data')    # for docker usage
image_dir = data_dir / 'image_process'
video_dir = data_dir / 'video_process'

image_names = []
for img in os.listdir(str(image_dir)):
    image_names.append(img)

video_names = []
for video in os.listdir(str(video_dir)):
    video_names.append(video)

# get through: wsk -i  property get --auth
auth_str = '23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP'
pwd_1, pwd_2 = auth_str.strip().split(':')
auth = (pwd_1, pwd_2)

mean_iat = 10  # seconds
intervals = np.random.exponential(scale=mean_iat, size=5000)

apps = 119

class OpenWhiskUser(HttpUser):
    # wait_time = between(5, 9)
    # return wait time in second
    def wait_time(self):
        global intervals
        global mean_iat
        return np.random.exponential(scale=mean_iat)
        # return random.choice(intervals)
        # self.last_wait_time += 1
        # return self.last_wait_time    

    @tag('pyaes')
    def pyaes(self):
        global apps
        params = {}
        # params['blocking'] = 'true'
        # params['result'] = 'true'

        url = '/api/v1/namespaces/_/actions/synthetic'
        function_id = random.randint(0, apps - 1)
        url += '-' + str(function_id)

        body = {}
        body['duration'] = random.randint(0, 1000)/100.0

        r = self.client.post(url, params=params,
            json=body, auth=auth, verify=False,
            name='/synthetic')

        if r.status_code > 202:
            logging.warning('synthetic resp.status = %d, text=%s' %(r.status_code,
                r.text))

        # try:
        #     aid = json.loads(r.text)['activationId']
        #     logging.info('aid--pyaes:%s' %aid)
        # except:
        #     logging.error('pyaes response json parsing error')

