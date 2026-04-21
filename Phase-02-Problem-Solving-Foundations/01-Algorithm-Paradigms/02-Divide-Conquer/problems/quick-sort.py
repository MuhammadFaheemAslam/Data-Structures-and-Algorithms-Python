"""
Problem: Quick Sort

Paradigm: Divide & Conquer
Difficulty: Easy-Medium (foundational algorithm)

---------------------------------------------------
Problem Statement:

Sort an array of comparable values in ascending order.

---------------------------------------------------
The Divide & Conquer Lens:

Quicksort is a Divide & Conquer algorithm that is the mirror image of
merge sort. Where merge sort does its work in the COMBINE step, quicksort
does its work in the DIVIDE step, using a technique called "partitioning".

    Divide:  pick a pivot; partition the array into `< pivot` and `>= pivot`.
    Conquer: recursively sort each partition.
    Combine: NOTHING — the partitions are already in the right order.

Recurrence (average case with a good pivot):
    T(n) = 2 * T(n/2) + O(n)   →   O(n log n)

Worst case (consistently bad pivot — e.g., always the smallest element):
    T(n) = T(n-1) + O(n)       →   O(n²)

Key properties:
    - Average O(n log n), worst O(n²).  Randomization makes worst-case
      rare enough to ignore in practice.
    - In-place (O(log n) space for the recursion stack).
    - NOT stable — equal elements may get reordered.
    - Extremely cache-friendly in practice, often faster than merge sort
      on real hardware despite having the same Big-O.

---------------------------------------------------
The Pivot Problem:

Pivot choice determines everything. Strategies, from worst to best:

    1. Always pick first element
        - O(n²) on already-sorted input. NEVER ship this.
    2. Always pick middle element
        - Better, but still adversarial inputs exist.
    3. Random pivot
        - O(n log n) EXPECTED. No input can reliably defeat it.
    4. Median-of-three (first, middle, last — pick the median)
        - Strong constant factor, deterministic. What real libraries do.

We implement random pivot below (the interview-standard default).

---------------------------------------------------
Example:

    [38, 27, 43, 3, 9, 82, 10]
    -> [3, 9, 10, 27, 38, 43, 82]

---------------------------------------------------
"""

import random


# -------------------------------------------------
# The Quicksort Algorithm (Random Pivot, In-Place)
# -------------------------------------------------

def quick_sort(arr):
    """
    Sort `arr` in place using randomized quicksort.

    Time Complexity:  O(n log n) expected, O(n²) worst case
    Space Complexity: O(log n) expected for the call stack

    Returns `arr` (mutated) for convenience.
    """
    _quick_sort_helper(arr, 0, len(arr) - 1)
    return arr


def _quick_sort_helper(arr, lo, hi):
    if lo >= hi:
        return                                  # base case: 0 or 1 element

    # divide: partition around a random pivot
    pivot_index = _partition(arr, lo, hi)

    # conquer: sort the two partitions
    _quick_sort_helper(arr, lo, pivot_index - 1)
    _quick_sort_helper(arr, pivot_index + 1, hi)

    # combine: nothing to do — partitions are already in order


def _partition(arr, lo, hi):
    """
    Lomuto partition with a RANDOMIZED pivot.

    Randomization defends against adversarial inputs that would give
    worst-case O(n²) behaviour under a fixed pivot strategy.

    Returns the final index of the pivot element. After this call:
        arr[lo..pivot-1]  all <= arr[pivot]
        arr[pivot+1..hi]  all >  arr[pivot]
    """
    # random pivot → O(n log n) expected, regardless of input
    rand_index = random.randint(lo, hi)
    arr[rand_index], arr[hi] = arr[hi], arr[rand_index]

    pivot = arr[hi]
    i = lo - 1                                  # last index of elements <= pivot

    for j in range(lo, hi):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    # place the pivot just past the <= region
    arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
    return i + 1


# -------------------------------------------------
# Simpler "Textbook" Quicksort (Non-In-Place)
# -------------------------------------------------

def quick_sort_simple(arr):
    """
    The classic list-comprehension quicksort: short, readable, and a
    useful teaching tool — but NOT in place and with worse constants.

    Time Complexity:  O(n log n) average, O(n²) worst case
    Space Complexity: O(n log n) — builds new lists at each level

    Good for interviews where correctness and clarity matter more than
    memory efficiency. For production, use the in-place version.
    """
    if len(arr) <= 1:
        return arr[:]                           # copy, not alias

    pivot = arr[random.randint(0, len(arr) - 1)]
    less    = [x for x in arr if x <  pivot]
    equal   = [x for x in arr if x == pivot]
    greater = [x for x in arr if x >  pivot]

    return quick_sort_simple(less) + equal + quick_sort_simple(greater)


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    data = [38, 27, 43, 3, 9, 82, 10]

    # Note: quick_sort mutates; we pass a copy to show both values
    mutable = data[:]
    print(f"input:  {data}")
    print(f"quick_sort (in place): {quick_sort(mutable)}")
    print(f"quick_sort_simple:     {quick_sort_simple(data)}")
    print()

    # Test cases – covering the usual edge cases plus adversarial inputs
    test_cases = [
        [38, 27, 43, 3, 9, 82, 10],             # typical
        [],                                      # empty
        [5],                                     # single element
        [1, 2, 3, 4, 5],                         # already sorted (adversarial for fixed pivot)
        [5, 4, 3, 2, 1],                         # reverse sorted
        [3, 1, 3, 1, 3],                         # duplicates
        [0, -1, 2, -3, 4, -5],                   # negatives
        [7] * 20,                                # all equal (stress for partition)
        list(range(100, 0, -1)),                 # large descending
    ]

    # Seed for reproducibility of the randomized pivot
    random.seed(42)

    for i, data in enumerate(test_cases):
        expected = sorted(data)

        mutable = data[:]
        quick_sort(mutable)
        assert mutable == expected, (
            f"Test {i+1} (quick_sort) failed on {data}"
        )

        got_simple = quick_sort_simple(data)
        assert got_simple == expected, (
            f"Test {i+1} (quick_sort_simple) failed on {data}"
        )

        print(f"Test {i+1} passed: len={len(data)}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Merge Sort vs Quick Sort: When to Pick Which
    #
    #                Merge Sort              Quick Sort
    #   Average      O(n log n)              O(n log n)
    #   Worst        O(n log n)              O(n²)   ← pivot-dependent
    #   Space        O(n)  merge buffer       O(log n)  in-place
    #   Stable       Yes                     No
    #   Cache        Moderate                Excellent
    #   Use when     Need guarantees,        Speed on avg, memory matters,
    #                stability, external      stability not needed
    #                storage
    #
    # Python's built-in sort is Timsort — a merge-sort variant optimized
    # for real-world data (runs of pre-sorted data get O(n) detection).
    # ---------------------------------------------------------------
