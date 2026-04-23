"""
Problem: Generate All Subsets

Difficulty: Medium (LeetCode #78)

---------------------------------------------------
Problem Statement:

Given an integer array `nums` of DISTINCT elements, return ALL
possible subsets (the power set). The solution set must not contain
duplicate subsets.

    nums = [1, 2, 3]
    output = [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]

Total count: 2^n. For n = 20 → ~1 million; for n = 30 → 1 billion.

---------------------------------------------------
Four Approaches:

    1. Backtracking (include/exclude)     ← template
    2. Backtracking (subset-as-prefix)    ← every recursion visits a valid subset
    3. Iterative (build up)                ← start with [[]]; double on each new element
    4. Bitmask enumeration                 ← 2^n integers as subset indicators

All O(n · 2^n) time. Different implementations; same result.
"""


# =========================================================================
# 1. Backtracking via Include/Exclude (The Template Form)
# =========================================================================

def subsets_include_exclude(nums):
    """
    At each index, DECIDE whether to include nums[i] in the current subset.
    Two recursive branches per index → 2^n total leaf nodes.

    Time:  O(n · 2^n)
    Space: O(n) stack
    """
    result = []
    path = []

    def backtrack(index):
        if index == len(nums):
            result.append(path[:])                 # snapshot
            return

        # EXCLUDE nums[index]
        backtrack(index + 1)

        # INCLUDE nums[index]
        path.append(nums[index])
        backtrack(index + 1)
        path.pop()                                 # un-choose

    backtrack(0)
    return result


# =========================================================================
# 2. Backtracking via "Subset-As-Prefix" (Also Valid)
# =========================================================================

def subsets_prefix_form(nums):
    """
    Walk indices forward. At each step, the CURRENT path IS a valid
    subset (record it immediately). Then try extending with each
    remaining element.

    Same Big-O, different traversal order.

    Time:  O(n · 2^n)
    """
    result = []
    path = []

    def backtrack(start):
        # EVERY prefix is a valid subset — record as we go
        result.append(path[:])

        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1)
            path.pop()

    backtrack(0)
    return result


# =========================================================================
# 3. Iterative — Double the Result List on Each New Element
# =========================================================================

def subsets_iterative(nums):
    """
    Start with [[]] (one empty subset). For each new element x, double
    the result list by producing, for every existing subset, a COPY
    with x appended.

    Time:  O(n · 2^n)
    Space: O(n · 2^n)

    Elegantly simple. Doesn't use recursion at all — gets O(2^n)
    subsets by doubling k times.
    """
    result = [[]]
    for x in nums:
        # Extend result with each subset + x
        result = result + [s + [x] for s in result]
    return result


# =========================================================================
# 4. Bitmask Enumeration
# =========================================================================

def subsets_bitmask(nums):
    """
    Enumerate integers 0 through 2^n - 1. Each integer's bit pattern
    encodes which elements of `nums` are in that subset.

    Time:  O(n · 2^n)
    Space: O(n · 2^n) output

    Beyond pedagogical — this is how CPython-level bitmask-DP works
    (Phase 02 / 02 / 11-Bit-Manipulation).
    """
    n = len(nums)
    result = []
    for mask in range(1 << n):
        subset = [nums[i] for i in range(n) if mask & (1 << i)]
        result.append(subset)
    return result


# =========================================================================
# Test
# =========================================================================

def _normalize(subsets):
    """Sort subsets for comparison (order-independent)."""
    return sorted([sorted(s) for s in subsets])


if __name__ == "__main__":
    cases = [
        [1, 2, 3],
        [],
        [1],
        [0],
        [9, 0, 3, 5, 7],
    ]

    for nums in cases:
        a = subsets_include_exclude(nums)
        b = subsets_prefix_form(nums)
        c = subsets_iterative(nums)
        d = subsets_bitmask(nums)

        expected_count = 2 ** len(nums)
        assert len(a) == len(b) == len(c) == len(d) == expected_count

        na, nb, nc, nd = map(_normalize, (a, b, c, d))
        assert na == nb == nc == nd

        print(f"subsets({nums}): {len(a)} subsets (expected 2^{len(nums)} = {expected_count})")

    # Display sample
    print(f"\nsubsets([1, 2, 3]) = {subsets_include_exclude([1, 2, 3])}")

    # Timing comparison
    import time
    nums = list(range(18))                          # 2^18 = 262144 subsets

    for fn in (subsets_include_exclude, subsets_prefix_form,
               subsets_iterative, subsets_bitmask):
        t0 = time.time()
        out = fn(nums)
        elapsed = time.time() - t0
        print(f"   {fn.__name__:30}  n={len(nums)}:  {elapsed:.3f}s,  {len(out)} subsets")

    print("\nAll tests passed!")
