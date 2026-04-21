"""
Problem: Subset Sum

Technique: Meet in the Middle
Difficulty: NP-Hard in general; tractable via MITM for n ≤ ~40

---------------------------------------------------
Problem Statement:

Given an array `nums` (possibly containing negatives) and an integer
`target`, return True iff some SUBSET of `nums` sums to exactly `target`.

No length constraints on n. Values can be arbitrarily large (including
negative). In particular, DP's pseudo-polynomial bound O(n · T) is
useless when T is big (say, 10^15).

---------------------------------------------------
Why This Is the Canonical MITM Problem:

    Brute force:  O(2^n)         – unusable past n = 25
    DP:           O(n · |T|)     – pseudo-polynomial; fails when T is huge
    MITM:         O(n · 2^(n/2)) – usable up to n ≈ 40–50

MITM is the natural fit when:
    - n is small (≤ 40ish)
    - values can be large (breaks DP)
    - values can be negative (breaks standard DP)

The technique: split the array in half. Enumerate the 2^(n/2) subset
sums of each half. For each sum in the right half, look up whether the
left half produced `target - sum_right`. That's a hash-set lookup.

Total cost: O(n · 2^(n/2)). For n = 40 that's 40 · 10^6 ≈ 4·10^7 —
instant. For n = 50, ~1.5·10^9 — borderline but often feasible.

---------------------------------------------------
Example:

    nums = [3, 34, 4, 12, 5, 2], target = 9
    -> True     # {4, 5} sums to 9

    nums = [3, 34, 4, 12, 5, 2], target = 30
    -> False

    nums = [3, -4, 2, 5], target = 0
    -> True     # {3, -4, 2, -1?} — actually need to find a subset summing to 0.
                # {3 + 2 + (-5)} — not present. {−4 + 2 + something}?
                # {3, −4, 2, 5} — total 6. 6 - target 0 → need subset summing to 6.
                # {-4 + 5 + 2 + 3} = 6. Complement of that is the empty set (sum 0). So yes.
                # Or simpler: subset {3 + (−4) + 5 + (−?)} … the empty subset sums to 0.
                # So True trivially.

    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], target = 55
    -> True     # the whole array

---------------------------------------------------
"""

import math


# -------------------------------------------------
# Approach 1: Meet in the Middle
# -------------------------------------------------

def has_subset_sum_mitm(nums, target):
    """
    Meet-in-the-middle subset-sum solver.

    Time Complexity:  O(n * 2^(n/2))
    Space Complexity: O(2^(n/2))
    """
    n = len(nums)
    if n == 0:
        return target == 0

    mid = n // 2
    left = nums[:mid]
    right = nums[mid:]

    # Enumerate all subset sums of the LEFT half into a set (for O(1)
    # lookup). Done iteratively so we don't allocate 2^n intermediate
    # structures.
    left_sums = {0}
    for x in left:
        left_sums |= {s + x for s in left_sums}

    # For each subset sum of the right half, check whether the
    # complement exists in left_sums.
    right_sums = [0]
    for x in right:
        right_sums = right_sums + [s + x for s in right_sums]

    for sb in right_sums:
        if (target - sb) in left_sums:
            return True

    return False


# -------------------------------------------------
# Approach 2: Brute Force (For Verification, n ≤ 20)
# -------------------------------------------------

def has_subset_sum_brute(nums, target):
    """
    Enumerate every subset via bitmask. O(n * 2^n).
    """
    n = len(nums)
    for mask in range(1 << n):
        s = 0
        for k in range(n):
            if mask & (1 << k):
                s += nums[k]
        if s == target:
            return True
    return False


# -------------------------------------------------
# Approach 3: Dynamic Programming (Pseudo-Polynomial, Positives Only)
# -------------------------------------------------

