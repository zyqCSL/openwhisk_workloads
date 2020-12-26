docker run -v $PWD/src:/mnt/locust -v $PWD/faas_data:/mnt/faas_data -v $HOME/openwhisk_locust_log:/mnt/locust_log sailresearch/locust_openwhisk \
	-f /mnt/locust/locust_file_iat_1.py \
	--csv=/mnt/locust_log/$3 --headless -t $1 \
	--host https://172.17.0.1 --users $2 \
	--tags $3 --logfile /mnt/locust_log/locust_openwhisk_log.txt