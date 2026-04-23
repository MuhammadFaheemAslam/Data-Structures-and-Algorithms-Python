"""
Problem: K Largest Elements in an Array

Technique: Min-Heap of Size K
Difficulty: Medium (LeetCode #215 variant; "find ALL top-k" rather than "kth")

---------------------------------------------------
Problem Statement:

Given an array `nums` and an integer `k`, return the k LARGEST elements
of the array (any order).

    nums = [3, 2, 1, 5, 6, 4], k = 3
    → [4, 5, 6]   (any order works)

---------------------------------------------------
Why a Min-Heap of Size K?

Contrast this with Phase-03 / 03 / 02-Quick-Sort / problems / kth-largest.py
— which finds JUST the k-th largest. Here we want ALL k of them.

Four approaches to this problem:

    1. Sort and take the last k:             O(n log n) time, O(1) space
    2. Max-heap, pop k times:                O(n + k log n)
    3. **Min-heap of size k**:               **O(n log k)** — the classic
    4. Quickselect then partition:           O(n) expected

The min-heap-of-size-k approach (#3) is the textbook answer for
**streaming** problems:

    - It only needs O(k) memory — regardless of n.
    - It works on unbounded / infinite streams.
    - Each new element: either ignore (smaller than heap min) or swap
      with the heap min in O(log k).

When nums is a list in memory, quickselect (#4) beats it. But for
streams, min-heap-of-size-k is the gold standard.

---------------------------------------------------
The Algorithm:

    heap = []   # min-heap of size ≤ k
    for x in nums:
        if len(heap) < k:
            heappush(heap, x)             # heap is still filling up
        elif x > heap[0]:
            heapreplace(heap, x)          # x is bigger than our current min — swap
    return heap   # these are the k largest elements

After the loop, `heap` contains the k largest elements (in heap order,
not sorted).

---------------------------------------------------
Example:

    nums = [3, 2, 1, 5, 6, 4], k = 3

    heap after each step:
        [3]
        [2, 3]
        [1, 3, 2]
        1 < x=5 → replace: [2, 3, 5]  (now min-heap: [2, 3, 5])
        2 < x=6 → replace: [3, 6, 5]  (heap reorganises)
        3 < x=4 → replace: [4, 6, 5]

    Final heap: {4, 5, 6} ✓

---------------------------------------------------
"""

import heapq


# =========================================================================
# Approach 1: Min-Heap of Size K — O(n log k) — THE Classic
# =========================================================================

def k_largest_heap(nums, k):
    """
    Return the k largest elements in `nums` using a min-heap of size k.

    Time:   O(n log k)
    Space:  O(k)

    The order of the returned list is the heap's internal order — NOT
    sorted by value. Call `sorted(result)` if you need them sorted.
    """
    if k <= 0:
        return []

    heap = []
    for x in nums:
        if len(heap) < k:
            heapq.heappush(heap, x)
        elif x > heap[0]:
            heapq.heapreplace(heap, x)

    return heap


# =========================================================================
# Approach 2: heapq.nlargest — Built-In (What You'd Actually Use)
# =========================================================================

def k_largest_builtin(nums, k):
    """
    Python's built-in — uses the min-heap-of-size-k strategy internally.

    Time:   O(n log k)
    Space:  O(k)

    For production code, this is the right answer. Returns results
    in DESCENDING order.
    """
    return heapq.nlargest(k, nums)


# =========================================================================
# Approach 3: Sort and Slice — O(n log n)
# =========================================================================

def k_largest_sort(nums, k):
    """Sort and take the last k. Simple; slower asymptotically."""
    return sorted(nums)[-k:] if k > 0 else []


# =========================================================================
# Approach 4: Max-Heap, Pop K Times — O(n + k log n)
# =========================================================================

def k_largest_max_heap(nums, k):
    """
    Build a max-heap of ALL n elements (O(n) via Floyd), then pop k.

    Time:   O(n + k log n)
    Space:  O(n)

    Faster than Approach 1 when k is close to n. Much slower memory-
    wise — needs to hold the full array.
    """
    if k <= 0:
        return []

    neg = [-x for x in nums]                      # min-heap negated = max-heap
    heapq.heapify(neg)                            # O(n)

    result = []
    for _ in range(k):
        if not neg:
            break
        result.append(-heapq.heappop(neg))
    return result


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    nums = [3, 2, 1, 5, 6, 4]
    k = 3
    print(f"nums = {nums}, k = {k}")
    print(f"k_largest_heap:        {sorted(k_largest_heap(nums, k))}")
    print(f"k_largest_builtin:     {k_largest_builtin(nums, k)}")
    print(f"k_largest_sort:        {k_largest_sort(nums, k)}")
    print(f"k_largest_max_heap:    {k_largest_max_heap(nums, k)}")
    print()

    # Test cases — (nums, k, expected_sorted)
    test_cases = [
        ([3, 2, 1, 5, 6, 4],         3,   [4, 5, 6]),
        ([1, 2],                     1,   [2]),
        ([1, 2],                     2,   [1, 2]),
        ([7, 7, 7, 7, 7],            3,   [7, 7, 7]),
        ([-1, -2, -3, -4, -5],       2,   [-2, -1]),
        ([1],                        1,   [1]),
        ([1, 2, 3],                  0,   []),
        ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4,  [4, 5, 5, 6]),
        (list(range(1, 101)),        10,  list(range(91, 101))),
    ]

    for i, (data, kk, expected) in enumerate(test_cases):
        for fn in (
            k_largest_heap,
            k_largest_builtin,
            k_largest_sort,
            k_largest_max_heap,
        ):
            got = sorted(fn(data, kk))
            assert got == expected, (
                f"Test {i+1} ({fn.__name__}): expected {expected}, got {got}"
            )
        print(f"Test {i+1} passed: len={len(data)}, k={kk}")

    # Streaming demonstration — process items one at a time, never holding all n
    print()
    print("Streaming demo — find top-3 of a generator (never holds full list):")
    import random
    random.seed(42)

    def streaming_source(n):
        """Yields n integers, never materializing the full list."""
        for _ in range(n):
            yield random.randint(0, 1000)

    k = 3
    heap = []
    for x in streaming_source(100_000):
        if len(heap) < k:
            heapq.heappush(heap, x)
        elif x > heap[0]:
            heapq.heapreplace(heap, x)

    print(f"   top-{k} from 100_000-element stream (sorted): {sorted(heap)}")
    print(f"   memory used: just {k} integers, regardless of stream length")

    # Stress test
    random.seed(0)
    for _ in range(200):
        n = random.randint(1, 100)
        data = [random.randint(-200, 200) for _ in range(n)]
        k = random.randint(1, n)
        expected = sorted(sorted(data)[-k:])
        for fn in (k_largest_heap, k_largest_builtin, k_largest_sort, k_largest_max_heap):
            got = sorted(fn(data, k))
            assert got == expected

    print("\nStress test: 200 random inputs — all four approaches agree")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # When to Use Which:
    #
    #                         time        space     when to pick
    #   min-heap of size k    O(n log k)  O(k)      **streaming**, k << n
    #   heapq.nlargest        O(n log k)  O(k)      production Python
    #   sort and slice        O(n log n)  O(n)      simple, small n
    #   max-heap (full)       O(n+k log n) O(n)     k close to n
    #
    # The min-heap-of-size-k pattern is the "canonical" answer because
    # it's the only one that works for UNBOUNDED STREAMS. Keeping k
    # elements is a fixed cost; keeping all n may be impossible.
    # ---------------------------------------------------------------
