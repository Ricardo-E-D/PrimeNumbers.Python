from multiprocessing import Pool, Process
from threading import Thread
import time
import numpy as np


def calculate_primes(arr):
    for i, _ in enumerate(arr):
        for next in range(2, arr[i]):
            if (arr[i] % next) == 0:
                arr[i] = 0
                break
    return arr


def calculate_prime(num):
    if num > 2:
        for i in range(3, int(num ** 0.5) + 1,2):
            if (num % i) == 0:
                break
        else: 
            return num


def get_primes_sequential(arr):
    start = time.time()
    calculate_primes(arr)
    end = time.time()

    print("{:.4f}".format(end - start), "sec.")


def get_primes_threading(arr):
    split = 20
    threads = []
    newArr = np.array_split(arr, split)     # splitting the arr into equal chunks, and having each thread execute
                                            # their own arr[i]
    for i in range(split):
        threads.append(Thread(target=calculate_primes,args=([newArr[i].tolist()])))

    start = time.time()
    for t in threads:
        t.start()
    for i in threads:
        t.join()
    end = time.time()

    print("{:.4f}".format(end - start), "sec.")


def get_primes_processing(arr):
    start = time.time()
    with Pool(6) as p:
        p.map(calculate_prime,arr)
    end = time.time()

    print("{:.4f}".format(end - start), "sec.")


if __name__ == '__main__':
    size = 100000000 # Number of random numbers to add
    arr_seq = np.random.randint(1, 100, size).tolist()
    arr_thread = np.random.randint(1, 100, size).tolist()
    arr_mul_proc = np.random.randint(1, 100, size).tolist()

    get_primes_sequential(arr_seq)
    get_primes_threading(arr_thread)
    get_primes_processing(arr_mul_proc)

    # Observations:
    # array length             sequential           threading           multiprocessing
    #     1 000 000             0,628 sec.           0,614 sec.          0,472 sec.
    #    10 000 000             6,407 sec.           6,034 sec.          1,806 sec.
    #   100 000 000            56,810 sec.          58,225 sec.         11,760 sec.
    # 1 000 000 000                N/A                  N/A            165,897 sec.
