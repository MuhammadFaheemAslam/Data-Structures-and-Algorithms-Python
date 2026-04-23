"""
Problem: K Smallest Elements / Kth Smallest in a Sorted Matrix

Difficulty: Medium (LeetCode #378 for the matrix variant)

This file covers two related "k smallest" problems:

    1. K smallest in an UNSORTED ARRAY.       — mirror of k-largest.py
    2. K smallest in a SORTED n×n MATRIX.     — classic heap-merge problem (LC #378)

---------------------------------------------------
Part 1 — K smallest in an array (top-k with max-heap):

Symmetric to k-largest: keep a MAX-heap of size k, discard anything
larger than the heap's max. Python's heapq is min-only, so we negate.

    Time: O(n log k), Space: O(k).

---------------------------------------------------
Part 2 — K-th smallest in a sorted matrix (LC #378):

Matrix:
    [[ 1,  5,  9],
     [10, 11, 13],
     [12, 13, 15]]
    k = 8 → 13

Rows and columns are SORTED (but the rows don't chain — row[i][-1] can
be greater than row[i+1][0]; don't assume a flat order).

Clever approach — k-way merge via min-heap:
    - Seed the heap with the first element of each row: (val, row, col).
    - Pop k-1 times. After each pop, if there's a next element in
      the same row, push it.
    - The k-th pop is the answer.

Complexity: O(k log n) time, O(n) heap space.

A BINARY SEARCH ON THE VALUE approach is even tighter asymptotically
O(n log(max-min)) but more subtle; we include it as a bonus.
"""

import heapq


# =========================================================================
# Part 1 — k smallest in an array
# =========================================================================

def k_smallest_array(nums, k):
    """
    Return the k SMALLEST values from `nums`, in ascending order.

    Time:  O(n log k), Space: O(k).
    """
    # Max-heap of size k (negate to simulate with heapq)
    heap = []
    for x in nums:
        if len(heap) < k:
            heapq.heappush(heap, -x)
        elif x < -heap[0]:                         # x beats the heap's current max
            heapq.heapreplace(heap, -x)
    return sorted(-x for x in heap)


# =========================================================================
# Part 2 — k-th smallest in a sorted n×n matrix
# =========================================================================

def kth_smallest_matrix_heap(matrix, k):
    """
    Time:  O(k log n), Space: O(n).
    """
    n = len(matrix)

    # Min-heap seeded with first element of each row
    heap = []
    for r in range(min(n, k)):                     # only need first k rows' heads
        heapq.heappush(heap, (matrix[r][0], r, 0))

    # Pop k-1 times
    for _ in range(k - 1):
        val, r, c = heapq.heappop(heap)
        if c + 1 < n:
            heapq.heappush(heap, (matrix[r][c + 1], r, c + 1))

    return heap[0][0]


def kth_smallest_matrix_binary_search(matrix, k):
    """
    Binary search on the VALUE range. For a candidate `mid`, count how
    many matrix entries are ≤ mid using the sorted-matrix structure
    (a staircase scan from the bottom-left). Converge to the smallest
    `mid` such that count ≥ k.

    Time: O(n log(max - min)), Space: O(1).
    """
    n = len(matrix)
    lo, hi = matrix[0][0], matrix[-1][-1]

    def count_le(mid):
        """How many entries ≤ mid? Staircase from bottom-left."""
        count = 0
        r, c = n - 1, 0
        while r >= 0 and c < n:
            if matrix[r][c] <= mid:
                count += r + 1                     # everything above in this column too
                c += 1
            else:
                r -= 1
        return count

    while lo < hi:
        mid = (lo + hi) // 2
        if count_le(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Part 1
    assert k_smallest_array([3, 2, 1, 5, 6, 4], 2) == [1, 2]
    assert k_smallest_array([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == [1, 2, 2, 3]
    assert k_smallest_array([5], 1) == [5]

    # Stress part 1
    import random
    random.seed(42)
    for _ in range(200):
        n = random.randint(1, 100)
        nums = [random.randint(-50, 50) for _ in range(n)]
        k = random.randint(1, n)
        assert k_smallest_array(nums, k) == sorted(nums)[:k]

    # Part 2 — LC #378 example
    mat = [[1, 5, 9], [10, 11, 13], [12, 13, 15]]
    assert kth_smallest_matrix_heap(mat, 8) == 13
    assert kth_smallest_matrix_binary_search(mat, 8) == 13

    assert kth_smallest_matrix_heap([[-5]], 1) == -5
    assert kth_smallest_matrix_heap([[1, 2], [1, 3]], 2) == 1
    assert kth_smallest_matrix_heap([[1, 2], [1, 3]], 3) == 2

    # Stress part 2: random sorted matrices
    for _ in range(100):
        n = random.randint(1, 10)
        # Build a sorted matrix by generating n*n sorted values and reshaping row-wise
        flat = sorted(random.randint(-50, 50) for _ in range(n * n))
        mat = [flat[i * n:(i + 1) * n] for i in range(n)]
        # Also sort each column so BOTH rows and columns are sorted
        # (row-sort is already done; columns might not be. For this
        # simple test, we'll just sort each column after row-sort.)
        cols = list(map(list, zip(*mat)))
        cols = [sorted(c) for c in cols]
        mat = list(map(list, zip(*cols)))

        for k in range(1, n * n + 1):
            expected = sorted(sum(mat, []))[k - 1]
            assert kth_smallest_matrix_heap(mat, k) == expected
            assert kth_smallest_matrix_binary_search(mat, k) == expected

    print("All tests passed!")
