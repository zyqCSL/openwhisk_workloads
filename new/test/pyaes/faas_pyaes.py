import string
import random
import pyaes
from time import time

def generate(length):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def main(params):
    length = int(params['length'])
    iteration = int(params['iteration'])

    message = generate(length)

    # 128-bit key (16 bytes)
    KEY = b'\xa1\xf6%\x8c\x87}_\xcd\x89dHE8\xbf\xc9,'

    start = time()
    for loops in range(iteration):
        aes = pyaes.AESModeOfOperationCTR(KEY)
        ciphertext = aes.encrypt(message)
        # print(ciphertext)

        aes = pyaes.AESModeOfOperationCTR(KEY)
        plaintext = aes.decrypt(ciphertext)
        # print(plaintext)
        aes = None

    latency = time() - start
    ret_val = {}
    ret_val['latency'] = latency

    return ret_val

if __name__ == '__main__':
    params = {}
    params['length'] = 3000 # (500-3000)
    params['iteration'] = 500 # (100-500)
    print(main(params)['latency'])