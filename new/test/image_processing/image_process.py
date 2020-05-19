from PIL import Image, ImageFilter
from time import time
import base64
import io
import os

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
    img_binary = base64.b64decode(params['image'])

    tempBuff = io.BytesIO()
    tempBuff.write(img_binary)
    tempBuff.flush()
    # tempBuff.seek(0) #need to jump back to the beginning before handing it off to PIL
    image = Image.open(tempBuff)
    if image.mode != 'RGB':
        image = image.convert('RGB')

    start = time()

    flip(image)
    rotate(image)
    filter(image)
    gray_scale(image)
    resize(image)

    lat = time() - start
    print(lat)

    ret_val = {}
    ret_val['latency'] = lat
    return ret_val

if __name__ == '__main__':
    img_dir = '../../../dataset/image_process_base64/'
    for img in os.listdir(img_dir):
        print(img)
        path = img_dir + img
        params = {}
        with open(path, 'rb') as f:
            params['image'] = f.read()
        main(params)

