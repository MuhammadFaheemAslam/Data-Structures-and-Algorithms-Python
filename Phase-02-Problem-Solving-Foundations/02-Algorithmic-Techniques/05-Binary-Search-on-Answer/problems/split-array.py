"""
Problem: Split Array Largest Sum

Technique: Binary Search on Answer (with a greedy feasibility check)
Difficulty: Hard (LeetCode #410)

---------------------------------------------------
Problem Statement:

Given an integer array `nums` and an integer `m`, split `nums` into
`m` NON-EMPTY CONTIGUOUS subarrays. Return the MINIMUM possible LARGEST
SUM among those subarrays.

(Equivalently: "minimize the maximum load on any worker when dividing
work into m consecutive chunks".)

---------------------------------------------------
The Binary-Search-on-Answer Lens:

The "obvious" approach is DP: `dp[i][k]` = min-largest-sum splitting
the first i elements into k subarrays. That's O(n^2 * m) time — works,
but overkill.

A slicker approach: binary search over the ANSWER — the largest-sum X.

Feasibility check:
    check(X) = "can we split nums into AT MOST m subarrays, each with
                sum <= X?"

Greedy implementation of `check`:
    - Walk nums, keep a running subarray sum.
    - When adding the next element would exceed X, close off the current
      subarray and start a new one.
    - Count the number of subarrays needed; feasible iff count <= m.

Monotonicity: larger X means fewer subarrays needed (more slack per
piece), which only helps. So feasibility is monotone: "False for small
X, becomes True at some point, True forever."

Template A applies: find the MINIMUM X with check(X) == True.

---------------------------------------------------
Search Range:

    lo = max(nums)        (a subarray must hold at least one element)
    hi = sum(nums)        (worst case: single subarray of the whole array)

A smaller lo is wrong: if X < max(nums), the single-element subarray
containing max(nums) already violates sum <= X.

A larger hi is wasteful but correct: the BSOA converges in log(hi - lo)
iterations regardless.

---------------------------------------------------
Complexity:

    Binary search:     O(log(sum(nums) - max(nums)))  ≈  O(log(sum(nums)))
    Feasibility check: O(n)
    Total:             O(n log(sum(nums)))

For sum(nums) up to 10^9 and n up to 1000, this is ~30 * 1000 = 30k
operations. Immediate.

---------------------------------------------------
Example:

    nums = [7, 2, 5, 10, 8],  m = 2

    Optimal split: [7, 2, 5 | 10, 8] → largest sum 18.
    (Other split [7 | 2, 5, 10, 8] has largest sum 25.)

---------------------------------------------------
"""

# -------------------------------------------------
# The Binary-Search-on-Answer Solution
# -------------------------------------------------

def split_array(nums, m):
    """
    Return the minimum possible largest-subarray sum when splitting
    nums into exactly m non-empty contiguous subarrays.

    Time Complexity:  O(n * log(sum(nums)))
    Space Complexity: O(1)
    """
    def can_split_with_max_sum(max_sum):
        """
        Greedy: walk nums; start a new subarray whenever adding the next
        element would push the running sum past max_sum. Return True iff
        at most m subarrays are needed.
        """
        pieces = 1
        running = 0
        for x in nums:
            if running + x <= max_sum:
                running += x
            else:
                pieces += 1
                running = x
                if pieces > m:
                    return False
        return True

    lo = max(nums)                                # one subarray must hold at least max(nums)
    hi = sum(nums)                                # single-subarray split

    # Template A: smallest feasible X
    while lo < hi:
        mid = (lo + hi) // 2
        if can_split_with_max_sum(mid):
            hi = mid                              # mid works — try smaller
        else:
            lo = mid + 1                          # mid fails — must be bigger

    return lo


# -------------------------------------------------
# For Contrast: the Dynamic Programming Solution — O(n^2 * m)
# -------------------------------------------------

def split_array_dp(nums, m):
    """
    DP reference: dp[i][k] = min largest-sum splitting nums[0..i-1] into
    k subarrays.

    Recurrence:
        dp[i][k] = min over j in [k-1, i-1] of max(dp[j][k-1], sum(nums[j..i-1]))

    Time Complexity:  O(n^2 * m)
    Space Complexity: O(n * m)

    Correct but much slower than BSOA. Included to verify BSOA against.
    """
    n = len(nums)
    # prefix sums for O(1) range sums
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]

    INF = float("inf")
    dp = [[INF] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 0

    for i in range(1, n + 1):
        for k in range(1, m + 1):
            for j in range(k - 1, i):
                subarray_sum = prefix[i] - prefix[j]
                dp[i][k] = min(dp[i][k], max(dp[j][k - 1], subarray_sum))

    return dp[n][m]


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    nums, m = [7, 2, 5, 10, 8], 2
    print(f"nums = {nums}, m = {m}")
    print(f"split_array (BSOA): {split_array(nums, m)}")
    print(f"split_array_dp:     {split_array_dp(nums, m)}")
    print()

    # Test cases — (nums, m, expected)
    test_cases = [
        ([7, 2, 5, 10, 8],          2,   18),
        ([1, 2, 3, 4, 5],           2,   9),      # [1,2,3,4 | 5] → 10, or [1,2,3 | 4,5] → 9
        ([1, 4, 4],                 3,   4),
        ([1, 2, 3, 4, 5],           5,   5),      # m = n → every element is its own piece
        ([100],                     1,   100),
        ([1, 1, 1, 1, 1, 1],        3,   2),      # split as [1,1|1,1|1,1] → max 2
        ([10, 20, 30, 40, 50],      1,   150),    # m = 1 → whole sum
        ([5, 6, 7, 8, 9],           5,   9),
        ([1, 2147483646],           2,   2147483646),
    ]

    for i, (data, mm, expected) in enumerate(test_cases):
        got = split_array(data, mm)
        assert got == expected, (
            f"Test {i+1} (BSOA): nums={data}, m={mm} → expected {expected}, got {got}"
        )
        # cross-check DP on small inputs
        if len(data) <= 50:
            dp = split_array_dp(data, mm)
            assert got == dp, f"Test {i+1}: BSOA ({got}) disagrees with DP ({dp})"
        print(f"Test {i+1} passed: nums={data}, m={mm} -> {expected}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Why This Problem Is the Best BSOA Showcase:
    #
    #   - Its OBVIOUS solution is DP: "try every split point, memoize".
    #     That's O(n^2 * m). Not incorrect — just unnecessary.
    #
    #   - The BSOA reframing is non-obvious: "what if we GUESSED the
    #     answer and checked?" That check is a one-loop greedy.
    #
    # This is the kind of pattern-recognition that separates a good
    # solution from a great one. Every "minimize the maximum X" or
    # "maximize the minimum X" problem is a candidate for BSOA —
    # always check before reaching for DP.
    # ---------------------------------------------------------------
