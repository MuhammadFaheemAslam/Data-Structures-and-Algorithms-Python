"""
binary-insertion.py – Insertion Sort with Binary Search

A variant of insertion sort that uses BINARY SEARCH to find the
correct insertion point, reducing comparisons from O(n) to O(log n)
per element.

---------------------------------------------------
Time:   O(n log n) COMPARISONS, O(n²) MOVES
Space:  O(1)
Stable: Yes

The comparison count drops to O(n log n) — matching the theoretical
lower bound for comparison-based sorting. But the SHIFTS are still
O(n²): inserting at position k still requires shifting (n - k)
elements right.

So in Python (where shifts and comparisons cost about the same),
binary insertion sort is only a TINY improvement over regular
insertion sort.

Where it matters: when COMPARISONS are expensive (big objects,
deep object graphs, custom `__lt__`), binary insertion sort is a real
win. It's the insertion-point optimization inside production
Timsort for this reason.

---------------------------------------------------
The Algorithm:

    for i in range(1, n):
        key = arr[i]
        pos = bisect.bisect_left(arr, key, 0, i)  # binary search: O(log i)
        # shift arr[pos..i-1] one step right
        arr[pos + 1 : i + 1] = arr[pos : i]
        arr[pos] = key

---------------------------------------------------
"""

from bisect import bisect_left, insort


# =========================================================================
# Binary Insertion Sort — Explicit Shift
# =========================================================================

def binary_insertion_sort(arr):
    """
    Insertion sort with binary search for the insertion point.

    Time:   O(n log n) comparisons, O(n²) element moves.
    Space:  O(1)
    Stable: Yes — use bisect_LEFT so equal elements insert at the
            leftmost valid position (after the already-sorted equals
            that came earlier, preserving input order).

    Wait, that's backwards — to be stable we need NEW equals to land
    AFTER existing ones. That's bisect_RIGHT. See the note below.
    """
    for i in range(1, len(arr)):
        key = arr[i]
        # we want the new `key` to go AFTER any existing equals to
        # preserve stability → bisect_right, not bisect_left
        pos = _bisect_right_bounded(arr, key, 0, i)

        # shift arr[pos..i-1] one position to the right
        # Python lets us do this in one slice assignment — O(i - pos)
        arr[pos + 1 : i + 1] = arr[pos : i]
        arr[pos] = key

    return arr


def _bisect_right_bounded(arr, key, lo, hi):
    """
    bisect_right on a bounded range [lo, hi). Equivalent to the stdlib's
    bisect.bisect_right(arr, key, lo, hi). Inlined for self-containment.
    """
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] <= key:
            lo = mid + 1
        else:
            hi = mid
    return lo


# =========================================================================
# Using Python's Built-In bisect.insort (For Reference)
# =========================================================================

def binary_insertion_sort_builtin(arr):
    """
    Same algorithm using Python's bisect.insort — which internally does
    binary search + insert.

    Still O(n²) because insort's insertion into the middle of a list
    is O(n).
    """
    result = []
    for x in arr:
        insort(result, x)                         # binary search + insert
    # mutate `arr` to match `result` so the function contract matches
    arr[:] = result
    return arr


# =========================================================================
# Contrast: Regular Insertion Sort (For Comparison)
# =========================================================================

def insertion_sort(arr):
    """Regular insertion sort — same cost in Python."""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    arr = [5, 2, 4, 6, 1, 3]
    original = list(arr)
    binary_insertion_sort(arr)
    print(f"Input:  {original}")
    print(f"Sorted: {arr}")
    print()

    # Test cases
    test_cases = [
        [5, 2, 4, 6, 1, 3],
        [],
        [1],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5],
        [0, -1, 2, -3, 4, -5],
        [7, 7, 7, 7, 7],
    ]

    for i, data in enumerate(test_cases):
        expected = sorted(data)
        for fn in (binary_insertion_sort, binary_insertion_sort_builtin, insertion_sort):
            got = fn(list(data))
            assert got == expected, (
                f"Test {i+1} ({fn.__name__}) failed on {data}"
            )
        print(f"Test {i+1} passed: {data} -> {expected}")

    # Stability check
    pairs = [(1, "a"), (2, "b"), (1, "c"), (2, "d"), (1, "e")]
    def binary_insertion_sort_pairs(arr):
        arr = list(arr)
        for i in range(1, len(arr)):
            key = arr[i]
            # stable insertion for pairs by first element
            lo, hi = 0, i
            while lo < hi:
                mid = (lo + hi) // 2
                if arr[mid][0] <= key[0]:
                    lo = mid + 1
                else:
                    hi = mid
            arr[lo + 1 : i + 1] = arr[lo : i]
            arr[lo] = key
        return arr

    sorted_pairs = binary_insertion_sort_pairs(pairs)
    assert sorted_pairs == [(1, "a"), (1, "c"), (1, "e"), (2, "b"), (2, "d")]
    print(f"\nStability check passed: {sorted_pairs}")

    # Timing comparison — comparisons vs shifts
    import random
    import time

    random.seed(42)

    # For Python with int comparisons (cheap), both should be similar
    print("\nTiming comparison on random input (n=3000):")
    n = 3000
    data = [random.randint(0, 10000) for _ in range(n)]

    t0 = time.time()
    insertion_sort(list(data))
    t_regular = time.time() - t0

    t0 = time.time()
    binary_insertion_sort(list(data))
    t_binary = time.time() - t0

    print(f"   regular insertion sort:  {t_regular:.4f}s")
    print(f"   binary insertion sort:   {t_binary:.4f}s")
    print("   (both O(n²) in total work; comparisons cheap here, so similar.)")

    print("\nAll tests passed!")
