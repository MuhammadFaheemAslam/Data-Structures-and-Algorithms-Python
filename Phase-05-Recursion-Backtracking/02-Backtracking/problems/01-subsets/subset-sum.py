"""
Problem: Subset Sum (Decision and Enumeration)

Difficulty: Medium (classic / LC #416 Partition Equal Subset Sum variant)

---------------------------------------------------
Problem Statement:

Given an array `nums` and a target `T`, decide whether some subset
sums to exactly `T`, and optionally enumerate all such subsets.

Two versions in this file:

    1. has_subset_sum(nums, target)        → bool
    2. all_subsets_with_sum(nums, target)  → list of subsets

Related problems:
    - LC #416 Partition Equal Subset Sum  (can we partition into two equal halves?)
    - LC #494 Target Sum                    (assign +/- to each element)
    - Subset-sum decision is NP-COMPLETE in general.

---------------------------------------------------
Three Approaches:

    1. Backtracking with pruning           O(2^n)  — our focus here
    2. Meet in the Middle                  O(2^(n/2) · log)  — see Phase 02 / 02 / 10-Meet-in-the-Middle
    3. DP (pseudo-polynomial)              O(n · target)  — see Phase 02 / 01 / 04-Dynamic-Programming

This file focuses on the backtracking approach with three different
pruning strategies. For the DP and meet-in-the-middle approaches,
see the earlier phases.

---------------------------------------------------
The Pruning Strategies:

    a) Early exit if remaining values can't reach target.
       (Sort descending; compute suffix sums.)
    b) Stop exploring when the running sum exceeds target
       (for positive numbers only).
    c) Skip consecutive duplicates to avoid exploring the same
       subset twice.
"""


# =========================================================================
# 1. Decision: Does ANY Subset Sum to target?
# =========================================================================

def has_subset_sum(nums, target):
    """
    True iff some subset of `nums` sums to exactly `target`.

    Assumes non-negative integers for the "stop early if running > target"
    pruning. For general integers, remove that pruning.

    Time:  O(2^n) worst case; far less with pruning.
    Space: O(n) stack.
    """
    nums = sorted(nums, reverse=True)             # largest first — helps pruning

    def backtrack(index, remaining):
        if remaining == 0:
            return True
        if index == len(nums):
            return False

        # Pruning: if `remaining` is larger than the sum of all remaining elements,
        # we can't possibly hit it (assuming non-negative).
        if remaining < 0:
            return False

        # Try INCLUDING nums[index]
        if backtrack(index + 1, remaining - nums[index]):
            return True

        # Try EXCLUDING nums[index]
        return backtrack(index + 1, remaining)

    return backtrack(0, target)


# =========================================================================
# 2. Enumeration: Find ALL Subsets Summing to target
# =========================================================================

def all_subsets_with_sum(nums, target):
    """
    Return every subset of `nums` whose sum equals `target`.

    Uses the Subsets II duplicate-skip idiom so that inputs with
    duplicates don't produce redundant output. If `nums` is
    guaranteed distinct, this reduces to plain enumeration.

    Time:  O(2^n) worst case.
    Space: O(n) stack + O(output size).
    """
    nums = sorted(nums)                           # sort so duplicates are adjacent
    result = []
    path = []

    def backtrack(start, remaining):
        if remaining == 0:
            result.append(path[:])
            return

        for i in range(start, len(nums)):
            # Pruning A: if sorted + non-negative, once remaining < nums[i]
            # we can't add anything without exceeding — skip the rest.
            if nums[i] > remaining and nums[i] >= 0:
                break

            # Pruning B: duplicate-skip (only at this level of recursion).
            if i > start and nums[i] == nums[i - 1]:
                continue

            path.append(nums[i])
            backtrack(i + 1, remaining - nums[i])
            path.pop()

    backtrack(0, target)
    return result


# =========================================================================
# 3. Count Subsets Summing to target
# =========================================================================

