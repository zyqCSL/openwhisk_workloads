python3 ./profile_function.py --min-users 1 --max-users 5 --user-step 1 --profile-users 2 --function video_process --iat 1
python3 ./profile_function.py --min-users 5 --max-users 40 --user-step 5 --profile-users 10 --function image_process --iat 1
python3 ./profile_function.py --min-users 2 --max-users 12 --user-step 2 --profile-users 4 --function mobilenet --iat 1
python3 ./profile_function.py --min-users 1 --max-users 7 --user-step 1 --profile-users 2 --function linpack --iat 1
python3 ./profile_function.py --min-users 10 --max-users 80 --user-step 10 --profile-users 10 --function matmult --iat 1
python3 ./profile_function.py --min-users 2 --max-users 10 --user-step 2 --profile-users 4 --function pyaes --iat 1
python3 ./profile_function.py --min-users 2 --max-users 12 --user-step 2 --profile-users 4 --function float_op --iat 1
python3 ./profile_function.py --min-users 1 --max-users 6 --user-step 1 --profile-users 2 --function lr_review --iat 1