docker run -v $PWD/src:/mnt/locust -v $PWD/faas_data:/mnt/faas_data \
	-v $PWD/minio_config.json:/mnt/minio_config.json \
	-v $HOME/openwhisk_locust_log:/mnt/locust_log sailresearch/locust_openwhisk \
	-f /mnt/locust/locust_file_iat_10_all.py \
	--csv=/mnt/locust_log/mixed --headless -t $1 \
	--host https://172.17.0.1 --users $2 \
	--logfile /mnt/locust_log/locust_openwhisk_log.txt