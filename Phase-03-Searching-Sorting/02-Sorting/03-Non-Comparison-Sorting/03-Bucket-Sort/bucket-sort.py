"""
bucket-sort.py – Bucket Sort

A non-comparison sort that distributes elements into BUCKETS, sorts
each bucket (usually with insertion sort), and concatenates. When
the input is approximately uniformly distributed, bucket sort runs
in **O(n)** expected time.

---------------------------------------------------
Expected time:  O(n + k) where k = number of buckets (often k ≈ n)
Worst case:     O(n²) — if all elements land in one bucket
Space:          O(n + k)
Stable:         Yes, if each bucket is sorted stably

---------------------------------------------------
The Algorithm:

    1. Pick `k` buckets (typically k = n) and a function
       `bucket_index(x)` that maps each value to an integer bucket.
       For values uniformly distributed in [0, 1):
           bucket_index(x) = int(x * n)
    2. Distribute each element into its bucket.
    3. Sort each bucket (usually with insertion sort — each bucket is
       expected to hold O(1) elements on average).
    4. Concatenate the buckets in order.

---------------------------------------------------
Why It's O(n) Expected for Uniform Input:

With k = n buckets and n elements uniformly distributed, each bucket
has O(1) elements on average. Insertion-sorting an O(1)-size bucket
is O(1). Total work: O(n) distribution + n · O(1) sorting = O(n).

If all elements fall into the SAME bucket (worst case — highly
non-uniform input), bucket sort degenerates to O(n²) via the inner
insertion sort. Random pivot / shuffling doesn't help because bucket
sort's behaviour is determined by the input DISTRIBUTION, not a
partition decision.

---------------------------------------------------
Two Common Bucketing Strategies:

### Uniform distribution over [0, 1)

For floats in [0, 1):
    bucket_index(x) = min(int(x * n), n - 1)

### Range-based

For integers in [lo, hi]:
    bucket_index(x) = (x - lo) * k // (hi - lo + 1)

Any continuous range can be mapped linearly to k buckets.

---------------------------------------------------
Example:

    arr = [0.42, 0.32, 0.23, 0.52, 0.25, 0.47, 0.51]  (uniform in [0, 1))
    n=7 buckets — bucket_index(x) = int(x * 7):

    bucket[0]: []
    bucket[1]: [0.23, 0.25]          → insertion sort → [0.23, 0.25]
    bucket[2]: [0.32]
    bucket[3]: [0.42, 0.47]
    bucket[4]: []
    bucket[5]: []
    bucket[6]: [0.52, 0.51]          → insertion sort → [0.51, 0.52]

    Concatenated: [0.23, 0.25, 0.32, 0.42, 0.47, 0.51, 0.52]

---------------------------------------------------
"""

# =========================================================================
# Bucket Sort for Floats in [0, 1)
# =========================================================================

def bucket_sort(arr):
    """
    Sort an array of floats in [0, 1) via bucket sort.

    Expected time: O(n)  — for uniformly distributed input
    Worst case:    O(n²) — when all elements collide in one bucket
    Space:         O(n)
    Stable:        Yes
    """
    n = len(arr)
    if n <= 1:
        return list(arr)

    # Create n empty buckets
    buckets = [[] for _ in range(n)]

    # Distribute elements
    for x in arr:
        if not 0 <= x < 1:
            raise ValueError("bucket_sort expects floats in [0, 1); "
                             "use bucket_sort_range() for other ranges")
        idx = min(int(x * n), n - 1)              # clamp for x == 1.0 edge case
        buckets[idx].append(x)

    # Sort each bucket
    for b in buckets:
        _insertion_sort(b)

    # Concatenate
    result = []
    for b in buckets:
        result.extend(b)
    return result


# =========================================================================
# Bucket Sort for Any Numeric Range
# =========================================================================

def bucket_sort_range(arr, num_buckets=None):
    """
    Sort an array of numbers in ANY range via bucket sort.

    Expected time: O(n)  — for uniformly distributed input
    Worst case:    O(n²)
    Space:         O(n)

    By default `num_buckets = n`. Adjust if you know your data's
    distribution (e.g., heavily skewed → fewer buckets).
    """
    n = len(arr)
    if n <= 1:
        return list(arr)

    if num_buckets is None:
        num_buckets = n

    min_val = min(arr)
    max_val = max(arr)
    if min_val == max_val:
        return list(arr)                          # all equal — already sorted

    buckets = [[] for _ in range(num_buckets)]

    # Linear mapping from [min_val, max_val] to [0, num_buckets - 1]
    span = max_val - min_val
    for x in arr:
        # map x's position in [min_val, max_val] to a bucket index
        idx = int((x - min_val) / span * num_buckets)
        if idx == num_buckets:                    # x == max_val rounds up
            idx = num_buckets - 1
        buckets[idx].append(x)

    for b in buckets:
        _insertion_sort(b)

    result = []
    for b in buckets:
        result.extend(b)
    return result


# =========================================================================
# Inner Sort: Insertion Sort
# =========================================================================

