## Example Functions and Applications

We include a number of representative microbenchmarks a applications, which you could use in your studies. All of them have been successfully tested in OpenWhisk.

Here is a list of microbenchmarks:

Microbenchmark | Languages Provided
--- | --- 
base64 | [NodeJS, Python, Ruby, Swift] 
http-endpoint | [NodeJS, Python, Ruby, Swift] 
json | [NodeJS, Python, Ruby] 
primes | [NodeJS, Python, Ruby, Swift] 

And a list of applications:

Application | Description | Runtime
--- | --- | ---
autocomplete | Autocomplete a user string from a corpus | Runtime
img-resize | Resizes an image to several icons | NodeJS
markdown | Renders Markdown text to HTML | Python
ocr-img | Find text in user image using Tesseract OCR | NodeJS + binary
sentiment | Sentiment analysis of given text | Python

Register & Usage

In order to register serverless functions, be sure to copy wsk (wsk_cli) to /usr/local/bin. 

1. Autocomplete
	sudo npm link 
	Register: In autocomplete/bin, ./register_actions.js 

2. Img-resize
	Install dependencies in ./img-resize: npm install node-zip jimp --save 
	zip -r action.zip ./* 
	wsk action create img-resize --kind nodejs:8 action.zip --web raw -i 
 
	wsk action get img-resize --url -i  (get the URL that we want to curl) 
	curl -X POST -H "Content-Type: image/jpeg" --data-binary @./libertybell.jpg https://172.17.0.1/api/v1/web/guest/default/img-resize -k -v   
	(./liberty must be in directory) 

3. Markdown-to-html
	wsk action create markdown2html markdown2html.py --docker immortalfaas/markdown-to-html --web raw -i 
	wsk action invoke markdown2html -i -P openpiton-readme.json -r -v (input file must be base64) 

4. ocr-img (optical character recognition)
	wsk action create ocr-img handler.js --docker immortalfaas/nodejs-tesseract --web raw -i 
	wsk action get ocr-img --url -i  (get url to curl) 
	curl -X POST -H "Content-Type: image/png" --data-binary @./pitontable.png https://172.17.0.1/api/v1/web/guest/default/ocr-img -k -v 
	 
5. Sentiment analysis
	wsk action create sentiment sentiment.py --docker immortalfaas/sentiment --web raw -i 
 
	With input string 
		wsk action invoke sentiment -i -p "analyse" "delightful" -r -v 
	 
	With json file 
		wsk action invoke sentiment -i -P declaration.json -r -v 

6. Chameleon
	wsk action create chameleon faas_chameleon.py --docker yz2297/chameleon_openwhisk --web raw -i
	wsk action invoke sentiment -i -p rows 5 -p cols 5 --memory 1024 -r -v

7. Floating point operation
	wsk action create float_op float_operation.py -i 
	wsk action invoke float_op -i -p N 10 -r -v

8. Image processing
	wsk action create image_process image_process.py --docker yz2297/python3_openwhisk --web raw -i

9. linpack
	wsk action create linpack linpack.py --docker yz2297/python3_openwhisk --web raw --memory 1024 -i
	wsk action invoke linpack -i -p N 10 -r -v

10. matmult
	wsk action create matmult matmult.py --docker yz2297/python3_openwhisk --web raw --memory 1024 -i
	wsk action invoke matmult -i -p N 10 -r -v

11. pyaes
	wsk action create pyaes faas_pyaes.py --docker yz2297/pyaes_openwhisk --web raw -i
	wsk action invoke pyaes -i -p length 10 -p iteration 10 -r -v

12. video_processing
	wsk action create video_process video_process.py --docker yz2297/video_process_openwhisk --web raw -i

