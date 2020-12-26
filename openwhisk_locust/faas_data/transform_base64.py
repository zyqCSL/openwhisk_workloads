import os
import sys
import base64

# src_dir = './image_process/'
# targ_dir = './image_process_base64/'

src_dir = './video_process/'
targ_dir = './video_process_base64/'

if __name__ == '__main__':
	if not os.path.isdir(targ_dir):
		os.makedirs(targ_dir)
	for img in os.listdir(src_dir):
		src_path = src_dir + img
		with open(src_path, 'rb') as f:
			b64_str = base64.b64encode(f.read())
		targ_path = targ_dir + 'b64_' + img
		with open(targ_path, 'wb+') as f:
			f.write(b64_str)
