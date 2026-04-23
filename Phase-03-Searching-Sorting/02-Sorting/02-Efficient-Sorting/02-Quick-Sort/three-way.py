"""
three-way.py – Three-Way Partition Quick Sort (Dutch National Flag)

Classical (2-way) quick sort partitions into:

    [ ≤ pivot ]  [ pivot ]  [ > pivot ]

On arrays with MANY DUPLICATES, this is wasteful — equal elements get
recursively re-sorted for no reason. Three-way partitioning:

    [ < pivot ]  [ = pivot ]  [ > pivot ]

skips the middle block entirely when recursing. On arrays where every
value appears many times, three-way partitioning is dramatically
faster — going from O(n log n) to **O(n · k)** where k is the number
of DISTINCT values (LinearTime when k is a constant!).

Named after the **Dutch National Flag Problem** (Dijkstra, 1976):
sort an array of only three values (red/white/blue) in one pass,
in place.

---------------------------------------------------
Time:     O(n log n) average, O(n · H) where H is the entropy of
          the value distribution. On arrays with many duplicates,
          approaches O(n).
Space:    O(log n) recursion depth.
Stable:   No.
In place: Yes.

---------------------------------------------------
The Algorithm (Dijkstra's Invariant):

Maintain three regions during the partition:

    arr[lo..lt - 1]    < pivot
    arr[lt..gt]        = pivot
    arr[gt + 1..hi]    > pivot
    arr[gt + 1..i - 1] is UNPROCESSED (shrinks each step)

Scan with pointer `i`. At each step:
    if arr[i] < pivot: swap with arr[lt]; lt += 1; i += 1
    elif arr[i] > pivot: swap with arr[gt]; gt -= 1 (do NOT advance i —
                         the swapped-in value is still unprocessed)
    else: i += 1 (it's already in the middle region)

After the scan, recurse on [lo, lt - 1] and [gt + 1, hi].

---------------------------------------------------
Example:

    arr = [3, 1, 3, 3, 7, 3, 5, 3]
    pivot = 3
    partition:
        [1] [3, 3, 3, 3, 3] [7, 5]
    recurse on [1] (sorted) and [7, 5] (sort to [5, 7])
    final: [1, 3, 3, 3, 3, 3, 5, 7]

Most elements were skipped — they're in the "equal" block and never
get re-sorted.

---------------------------------------------------
"""

import random


# =========================================================================
# Three-Way Partition Quick Sort (Dutch National Flag)
# =========================================================================

def quick_sort_three_way(arr):
    """
    In-place three-way partitioning quick sort.

    Time:   O(n log n) average; O(n) on arrays with O(1) distinct values
    Space:  O(log n) recursion depth
    Stable: No
    """
    _qs3_range(arr, 0, len(arr) - 1)
    return arr


def _qs3_range(arr, lo, hi):
    if lo >= hi:
        return

    # Use a random pivot to avoid O(n²) worst case on sorted inputs
    pivot_idx = random.randint(lo, hi)
    pivot = arr[pivot_idx]

    lt = lo                                       # arr[lo..lt-1] < pivot
    gt = hi                                       # arr[gt+1..hi] > pivot
    i = lo                                        # current scan position

    while i <= gt:
        if arr[i] < pivot:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1
            i += 1
        elif arr[i] > pivot:
            arr[gt], arr[i] = arr[i], arr[gt]
            gt -= 1
            # DON'T advance i — the swapped-in value is unprocessed
        else:
            i += 1

    # Now: arr[lo..lt-1] < pivot, arr[lt..gt] == pivot, arr[gt+1..hi] > pivot
    _qs3_range(arr, lo, lt - 1)
    _qs3_range(arr, gt + 1, hi)


# =========================================================================
# Dutch National Flag Problem (Standalone Function)
# =========================================================================

