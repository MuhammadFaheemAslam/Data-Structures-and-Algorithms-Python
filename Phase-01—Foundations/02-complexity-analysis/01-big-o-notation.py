"""

This script demonstrates common Big O time complexities with simple Python functions.
Each function performs an operation that scales in a specific way with input size n.
We also measure and print the execution time for different n to visualize growth.
"""

import time
import math

# -------------------- O(1) - Constant Time --------------------
def constant_time_example(arr):
    """
    Returns the first element of the list.
    No matter how large the list, this takes the same time.
    """
    return arr[0]

# -------------------- O(log n) - Logarithmic Time --------------------
def logarithmic_time_example(n):
    """
    Counts how many times we can divide n by 2 until it becomes 0.
    This is a classic O(log n) operation.
    """
    count = 0
    i = n
    while i > 0:
        i //= 2
        count += 1
    return count

# -------------------- O(n) - Linear Time --------------------
def linear_time_example(arr):
    """
    Computes the sum of all elements in the list.
    Must visit each element once -> O(n).
    """
    total = 0
    for x in arr:
        total += x
    return total

# -------------------- O(n log n) - Linearithmic Time --------------------
def linearithmic_time_example(n):
    """
    Performs an O(n log n) operation: outer loop n times, inner loop log n times.
    """
    total = 0
    for i in range(n):                # n iterations
        j = n
        while j > 0:                   # log n iterations
            total += i * j
            j //= 2
    return total

# -------------------- O(n²) - Quadratic Time --------------------
def quadratic_time_example(arr):
    """
    Counts pairs (i, j) where i < j. Nested loops over n elements -> O(n²).
    """
    n = len(arr)
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] + arr[j] == 0:   # some dummy condition
                count += 1
    return count

# -------------------- Helper to time a function --------------------
def time_function(func, *args, repeats=3):
    """
    Runs func(*args) `repeats` times and returns the average time in seconds.
    """
    total_time = 0
    for _ in range(repeats):
        start = time.perf_counter()
        func(*args)
        end = time.perf_counter()
        total_time += (end - start)
    return total_time / repeats

# -------------------- Demonstration --------------------
if __name__ == "__main__":
    print("Big O Notation Demonstration\n")

    # Different input sizes to test
    sizes = [10, 100, 1000, 10000, 100000]

    print("Note: Times are approximate and may vary between runs.\n")

    # O(1) test
    print("O(1) - Constant Time (first element access)")
    for n in sizes:
        arr = list(range(n))
        t = time_function(constant_time_example, arr)
        print(f"  n = {n:6d} -> {t:.8f} sec")
    print()

    # O(log n) test
    print("O(log n) - Logarithmic Time (count divisions by 2)")
    for n in sizes:
        t = time_function(logarithmic_time_example, n)
        print(f"  n = {n:6d} -> {t:.8f} sec")
    print()

    # O(n) test
    print("O(n) - Linear Time (sum of list)")
    for n in sizes:
        arr = list(range(n))
        t = time_function(linear_time_example, arr)
        print(f"  n = {n:6d} -> {t:.8f} sec")
    print()

    # O(n log n) test
    print("O(n log n) - Linearithmic Time (nested loops with halving)")
    # Use smaller sizes because O(n log n) grows faster
    for n in [10, 100, 1000, 2000, 11000]:
        t = time_function(linearithmic_time_example, n)
        print(f"  n = {n:6d} -> {t:.8f} sec")
    print()

    # O(n²) test
    print("O(n²) - Quadratic Time (nested loops)")
    # Use much smaller sizes to avoid extremely long runs
    for n in [10, 50, 100, 200, 400, 1000]:
        arr = list(range(n))
        t = time_function(quadratic_time_example, arr)
        print(f"  n = {n:6d} -> {t:.8f} sec")
    print()

    print("Observation: As n increases, the runtime grows according to its Big O class.")