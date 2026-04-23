"""
quick-select.py – Quickselect (kth Smallest Element in Expected O(n))

Quickselect is quick sort applied to a SELECTION problem rather than
a sort. Given an array and an integer k, find the k-th smallest
element (or equivalently: the value that WOULD be at index k if the
array were sorted).

    Time (expected):  O(n)        — amazing for a selection problem
    Time (worst):     O(n²)       — same pathology as quicksort
    Space:            O(log n) recursion
    In place:         Yes

The trick: after partitioning with a random pivot, we know exactly
where the pivot ends up. If that position == k, we're done. Otherwise,
we recurse into ONLY ONE side — the one containing the k-th slot.

---------------------------------------------------
Why Only ONE Side = O(n) Expected:

In quick sort, we recurse on BOTH sides:
    T(n) = 2·T(n/2) + O(n)  →  O(n log n)

In quickselect, we recurse on ONE side:
    T(n) = T(n/2) + O(n)    →  O(n)

(Geometric series: n + n/2 + n/4 + … = 2n.)

Same partitioning, half the recursion — linear expected time. The
worst case is still O(n²) if the pivot choices are consistently bad;
randomization prevents that with high probability.

---------------------------------------------------
Applications:

    - **Find the median** of an array without sorting it (k = n // 2).
    - **Top-k elements** (LC #215 "Kth Largest Element in an Array").
    - **Quantile statistics** on streams too large to sort in full.
    - Inner routine of introsort and pdqsort (which use a tighter
      median-of-medians for guaranteed O(n)).

---------------------------------------------------
The Algorithm:

    def quickselect(arr, k):
        lo, hi = 0, len(arr) - 1
        while lo < hi:
            p = partition(arr, lo, hi)        # random pivot
            if p == k: return arr[k]
            if p < k: lo = p + 1              # k is in the right half
            else:     hi = p - 1              # k is in the left half
        return arr[lo]

Note: this iterative version uses O(1) extra space (no recursion stack).

---------------------------------------------------
Example:

    arr = [7, 10, 4, 3, 20, 15], k = 3  (0-indexed: 4th smallest)
    sorted would be [3, 4, 7, 10, 15, 20]
    arr[3] in sorted order = 10  → answer: 10

---------------------------------------------------
"""

import random


# =========================================================================
# Quickselect — Iterative
# =========================================================================

def quickselect(arr, k):
    """
    Return the k-th smallest element of `arr` (0-indexed k).

    Expected time:  O(n)
    Worst case:     O(n²)
    Space:          O(1) — iterative
    Mutates:        arr is partitioned in place as a side-effect
    """
    if not 0 <= k < len(arr):
        raise IndexError(f"k={k} out of range for arr of length {len(arr)}")

    lo, hi = 0, len(arr) - 1

    while lo < hi:
        p = _partition(arr, lo, hi)

        if p == k:
            return arr[k]
        elif p < k:
            lo = p + 1
        else:
            hi = p - 1

    return arr[lo]                                # lo == hi, we're at index k


def _partition(arr, lo, hi):
    """
    Random-pivot Lomuto partition.

    Picks a random pivot, moves it to position `hi`, partitions so that
    arr[lo..p-1] ≤ pivot ≤ arr[p+1..hi], returns p.
    """
    # Random pivot — critical for expected O(n)
    pivot_idx = random.randint(lo, hi)
    arr[pivot_idx], arr[hi] = arr[hi], arr[pivot_idx]

    pivot = arr[hi]
    i = lo - 1
    for j in range(lo, hi):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
    return i + 1


# =========================================================================
# Convenience: find median / kth-largest
# =========================================================================