def dutch_national_flag(arr):
    """
    Sort an array containing only three distinct values (encoded as
    0, 1, 2) in one pass, in place.

    Time:   O(n)
    Space:  O(1)

    This is the "one-pass partition at pivot 1" version of three-way
    quicksort — no recursion needed when there are exactly 3 values.

    Used directly for LeetCode #75 "Sort Colors". See also
    problems/sort-colors.py.
    """
    lo = 0
    hi = len(arr) - 1
    i = 0

    while i <= hi:
        if arr[i] == 0:
            arr[lo], arr[i] = arr[i], arr[lo]
            lo += 1
            i += 1
        elif arr[i] == 2:
            arr[hi], arr[i] = arr[i], arr[hi]
            hi -= 1
            # don't advance i
        else:                                     # arr[i] == 1
            i += 1

    return arr


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    random.seed(0)

    # Classical sort
    arr = [3, 1, 3, 3, 7, 3, 5, 3]
    print(f"Input:  {arr}")
    quick_sort_three_way(arr)
    print(f"Sorted: {arr}")
    print()

    # Test cases
    test_cases = [
        [3, 1, 3, 3, 7, 3, 5, 3],
        [],
        [5],
        [1, 2, 3, 4, 5],                          # sorted
        [5, 4, 3, 2, 1],                          # reverse
        [3, 1, 3, 1, 3],                          # duplicates
        [7] * 50,                                 # all equal — this is where 3-way WINS
        [0, -1, 2, -3, 4, -5],
        list(range(100, 0, -1)),
    ]

    for i, data in enumerate(test_cases):
        expected = sorted(data)
        got = quick_sort_three_way(data[:])
        assert got == expected, f"Test {i+1} failed on len={len(data)}"
        print(f"Test {i+1} passed: len={len(data)}")

    # Dutch national flag
    print()
    print("Dutch National Flag (one-pass 3-way partition):")
    dnf_cases = [
        [2, 0, 2, 1, 1, 0],
        [2, 0, 1],
        [0, 1, 2],
        [1, 1, 1],
        [0, 0, 0],
        [2, 2, 2],
        [],
        [0, 2, 1, 2, 0, 1, 0, 2, 1, 0],
    ]
    for data in dnf_cases:
        got = dutch_national_flag(data[:])
        expected = sorted(data)
        assert got == expected
        print(f"   {data} -> {got}")

    # Benchmark — 3-way partitioning's headline advantage on duplicates
    import time

    def plain_quick_sort(arr):
        """Regular 2-way quick sort with random pivot for comparison."""
        def qs(lo, hi):
            if lo >= hi:
                return
            pivot = arr[random.randint(lo, hi)]
            i = lo - 1
            # Lomuto-like partition around `pivot`
            # Move pivot to hi first
            for k in range(lo, hi + 1):
                if arr[k] == pivot:
                    arr[k], arr[hi] = arr[hi], arr[k]
                    break
            for j in range(lo, hi):
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
            p = i + 1
            qs(lo, p - 1)
            qs(p + 1, hi)

        qs(0, len(arr) - 1)
        return arr

    print()
    print("Benchmark — array with many duplicates (n=3_000, 5 distinct values):")
    # Note: plain quicksort on a duplicate-heavy array hits its pathological
    # case (repeated pivots collapse to O(n²)); even at n=20k this blows
    # the default recursion limit. n=3k is enough to show the gap.
    data = [random.randint(0, 4) for _ in range(3_000)]

    import sys
    sys.setrecursionlimit(10_000)

    random.seed(1)
    t0 = time.time()
    quick_sort_three_way(data[:])
    t_3way = time.time() - t0

    random.seed(1)
    t0 = time.time()
    plain_quick_sort(data[:])
    t_plain = time.time() - t0

    print(f"   3-way:  {t_3way:.4f}s   (~O(n) with 5 distinct values)")
    print(f"   plain:  {t_plain:.4f}s   (~O(n²) on this adversarial input)")

    # Stress test
    random.seed(42)
    for _ in range(200):
        n = random.randint(0, 80)
        data = [random.randint(-5, 5) for _ in range(n)]   # lots of duplicates
        expected = sorted(data)
        assert quick_sort_three_way(data[:]) == expected
    print("\nStress test: 200 duplicate-heavy arrays matched sorted()")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # When to Use 3-Way Partitioning:
    #
    #   - Arrays with repeated values. THE classic case.
    #   - Logs, IDs, category data — anything with a bounded universe.
    #   - After a radix-like preprocessing step where many items
    #     share buckets.
    #
    # For unique or mostly-unique data, regular 2-way quicksort is
    # simpler and about as fast. The overhead of managing three
    # regions adds constant factor costs.
    # ---------------------------------------------------------------
