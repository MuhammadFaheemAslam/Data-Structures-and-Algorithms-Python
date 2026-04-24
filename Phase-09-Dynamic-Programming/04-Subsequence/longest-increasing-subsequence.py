"""
Problem: Longest Increasing Subsequence

Difficulty: Medium (LeetCode #300)

---------------------------------------------------
Problem Statement:

Given an integer array `nums`, return the length of the longest
STRICTLY INCREASING subsequence.

Example:
    [10, 9, 2, 5, 3, 7, 101, 18]        →  4     (LIS: [2, 3, 7, 101])
    [0, 1, 0, 3, 2, 3]                   →  4     (LIS: [0, 1, 2, 3])
    [7, 7, 7, 7]                         →  1     (any single 7)

---------------------------------------------------
Two Classic Solutions:

### 1. O(n²) DP — the natural formulation

    dp[i] = length of the longest INCREASING subseq that ENDS AT index i

    dp[i] = 1 + max(dp[j] for j < i if nums[j] < nums[i])
          (or 1 if no such j exists)

    answer = max(dp)

Each index compares with every previous index → O(n²). Easy to code,
easy to reason about, always correct.

### 2. O(n log n) — Patience Sorting

Maintain a list `tails` where `tails[k]` is the SMALLEST possible
tail-value of any LIS of length k+1 seen so far. Insert each number
by binary-searching (bisect_left) for its position; either extend
tails (if it's bigger than every tail so far) or overwrite the first
tail that's ≥ this number.

At the end, `len(tails)` IS the LIS length. `tails` itself is NOT a
valid LIS — overwrites may place values that don't appear in any
single subsequence. (We include a reconstruction variant for that.)

    Why it works (sketch): by overwriting, we keep tails SORTED.
    A smaller tail at length k is always better — it's easier to
    extend. When we land a new value v, binary search finds the
    first tail ≥ v; overwriting it means "LIS of that length now
    ends with a smaller value, leaving more room to grow".

    This is the same algorithm as the card-game PATIENCE.

---------------------------------------------------
Where LIS Shows Up:

- Scheduling problems (longest chain of compatible tasks).
- "Russian Doll Envelopes" (LC #354) reduces to LIS after a clever sort.
- Longest bitonic subsequence, longest alternating subsequence —
  variants with slightly different transitions.
- "Stock span", "longest chain of pairs", etc. — all LIS variants.

---------------------------------------------------
Complexity:

    O(n²) DP:            Time O(n²),      Space O(n).
    O(n log n) patience: Time O(n log n), Space O(n).
"""

import bisect


# -------- Solution 1: O(n²) DP --------

def lis_dp(nums):
    """
    O(n²) DP. Easy-to-state, slower but more intuitive.

    Time: O(n²), Space: O(n).
    """
    if not nums:
        return 0
    dp = [1] * len(nums)
    for i in range(1, len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


# -------- Solution 2: O(n log n) patience sort --------

def lis_patience(nums):
    """
    O(n log n) via patience-sort with `bisect`.

    Time: O(n log n), Space: O(n).
    """
    tails = []
    for x in nums:
        idx = bisect.bisect_left(tails, x)
        if idx == len(tails):
            tails.append(x)
        else:
            tails[idx] = x
    return len(tails)


# -------- Reconstruction: an actual LIS (not just length) --------

def lis_reconstruct(nums):
    """
    Return one LIS as a list. Uses O(n²) DP + backtracking for clarity.

    There may be multiple LISs of the same length; we return whichever
    the algorithm happens to trace.

    Time: O(n²), Space: O(n).
    """
    if not nums:
        return []
    n = len(nums)
    dp = [1] * n
    prev = [-1] * n
    best_idx = 0

    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                prev[i] = j
        if dp[i] > dp[best_idx]:
            best_idx = i

    out = []
    i = best_idx
    while i != -1:
        out.append(nums[i])
        i = prev[i]
    return list(reversed(out))


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #300 examples
    cases = [
        ([10, 9, 2, 5, 3, 7, 101, 18], 4),
        ([0, 1, 0, 3, 2, 3], 4),
        ([7, 7, 7, 7], 1),
        ([1, 3, 6, 7, 9, 4, 10, 5, 6], 6),
        ([], 0),
        ([1], 1),
        ([1, 2, 3, 4, 5], 5),
        ([5, 4, 3, 2, 1], 1),
        ([1, 3, 2, 4], 3),                          # LIS: [1,2,4] or [1,3,4]
    ]

    for nums, expected in cases:
        assert lis_dp(nums) == expected, f"dp({nums})"
        assert lis_patience(nums) == expected, f"patience({nums})"

    # Reconstruction returns a valid LIS
    def is_strictly_increasing(seq):
        return all(seq[i] < seq[i + 1] for i in range(len(seq) - 1))

    def is_subseq(sub, full):
        i = 0
        for x in full:
            if i < len(sub) and sub[i] == x:
                i += 1
        return i == len(sub)

    for nums, expected in cases:
        out = lis_reconstruct(nums)
        assert len(out) == expected
        assert is_strictly_increasing(out)
        assert is_subseq(out, nums)

    # Stress: both solvers agree on random arrays
    import random
    random.seed(42)
    for _ in range(200):
        n = random.randint(0, 50)
        nums = [random.randint(-20, 20) for _ in range(n)]
        a = lis_dp(nums)
        b = lis_patience(nums)
        assert a == b, f"mismatch: {nums} → dp={a}, patience={b}"

    # Performance demo: O(n²) vs O(n log n) on large input
    import time
    random.seed(0)
    big = [random.randint(0, 10 ** 6) for _ in range(5000)]
    t0 = time.time()
    a = lis_dp(big)
    t_dp = time.time() - t0
    t0 = time.time()
    b = lis_patience(big)
    t_p = time.time() - t0
    assert a == b
    print(f"LIS on n=5000 random ints:")
    print(f"   O(n²) DP:           {t_dp * 1000:7.1f} ms   → LIS length {a}")
    print(f"   O(n log n) patience: {t_p * 1000:7.1f} ms   → LIS length {b}")

    print("\nAll tests passed!")
