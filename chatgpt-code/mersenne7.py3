#!/usr/bin/env python3
import concurrent.futures
import itertools
import math
import numpy as np
from numba import cuda, int64, boolean

@cuda.jit(device=True)
def is_prime_gpu(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

@cuda.jit
def find_mersenne_prime_gpu(start, end, results):
    idx = cuda.grid(1)
    if start + idx < end:
        p = start + idx
        if is_prime_gpu(p):
            mersenne_number = 2 ** p - 1
            if is_prime_gpu(mersenne_number):
                results[idx, 0] = p
                results[idx, 1] = mersenne_number

def main():
    start_exponent = 8191 + 1
    search_range = 1000000
    num_blocks = 100
    threads_per_block = 512

    results_device = cuda.device_array((search_range, 2), dtype=np.int64)

    find_mersenne_prime_gpu[num_blocks, threads_per_block](start_exponent, start_exponent + search_range, results_device)
    
    results = results_device.copy_to_host()
    
    for prime_exponent, mersenne_prime in results:
        if prime_exponent > 0:
            print(f"Found Mersenne prime: 2^{prime_exponent} - 1 = {mersenne_prime}")

if __name__ == "__main__":
    main()
