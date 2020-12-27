# docker build -f Dockerfile -t test_video_process .
import cv2
from time import time
from minio import Minio
import io
import numpy as np
import os

def video_processing(video_name, video_path):
    result_file_path = '/tmp/output-'+ video_name

    video = cv2.VideoCapture(video_path)

    width = int(video.get(3))
    height = int(video.get(4))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(result_file_path, fourcc, 20.0, (width, height))

    start = time()
    while(video.isOpened()):
        ret, frame = video.read()

        if ret:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            is_success, buff = cv2.imencode(".jpg", gray_frame)
            io_buf = io.BytesIO(buff)
            gray_frame = cv2.imdecode(np.frombuffer(io_buf.getbuffer(), np.uint8), -1)
            out.write(gray_frame)
        else:
            break

    latency = time() - start

    video.release()
    out.release()
    return latency, result_file_path

def main():
    # endpoint = params['endpoint']
    # access_key = params['access_key']
    # secret_key = params['secret_key']
    # bucket = params['params']
    endpoint = '128.253.128.68:9001'
    access_key = '5VCTEQOQ0GR0NV1T67GN'
    secret_key = '8MBK5aJTR330V1sohz4n1i7W5Wv/jzahARNHUzi3'
    bucket = 'openwhisk'

    minio_client = Minio(endpoint=endpoint,
                     access_key=access_key,
                     secret_key=secret_key,
                     secure=False)
    found = minio_client.bucket_exists(bucket)
    if not found:
        print("Bucket '%s' does not exist" %bucket)
    
    video_dir = '/tmp/faas_data/video_process'

    for video_name in os.listdir(video_dir):
        video_path = '/tmp/' + video_name

        minio_client.fget_object(bucket_name=bucket,
                        object_name=video_name,
                        file_path=video_path)

        latency, _ = video_processing(video_name, video_path)

        ret_val = {}
        ret_val['latency'] = latency
        print('%s done' %video_name)

if __name__ == '__main__':
    main()