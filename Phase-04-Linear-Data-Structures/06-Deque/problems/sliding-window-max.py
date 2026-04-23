"""
Problem: Sliding Window Maximum

Difficulty: Hard (LeetCode #239)

---------------------------------------------------
Problem Statement:

Given an array `nums` and an integer `k`, return an array where the
i-th element is the maximum of nums[i..i+k-1] — the maximum of each
length-k window as the window slides across the array.

    nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3
    output = [3, 3, 5, 5, 6, 7]

Must do it in **O(n)** time. A naïve solution takes O(n · k).

---------------------------------------------------
Why This Is the Canonical Deque Problem:

The naïve solution recomputes the max of each window from scratch:
O(n · k). For a million-element array with a 1000-element window,
that's 10⁹ ops — too slow.

**Monotonic-deque** solution: maintain a deque of INDICES whose values
are in strictly DECREASING order from front to back. The front of the
deque is always the index of the window's maximum.

For each new index i:

    1. Evict the back while its value ≤ nums[i]  (they're dominated)
    2. Append i at the back
    3. Evict the front if it's fallen out of the window (index < i - k + 1)
    4. If the window is now full (i ≥ k - 1), emit nums[deque.front()]

Each index is added once and removed once → **O(n) total**.

---------------------------------------------------
Why Values at the Back Get Evicted:

If nums[i] ≥ nums[j] for some earlier j that's still in the window,
then nums[j] can NEVER be the window max while nums[i] is still in
the window (j will exit before i). So we can drop j forever.

By keeping the deque strictly decreasing, the front is always the
largest value in the current window.

---------------------------------------------------
"""

from collections import deque


# =========================================================================
# Solution 1: Monotonic Deque — O(n) ✓
# =========================================================================

def sliding_window_max(nums, k):
    """
    Monotonic-deque solution for LC #239.

    Time:  O(n)   — each index enters and leaves the deque once
    Space: O(k)
    """
    if not nums or k <= 0:
        return []

    dq = deque()                                  # stores INDICES; values decreasing front → back
    result = []

    for i, x in enumerate(nums):
        # 1. Evict dominated values from the back
        while dq and nums[dq[-1]] <= x:
            dq.pop()

        # 2. Append the new index
        dq.append(i)

        # 3. Evict stale indices from the front (out of window)
        while dq[0] <= i - k:
            dq.popleft()

        # 4. Emit the max once the window is full
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result


# =========================================================================
# Solution 2: Naïve Brute Force — O(n · k)
# =========================================================================

def sliding_window_max_brute(nums, k):
    """
    For each window position, compute max from scratch.

    Time:  O(n · k)
    Space: O(1)

    Used to validate the deque solution.
    """
    if not nums or k <= 0:
        return []
    return [max(nums[i:i + k]) for i in range(len(nums) - k + 1)]


# =========================================================================
# Solution 3: Max-Heap (Lazy Deletion) — O(n log n)
# =========================================================================

def sliding_window_max_heap(nums, k):
    """
    Use a max-heap of (-value, index) pairs. Python's heapq is a
    min-heap, so negate values.

    On each step, before reading the top, DISCARD entries whose index
    has fallen out of the window. (Lazy deletion — we don't eagerly
    remove elements from the heap when they "expire".)

    Time:  O(n log n)
    Space: O(n)  — in the worst case, the heap holds every index ever seen.

    Not as good as the deque version (O(n log n) vs O(n)), but simpler
    to think about once you're comfortable with heaps.
    """
    import heapq

    if not nums or k <= 0:
        return []

    heap = []
    result = []

    for i, x in enumerate(nums):
        heapq.heappush(heap, (-x, i))

        if i >= k - 1:
            # drop stale entries from the top
            while heap[0][1] <= i - k:
                heapq.heappop(heap)
            result.append(-heap[0][0])

    return result


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    # LC #239 canonical example
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    expected = [3, 3, 5, 5, 6, 7]

    print(f"nums = {nums}, k = {k}")
    for fn in (sliding_window_max, sliding_window_max_brute, sliding_window_max_heap):
        got = fn(nums, k)
        assert got == expected
        print(f"   {fn.__name__}: {got}")
    print()

    # Edge cases
    test_cases = [
        ([],                          3,  []),
        ([1],                         1,  [1]),
        ([1, 2, 3],                   1,  [1, 2, 3]),                   # k=1 is identity
        ([1, 2, 3],                   3,  [3]),                          # one full window
        ([1, 2, 3],                   5,  []),                           # k > n — no full window
        ([5, 4, 3, 2, 1],             3,  [5, 4, 3]),                    # monotone decreasing
        ([1, 2, 3, 4, 5],             3,  [3, 4, 5]),                    # monotone increasing
        ([-1, -2, -3, -4],            2,  [-1, -2, -3]),                 # all negative
        ([7, 7, 7, 7],                2,  [7, 7, 7]),                    # all equal
        ([1, -1],                     1,  [1, -1]),
    ]

    for nums, k, expected in test_cases:
        for fn in (sliding_window_max, sliding_window_max_brute, sliding_window_max_heap):
            got = fn(nums, k)
            assert got == expected, f"{fn.__name__}({nums}, {k}): {got} != {expected}"
        print(f"{nums} k={k} → {expected}")

    # Stress test — all three approaches should agree
    import random
    random.seed(42)
    for _ in range(300):
        n = random.randint(0, 50)
        nums = [random.randint(-100, 100) for _ in range(n)]
        k = random.randint(1, max(1, n + 1))

        a = sliding_window_max(nums, k)
        b = sliding_window_max_brute(nums, k)
        c = sliding_window_max_heap(nums, k)
        assert a == b == c, f"disagreement on nums={nums}, k={k}"

    print("\nStress test: 300 random cases — all three approaches agree")

    # Timing — deque crushes brute force at scale
    import time
    random.seed(0)
    big_nums = [random.randint(0, 10**6) for _ in range(200_000)]
    big_k = 1_000

    t0 = time.time()
    sliding_window_max(big_nums, big_k)
    t_deque = time.time() - t0

    t0 = time.time()
    sliding_window_max_brute(big_nums, big_k)
    t_brute = time.time() - t0

    t0 = time.time()
    sliding_window_max_heap(big_nums, big_k)
    t_heap = time.time() - t0

    print(f"\nTiming on n=200k, k=1k:")
    print(f"   deque (O(n)):       {t_deque:.3f}s")
    print(f"   brute (O(n·k)):     {t_brute:.3f}s")
    print(f"   heap  (O(n log n)): {t_heap:.3f}s")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Monotonic-Deque Family:
    #
    #   Same structure solves many "window with extremum" problems:
    #
    #     - Sliding Window Maximum (this)
    #     - Sliding Window Minimum (flip the comparison)
    #     - Constrained Subsequence Sum (LC #1425)
    #     - Shortest Subarray with Sum at Least K (LC #862)
    #     - Jump Game VI (LC #1696)
    #
    # Recognizing this pattern is the skill: "I'm doing an extremum
    # query over a sliding window of indices — deque of indices with
    # a monotonic invariant." Once you see it, it's everywhere.
    # ---------------------------------------------------------------
