import numpy as np
import numpy as np
import tensorflow as tf
import time
import base64

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
    img_binary = base64.b64decode(params['image'])
    img_format = params['format']
    img_path = '/tmp/img.' + img_format
    with open(img_path, 'wb+') as f:
        f.write(img_binary)        
    return predict(img_path)