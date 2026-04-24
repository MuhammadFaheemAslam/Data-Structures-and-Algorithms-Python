"""
Problem: Partition Equal Subset Sum

Difficulty: Medium (LeetCode #416)

---------------------------------------------------
Problem Statement:

Given a non-empty array of POSITIVE integers, can you partition the
array into TWO SUBSETS whose sums are EQUAL?

Example:
    [1, 5, 11, 5]       → True     ({1, 5, 5} and {11})
    [1, 2, 3, 5]        → False     (total 11 — odd, can't split)

---------------------------------------------------
Why It's A Knapsack Problem:

If total sum is `S`, we need one subset summing to `S / 2`. That's
the classic SUBSET-SUM question: "can I pick some items to hit
EXACTLY this target?"

    State:       dp[c] = True iff some subset sums to c
    Transition:  for each x in nums: dp[c] = dp[c] or dp[c - x]
    Target:      dp[S/2]

Iterate capacity BACKWARDS (0/1 semantics — each element used at most once).

Short-circuit: if `S` is ODD, return False immediately.

---------------------------------------------------
Complexity:

    Time:  O(n · S/2)           S = sum(nums)
    Space: O(S/2)
"""


def can_partition(nums):
    """
    True iff nums can be split into two equal-sum subsets.

    Time: O(n · S), Space: O(S).
    """
    S = sum(nums)
    if S % 2:
        return False

    target = S // 2
    dp = [False] * (target + 1)
    dp[0] = True                                            # empty subset sums to 0

    for x in nums:
        # Backward iteration — 0/1 knapsack semantics
        for c in range(target, x - 1, -1):
            if dp[c - x]:
                dp[c] = True
                if c == target:
                    return True                             # early exit

    return dp[target]


# -------- Bitmask variant — concise and fast --------

def can_partition_bitmask(nums):
    """
    Same idea using a single Python int as a bitmask.

    Bit `c` of `bits` is 1 iff some subset has sum `c`. For each x,
    we OR-in (bits << x): this adds x to every currently-reachable sum.

    Time: O(n · S / 64) in practice (big-int shift amortizes)
    Space: O(S / 8) bits of int
    """
    S = sum(nums)
    if S % 2:
        return False
    target = S // 2

    bits = 1                                                # only sum 0 reachable
    for x in nums:
        bits |= bits << x

    return (bits >> target) & 1 == 1


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #416 examples
    assert can_partition([1, 5, 11, 5]) is True
    assert can_partition([1, 2, 3, 5]) is False

    # Trivial
    assert can_partition([1, 1]) is True
    assert can_partition([2]) is False                      # sum odd in terms of split
    # Actually [2] total = 2, half = 1, but no subset sums to 1 → False
    assert can_partition([2, 2]) is True
    assert can_partition([1]) is False

    # Odd total: always false
    assert can_partition([1, 1, 1]) is False

    # All zeros (but problem says POSITIVE, so this is just a sanity check)
    # Let's use small positives that sum to a power of 2
    assert can_partition([1, 1, 3, 3]) is True              # {1,3} vs {1,3}
    assert can_partition([1, 2, 3, 4, 5, 6, 7]) is True     # sum 28, half 14: {7,6,1} = 14, other = 14

    # Large but checkable
    nums = [3, 3, 3, 4, 5]
    assert can_partition(nums) is True                      # 9 + 9 = 18? sum is 18. {3,3,3} = 9 and {4,5} = 9.

    # Stress: both methods agree
    import random
    random.seed(42)
    for _ in range(200):
        n = random.randint(1, 15)
        nums = [random.randint(1, 20) for _ in range(n)]
        assert can_partition(nums) == can_partition_bitmask(nums)

    # Brute force: enumerate subsets
    def brute(nums):
        S = sum(nums)
        if S % 2:
            return False
        target = S // 2
        n = len(nums)
        for mask in range(1 << n):
            s = sum(nums[i] for i in range(n) if (mask >> i) & 1)
            if s == target:
                return True
        return False

    for _ in range(100):
        n = random.randint(1, 12)
        nums = [random.randint(1, 20) for _ in range(n)]
        assert can_partition(nums) == brute(nums)
        assert can_partition_bitmask(nums) == brute(nums)

    # Timing: bitmask is often faster in practice on large inputs
    import time
    big = [random.randint(1, 100) for _ in range(200)]
    if sum(big) % 2:
        big.append(1)

    t0 = time.time()
    for _ in range(100):
        can_partition(big)
    t_dp = time.time() - t0

    t0 = time.time()
    for _ in range(100):
        can_partition_bitmask(big)
    t_bits = time.time() - t0

    print(f"Partition on n=200:")
    print(f"   boolean DP:   {t_dp * 1000:6.1f} ms (100 runs)")
    print(f"   bitmask:      {t_bits * 1000:6.1f} ms (100 runs)")
    print(f"   speedup: {t_dp / t_bits:.1f}×")

    print("\nAll tests passed!")
