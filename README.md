# Usage

Before registering the functions, be sure to copy `wsk` (wsk_cli) to `/usr/local/bin`. 


- chameleon

	```bash
	wsk action create chameleon faas_chameleon.py --docker yz2297/chameleon_openwhisk --web raw -i --memory 1024
	wsk action invoke chameleon -i -p rows 5 -p cols 5 -r -v
	```

- floating point operation

	```bash
	wsk action create float_op float_operation.py -i 
	wsk action invoke float_op -i -p N 10 -r -v
	```

- Image processing

	```bash
	wsk action create image_process image_process.py --docker yz2297/python3_openwhisk --web raw -i
	```


- linpack

	```bash
	wsk action create linpack linpack.py --docker yz2297/python3_openwhisk --web raw --memory 1024 -i
	wsk action invoke linpack -i -p N 10 -r -v
	```

- matmult

	```bash
	wsk action create matmult matmult.py --docker yz2297/python3_openwhisk --web raw --memory 1024 -i
	wsk action invoke matmult -i -p N 10 -r -v
	```

- pyaes

	```bash
	wsk action create pyaes faas_pyaes.py --docker yz2297/pyaes_openwhisk --web raw -i
	wsk action invoke pyaes -i -p length 10 -p iteration 10 -r -v
	```

- video processing

	```bash
	wsk action create video_process video_process.py --docker yz2297/video_process_openwhisk --web raw -i
	```

- logistic regression review

	```bash
	wsk action create lr_review lr_review.py --docker yz2297/lr_review_openwhisk --web raw -i
	wsk action invoke lr_review -i -p text "Just fine" -r -v
	```

- mobilenet

	```bash
	wsk action create mobilenet mobilenet.py --docker yz2297/mobilenet_openwhisk --web raw -i
	```

