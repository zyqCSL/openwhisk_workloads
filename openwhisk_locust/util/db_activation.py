import base64
import json
import subprocess
import sys

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# CrouchDB (from #OPENWHISK_DIR/ansible/db_local.ini)
DB_PROVIDER = 'CouchDB'
DB_USERNAME = 'yz2297'
DB_PASSWORD = 'openwhisk_couch'
DB_PROTOCOL = 'http'
DB_HOST = '128.253.128.68'
DB_PORT = '5984'

def get_activations(timestamp_since, limit=25):
    timestamp_milli = timestamp_since * 1000
    res = requests.post(url=DB_PROTOCOL + '://' + DB_HOST + ':' + DB_PORT + '/' + 'local_activations/_find',
                        json={
                            'selector': {
                                'start': {'$gt': timestamp_milli}
                            },
                            'limit': limit,
                            'execution_stats': True
                        },
                        auth=(DB_USERNAME, DB_PASSWORD))
    activations = json.loads(res.text)['docs']
    return activations

def get_activation_by_id(activation_id, namespace='guest'):
    url = DB_PROTOCOL + '://' + DB_HOST + ':' + DB_PORT + '/' + 'whisk_local_activations/' + \
        namespace + '%2F' + activation_id

    headers = {
        'Content-Type': 'application/json',
    }

    res = requests.get(url=url,
                        headers=headers,
                        auth=(DB_USERNAME, DB_PASSWORD))

    activation = json.loads(res.text)
    if 'duration' not in activation or 'annotations' not in activation:
        print("Incomplete activation")
        print(activation)
        return None

    return activation