import cv2
from time import time
import base64
import io
import numpy as np

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

def main(params):
    video_binary = base64.b64decode(params['video'])
    video_name = params['video_name']
    video_path = '/tmp/' + video_name

    with open(video_path, 'wb+') as f:
        f.write(video_binary)

    latency, result_path = video_processing(video_name, video_path)

    ret_val = {}
    ret_val['latency'] = latency
    return ret_val