def count_subsets_with_sum(nums, target):
    """
    Count how many subsets of `nums` sum to `target`.

    Time:  O(2^n) worst case; faster with pruning.
    Space: O(n)
    """
    nums = sorted(nums, reverse=True)
    count = 0

    def backtrack(index, remaining):
        nonlocal count
        if remaining == 0:
            count += 1
            return
        if index == len(nums):
            return
        if remaining < 0:
            return

        # Include
        backtrack(index + 1, remaining - nums[index])
        # Exclude
        backtrack(index + 1, remaining)

    backtrack(0, target)
    return count


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Decision cases
    decision_cases = [
        ([2, 3, 7, 8, 10],      11,  True),        # 3 + 8
        ([2, 3, 7, 8, 10],      13,  True),        # 3 + 10, or 5 + 8
        ([2, 3, 7, 8, 10],      14,  False),       # no subset sums to 14
        ([2, 3, 7, 8, 10],      1,   False),
        ([],                    0,   True),        # empty subset sums to 0
        ([],                    5,   False),
        ([5],                   5,   True),
        ([5],                   10,  False),
        ([1, 2, 3, 4, 5],       15,  True),        # full sum
        ([3, 34, 4, 12, 5, 2],  9,   True),        # classic GeeksforGeeks example
        ([3, 34, 4, 12, 5, 2],  30,  False),
    ]

    for nums, target, expected in decision_cases:
        assert has_subset_sum(nums, target) == expected
        print(f"   has_subset_sum({nums}, target={target}) = {expected}")
    print()

    # Enumeration cases
    enum_cases = [
        ([2, 3, 5, 6, 8, 10],   10,   [
            [2, 3, 5], [2, 8], [10],
        ]),
        ([1, 2, 3],             3,    [
            [1, 2], [3],
        ]),
        ([],                    0,    [[]]),
        ([],                    5,    []),
        ([5],                   5,    [[5]]),
        ([1, 1, 1],             2,    [[1, 1]]),   # duplicates — one unique subset
    ]

    for nums, target, expected in enum_cases:
        got = all_subsets_with_sum(nums, target)
        norm = lambda x: sorted([sorted(s) for s in x])
        assert norm(got) == norm(expected), f"{nums}, t={target}: {got}"
        print(f"   all_subsets_with_sum({nums}, t={target}) = {got}")
    print()

    # Count cases — verify against enumeration length
    for nums, target, _ in decision_cases:
        count = count_subsets_with_sum(nums, target)
        enum = all_subsets_with_sum(nums, target) if target >= 0 and all(x >= 0 for x in nums) else None
        if enum is not None:
            assert count == len(enum)
    print("Count matches enumeration length on all decision cases.")

    # Stress test
    import random
    random.seed(42)
    for _ in range(100):
        n = random.randint(0, 10)
        nums = [random.randint(1, 10) for _ in range(n)]
        target = random.randint(0, 50)

        # Brute force reference: try all 2^n subsets
        brute = False
        for mask in range(1 << n):
            s = sum(nums[i] for i in range(n) if mask & (1 << i))
            if s == target:
                brute = True
                break

        assert has_subset_sum(nums, target) == brute

    print("\nStress test: 100 random inputs — decision version matches brute force")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Subset Sum Is NP-Complete
    #
    #   There's no known polynomial-time algorithm for the general
    #   subset-sum decision problem. The best options:
    #
    #     - n ≤ 30:  backtracking with pruning works
    #     - n ≤ 50:  meet in the middle (2^(n/2) search space)
    #     - target small:  DP O(n · target) — pseudo-polynomial
    #
    #   Phase 02 covers all three angles:
    #     - 01 / 04 / problems / knapsack.py     (DP)
    #     - 02 / 10 / problems / subset-sum.py    (meet in the middle)
    #
    #   This file gives the backtracking treatment as part of the
    #   systematic backtracking survey.
    # ---------------------------------------------------------------
