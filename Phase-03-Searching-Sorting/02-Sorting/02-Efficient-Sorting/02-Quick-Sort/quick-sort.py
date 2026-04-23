"""
quick-sort.py – Quick Sort (Classical Lomuto Partition)

Quick Sort is the algorithm most real-world non-stable sorts are built
on. In practice it beats merge sort by a constant factor despite
having the same O(n log n) average case — its in-place partition is
very cache-friendly.

    Time:   O(n log n) average
            O(n²) worst case — with a fixed pivot, a sorted input is adversarial
    Space:  O(log n) for the recursion stack (in place beyond that)
    Stable: No — the partition can reorder equal elements
    In place: Yes

This file implements the CLASSICAL version with a Lomuto partition
and the LAST ELEMENT as the pivot. The random-pivot variant (the one
you'd actually ship) lives in random-pivot.py.

---------------------------------------------------
The Algorithm:

    def quick_sort(arr, lo, hi):
        if lo >= hi: return
        pivot_index = partition(arr, lo, hi)
        quick_sort(arr, lo, pivot_index - 1)
        quick_sort(arr, pivot_index + 1, hi)

    def partition(arr, lo, hi):
        pivot = arr[hi]                         # Lomuto: last element is pivot
        i = lo - 1                              # boundary of "≤ pivot" region
        for j in range(lo, hi):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
        return i + 1

After partition:
    arr[lo .. pivot_index - 1]  ≤ pivot
    arr[pivot_index]            = pivot (in its final sorted position)
    arr[pivot_index + 1 .. hi]  > pivot

---------------------------------------------------
Why the Last-Element Pivot Is Bad:

On a SORTED input, the pivot is always the maximum, so one partition
is empty and the other has n - 1 elements. Recursion depth becomes
n, and total work is O(n²). The same disaster happens on
reverse-sorted input.

The fix is RANDOMIZED PIVOTS — see random-pivot.py. Always ship with
randomization; the fixed-pivot version exists only for teaching.

---------------------------------------------------
"""

# =========================================================================
# Classical Quick Sort — Lomuto Partition, Last-Element Pivot
# =========================================================================

def quick_sort(arr):
    """
    Sort `arr` in place using quick sort.

    Time:   O(n log n) average; O(n²) on sorted / reverse-sorted input
    Space:  O(log n) average recursion depth
    Stable: No
    """
    _quick_sort_range(arr, 0, len(arr) - 1)
    return arr


def _quick_sort_range(arr, lo, hi):
    """Recursive helper — sort arr[lo..hi] (inclusive)."""
    if lo >= hi:
        return

    pivot_index = _partition_lomuto(arr, lo, hi)
    _quick_sort_range(arr, lo, pivot_index - 1)
    _quick_sort_range(arr, pivot_index + 1, hi)


def _partition_lomuto(arr, lo, hi):
    """
    Lomuto partition: pivot is arr[hi].

    After the call:
        arr[lo .. return_value - 1]  ≤ pivot
        arr[return_value]            = pivot (final position)
        arr[return_value + 1 .. hi]  > pivot

    Returns the final index of the pivot.
    """
    pivot = arr[hi]
    i = lo - 1                                    # last index in the "≤ pivot" region

    for j in range(lo, hi):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    # place the pivot just after the "≤ pivot" region
    arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
    return i + 1


# =========================================================================
# Hoare Partition — An Alternative Partitioning Scheme
# =========================================================================

def quick_sort_hoare(arr):
    """
    Quick sort with HOARE partition instead of Lomuto.

    Hoare partitions by walking two pointers inward and swapping
    out-of-place pairs. It does fewer swaps on average than Lomuto —
    3x fewer in the worst case — so it's typically faster in practice.

    Downside: the partition boundary semantics are different (returns
    an index that is NOT the pivot's final position), which makes the
    recursion bounds trickier to get right.

    Time:   O(n log n) average
    Space:  O(log n)
    Stable: No
    """
    _quick_sort_hoare_range(arr, 0, len(arr) - 1)
    return arr


def _quick_sort_hoare_range(arr, lo, hi):
    if lo >= hi:
        return
    p = _partition_hoare(arr, lo, hi)
    _quick_sort_hoare_range(arr, lo, p)            # p is NOT the pivot's position
    _quick_sort_hoare_range(arr, p + 1, hi)


def _partition_hoare(arr, lo, hi):
    """
    Hoare partition. Pivot is arr[lo]. Returns an index p such that:

        arr[lo .. p]     are all ≤ pivot
        arr[p + 1 .. hi] are all ≥ pivot

    (Note: the pivot may NOT end up at position p.)
    """
    pivot = arr[lo]
    i = lo - 1
    j = hi + 1

    while True:
        # move `i` right until arr[i] >= pivot
        i += 1
        while arr[i] < pivot:
            i += 1

        # move `j` left until arr[j] <= pivot
        j -= 1
        while arr[j] > pivot:
            j -= 1

        if i >= j:
            return j

        arr[i], arr[j] = arr[j], arr[i]


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    arr = [10, 7, 8, 9, 1, 5]
    print(f"Input:  {arr}")
    mut = arr[:]
    quick_sort(mut)
    print(f"Sorted (Lomuto): {mut}")
    mut = arr[:]
    quick_sort_hoare(mut)
    print(f"Sorted (Hoare):  {mut}")
    print()

    # Test cases
    test_cases = [
        [10, 7, 8, 9, 1, 5],
        [],
        [5],
        [1, 2, 3, 4, 5],                          # WORST case for last-element pivot
        [5, 4, 3, 2, 1],                          # also bad for this variant
        [3, 1, 3, 1, 3],                          # duplicates
        [0, -1, 2, -3, 4, -5],
        [7] * 20,                                 # all equal — pathological for naïve quicksort
        list(range(100, 0, -1)),                   # large reverse
    ]

    for i, data in enumerate(test_cases):
        expected = sorted(data)
        for fn in (quick_sort, quick_sort_hoare):
            got = fn(data[:])
            assert got == expected, (
                f"Test {i+1} ({fn.__name__}) failed on {data}"
            )
        print(f"Test {i+1} passed: len={len(data)}")

    # Worst-case depth note — NOT enforced, just demonstrated:
    # this fixed-pivot version would hit O(n²) on the sorted input above
    # if n were ~10_000. With randomization (see random-pivot.py), it
    # doesn't. Python's default recursion limit may need bumping for
    # large reverse-sorted inputs.

    # Stress test — smaller n to avoid the recursion-depth trap
    import random
    random.seed(42)
    for _ in range(100):
        n = random.randint(0, 50)
        data = [random.randint(-100, 100) for _ in range(n)]
        expected = sorted(data)
        for fn in (quick_sort, quick_sort_hoare):
            assert fn(data[:]) == expected
    print("\nStress test: 100 random arrays — both Lomuto and Hoare versions match sorted()")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Lomuto vs Hoare:
    #
    #   Lomuto:
    #     - Simpler code, easier to verify by hand.
    #     - Does ~3× more swaps on average.
    #     - The returned index IS the pivot's final position.
    #
    #   Hoare:
    #     - More compact pointer-walk logic.
    #     - Fewer swaps — typically faster in practice.
    #     - The returned index is a BOUNDARY, not a pivot position.
    #
    #   Production-quality quicksort (C stdlib, Java's Arrays.sort for
    #   primitives) uses Hoare-style partitioning. For teaching,
    #   Lomuto is clearer.
    # ---------------------------------------------------------------
