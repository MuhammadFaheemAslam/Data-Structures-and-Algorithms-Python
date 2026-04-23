"""
Problem: Kth Largest Element in an Array

Technique: Quickselect (expected O(n)) and Heap (O(n log k))
Difficulty: Medium (LeetCode #215)

---------------------------------------------------
Problem Statement:

Given an integer array `nums` and an integer `k`, return the k-th
LARGEST element.

(Note: "k-th largest" means "the one that would be at index n-k if
`nums` were sorted ascending". For k=1, that's the maximum.)

---------------------------------------------------
Three Ways to Solve It:

    1. Full sort + index.                O(n log n) time, O(1) space
                                         Simple, great for small n.

    2. Max-heap of all elements.         O(n + k log n) time
                                         Or pop k times from a max-heap.

    3. Min-heap of size k.               O(n log k) time, O(k) space
                                         Streaming-friendly; k can be huge
                                         and the algorithm only uses O(k) memory.

    4. Quickselect.                      O(n) expected time
                                         Fastest single-shot solution.

Quickselect is the "intended" answer for LC #215. In interviews, be
ready to discuss all four — picking heap-of-size-k for streaming
scenarios, quickselect for bounded-input performance.

---------------------------------------------------
Quickselect for kth Largest:

The k-th largest is at index `n - k` in the sorted order. So:

    kth_largest(nums, k) = quickselect(nums, len(nums) - k)

That's one line once quickselect is in hand.

---------------------------------------------------
Example:

    nums = [3, 2, 1, 5, 6, 4], k = 2
    -> 5
    (sorted: [1, 2, 3, 4, 5, 6]; index n - k = 4; value 5)

    nums = [3, 2, 3, 1, 2, 4, 5, 5, 6], k = 4
    -> 4

---------------------------------------------------
"""

import heapq
import random


# =========================================================================
# Approach 1: Full Sort — O(n log n)
# =========================================================================

def kth_largest_sort(nums, k):
    """Sort and index."""
    return sorted(nums)[-k]


# =========================================================================
# Approach 2: Max-Heap — O(n + k log n)
# =========================================================================

def kth_largest_max_heap(nums, k):
    """
    Build a max-heap of all n elements (O(n)), then pop k times
    (O(k log n)).

    Python's `heapq` only provides MIN-heaps, so we negate values.
    """
    neg = [-x for x in nums]
    heapq.heapify(neg)                            # O(n)
    for _ in range(k - 1):
        heapq.heappop(neg)
    return -heapq.heappop(neg)


# =========================================================================
# Approach 3: Min-Heap of Size K — O(n log k)
# =========================================================================

def kth_largest_min_heap(nums, k):
    """
    Maintain a min-heap of size K. After processing all n elements,
    the heap contains the k largest, and the smallest (at the root)
    is the k-th largest.

    Time:   O(n log k)
    Space:  O(k)

    **Streaming-friendly** — if nums is a stream, this uses only O(k)
    memory regardless of n. That's its real advantage.
    """
    heap = []
    for x in nums:
        if len(heap) < k:
            heapq.heappush(heap, x)
        elif x > heap[0]:
            heapq.heapreplace(heap, x)
    return heap[0]                                # smallest of top-k = k-th largest


# =========================================================================
# Approach 4: Quickselect — Expected O(n)
# =========================================================================

def kth_largest_quickselect(nums, k):
    """
    Quickselect for the (n - k)-th smallest. Expected O(n).

    Uses random pivots to avoid the O(n²) worst case.
    """
    nums = nums[:]                                # don't mutate caller's input
    target = len(nums) - k                        # index in sorted order

    lo, hi = 0, len(nums) - 1
    while lo < hi:
        p = _partition(nums, lo, hi)
        if p == target:
            return nums[p]
        elif p < target:
            lo = p + 1
        else:
            hi = p - 1
    return nums[lo]


def _partition(arr, lo, hi):
    """Random-pivot Lomuto partition."""
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
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    random.seed(0)                                # deterministic for tests

    nums = [3, 2, 1, 5, 6, 4]
    k = 2
    print(f"nums = {nums}, k = {k}")
    print(f"sorted: {sorted(nums)} — expecting {sorted(nums)[-k]} at position -{k}")
    print()
    print(f"kth_largest_sort:          {kth_largest_sort(nums, k)}")
    print(f"kth_largest_max_heap:      {kth_largest_max_heap(nums, k)}")
    print(f"kth_largest_min_heap:      {kth_largest_min_heap(nums, k)}")
    print(f"kth_largest_quickselect:   {kth_largest_quickselect(nums, k)}")
    print()

    # Test cases — (nums, k, expected)
    test_cases = [
        ([3, 2, 1, 5, 6, 4],             2,  5),
        ([3, 2, 3, 1, 2, 4, 5, 5, 6],    4,  4),
        ([1],                            1,  1),
        ([1, 2],                         1,  2),
        ([1, 2],                         2,  1),
        ([7, 7, 7, 7, 7],                3,  7),        # all equal
        ([-1, -2, -3, -4, -5],           2, -2),
        (list(range(1, 101)),            50, 51),       # known answer on range
    ]

    for i, (data, kk, expected) in enumerate(test_cases):
        for fn in (
            kth_largest_sort,
            kth_largest_max_heap,
            kth_largest_min_heap,
            kth_largest_quickselect,
        ):
            got = fn(data[:], kk)
            assert got == expected, (
                f"Test {i+1} ({fn.__name__}) failed: expected {expected}, got {got}"
            )
        print(f"Test {i+1} passed: len={len(data)}, k={kk} -> {expected}")

    # Stress test — random inputs, every approach must agree
    random.seed(42)
    for _ in range(200):
        n = random.randint(1, 60)
        data = [random.randint(-100, 100) for _ in range(n)]
        k = random.randint(1, n)
        expected = sorted(data)[-k]
        for fn in (
            kth_largest_sort,
            kth_largest_max_heap,
            kth_largest_min_heap,
            kth_largest_quickselect,
        ):
            assert fn(data[:], k) == expected

    print("\nStress test: 200 random queries — all four approaches agree")

    # Timing demo on large input
    import time
    random.seed(1)
    big = [random.randint(0, 10**6) for _ in range(100_000)]
    k = 10_000

    for name, fn in [
        ("sort        ", kth_largest_sort),
        ("max heap    ", kth_largest_max_heap),
        ("min heap (k)", kth_largest_min_heap),
        ("quickselect ", kth_largest_quickselect),
    ]:
        t0 = time.time()
        got = fn(big[:], k)
        print(f"   {name}  n=100_000, k={k}:  {time.time() - t0:.4f}s  (answer {got})")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Which Approach Is Best?
    #
    #                         time        space      when to pick
    #   full sort             O(n log n)  O(1)*      small n; already need a sort
    #   max heap (all)        O(n+k log n) O(n)      k close to n
    #   min heap (size k)     O(n log k)  O(k)       **STREAMING** (nums is a stream)
    #   quickselect           O(n) exp.   O(log n)   bounded input, best for LC
    #
    # (* sorted() makes a copy, so technically O(n). In C-level Python
    #  the sort is vastly faster than pure-Python alternatives.)
    #
    # For a LeetCode submission: quickselect (fastest).
    # For production streaming: min-heap of size k.
    # For prototype: just use sorted().
    # ---------------------------------------------------------------
