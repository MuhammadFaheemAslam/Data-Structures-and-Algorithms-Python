"""
Problem: Find Median From Data Stream

Difficulty: Hard (LeetCode #295)

---------------------------------------------------
Problem Statement:

Design a data structure that supports:

    add_num(x)           — add `x` to the stream.          (amortized O(log n))
    find_median()        — return the current median.      (O(1))

Median convention: for an even number of elements, return the mean of
the two middle elements.

---------------------------------------------------
The Two-Heap Trick:

Maintain TWO heaps that together hold all numbers:

    low   = MAX-heap of the smaller half        top = largest-of-smaller-half
    high  = MIN-heap of the larger half         top = smallest-of-larger-half

Invariants:
    1.  every element in `low` ≤ every element in `high`
    2.  len(low) == len(high) OR len(low) == len(high) + 1
        (we keep `low` one bigger when odd — by convention)

Given invariants:
    median = low.top                             if odd count
    median = (low.top + high.top) / 2            if even count

---------------------------------------------------
`add_num(x)` (the insert algorithm):

    1. Tentatively put x in `low`:
         push x into low (max-heap)
         then move low.pop() to high               (top-of-low may now belong to high)
    2. Rebalance if high has more elements than low:
         push high.pop() into low

This 2-shuffle guarantees the invariants. O(log n) amortized.

Python's `heapq` is min-only, so we simulate the max-heap by negating.

---------------------------------------------------
Complexity:

    add_num:      O(log n)
    find_median:  O(1)
"""

import heapq


class MedianFinder:
    """Running-median data structure. add_num O(log n), find_median O(1)."""

    def __init__(self):
        self._low = []                             # max-heap (negated values)
        self._high = []                            # min-heap

    def add_num(self, x):
        """O(log n)."""
        # Step 1: push x into low, then rebalance the top to high
        heapq.heappush(self._low, -x)
        heapq.heappush(self._high, -heapq.heappop(self._low))

        # Step 2: if high has more elements, pop one back to low
        if len(self._high) > len(self._low):
            heapq.heappush(self._low, -heapq.heappop(self._high))

    def find_median(self):
        """O(1)."""
        if not self._low:
            raise LookupError("no data yet")
        if len(self._low) == len(self._high):
            return (-self._low[0] + self._high[0]) / 2
        return -self._low[0]                       # odd count → low has one extra


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #295 example
    mf = MedianFinder()
    mf.add_num(1)
    assert mf.find_median() == 1
    mf.add_num(2)
    assert mf.find_median() == 1.5
    mf.add_num(3)
    assert mf.find_median() == 2

    # Sorted-ascending insertion
    mf = MedianFinder()
    medians = []
    for x in range(1, 11):
        mf.add_num(x)
        medians.append(mf.find_median())
    # After n elements we've added 1..n; median of 1..n is (n+1)/2 for odd n
    # or (n + (n+1))/2 / 2 — i.e. the classic arithmetic-mean computation
    assert medians == [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5]

    # Sorted-descending insertion
    mf = MedianFinder()
    medians = []
    for x in range(10, 0, -1):
        mf.add_num(x)
        medians.append(mf.find_median())
    # After inserting [10], [10,9], [10,9,8], ...:
    # median of these is: 10, 9.5, 9, 8.5, ...
    assert medians == [10, 9.5, 9, 8.5, 8, 7.5, 7, 6.5, 6, 5.5]

    # Negative and duplicate values
    mf = MedianFinder()
    for x in [5, -3, 5, 2, -3, 0]:
        mf.add_num(x)
    # Sorted: [-3, -3, 0, 2, 5, 5] → median = (0 + 2)/2 = 1
    assert mf.find_median() == 1

    # Stress: 10000 random inserts, check median matches sorted-list's
    import bisect
    import random
    random.seed(42)

    sorted_arr = []
    mf = MedianFinder()
    for _ in range(10_000):
        x = random.randint(-1000, 1000)
        mf.add_num(x)
        bisect.insort(sorted_arr, x)
        n = len(sorted_arr)
        expected = (sorted_arr[n // 2] if n % 2
                    else (sorted_arr[n // 2 - 1] + sorted_arr[n // 2]) / 2)
        assert mf.find_median() == expected

    print(f"Stress test: 10000 add_num + find_median calls, all medians correct")
    print("All tests passed!")
