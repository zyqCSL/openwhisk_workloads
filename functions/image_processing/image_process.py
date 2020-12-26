from PIL import Image, ImageFilter
from time import time
import base64
import io
from minio import Minio

def flip(image):
    img_1 = image.transpose(Image.FLIP_LEFT_RIGHT)
    img_2 = image.transpose(Image.FLIP_TOP_BOTTOM)
    return [img_1, img_2]

def rotate(image):
    img_1 = image.transpose(Image.ROTATE_90)
    img_2 = image.transpose(Image.ROTATE_180)
    img_3 = image.transpose(Image.ROTATE_270)
    return [img_1, img_2, img_3]

def filter(image):
    img_1 = image.filter(ImageFilter.BLUR)
    img_2 = image.filter(ImageFilter.CONTOUR)
    img_3 = image.filter(ImageFilter.SHARPEN)
    return [img_1, img_2, img_3]

def gray_scale(image):
    img = image.convert('L')
    return img

def resize(image):
    img = image.thumbnail((128, 128))
    return img

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
    
    image_name = params['image']
    image_path = '/tmp/' + image_name

    minio_client.fget_object(bucket_name=bucket,
                       object_name=image_name,
                       file_path=image_path)
    # tempBuff.seek(0) #need to jump back to the beginning before handing it off to PIL
    image = Image.open(image_path)
    if image.mode != 'RGB':
        image = image.convert('RGB')

    start = time()
    flip(image)
    rotate(image)
    filter(image)
    gray_scale(image)
    resize(image)
    lat = time() - start

    ret_val = {}
    ret_val['latency'] = lat
    return ret_val
