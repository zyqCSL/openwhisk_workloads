import numpy as np
import numpy as np
import tensorflow as tf
import time
import base64
import os

def predict(img_path):
    start = time.time()
    img = tf.keras.preprocessing.image.load_img(img_path, target_size=[224, 224])
    x = tf.keras.preprocessing.image.img_to_array(img)
    x = tf.keras.applications.mobilenet.preprocess_input(x[tf.newaxis,...])
    pretrained_model = tf.keras.applications.MobileNet()
    result = pretrained_model(x)
    ret_val = {}
    ret_val['latency'] = time.time() - start
    return ret_val

def main():
    img_dir = '/tmp/image_process_base64/'
    for img_name in os.listdir(img_dir):
        if 'jpg' not in img_name:
            continue
        print(img_name)
        img_path = img_dir + img_name
        with open(img_path, 'r') as f:
            img_binary = base64.b64decode(f.read())
            temp_path = '/tmp/img.jpg'
            with open(temp_path, 'wb+') as ff:
                ff.write(img_binary)
            print(predict(temp_path))

if __name__ == '__main__':
    main()