"""
Problem: Subsets With Duplicates

Difficulty: Medium (LeetCode #90)

---------------------------------------------------
Problem Statement:

Given an array `nums` that MAY contain duplicates, return all
possible UNIQUE subsets.

    nums = [1, 2, 2]
    output = [[], [1], [2], [1, 2], [2, 2], [1, 2, 2]]

Note: `[1, 2]` appears only ONCE even though `nums` has two 2's.
Just one of them is enough to form `[1, 2]`; we don't want
`[1, 2a]` and `[1, 2b]` as distinct subsets.

---------------------------------------------------
The Duplicate-Skipping Trick:

Sort `nums` first so duplicates are adjacent. Then, during the
"extending subsets with new elements" loop, **skip any duplicate
that has the same value as the PREVIOUS element at the SAME level**
of the recursion tree:

    for i in range(start, len(nums)):
        if i > start and nums[i] == nums[i - 1]:
            continue                          # skip duplicate at this level
        path.append(nums[i])
        backtrack(i + 1)
        path.pop()

The key is `i > start` — NOT `i > 0`. This ensures we skip only
duplicates at the SAME RECURSION LEVEL (sibling calls); we still
USE duplicates at DEEPER levels (child calls). Otherwise we'd fail
to generate `[2, 2]` at all.

---------------------------------------------------
Why This Works:

Think of the search as a tree. At level 0 of the tree, the first
"2" starts a subtree that contains `[2]` and `[2, 2]`. A second "2"
at the same level would start a subtree containing `[2]` and
`[2, 2]` — EXACTLY THE SAME subtrees. So we skip it.

At a DEEPER level, a "2" that comes AFTER a previous "2" is a
NEW, DISTINCT choice (we're extending a subset that already has a 2
into one with two 2's).

The distinction is captured by `i > start` — "is this index the
FIRST one at this level?"

---------------------------------------------------
"""


# =========================================================================
# Backtracking with Sort + Duplicate Skip
# =========================================================================

def subsets_with_dup(nums):
    """
    Generate all UNIQUE subsets of `nums`, which may contain duplicates.

    Time:  O(n · 2^n) worst case; far less when there are many duplicates
    Space: O(n) stack + O(output size)
    """
    nums = sorted(nums)                           # essential: duplicates adjacent
    result = []
    path = []

    def backtrack(start):
        result.append(path[:])

        for i in range(start, len(nums)):
            # DUPLICATE-SKIP: if this is NOT the first choice at this
            # level, and it's the same as the previous, skip it.
            if i > start and nums[i] == nums[i - 1]:
                continue

            path.append(nums[i])
            backtrack(i + 1)
            path.pop()

    backtrack(0)
    return result


# =========================================================================
# Alternative: Counting Duplicates — How Many of Each Distinct Value to Take
# =========================================================================

def subsets_with_dup_counting(nums):
    """
    Alternative approach: group duplicates and decide "how many of
    this value to include" (0, 1, 2, ..., count).

    Equivalent output; different decision tree structure.

    Time:  O(n · 2^n) worst case, often much less
    """
    from collections import Counter

    counts = Counter(nums)
    items = sorted(counts.items())                 # [(value, count), ...]
    result = []
    path = []

    def backtrack(index):
        if index == len(items):
            result.append(path[:])
            return

        value, cnt = items[index]
        for take in range(cnt + 1):               # take 0, 1, …, cnt copies
            for _ in range(take):
                path.append(value)
            backtrack(index + 1)
            for _ in range(take):
                path.pop()

    backtrack(0)
    return result


# =========================================================================
# Reference: Brute Force via Set of Frozensets
# =========================================================================

def subsets_with_dup_brute(nums):
    """
    Generate all 2^n subsets (including duplicates), then dedupe via
    a set of sorted tuples.

    Time:  O(n · 2^n) and O(n · 2^n) for the set
    Space: O(n · 2^n)

    Used to validate the above approaches.
    """
    seen = set()
    n = len(nums)
    for mask in range(1 << n):
        subset = tuple(sorted(nums[i] for i in range(n) if mask & (1 << i)))
        seen.add(subset)
    return [list(s) for s in seen]


# =========================================================================
# Test
# =========================================================================

def _normalize(subsets):
    return sorted([tuple(sorted(s)) for s in subsets])


if __name__ == "__main__":
    cases = [
        ([1, 2, 2],                 6),             # [], [1], [2], [1,2], [2,2], [1,2,2]
        ([],                        1),             # just [[]]
        ([1],                       2),
        ([1, 1],                    3),             # [], [1], [1, 1]
        ([1, 1, 1],                 4),
        ([4, 4, 4, 1, 4],           10),
        ([1, 2, 3],                 8),             # all distinct → full 2^3
        ([0],                       2),
    ]

    for nums, expected_count in cases:
        a = subsets_with_dup(nums)
        b = subsets_with_dup_counting(nums)
        c = subsets_with_dup_brute(nums)

        assert len(a) == len(b) == len(c) == expected_count
        assert _normalize(a) == _normalize(b) == _normalize(c)

        print(f"subsets_with_dup({nums}) — {expected_count} unique")
    print()

    print(f"subsets_with_dup([1, 2, 2]):")
    for s in sorted(subsets_with_dup([1, 2, 2])):
        print(f"   {s}")

    # Stress test
    import random
    random.seed(42)
    for _ in range(50):
        n = random.randint(0, 8)
        nums = [random.randint(0, 3) for _ in range(n)]
        a = _normalize(subsets_with_dup(nums))
        b = _normalize(subsets_with_dup_counting(nums))
        c = _normalize(subsets_with_dup_brute(nums))
        assert a == b == c

    print("\nStress test: 50 random arrays — all three approaches agree")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Duplicate-Skip Idiom:
    #
    #   `if i > start and nums[i] == nums[i - 1]: continue`
    #
    #   This exact line appears in DOZENS of backtracking problems:
    #
    #     - Subsets II (LC #90)        ← this file
    #     - Permutations II (LC #47)   ← similar pattern with `used[]`
    #     - Combination Sum II (LC #40)
    #     - 3Sum (LC #15) — in the post-match advance
    #
    #   Master the `i > start` distinction; you'll never again
    #   produce duplicate solutions on problems where the input has
    #   repeats.
    # ---------------------------------------------------------------
