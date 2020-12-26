import sys
import os
import json

minio_config = {}
minio_config['endpoint'] = '128.253.128.68:9001' # ath-5
minio_config['access_key'] = '5VCTEQOQ0GR0NV1T67GN'
minio_config['secret_key'] = '8MBK5aJTR330V1sohz4n1i7W5Wv/jzahARNHUzi3'
minio_config['bucket'] = 'openwhisk'

with open('./minion_config.json', 'w+') as f:
    json.dump(minio_config, f, indent=4, sort_keys=True)