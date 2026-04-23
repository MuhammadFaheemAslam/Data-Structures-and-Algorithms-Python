"""
random-pivot.py – Quick Sort with a Randomized Pivot

The fix for quick sort's O(n²) worst case: pick a RANDOM element as
the pivot instead of a fixed position. This makes the O(n²) case
require an adversarial input SPECIFICALLY TARGETING your randomness —
practically impossible for a fair RNG.

    Expected time:  O(n log n)      (probabilistic guarantee)
    Worst case:     O(n²)           (probability → 0 with good RNG)
    Space:          O(log n) expected recursion depth
    Stable:         No
    In place:       Yes

This is the version you'd actually ship. Everywhere. Python's
`list.sort()` happens to be Timsort rather than quicksort, but most
other languages' default sorts are some variant of this.

---------------------------------------------------
Two Common Randomization Strategies:

    1. Random pivot:
           pivot_idx = random.randint(lo, hi)
           swap arr[pivot_idx] and arr[hi]
       Simple; great in practice.

    2. Median-of-three:
           Take the median of arr[lo], arr[mid], arr[hi].
           Swap that median into arr[hi].
       Deterministic, but harder to adversarialize than a fixed pivot.
       Standard in many STL implementations.

    3. Median-of-medians (BFPRT):
           True O(n) worst-case pivot selection.
           Theoretically perfect but impractical — too much overhead.

This file implements options 1 and 2.

---------------------------------------------------
Why Randomization Matters:

Fixed-pivot quick sort's worst case is any SORTED input — arguably
the most common adversarial case in real data. A sorted file, a log
with timestamps, a pre-indexed database extract — all cause O(n²)
behaviour.

Random pivots make the worst case require specific inputs that can't
be produced without knowing the RNG seed. It's a strong practical
defense.

---------------------------------------------------
"""

import random


# =========================================================================
# Quick Sort with Random Pivot
# =========================================================================

def quick_sort_random(arr):
    """
    Sort `arr` in place using quick sort with random pivots.

    Expected time:  O(n log n)
    Expected space: O(log n) recursion depth
    Stable:         No
    """
    _quick_sort_random_range(arr, 0, len(arr) - 1)
    return arr


def _quick_sort_random_range(arr, lo, hi):
    if lo >= hi:
        return

    # Pick a random pivot and move it to the `hi` position before partitioning.
    pivot_index = random.randint(lo, hi)
    arr[pivot_index], arr[hi] = arr[hi], arr[pivot_index]

    # Now partition using Lomuto with arr[hi] as pivot.
    p = _partition_lomuto(arr, lo, hi)
    _quick_sort_random_range(arr, lo, p - 1)
    _quick_sort_random_range(arr, p + 1, hi)


def _partition_lomuto(arr, lo, hi):
    """Lomuto partition with arr[hi] as pivot."""
    pivot = arr[hi]
    i = lo - 1

    for j in range(lo, hi):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
    return i + 1


# =========================================================================
# Quick Sort with Median-of-Three Pivot
# =========================================================================

def quick_sort_median3(arr):
    """
    Quick sort with median-of-three pivot selection.

    Expected time:  O(n log n)
    Adversarial resistance: much better than fixed pivot, not as
    uniformly random, but DETERMINISTIC — which is valuable in
    reproducible-testing contexts.

    Before partitioning, examine arr[lo], arr[mid], arr[hi]. Move their
    MEDIAN into arr[hi] so Lomuto's last-element partition sees a
    decent pivot.
    """
    _quick_sort_median3_range(arr, 0, len(arr) - 1)
    return arr


def _quick_sort_median3_range(arr, lo, hi):
    if lo >= hi:
        return

    _move_median_to_hi(arr, lo, hi)
    p = _partition_lomuto(arr, lo, hi)
    _quick_sort_median3_range(arr, lo, p - 1)
    _quick_sort_median3_range(arr, p + 1, hi)


def _move_median_to_hi(arr, lo, hi):
    """Pick the median of arr[lo], arr[mid], arr[hi] and swap to arr[hi]."""
    mid = lo + (hi - lo) // 2
    # We want the median of the three; a simple way is to sort them in place.
    # After these three compare-swaps, arr[lo] ≤ arr[mid] ≤ arr[hi].
    if arr[lo] > arr[mid]:
        arr[lo], arr[mid] = arr[mid], arr[lo]
    if arr[lo] > arr[hi]:
        arr[lo], arr[hi] = arr[hi], arr[lo]
    if arr[mid] > arr[hi]:
        arr[mid], arr[hi] = arr[hi], arr[mid]
    # Now arr[mid] is the median. Move it to arr[hi] for Lomuto.
    arr[mid], arr[hi] = arr[hi], arr[mid]
    # Wait: we just moved the MAX (arr[hi]) to the middle, and the median
    # to arr[hi]. But arr[hi - 1] now is out of order — fix not needed
    # because Lomuto operates on the whole [lo, hi] range and will treat
    # arr[hi] as the pivot and rearrange everything else.