def has_subset_sum_dp(nums, target):
    """
    Classical DP: dp[i][s] = can we make sum `s` using the first i items?

    Time Complexity:  O(n * |range of sums|)
    Space Complexity: O(|range of sums|)

    Works well when the SUM range is small (e.g., target ≤ 10^5). Fails
    catastrophically when target is huge.

    Handles negatives by shifting: we offset sums so the minimum possible
    sum maps to index 0.
    """
    min_sum = sum(x for x in nums if x < 0)
    max_sum = sum(x for x in nums if x > 0)

    if target < min_sum or target > max_sum:
        return False

    width = max_sum - min_sum + 1
    dp = [False] * width
    dp[0 - min_sum] = True            # the empty subset produces sum 0

    for x in nums:
        # iterate in a direction that prevents double-counting
        if x > 0:
            # fill right-to-left (so we don't reuse items)
            for s in range(max_sum, min_sum - 1, -1):
                prev = s - x
                if min_sum <= prev <= max_sum and dp[prev - min_sum]:
                    dp[s - min_sum] = True
        else:
            # fill left-to-right
            for s in range(min_sum, max_sum + 1):
                prev = s - x
                if min_sum <= prev <= max_sum and dp[prev - min_sum]:
                    dp[s - min_sum] = True

    return dp[target - min_sum]


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    # Classic Examples
    print(f"has_subset_sum_mitm([3,34,4,12,5,2], 9)  = {has_subset_sum_mitm([3, 34, 4, 12, 5, 2], 9)}")
    print(f"has_subset_sum_mitm([3,34,4,12,5,2], 30) = {has_subset_sum_mitm([3, 34, 4, 12, 5, 2], 30)}")
    print()

    # Test cases — (nums, target, expected)
    test_cases = [
        # Standard positives
        ([3, 34, 4, 12, 5, 2],       9,   True),      # {4, 5}
        ([3, 34, 4, 12, 5, 2],       30,  False),
        ([3, 34, 4, 12, 5, 2],       0,   True),      # empty subset
        ([3, 34, 4, 12, 5, 2],       60,  60 == sum([3, 34, 4, 12, 5, 2])),

        # Negatives
        ([3, -4, 2, 5],              0,   True),
        ([3, -4, 2, 5],              -4,  True),
        ([-1, -2, -3],               -5,  True),      # {-2, -3}
        ([-1, -2, -3],               1,   False),

        # Edge cases
        ([],                         0,   True),      # empty subset sums to 0
        ([],                         5,   False),
        ([7],                        7,   True),
        ([7],                        0,   True),
        ([7],                        3,   False),

        # Single solution requires all elements
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 55, True),

        # Large solution / negatives mix
        ([10, 20, -15, 30, 5],       25,  True),      # {10, 20, -15, ? } — 10+20-15 = 15; 30-5 = 25 ✓
        ([10, 20, -15, 30, 5],       100, False),     # total is 50
    ]

    for i, (nums, target, expected) in enumerate(test_cases):
        # MITM
        got_mitm = has_subset_sum_mitm(nums, target)
        assert got_mitm == expected, (
            f"Test {i+1} (MITM) failed on {nums}, target={target}: "
            f"expected {expected}, got {got_mitm}"
        )

        # Brute force — only for small inputs
        if len(nums) <= 20:
            got_bf = has_subset_sum_brute(nums, target)
            assert got_bf == expected, (
                f"Test {i+1} (brute): expected {expected}, got {got_bf}"
            )

        # DP — only when the sum range is reasonable
        min_s = sum(x for x in nums if x < 0)
        max_s = sum(x for x in nums if x > 0)
        if max_s - min_s <= 1000:
            got_dp = has_subset_sum_dp(nums, target)
            assert got_dp == expected, (
                f"Test {i+1} (DP): expected {expected}, got {got_dp}"
            )

        print(f"Test {i+1} passed: len={len(nums)}, target={target} -> {expected}")

    # Stress test: random n = 15 inputs against brute force
    import random
    random.seed(3)
    for trial in range(100):
        n = random.randint(0, 15)
        nums = [random.randint(-20, 20) for _ in range(n)]
        target = random.randint(-100, 100)

        mitm = has_subset_sum_mitm(nums, target)
        bf = has_subset_sum_brute(nums, target)
        assert mitm == bf, f"Stress #{trial}: nums={nums}, target={target}: MITM={mitm}, brute={bf}"
    print("\nStress test: 100 random n≤15 inputs matched brute force")

    # Large-n demonstration — something brute force could NEVER do
    # n = 40, random values, target = sum / 2
    random.seed(99)
    big_n = 40
    big_nums = [random.randint(1, 10**6) for _ in range(big_n)]
    big_target = sum(big_nums) // 2

    got = has_subset_sum_mitm(big_nums, big_target)
    print(f"\nLarge-n demo: n={big_n}, target≈{big_target}")
    print(f"   has_subset_sum_mitm = {got}")
    print(f"   (brute force would be 2^40 ≈ 10^12 ops — infeasible)")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Three Regimes:
    #
    #                              time        space        best when
    #   brute force                O(n · 2^n)  O(1)         n ≤ 25
    #   DP (pseudo-polynomial)     O(n · T)    O(T)         T is small
    #   meet in the middle         O(n · 2^(n/2)) O(2^(n/2)) n ≤ 50, T is huge
    #
    # Subset Sum is the canonical example of a problem where the right
    # algorithm depends entirely on WHICH INPUT IS BIG.
    # ---------------------------------------------------------------
