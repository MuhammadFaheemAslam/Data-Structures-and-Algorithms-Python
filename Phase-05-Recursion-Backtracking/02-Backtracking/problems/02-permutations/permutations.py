"""
Problem: Generate All Permutations

Difficulty: Medium (LeetCode #46)

---------------------------------------------------
Problem Statement:

Given an array `nums` of DISTINCT integers, return all n!
permutations in any order.

    nums = [1, 2, 3]
    output = [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]

---------------------------------------------------
The Template in Its Purest Form:

Permutations are the cleanest backtracking problem because the
template fits almost verbatim:

    state       = current (partial) permutation
    candidates  = all elements NOT YET used
    feasible    = always True
    apply       = add the chosen element
    revert      = remove it

Every backtracking problem in the next six modules is a variation
on this shape.

---------------------------------------------------
Complexity:

    Time:  O(n · n!)   — n! permutations, each O(n) to construct
    Space: O(n) stack + O(n · n!) output
"""


# =========================================================================
# 1. Canonical Backtracking with `used[]` Flag Array
# =========================================================================

def permute(nums):
    """
    Generate all permutations using a boolean `used[]` array to
    track which elements are already in the current path.

    Time:  O(n · n!)
    Space: O(n)
    """
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

            # CHOOSE
            path.append(nums[i])
            used[i] = True

            # EXPLORE
            backtrack()

            # UN-CHOOSE
            path.pop()
            used[i] = False

    backtrack()
    return result


# =========================================================================
# 2. Backtracking via In-Place Swapping (No Extra Memory)
# =========================================================================

def permute_swap(nums):
    """
    Generate permutations by SWAPPING in place. At each recursion
    level, swap index `i` with every index ≥ i (including itself).

    Time:  O(n · n!)
    Space: O(n) stack + no extra flags

    Avoids the `used[]` array. Produces permutations in a different
    order, but the same set.
    """
    result = []
    nums = list(nums)                             # mutable copy

    def backtrack(start):
        if start == len(nums):
            result.append(nums[:])
            return

        for i in range(start, len(nums)):
            # CHOOSE: bring nums[i] to position `start`
            nums[start], nums[i] = nums[i], nums[start]

            # EXPLORE: recurse on the rest
            backtrack(start + 1)

            # UN-CHOOSE: swap back
            nums[start], nums[i] = nums[i], nums[start]

    backtrack(0)
    return result


# =========================================================================
# 3. Using itertools.permutations (Python Built-In)
# =========================================================================

def permute_stdlib(nums):
    """
    For completeness — Python's built-in.

    Works but not the interview answer. Included to validate the
    hand-written versions.
    """
    from itertools import permutations
    return [list(p) for p in permutations(nums)]


# =========================================================================
# Test
# =========================================================================

def _normalize(perms):
    return sorted(tuple(p) for p in perms)


if __name__ == "__main__":
    import math

    cases = [
        [1, 2, 3],
        [],
        [1],
        [1, 2],
        [9, 8, 7, 6],
    ]

    for nums in cases:
        a = permute(nums)
        b = permute_swap(nums)
        c = permute_stdlib(nums)

        expected_count = math.factorial(len(nums))
        assert len(a) == len(b) == len(c) == expected_count
        assert _normalize(a) == _normalize(b) == _normalize(c)
        print(f"permute({nums}): {expected_count} permutations")

    # Sample
    print(f"\npermute([1, 2, 3]) = {permute([1, 2, 3])}")

    # Larger stress
    import random
    random.seed(42)
    for n in range(6):
        nums = list(range(n))
        a = permute(nums)
        b = permute_swap(nums)
        assert _normalize(a) == _normalize(b)

    print("\nStress: n=0..5 consistent across implementations")

    print("\nAll tests passed!")
