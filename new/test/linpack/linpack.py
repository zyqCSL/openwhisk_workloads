from numpy import matrix, linalg, random, amax
from time import time

def linpack(N):
    eps = 2.22e-16

    ops = (2.0*N)*N*N/3.0+(2.0*N)*N

    # Create AxA array of random numbers -0.5 to 0.5
    A = random.random_sample((N, N))-0.5
    B = A.sum(axis=1)

    # Convert to matrices
    A = matrix(A)

    B = matrix(B.reshape((N, 1)))

    start = time()
    X = linalg.solve(A, B)
    latency = time() - start

    mflops = (ops*1e-6/latency)

    result = {
        'mflops': mflops,
        'latency': latency
    }

    return result

def main(params):
    N = params['N']
    ret_val = linpack(N)

    return ret_val

if __name__ == '__main__':
    params = {}
    params['N'] = 4500  #(3000-4500)
    print(main(params)['latency'])
