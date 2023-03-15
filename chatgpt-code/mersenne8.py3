#!/usr/bin/env python3
import numpy as np
from numba import cuda, int64, boolean
import sys

@cuda.jit(device=True)
def is_prime(n):
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

@cuda.jit("void(int64, int64, int64[:, ::1])")
def find_mersenne_prime_gpu(start_exponent, end_exponent, results):
    idx = cuda.grid(1)
    exponent = start_exponent + idx
    if exponent < end_exponent:
        candidate = 2 ** exponent - 1
        if is_prime(exponent) and is_prime(candidate):
            results[idx, 0] = exponent
            results[idx, 1] = candidate

def main():
    search_range = 10000
    start_exponent = 2

    threads_per_block = 256
    num_blocks = (search_range + threads_per_block - 1) // threads_per_block

    results_device = cuda.device_array((search_range, 2), dtype=np.int64)

    find_mersenne_prime_gpu[num_blocks, threads_per_block](start_exponent, start_exponent + search_range, results_device)

    results = results_device.copy_to_host()

    for prime_exponent, mersenne_prime in results:
        if prime_exponent > 0:
            print(f"Found Mersenne prime: 2^{prime_exponent} - 1 = {mersenne_prime}")

if __name__ == "__main__":
    main()
