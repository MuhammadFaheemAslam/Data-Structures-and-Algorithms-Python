"""
insertion-sort.py – Insertion Sort

Build the sorted array ONE element at a time. On each pass, take the
next unsorted element and INSERT it into its correct position among
the already-sorted prefix — shifting larger elements right to make room.

---------------------------------------------------
Time:   O(n) best (already sorted) — **ADAPTIVE**
        O(n²) average
        O(n²) worst (reverse sorted)
Space:  O(1)
Stable: Yes
Online: Yes — can sort a stream one element at a time
In place: Yes

Insertion sort is the BEST of the three O(n²) sorts:
    - Adaptive (fast on nearly-sorted input)
    - Stable
    - Online (handles streaming input)
    - Very small constant factors
    - USED IN PRODUCTION — as the "base case" inside Timsort (runs ≤ 32)
      and most other O(n log n) sorts.

This makes it genuinely useful, not just pedagogical.

---------------------------------------------------
The Algorithm:

    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]        # shift right
            j -= 1
        arr[j + 1] = key                # insert in place

At each iteration, the prefix arr[:i] is already sorted. We pull the
next element (arr[i]) out as `key` and shift back through the prefix,
moving elements right until we find key's correct spot.

---------------------------------------------------
Why Insertion Sort Is Used in Production (Timsort):

For small subarrays (n ≤ 32 or so), insertion sort is FASTER than
Merge Sort or Quick Sort despite the worse Big-O. Reasons:

    1. **Cache friendliness.** Insertion sort only touches adjacent
       memory; perfect for the cache.
    2. **No recursion overhead.** Important on tiny inputs.
    3. **Adaptive.** Partially sorted small runs finish in near O(n).
    4. **Stable.** Preserves order required for Timsort's correctness.

Python's `list.sort()`, Java's `Collections.sort()`, and most C++
STL implementations use insertion sort as the inner loop for small
partitions.

---------------------------------------------------
"""

# =========================================================================
# Insertion Sort — Classical (Shift-Based)
# =========================================================================

def insertion_sort(arr):
    """
    Standard insertion sort via shifting.

    Time:   O(n²) worst, O(n) best
    Space:  O(1)
    Stable: Yes (uses `>`, not `>=`, so equal elements don't shift)
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


# =========================================================================
# Insertion Sort — Swap-Based (Educational)
# =========================================================================

def insertion_sort_swap(arr):
    """
    Same algorithm via repeated ADJACENT SWAPS instead of shift + insert.

    Slightly worse constant factor (swaps touch two memory locations
    where shift touches one), but easier to explain: "walk the new
    element back through the sorted prefix, swapping with anything larger".

    Time:   O(n²) worst, O(n) best
    Space:  O(1)
    Stable: Yes
    """
    for i in range(1, len(arr)):
        j = i
        while j > 0 and arr[j - 1] > arr[j]:
            arr[j - 1], arr[j] = arr[j], arr[j - 1]
            j -= 1
    return arr


# =========================================================================
# Insertion Sort — Recursive (Educational)
# =========================================================================

def insertion_sort_recursive(arr, n=None):
    """
    Recursive formulation: sort the first n - 1 elements recursively,
    then insert arr[n - 1] into that sorted prefix.

    Time:   O(n²)
    Space:  O(n) for the call stack — doesn't beat the iterative version.

    Included to show the recursion structure, not for practical use.
    """
    if n is None:
        n = len(arr)

    if n <= 1:
        return arr

    insertion_sort_recursive(arr, n - 1)

    # insert arr[n - 1] into arr[:n - 1]
    key = arr[n - 1]
    j = n - 2
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
    insertion_sort(arr)
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
        for fn in (insertion_sort, insertion_sort_swap, insertion_sort_recursive):
            got = fn(list(data))
            assert got == expected, (
                f"Test {i+1} ({fn.__name__}) failed on {data}"
            )
        print(f"Test {i+1} passed: {data} -> {expected}")

    # Stability check
    pairs = [(1, "a"), (2, "b"), (1, "c"), (2, "d"), (1, "e")]
    def insertion_sort_pairs(arr):
        arr = list(arr)
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j][0] > key[0]:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr

    sorted_pairs = insertion_sort_pairs(pairs)
    assert sorted_pairs == [(1, "a"), (1, "c"), (1, "e"), (2, "b"), (2, "d")]
    print(f"\nStability check passed: {sorted_pairs}")

    # Timing — adaptive behaviour on nearly-sorted input
    print()
    print("Adaptive behaviour — insertion sort shines on nearly-sorted input:")
    import random, time

    n = 5000
    random.seed(0)

    # Completely random
    random_arr = [random.randint(0, 1000) for _ in range(n)]

    # Already sorted
    sorted_arr = list(range(n))

    # "Almost" sorted (swap 10 random pairs)
    almost_sorted = list(range(n))
    for _ in range(10):
        i, j = random.sample(range(n), 2)
        almost_sorted[i], almost_sorted[j] = almost_sorted[j], almost_sorted[i]

    for label, data in [("random", random_arr),
                        ("sorted (best case)", sorted_arr),
                        ("almost sorted", almost_sorted)]:
        t0 = time.time()
        insertion_sort(list(data))
        elapsed = time.time() - t0
        print(f"   {label:<20} n={n}: {elapsed:.4f}s")

    print("\n(Sorted and almost-sorted inputs are ~100x faster than random.)")

    # Stress test
    random.seed(42)
    for _ in range(200):
        n = random.randint(0, 40)
        data = [random.randint(-100, 100) for _ in range(n)]
        expected = sorted(data)
        assert insertion_sort(list(data)) == expected
    print("\nStress test: 200 random arrays matched sorted()")

    print("\nAll tests passed!")
