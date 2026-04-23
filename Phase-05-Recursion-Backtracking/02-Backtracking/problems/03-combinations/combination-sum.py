"""
Problem: Combination Sum

Difficulty: Medium (LeetCode #39)

---------------------------------------------------
Problem Statement:

Given DISTINCT positive integers `candidates` and a target `T`,
return all UNIQUE COMBINATIONS that sum to `T`. Each number may be
used an UNLIMITED number of times.

    candidates = [2, 3, 6, 7],  target = 7
    output = [[2, 2, 3], [7]]

Two combinations are the same iff they have the same MULTISET of
numbers (order doesn't matter; [2, 3, 2] and [2, 2, 3] are the same).

---------------------------------------------------
Key Twist vs Subsets/Permutations:

This is the first problem where an element can be **REUSED**. On
subsets, each element is used at most once. Here, you can use `2`
as many times as you want.

The template change: when you pick `candidates[i]` and recurse,
you recurse with `start = i` (not `i + 1`), allowing the same
element to be chosen again at the next level.

    for i in range(start, len(candidates)):
        path.append(candidates[i])
        backtrack(i, ...)                 # ← i, not i+1 (REUSE allowed)
        path.pop()

---------------------------------------------------
Complexity:

    Time:  O(N^(T/M)) where N = len(candidates), M = min(candidates)
    Space: O(T/M) recursion depth

It's exponential in (T / min_candidate) — reasonable for interview-
sized inputs (T ≤ ~150, N ≤ ~30 per LC constraints).
"""


# =========================================================================
# Backtracking with Pruning
# =========================================================================

def combination_sum(candidates, target):
    """
    Find all combinations summing to `target`, allowing repeated use.

    Time:  O(N^(T/M))
    Space: O(T/M) stack + O(output size)
    """
    candidates = sorted(candidates)               # sort → enables pruning
    result = []
    path = []

    def backtrack(start, remaining):
        if remaining == 0:
            result.append(path[:])
            return

        for i in range(start, len(candidates)):
            c = candidates[i]

            # PRUNING: since sorted, once c > remaining, no further choice fits
            if c > remaining:
                break

            path.append(c)
            # REUSE allowed — pass `i`, not `i + 1`
            backtrack(i, remaining - c)
            path.pop()

    backtrack(0, target)
    return result


# =========================================================================
# Alternative Phrasing: Decide "How Many Copies of Each"
# =========================================================================

def combination_sum_counting(candidates, target):
    """
    Instead of "pick one, recurse," decide HOW MANY copies of each
    candidate to include.

    Same Big-O; cleaner for some problems.
    """
    candidates = sorted(candidates)
    result = []
    path = []

    def backtrack(index, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        if index == len(candidates):
            return

        c = candidates[index]
        # Decide: take 0, 1, 2, …, floor(remaining / c) copies
        max_copies = remaining // c
        for k in range(max_copies + 1):
            for _ in range(k):
                path.append(c)
            backtrack(index + 1, remaining - k * c)
            for _ in range(k):
                path.pop()

    backtrack(0, target)
    return result


# =========================================================================
# Test
# =========================================================================

def _normalize(combos):
    return sorted([sorted(c) for c in combos])


if __name__ == "__main__":
    cases = [
        ([2, 3, 6, 7],      7,  [[2, 2, 3], [7]]),
        ([2, 3, 5],         8,  [[2, 2, 2, 2], [2, 3, 3], [3, 5]]),
        ([2],               1,  []),                             # impossible
        ([1],               3,  [[1, 1, 1]]),
        ([1, 2],            3,  [[1, 1, 1], [1, 2]]),
        ([8, 7, 4, 3],      11, [[3, 4, 4], [3, 8], [4, 7]]),
    ]

    for cands, target, expected in cases:
        a = combination_sum(cands, target)
        b = combination_sum_counting(cands, target)

        norm_expected = _normalize(expected)
        assert _normalize(a) == norm_expected
        assert _normalize(b) == norm_expected
        print(f"   combination_sum({cands}, t={target}) = {_normalize(a)}")

    # Stress test
    import random
    random.seed(42)
    for _ in range(50):
        cands = random.sample(range(1, 15), random.randint(1, 5))
        target = random.randint(1, 20)
        a = _normalize(combination_sum(cands, target))
        b = _normalize(combination_sum_counting(cands, target))
        assert a == b

    print("\nStress test: 50 random inputs — both formulations agree")

    print("\nAll tests passed!")
