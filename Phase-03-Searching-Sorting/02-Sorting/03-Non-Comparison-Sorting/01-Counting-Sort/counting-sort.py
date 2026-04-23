"""
counting-sort.py – Counting Sort

A NON-COMPARISON sort. Instead of comparing elements, it uses their
VALUES directly as indices into a count array. This lets it beat the
Ω(n log n) lower bound for comparison-based sorting — at the cost of
strict preconditions:

    - Keys must be INTEGERS (or easily mappable to integers).
    - The range of keys `k` must be O(n) — otherwise the counting
      array itself is too big.

---------------------------------------------------
Time:   O(n + k) where k = range of keys
Space:  O(n + k)
Stable: YES (with the proper implementation — see stable-counting.py)
In place: NO

When k = O(n), this is **O(n)** sorting — asymptotically faster than
any comparison-based sort. When k is very large (e.g., k = n²), the
algorithm degrades to O(n²) and you should use a different sort.

---------------------------------------------------
The Basic Algorithm (Non-Stable Version in This File):

    1. Count the occurrences of each value.
    2. Overwrite the input by emitting each value `count[v]` times
       in order of increasing v.

    counts = [0] * (max_val + 1)
    for x in arr:
        counts[x] += 1

    i = 0
    for v, c in enumerate(counts):
        for _ in range(c):
            arr[i] = v
            i += 1

This loses all original ordering — it's NOT stable by construction.
For a stable version that preserves satellite data associated with each
key, see `stable-counting.py`.

---------------------------------------------------
Example:

    arr = [4, 2, 2, 8, 3, 3, 1]
    counts: {1:1, 2:2, 3:2, 4:1, 8:1}
    output: [1, 2, 2, 3, 3, 4, 8]

---------------------------------------------------
Extensions Handled Here:

    1. counting_sort(arr)          — for non-negative integers
    2. counting_sort_range(arr)    — for any integer range including negatives
                                     (uses min(arr) as an offset)
    3. counting_sort_with_key(arr, key) — sort by a key function
"""

# =========================================================================
# 1. Basic Counting Sort (Non-Negative Integers Only)
# =========================================================================

def counting_sort(arr):
    """
    Sort an array of non-negative integers.

    Time:   O(n + k) where k = max(arr) + 1
    Space:  O(n + k)
    Stable: No (this basic version; see stable-counting.py for stable)

    Returns `arr` (mutated in place).
    """
    if not arr:
        return arr

    max_val = max(arr)
    if min(arr) < 0:
        raise ValueError("counting_sort requires non-negative integers; "
                         "use counting_sort_range() for arrays with negatives")

    counts = [0] * (max_val + 1)
    for x in arr:
        counts[x] += 1

    # write back in sorted order
    i = 0
    for value, count in enumerate(counts):
        for _ in range(count):
            arr[i] = value
            i += 1

    return arr


# =========================================================================
# 2. Counting Sort with Negative Numbers (Offset-Based)
# =========================================================================

def counting_sort_range(arr):
    """
    Counting sort for any integer range. Handles negatives by offsetting.

    Time:   O(n + k) where k = max(arr) - min(arr) + 1
    Space:  O(n + k)
    """
    if not arr:
        return arr

    min_val = min(arr)
    max_val = max(arr)
    range_size = max_val - min_val + 1

    counts = [0] * range_size
    for x in arr:
        counts[x - min_val] += 1

    i = 0
    for offset, count in enumerate(counts):
        for _ in range(count):
            arr[i] = offset + min_val
            i += 1

    return arr


# =========================================================================
# 3. Counting Sort with a Key Function
# =========================================================================

def counting_sort_with_key(arr, key):
    """
    Counting sort where the sort KEY is derived from each element via
    `key(x)`. The keys must be non-negative integers.

    This version is NOT stable — see stable-counting.py for a stable
    key-based version that preserves input order for equal keys.

    Time:   O(n + k) where k = max key + 1
    Space:  O(n + k)

    Returns a NEW sorted list (doesn't mutate input).
    """
    if not arr:
        return list(arr)

    max_key = max(key(x) for x in arr)
    buckets = [[] for _ in range(max_key + 1)]

    for x in arr:
        buckets[key(x)].append(x)

    result = []
    for bucket in buckets:
        result.extend(bucket)
    return result


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    arr = [4, 2, 2, 8, 3, 3, 1]
    print(f"Input:  {arr}")
    counting_sort(arr)
    print(f"Sorted: {arr}")
    print()

    # Test cases for each variant
    test_cases = [
        [4, 2, 2, 8, 3, 3, 1],
        [],
        [5],
        [1, 2, 3, 4, 5],                          # already sorted
        [5, 4, 3, 2, 1],                          # reverse sorted
        [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5],        # duplicates
        [7] * 20,                                 # all equal
        [0, 0, 0, 1],                             # with zero
    ]

    for i, data in enumerate(test_cases):
        expected = sorted(data)
        got = counting_sort(data[:])
        assert got == expected, f"Test {i+1} failed on {data}"
        # counting_sort_range should match too
        got2 = counting_sort_range(data[:])
        assert got2 == expected
        print(f"Test {i+1} passed: {data} -> {got}")

    # Negative numbers — only counting_sort_range works
    neg_cases = [
        [-3, -1, -4, -1, -5, -9, 2, 6, 5, 3, 5],
        [-5, -4, -3, -2, -1],
        [0, -1, 0, -2, 0],
    ]

    print()
    print("counting_sort_range (handles negatives):")
    for data in neg_cases:
        expected = sorted(data)
        got = counting_sort_range(data[:])
        assert got == expected
        print(f"   {data} -> {got}")

    # Key-based version
    print()
    print("counting_sort_with_key (sort pairs by second element):")
    pairs = [("a", 3), ("b", 1), ("c", 2), ("d", 1), ("e", 3)]
    sorted_pairs = counting_sort_with_key(pairs, key=lambda x: x[1])
    print(f"   input:  {pairs}")
    print(f"   sorted: {sorted_pairs}")
    assert [p[1] for p in sorted_pairs] == sorted(p[1] for p in pairs)

    # Stress test
    import random
    random.seed(42)
    for _ in range(200):
        n = random.randint(0, 100)
        # positive values for counting_sort
        data = [random.randint(0, 50) for _ in range(n)]
        assert counting_sort(data[:]) == sorted(data)

        # any range for counting_sort_range
        data = [random.randint(-50, 50) for _ in range(n)]
        assert counting_sort_range(data[:]) == sorted(data)

    print("\nStress test: 200 random inputs matched sorted()")

    # Performance demonstration — counting sort on a small-range input
    import time
    n = 100_000
    k = 100                                       # range is much smaller than n
    data = [random.randint(0, k - 1) for _ in range(n)]

    t0 = time.time()
    counting_sort(data[:])
    t_counting = time.time() - t0

    t0 = time.time()
    sorted(data)
    t_sorted = time.time() - t0

    print()
    print(f"Timing on n={n}, k={k} (k << n, counting sort wins):")
    print(f"   counting_sort:  {t_counting:.4f}s   (~O(n + k) = O(n))")
    print(f"   Python sorted:  {t_sorted:.4f}s      (Timsort in C — VERY fast constants)")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # When to Use Counting Sort:
    #
    #   - Small integer universe (k = O(n)).
    #   - Array has lots of duplicates — counting is cheap.
    #   - Building blocks for radix sort, where it's the inner loop.
    #
    # When NOT:
    #   - Keys are large / arbitrary integers (k >> n).
    #   - Keys are floats or strings (can't directly index an array).
    #   - You need stability (use stable-counting.py).
    # ---------------------------------------------------------------
