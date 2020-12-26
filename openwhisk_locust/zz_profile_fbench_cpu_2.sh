python3 ./zz_profile_cpu_limit.py --min-cpus 1.0  --max-cpus 2.0  --cpus-step 0.25 --users 1 --function image_process --iat 1 --exp-time 180s
python3 ./zz_profile_cpu_limit.py --min-cpus 1.0  --max-cpus 1.5  --cpus-step 0.25 --users 1 --function pyaes         --iat 1 --exp-time 180s
python3 ./zz_profile_cpu_limit.py --min-cpus 6.0  --max-cpus 15.0 --cpus-step 3.0  --users 1 --function matmult       --iat 1 --exp-time 180s
python3 ./zz_profile_cpu_limit.py --min-cpus 0.5  --max-cpus 5.0  --cpus-step 0.5  --users 1 --function video_process --iat 1 --exp-time 180s