# =========================================================================
# Timing Demo — Showing That Randomization Fixes the Sorted-Input Worst Case
# =========================================================================

def _fixed_pivot_quick_sort(arr):
    """Last-element pivot version (from quick-sort.py). For timing comparison."""
    def sort(lo, hi):
        if lo >= hi:
            return
        p = _partition_lomuto(arr, lo, hi)
        sort(lo, p - 1)
        sort(p + 1, hi)

    # Bump recursion limit just for the demo — the fixed-pivot version will
    # need it on sorted inputs
    import sys
    sys.setrecursionlimit(50_000)
    sort(0, len(arr) - 1)
    return arr


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    arr = [10, 7, 8, 9, 1, 5]
    print(f"Input:  {arr}")

    # Random pivot
    mut = arr[:]
    quick_sort_random(mut)
    print(f"Sorted (random pivot):     {mut}")

    # Median-of-three
    mut = arr[:]
    quick_sort_median3(mut)
    print(f"Sorted (median-of-three):  {mut}")
    print()

    # Test cases — include inputs that would kill fixed-pivot versions
    test_cases = [
        [10, 7, 8, 9, 1, 5],
        [],
        [5],
        [1, 2, 3, 4, 5],                          # sorted — fixed pivot's worst case
        [5, 4, 3, 2, 1],                          # reverse sorted
        [3, 1, 3, 1, 3],                          # duplicates
        [0, -1, 2, -3, 4, -5],
        [7] * 100,                                # all equal — large
        list(range(200, 0, -1)),                   # large reverse
        list(range(200)),                          # large sorted
    ]

    random.seed(0)                                # deterministic for tests

    for i, data in enumerate(test_cases):
        expected = sorted(data)
        for fn in (quick_sort_random, quick_sort_median3):
            got = fn(data[:])
            assert got == expected, (
                f"Test {i+1} ({fn.__name__}) failed on len={len(data)}"
            )
        print(f"Test {i+1} passed: len={len(data)}")

    # Demonstrate the O(n²) avoidance — time comparison on a sorted input
    import time
    print()
    print("Timing on a SORTED input (fixed-pivot's worst case):")
    sorted_input = list(range(2000))

    t0 = time.time()
    quick_sort_random(sorted_input[:])
    t_random = time.time() - t0

    t0 = time.time()
    quick_sort_median3(sorted_input[:])
    t_median = time.time() - t0

    print(f"   quick_sort_random    (n=2000, sorted): {t_random:.4f}s  (~O(n log n))")
    print(f"   quick_sort_median3   (n=2000, sorted): {t_median:.4f}s")

    # For contrast — fixed pivot is much slower (and risks RecursionError).
    # We run only a small input to keep the demo safe.
    small_sorted = list(range(200))
    t0 = time.time()
    _fixed_pivot_quick_sort(small_sorted[:])
    t_fixed = time.time() - t0
    print(f"   fixed-pivot          (n=200 only):     {t_fixed:.4f}s "
          "(scales as O(n²) on this input)")

    # Stress test — 300 random arrays
    random.seed(42)
    for _ in range(300):
        n = random.randint(0, 80)
        data = [random.randint(-100, 100) for _ in range(n)]
        expected = sorted(data)
        for fn in (quick_sort_random, quick_sort_median3):
            assert fn(data[:]) == expected

    print("\nStress test: 300 random arrays — both variants matched sorted()")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Which Randomization Strategy?
    #
    #   - `random.randint`-based: uniformly random, strong adversarial
    #     resistance, requires PRNG state. Standard choice.
    #   - Median-of-three: deterministic, no RNG needed, STRONG on
    #     real-world data (where sorted / partially-sorted inputs
    #     are common). Slightly worse on pathological inputs than
    #     random pivot. Used by the C stdlib's qsort.
    #
    # In Python, random pivot is simplest and sufficient. For systems
    # code or when determinism matters, median-of-three.
    # ---------------------------------------------------------------
