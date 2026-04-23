"""
implementation.py – Exponential Search (a.k.a. Galloping Search)

An O(log i) search on sorted arrays, where `i` is the position of the
target. Fast when the target is near the start of a LARGE array, and
the only viable option when the array's size is UNKNOWN (infinite /
streamed).

---------------------------------------------------
The Algorithm:

    1. Probe positions 1, 2, 4, 8, 16, ... (EXPONENTIALLY INCREASING).
    2. Stop at the first index whose value is >= target (or end of array).
    3. Binary-search the range [previous_probe, current_probe].

Concretely:

    if arr[0] == target: return 0

    bound = 1
    while bound < n and arr[bound] < target:
        bound *= 2              # exponential doubling

    # target, if present, is in [bound // 2, min(bound, n - 1)]
    return binary_search(arr, target, bound // 2, min(bound, n - 1))

Why it works:
    - The doubling phase takes O(log i) iterations to reach the target's
      neighbourhood (where i is the target's index).
    - The final binary search is over a range of size ≤ bound, which
      is also O(log i).

    Total: O(log i).

This is **faster than binary search** when `i << n` — i.e., when the
target is near the start. For a 1-billion-element array where the
target is at index 100, exponential search takes ~14 probes; binary
search takes 30.

---------------------------------------------------
The Killer Application — Unbounded / Infinite Arrays:

When the array's size is unknown (a sorted STREAM, a function you can
only query one index at a time, an infinite sorted list), binary
search CAN'T START — you don't know what `hi` should be.

Exponential search discovers an upper bound in O(log i) by doubling
the probe position. Once you have a bound, binary-search inside it.

This pattern shows up in:
    - Searching a sorted file / stream where length is unknown.
    - Searching a function f(i) where f is monotone and evaluating it
      is the cost you're minimizing.
    - Interview problem "Search in a Sorted Array of Unknown Size"
      (LC #702).

---------------------------------------------------
Example:

    arr = [2, 3, 4, 10, 40]
    exponential_search(arr, 10):
        probe 1: arr[1] = 3  < 10 → bound = 2
        probe 2: arr[2] = 4  < 10 → bound = 4
        probe 3: arr[4] = 40 ≥ 10 → stop
        binary-search arr[2..4] for 10 → found at index 3
"""

# =========================================================================
# Iterative Binary Search Helper (inlined for self-containment)
# =========================================================================

def _binary_search(arr, target, lo, hi):
    """Plain binary search within [lo, hi] INCLUSIVE."""
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


# =========================================================================
# Exponential Search (Bounded Arrays)
# =========================================================================

def exponential_search(arr, target):
    """
    Return the index of `target` in sorted `arr`, or -1 if not present.

    Time Complexity:  O(log i) where i is the target's index.
                      Never worse than O(log n).
    Space Complexity: O(1)
    """
    n = len(arr)
    if n == 0:
        return -1
    if arr[0] == target:
        return 0

    # Doubling phase — find a range [bound/2, bound] containing target.
    bound = 1
    while bound < n and arr[bound] < target:
        bound *= 2

    # Binary-search the discovered range
    return _binary_search(arr, target, bound // 2, min(bound, n - 1))


# =========================================================================
# Exponential Search on an Unbounded / Unknown-Size Array
# =========================================================================

class UnknownSizeArray:
    """
    Wrapper that acts like a sorted array but raises / returns a
    sentinel for out-of-bounds access — simulating an array whose
    length is unknown (LC #702's "ArrayReader").
    """

    SENTINEL = float("inf")                       # anything > any real value

    def __init__(self, data):
        self._data = data

    def get(self, i):
        """Read index i; return SENTINEL if out of range."""
        if 0 <= i < len(self._data):
            return self._data[i]
        return UnknownSizeArray.SENTINEL


def exponential_search_unbounded(reader, target):
    """
    Search a sorted, unknown-size "array" via a read-only probe.
    `reader.get(i)` returns arr[i] or SENTINEL (∞) if out of range.

    Time Complexity:  O(log i) where i is the target's index
    Space Complexity: O(1)

    Doubling phase discovers the upper bound; binary search finishes
    the job. Because SENTINEL is ∞, an out-of-range probe is
    indistinguishable from "target is smaller than this" — which is
    exactly the behaviour we need.
    """
    # doubling until reader.get(bound) >= target
    bound = 1
    while reader.get(bound) < target:
        bound *= 2

    # binary-search [bound//2, bound]
    lo, hi = bound // 2, bound
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        v = reader.get(mid)
        if v == target:
            return mid
        if v < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    arr = [2, 3, 4, 10, 40]

    print(f"arr = {arr}")
    print()
    for target in [10, 2, 40, 5, 100, 3]:
        got = exponential_search(arr, target)
        print(f"   exponential_search(arr, {target:3}) = {got}")
    print()

    # Test cases — (arr, target, expected)
    test_cases = [
        ([2, 3, 4, 10, 40],    10,  3),
        ([2, 3, 4, 10, 40],    2,   0),
        ([2, 3, 4, 10, 40],    40,  4),
        ([2, 3, 4, 10, 40],    5,   -1),
        ([2, 3, 4, 10, 40],    100, -1),
        ([],                   5,   -1),
        ([42],                 42,  0),
        ([42],                 5,   -1),
        ([1, 2, 3, 4, 5],      1,   0),
        ([1, 2, 3, 4, 5],      5,   4),
        (list(range(100)),     73,  73),            # larger array
        (list(range(100)),     999, -1),
    ]

    for i, (data, tgt, expected) in enumerate(test_cases):
        got = exponential_search(data, tgt)
        assert got == expected, (
            f"Test {i+1} failed on target={tgt}: expected {expected}, got {got}"
        )
        print(f"Test {i+1} passed: target={tgt} -> {got}")

    # Unbounded variant
    print()
    print("Unbounded array variant:")
    reader = UnknownSizeArray([1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21])
    for target in [9, 1, 21, 10, 50]:
        got = exponential_search_unbounded(reader, target)
        print(f"   unbounded_search(?, {target:2}) = {got}")

    # Stress test — compare against Python's index
    import random
    random.seed(9)
    for _ in range(200):
        n = random.randint(0, 100)
        arr = sorted(random.sample(range(-200, 200), n))
        target = random.randint(-250, 250)

        got = exponential_search(arr, target)
        expected = arr.index(target) if target in arr else -1
        if target in arr:
            assert got >= 0 and arr[got] == target
        else:
            assert got == -1

    print("\nStress test: 200 random sorted arrays agreed with linear scan")
    print("\nAll tests passed!")
