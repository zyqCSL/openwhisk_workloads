import numpy as np
import tensorflow as tf
import time
from minio import Minio

def predict(img_path):
    global pretrained_model

    start = time.time()
    img = tf.keras.preprocessing.image.load_img(img_path, target_size=[224, 224])
    x = tf.keras.preprocessing.image.img_to_array(img)
    x = tf.keras.applications.mobilenet.preprocess_input(x[tf.newaxis,...])
    pretrained_model = tf.keras.applications.MobileNet()
    result = pretrained_model(x)
    tf.keras.backend.clear_session()
    ret_val = {}
    ret_val['latency'] = time.time() - start
    return ret_val

def main(params):
    endpoint = params['endpoint']
    access_key = params['access_key']
    secret_key = params['secret_key']
    bucket = params['bucket']

    minio_client = Minio(endpoint=endpoint,
                     access_key=access_key,
                     secret_key=secret_key,
                     secure=False)
    found = minio_client.bucket_exists(bucket)
    if not found:
        print("Bucket '%s' does not exist" %bucket)

    img_name = params['image']
    img_path = '/tmp/' + img_name

    minio_client.fget_object(bucket_name=bucket,
                       object_name=img_name,
                       file_path=img_path)
     
    return predict(img_path)