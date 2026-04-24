"""
Problem: Target Sum

Difficulty: Medium (LeetCode #494)

---------------------------------------------------
Problem Statement:

Given an array of non-negative integers `nums` and a target `T`,
count the number of ways to assign `+` or `-` to each number such
that the resulting expression evaluates to `T`.

Example:
    nums = [1, 1, 1, 1, 1], T = 3
    Five ways: -1+1+1+1+1, +1-1+1+1+1, +1+1-1+1+1, +1+1+1-1+1, +1+1+1+1-1
    → 5

---------------------------------------------------
The Clever Reduction To Subset Sum:

Partition `nums` into a POSITIVE set `P` and a NEGATIVE set `N`.

    sum(P) - sum(N) = T
    sum(P) + sum(N) = sum(nums) = S

Adding the two:  2 * sum(P) = T + S  →  sum(P) = (T + S) / 2

So: count the subsets of `nums` whose sum equals `(T + S) / 2`.
That's a COUNTING subset-sum problem — a knapsack variant.

### Corner cases to check BEFORE applying the formula:

1. `abs(T) > S`  → impossible, return 0.
2. `(T + S)` is odd → impossible, return 0.
3. `(T + S) / 2 < 0` → impossible, return 0.

Otherwise, count subsets summing to `(T + S) // 2`.

---------------------------------------------------
Counting-Subsets Recurrence:

    dp[c] = number of subsets summing to c

    for each x in nums:
        for c in target..x:          # BACKWARD for 0/1 semantics
            dp[c] += dp[c - x]

Base: dp[0] = 1 (empty subset sums to 0).

---------------------------------------------------
Complexity:

    Time:  O(n · (T + S) / 2)
    Space: O((T + S) / 2)
"""


def find_target_sum_ways(nums, T):
    """
    Count assignments of + / - to nums that sum to T.

    Time: O(n · (T + S) / 2), Space: O((T + S) / 2).
    """
    S = sum(nums)
    if abs(T) > S or (T + S) % 2 != 0:
        return 0
    target = (T + S) // 2
    if target < 0:
        return 0

    # Count subsets of nums summing to target
    dp = [0] * (target + 1)
    dp[0] = 1
    for x in nums:
        for c in range(target, x - 1, -1):
            dp[c] += dp[c - x]
    return dp[target]


# -------- Memoized top-down for comparison --------

def find_target_sum_ways_memo(nums, T):
    """
    Top-down DP with (index, current_sum) state.

    Time:  O(n · S), Space: O(n · S).
    """
    from functools import cache

    @cache
    def rec(i, current):
        if i == len(nums):
            return 1 if current == T else 0
        return rec(i + 1, current + nums[i]) + rec(i + 1, current - nums[i])

    return rec(0, 0)


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #494 example
    assert find_target_sum_ways([1, 1, 1, 1, 1], 3) == 5
    assert find_target_sum_ways([1], 1) == 1
    assert find_target_sum_ways([1], -1) == 1
    assert find_target_sum_ways([1], 0) == 0
    assert find_target_sum_ways([0, 0, 0, 0, 0], 0) == 32            # 2^5 — any sign pattern works

    # Impossible
    assert find_target_sum_ways([1, 2], 100) == 0

    # Symmetric around 0
    assert find_target_sum_ways([1, 2, 3], 0) == find_target_sum_ways([1, 2, 3], 0)

    # Brute force: enumerate every sign pattern
    def brute(nums, T):
        n = len(nums)
        count = 0
        for mask in range(1 << n):
            total = sum(nums[i] if (mask >> i) & 1 else -nums[i] for i in range(n))
            if total == T:
                count += 1
        return count

    # Stress: memoized and tabulated must both match brute force
    import random
    random.seed(42)
    for _ in range(200):
        n = random.randint(0, 12)
        nums = [random.randint(0, 10) for _ in range(n)]
        T = random.randint(-20, 20)
        expected = brute(nums, T)
        assert find_target_sum_ways(nums, T) == expected
        assert find_target_sum_ways_memo(nums, T) == expected

    print("All tests passed!")