def _insertion_sort(arr):
    """
    In-place insertion sort — used as the inner sort for each bucket.
    For O(1)-size buckets, insertion sort is optimal.

    Stable.
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
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    # Classic example — floats in [0, 1)
    arr = [0.42, 0.32, 0.23, 0.52, 0.25, 0.47, 0.51]
    print(f"Input:  {arr}")
    print(f"Sorted: {bucket_sort(arr)}")
    print()

    # Test cases for bucket_sort (floats in [0, 1))
    float_cases = [
        [0.42, 0.32, 0.23, 0.52, 0.25, 0.47, 0.51],
        [],
        [0.5],
        [0.1, 0.2, 0.3, 0.4, 0.5],                # sorted
        [0.9, 0.8, 0.7, 0.6, 0.5],                # reverse
        [0.5, 0.5, 0.5, 0.5],                     # all equal
        [0.0, 0.0, 0.0],                          # all zero
    ]

    for i, data in enumerate(float_cases):
        expected = sorted(data)
        got = bucket_sort(data[:])
        assert got == expected, f"Test {i+1} failed on {data}"
        print(f"Test {i+1} passed: {data} -> {got}")

    # Range-based version (any numeric range)
    print()
    print("bucket_sort_range (any numeric range):")
    range_cases = [
        [170, 45, 75, 90, 802, 24, 2, 66],
        [-5, -1, -3, 0, 2, 4, -2],
        [100, 100, 100],                          # all equal
        [],
        [1, 2, 3, 4, 5],
        [3.14, 2.71, 1.41, 1.73],
    ]
    for data in range_cases:
        expected = sorted(data)
        got = bucket_sort_range(data[:])
        assert got == expected, f"{data}: expected {expected}, got {got}"
        print(f"   {data} -> {got}")

    # Stability check — when keys repeat, order must be preserved
    pairs = [(0.5, "a"), (0.3, "b"), (0.5, "c"), (0.3, "d")]
    def bucket_sort_pairs(arr):
        n = len(arr)
        if n <= 1:
            return list(arr)
        buckets = [[] for _ in range(n)]
        for p in arr:
            idx = min(int(p[0] * n), n - 1)
            buckets[idx].append(p)
        for b in buckets:
            # stable insertion sort by first element
            for i in range(1, len(b)):
                key = b[i]
                j = i - 1
                while j >= 0 and b[j][0] > key[0]:
                    b[j + 1] = b[j]
                    j -= 1
                b[j + 1] = key
        result = []
        for b in buckets:
            result.extend(b)
        return result

    sorted_pairs = bucket_sort_pairs(pairs)
    expected_stable = [(0.3, "b"), (0.3, "d"), (0.5, "a"), (0.5, "c")]
    assert sorted_pairs == expected_stable, (
        f"Stability broken: {sorted_pairs}"
    )
    print(f"\nStability check passed: {sorted_pairs}")

    # Stress test — uniform random floats in [0, 1)
    import random
    random.seed(42)
    for _ in range(200):
        n = random.randint(0, 100)
        data = [random.random() for _ in range(n)]   # uniform in [0, 1)
        assert bucket_sort(data[:]) == sorted(data)

    # Stress test — arbitrary numeric range
    for _ in range(200):
        n = random.randint(0, 100)
        data = [random.uniform(-1000, 1000) for _ in range(n)]
        assert bucket_sort_range(data[:]) == sorted(data)

    print("\nStress test: 200 uniform + 200 arbitrary-range inputs matched sorted()")

    # Demonstration — bucket sort shines on UNIFORM data, struggles on SKEWED data
    import time
    n = 100_000

    random.seed(0)
    uniform = [random.random() for _ in range(n)]

    # Skewed: all values clustered near 0
    skewed = [random.random() * 0.01 for _ in range(n)]

    t0 = time.time()
    bucket_sort(uniform[:])
    t_uniform = time.time() - t0

    t0 = time.time()
    bucket_sort(skewed[:])
    t_skewed = time.time() - t0

    print()
    print(f"Timing on n={n}:")
    print(f"   uniform distribution:  {t_uniform:.3f}s  (expected O(n))")
    print(f"   skewed to one bucket:  {t_skewed:.3f}s  (approaches O(n²))")
    print()
    print("Bucket sort's speedup is entirely about the INPUT DISTRIBUTION.")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # When Bucket Sort Wins:
    #
    #   - Values are UNIFORMLY DISTRIBUTED in a known range.
    #   - You can cheaply compute a good bucket index per element.
    #   - Large n, and you benefit from O(n) expected time.
    #
    # Where bucket sort appears in the wild:
    #   - Sorting floats (e.g., sorted random samples).
    #   - Postal sorting (ZIP codes have a known range).
    #   - Histogram binning (which is essentially half of bucket sort).
    #
    # In Python specifically, Python's built-in sorted() is so
    # fast that bucket sort rarely wins in practice. Its value is
    # ALGORITHMIC — understanding that O(n) sorting IS possible when
    # the input has exploitable structure.
    # ---------------------------------------------------------------
