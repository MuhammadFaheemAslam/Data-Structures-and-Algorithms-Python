"""
Problem: Permutations With Duplicates

Difficulty: Medium (LeetCode #47)

---------------------------------------------------
Problem Statement:

Given an array `nums` that MAY contain duplicates, return all
UNIQUE permutations.

    nums = [1, 1, 2]
    output = [[1, 1, 2], [1, 2, 1], [2, 1, 1]]

Without duplicate-handling, we'd get 3! = 6 permutations (each
with two internal variants of the 1's), which after deduplication
collapse to just 3.

---------------------------------------------------
The Key Insight:

The duplicate-skip rule is similar to Subsets II but with a twist.
Sort the input so duplicates are adjacent. Then at each recursion
level, **skip `nums[i]` if it equals `nums[i-1]` AND `nums[i-1]`
is NOT currently used.**

    for i in range(n):
        if used[i]: continue
        if i > 0 and nums[i] == nums[i-1] and not used[i-1]:
            continue             ← duplicate-skip

Why `not used[i-1]`? Because when we're deciding whether to use
`nums[i]`, its duplicate predecessor `nums[i-1]` is either:

    (a) already in our path (`used[i-1] == True`):
        different POSITION, same value. This is a genuinely new
        permutation (e.g., [1_a, 1_b, 2] vs [1_a, 1_b, 2]... wait,
        same). Actually if `nums[i-1]` is used and we use `nums[i]`,
        we're placing two copies of the value in the path at DIFFERENT
        positions, which is fine.
    (b) NOT yet in our path (`used[i-1] == False`):
        we've already EXPLORED the branch where `nums[i-1]` was used
        at this position. Using `nums[i]` here generates the SAME
        permutation prefix. Skip.

The `not used[i-1]` condition captures "have we already tried this
value at this position?" If the PREVIOUS duplicate is available and
we already skipped it, we've already done this work.

---------------------------------------------------
"""


# =========================================================================
# Backtracking with Duplicate Skip
# =========================================================================

def permute_unique(nums):
    """
    Generate all UNIQUE permutations of `nums` (with possible duplicates).

    Time:  O(n · n!)   worst case; often far less when many duplicates
    Space: O(n) stack
    """
    nums = sorted(nums)                           # essential — duplicates adjacent
    result = []
    path = []
    used = [False] * len(nums)

    def backtrack():
        if len(path) == len(nums):
            result.append(path[:])
            return

        for i in range(len(nums)):
            if used[i]:
                continue

            # DUPLICATE SKIP: if nums[i] equals nums[i-1] and nums[i-1]
            # is NOT currently used, skip — we've already tried this
            # value at this position via the i-1 branch.
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue

            path.append(nums[i])
            used[i] = True

            backtrack()

            path.pop()
            used[i] = False

    backtrack()
    return result


# =========================================================================
# Alternative: Count-Based Approach
# =========================================================================

def permute_unique_counting(nums):
    """
    Group by value; at each step, pick a value whose COUNT is > 0,
    decrement its count, recurse, restore.

    Equivalent output to permute_unique; different decision tree.

    Time:  O(n · n! / (k1! · k2! · ...))   where kᵢ are group sizes
    Space: O(n) stack + O(n) counter

    Often the cleanest implementation in practice — avoids sorting
    and the `used[]` + duplicate-skip gymnastics.
    """
    from collections import Counter

    counts = Counter(nums)
    n = len(nums)
    result = []
    path = []

    def backtrack():
        if len(path) == n:
            result.append(path[:])
            return

        for value in counts:
            if counts[value] == 0:
                continue

            path.append(value)
            counts[value] -= 1

            backtrack()

            path.pop()
            counts[value] += 1

    backtrack()
    return result


# =========================================================================
# Brute Force: Generate All Permutations, Dedupe
# =========================================================================

def permute_unique_brute(nums):
    """
    Generate n! permutations, then dedupe via a set.

    Time:  O(n · n! · log(n!)) for the set insertion
    Space: O(n · n!) for the set

    Slow on inputs with many duplicates. Used for validation only.
    """
    from itertools import permutations
    return [list(p) for p in set(permutations(nums))]


# =========================================================================
# Test
# =========================================================================

def _normalize(perms):
    return sorted(tuple(p) for p in perms)


if __name__ == "__main__":
    cases = [
        ([1, 1, 2],           3),
        ([1, 2, 3],           6),               # all distinct → full 3!
        ([1, 1, 1],           1),               # all same → only 1 unique
        ([],                  1),               # empty → one "empty" permutation
        ([5],                 1),
        ([1, 1, 2, 2],        6),               # 4!/(2!·2!) = 6
    ]

    for nums, expected_count in cases:
        a = permute_unique(nums)
        b = permute_unique_counting(nums)
        c = permute_unique_brute(nums)

        assert len(a) == len(b) == len(c) == expected_count
        assert _normalize(a) == _normalize(b) == _normalize(c)
        print(f"   permute_unique({nums}) → {expected_count} unique permutations")
    print()

    # Sample
    print(f"permute_unique([1, 1, 2]) = {permute_unique([1, 1, 2])}")

    # Stress test
    import random
    random.seed(42)
    for _ in range(50):
        n = random.randint(0, 6)
        nums = [random.randint(0, 2) for _ in range(n)]
        a = _normalize(permute_unique(nums))
        b = _normalize(permute_unique_counting(nums))
        c = _normalize(permute_unique_brute(nums))
        assert a == b == c

    print("\nStress test: 50 random arrays — all three approaches agree")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The `not used[i-1]` Check — An Easy-to-Mess-Up Detail:
    #
    #   Without it:   we'd skip genuine permutations that should exist.
    #   With wrong condition (used[i-1] instead of not used[i-1]):
    #                  we'd generate duplicates.
    #
    # The rule of thumb: think of duplicates as "indistinguishable."
    # We should only USE a later copy of a value AFTER we've already
    # used the EARLIER copy. That's what `not used[i-1]` enforces.
    # ---------------------------------------------------------------