def find_median(arr):
    """
    Return the median of `arr` in expected O(n).

    For odd n: the middle element.
    For even n: the average of the two middle elements.

    Note: this mutates `arr` (partial sort due to partitioning).
    """
    n = len(arr)
    if n == 0:
        raise ValueError("find_median requires a non-empty array")

    if n % 2 == 1:
        return quickselect(arr[:], n // 2)
    else:
        lo = quickselect(arr[:], n // 2 - 1)
        hi = quickselect(arr[:], n // 2)
        return (lo + hi) / 2


def kth_largest(arr, k):
    """
    Return the k-th LARGEST element (1-indexed, LC-style).

    Equivalent to finding the (n - k)-th smallest.

    Expected time: O(n)
    """
    return quickselect(arr[:], len(arr) - k)


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    random.seed(0)                                # deterministic tests

    arr = [7, 10, 4, 3, 20, 15]
    print(f"arr = {arr}")
    print(f"sorted = {sorted(arr)}")
    print()
    for k in range(len(arr)):
        ans = quickselect(arr[:], k)
        print(f"   quickselect(arr, k={k}) = {ans}")

    print()
    print(f"find_median({arr}) = {find_median(arr[:])}")
    print(f"kth_largest({arr}, 2) = {kth_largest(arr, 2)}    (second largest)")
    print()

    # Test cases
    import random as rnd
    rnd.seed(42)

    # quickselect
    test_cases = [
        ([7, 10, 4, 3, 20, 15],      3,   10),
        ([3, 2, 1, 5, 6, 4],         1,   2),           # 2nd smallest
        ([1],                        0,   1),
        ([1, 2],                     0,   1),
        ([1, 2],                     1,   2),
        ([5, 5, 5, 5, 5],            2,   5),           # all equal
        ([-1, -5, 3, 2, 0],          2,   0),
        (list(range(100, 0, -1)),    49,  50),           # reverse-sorted
    ]

    for i, (data, k, expected) in enumerate(test_cases):
        got = quickselect(data[:], k)
        assert got == expected, f"Test {i+1}: arr={data}, k={k}: expected {expected}, got {got}"
        print(f"Test {i+1} passed: quickselect(len={len(data)}, k={k}) = {got}")

    # median
    print()
    med_cases = [
        ([1, 2, 3, 4, 5],      3),                       # odd, middle
        ([1, 2, 3, 4],         2.5),                     # even, avg of 2,3
        ([5],                  5),
        ([5, 3],               4),                        # avg of 3, 5
        ([-1, -2, -3, -4, -5], -3),
    ]
    for data, expected in med_cases:
        got = find_median(data[:])
        assert got == expected, f"median({data}): expected {expected}, got {got}"
        print(f"   find_median({data}) = {got}")

    # Stress test — compare quickselect's answer with sorted(arr)[k]
    rnd.seed(9)
    for _ in range(300):
        n = rnd.randint(1, 100)
        data = [rnd.randint(-100, 100) for _ in range(n)]
        k = rnd.randint(0, n - 1)
        expected = sorted(data)[k]
        got = quickselect(data[:], k)
        assert got == expected, f"stress: arr={data}, k={k}: {got} vs {expected}"

    print("\nStress test: 300 random queries matched sorted()[k]")

    # Timing demo — quickselect vs full sort
    import time

    big = [rnd.randint(0, 1_000_000) for _ in range(100_000)]
    k = 50_000

    t0 = time.time()
    got1 = quickselect(big[:], k)
    t_qs = time.time() - t0

    t0 = time.time()
    got2 = sorted(big)[k]
    t_sort = time.time() - t0

    assert got1 == got2
    print()
    print(f"Timing on n=100_000:")
    print(f"   quickselect:  {t_qs:.4f}s  (expected O(n))")
    print(f"   full sort:    {t_sort:.4f}s  (O(n log n))")
    # Note: Python's sorted() is implemented in C and extremely fast —
    # it often beats pure-Python quickselect on small-to-medium n despite
    # the worse Big-O. This is a Python-specific constant-factor effect.

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Related Algorithms:
    #
    #   - **Median of medians (BFPRT):** guarantees O(n) worst case
    #     (not just expected). More complex, larger constants —
    #     theoretically important but rarely used in practice.
    #
    #   - **Heap-based selection:** maintain a heap of size k. O(n log k).
    #     Worse Big-O than quickselect, but SIMPLER and stable performance.
    #     See Phase-03 / 03 / 03-Heap-Sort / problems / k-largest.py.
    #
    # For single-shot k-th element queries on unsorted data, quickselect
    # is the default. For streaming / repeated queries, heap-based is
    # more flexible.
    # ---------------------------------------------------------------
