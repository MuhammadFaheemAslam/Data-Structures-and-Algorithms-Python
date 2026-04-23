"""
Problem: Kth Largest Element In An Array

Difficulty: Medium (LeetCode #215)

---------------------------------------------------
Problem Statement:

Given an integer array `nums` and integer `k`, return the k-th
LARGEST element. NOTE: not the k-th DISTINCT value — duplicates count.

Example:
    nums = [3, 2, 1, 5, 6, 4], k = 2 → 5
    nums = [3, 2, 3, 1, 2, 4, 5, 5, 6], k = 4 → 4

---------------------------------------------------
Three Solutions, Increasing Cleverness:

    1. Sort and index                    O(n log n) time, O(1) space (or O(n) if sorted() copies)
    2. Min-heap of size k                O(n log k) time, O(k) space  ← recommended
    3. Quickselect (partition-based)     O(n) avg time, O(n²) worst, O(1) space

Quickselect is the "optimal" answer on paper. Heap is the PRACTICAL
answer — simpler, predictable, and the same asymptotic when k ≪ n.

---------------------------------------------------
Why Min-Heap Of Size K?:

We want the k largest elements. Keep a min-heap of size k:
    - push anything;
    - if size > k, pop the smallest.

At the end, the smallest element in the heap is the k-th largest.

Why min-heap, not max? Because we want to CHEAPLY evict the smallest
of the "top-k candidates" as better contenders come in. A min-heap
makes that O(log k). A max-heap would make us scan all k to find
the min to evict.

---------------------------------------------------
Heap solution complexity:

    Time:  O(n log k).
    Space: O(k).
"""

import heapq


# -------- Solution 1: Sort and index (baseline) --------

def kth_largest_sort(nums, k):
    """Time O(n log n), Space O(n) (Python's sorted copies)."""
    return sorted(nums, reverse=True)[k - 1]


# -------- Solution 2: Min-heap of size k --------

def kth_largest_heap(nums, k):
    """
    Time:  O(n log k), Space: O(k).
    """
    heap = []
    for x in nums:
        if len(heap) < k:
            heapq.heappush(heap, x)
        elif x > heap[0]:                          # x beats the current kth-largest
            heapq.heapreplace(heap, x)             # pop min + push x in one op
    return heap[0]


# -------- Solution 3: Quickselect (Hoare partition) --------

def kth_largest_quickselect(nums, k):
    """
    Partition-based selection. Expected O(n), worst O(n²).

    Space: O(1) if we mutate in place; here we use recursive tail calls.
    """
    nums = nums[:]                                 # copy so we don't mutate caller's list
    target = len(nums) - k                         # 0-indexed position of the k-th largest
                                                   # when sorted ascending

    def select(lo, hi):
        """Find nums[target] by repeatedly partitioning."""
        if lo == hi:
            return nums[lo]

        import random
        pivot_idx = random.randint(lo, hi)         # random pivot avoids adversarial O(n²)
        pivot = nums[pivot_idx]
        nums[pivot_idx], nums[hi] = nums[hi], nums[pivot_idx]

        # Lomuto partition
        store = lo
        for i in range(lo, hi):
            if nums[i] < pivot:
                nums[store], nums[i] = nums[i], nums[store]
                store += 1
        nums[store], nums[hi] = nums[hi], nums[store]

        if store == target:
            return nums[store]
        if store < target:
            return select(store + 1, hi)
        return select(lo, store - 1)

    return select(0, len(nums) - 1)


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC examples
    cases = [
        ([3, 2, 1, 5, 6, 4], 2, 5),
        ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4, 4),
        ([1], 1, 1),
        ([2, 1], 1, 2),
        ([2, 1], 2, 1),
        ([1, 1, 1, 1], 2, 1),                      # duplicates count
    ]

    for nums, k, expected in cases:
        assert kth_largest_sort(nums, k) == expected
        assert kth_largest_heap(nums, k) == expected
        assert kth_largest_quickselect(nums, k) == expected

    # Stress on random inputs
    import random
    random.seed(42)
    for _ in range(500):
        n = random.randint(1, 100)
        nums = [random.randint(-100, 100) for _ in range(n)]
        k = random.randint(1, n)
        expected = kth_largest_sort(nums, k)
        assert kth_largest_heap(nums, k) == expected
        assert kth_largest_quickselect(nums, k) == expected

    # Timing demo on a large input
    import time
    random.seed(0)
    big = [random.randint(0, 10**9) for _ in range(1_000_000)]
    k = 10

    for solver in (kth_largest_sort, kth_largest_heap, kth_largest_quickselect):
        t0 = time.time()
        ans = solver(big, k)
        elapsed = time.time() - t0
        print(f"   {solver.__name__:<32}: {elapsed * 1000:6.1f} ms  → {ans}")

    print("\nAll tests passed!")
