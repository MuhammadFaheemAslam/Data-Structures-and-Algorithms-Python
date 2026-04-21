"""
Problem: Two Sum (Hashing Edition)

Technique: Hashing — complement lookup pattern
Difficulty: Easy (LeetCode #1)

---------------------------------------------------
Problem Statement:

Given an unsorted array `nums` and an integer `target`, return indices
(i, j) such that nums[i] + nums[j] == target.

You may assume exactly one solution exists. You may not use the same
element twice. Return the pair with i < j.

---------------------------------------------------
Note:

We saw this problem in two previous places:

    1. Phase-02 / 01 / 01-Brute-Force / problems / two-sum.py
         — the O(n²) baseline, "try every pair".
    2. Phase-02 / 02 / 01-Two-Pointers / problems / two-sum-sorted.py
         — the O(n) two-pointer solution for SORTED input.

This file closes the loop: the O(n) solution for UNSORTED input, via
hashing. It is the canonical demonstration of the "complement lookup"
pattern that shows up in dozens of other interview problems.

---------------------------------------------------
The Hashing Lens:

Brute force: for each pair (i, j), check the sum — O(n²).

Hashing insight: "to answer whether a partner exists, we don't need to
scan the rest of the list — we need to ask a dict."

    For each element x at index i:
        complement = target - x
        if complement is already in our dict:  done — return indices
        else: record x -> i in the dict for future elements to find

Each iteration is O(1) dict work. Single pass → O(n).

The technique beats two pointers when:
    - The input isn't sorted, AND
    - Sorting would lose information (we need original indices).

Time Complexity:  O(n)
Space Complexity: O(n)

---------------------------------------------------
Example:

    nums = [2, 7, 11, 15], target = 9
    -> (0, 1)       because 2 + 7 == 9

    nums = [3, 3], target = 6
    -> (0, 1)       (duplicates are allowed at different indices)

---------------------------------------------------
"""

# -------------------------------------------------
# The Hashing Solution — O(n)
# -------------------------------------------------

def two_sum(nums, target):
    """
    Return the indices (i, j) such that nums[i] + nums[j] == target.

    Time Complexity:  O(n)
    Space Complexity: O(n)
    """
    seen = {}                                    # value → index

    for i, x in enumerate(nums):
        complement = target - x
        if complement in seen:
            return (seen[complement], i)
        seen[x] = i

    return None


# -------------------------------------------------
# One-Pass vs Two-Pass: Both Are O(n)
# -------------------------------------------------

def two_sum_two_pass(nums, target):
    """
    Two-pass version — build the full dict first, then scan for complements.

    Same asymptotic cost (O(n)) but two passes. Slightly simpler to
    reason about because the dict is "fully built" when we query.

    Watch the EDGE CASE: if a value appears twice (e.g. [3, 3], target 6),
    we must not match a value with itself at the same index.
    """
    lookup = {}
    for i, x in enumerate(nums):
        lookup[x] = i

    for i, x in enumerate(nums):
        complement = target - x
        j = lookup.get(complement)
        if j is not None and j != i:
            return (min(i, j), max(i, j))

    return None


# -------------------------------------------------
# For Contrast: Brute Force — O(n²)
# -------------------------------------------------

def two_sum_brute_force(nums, target):
    """
    Nested loop baseline. O(n²) time, O(1) space.
    """
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return (i, j)
    return None


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    nums = [2, 7, 11, 15]
    target = 9

    print(f"nums = {nums}, target = {target}")
    print(f"two_sum (hashing):          {two_sum(nums, target)}")
    print(f"two_sum_two_pass (hashing): {two_sum_two_pass(nums, target)}")
    print(f"two_sum_brute_force:        {two_sum_brute_force(nums, target)}")
    print()

    # Test cases — (nums, target, expected)
    test_cases = [
        ([2, 7, 11, 15],     9,  (0, 1)),
        ([3, 2, 4],          6,  (1, 2)),
        ([3, 3],             6,  (0, 1)),        # duplicates allowed at different indices
        ([-1, -2, -3, -4, -5], -8, (2, 4)),
        ([0, 4, 3, 0],       0,  (0, 3)),        # two zeros
        ([1, 2, 3, 4, 5],    9,  (3, 4)),
        ([1],                1,  None),
        ([],                 0,  None),
        ([1, 2, 3],          10, None),          # no solution
    ]

    for i, (data, tgt, expected) in enumerate(test_cases):
        for fn in (two_sum, two_sum_two_pass, two_sum_brute_force):
            got = fn(data, tgt)
            assert got == expected, (
                f"Test {i+1} ({fn.__name__}) failed on {data} target={tgt}: "
                f"expected {expected}, got {got}"
            )
        print(f"Test {i+1} passed: nums={data}, target={tgt} -> {expected}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Three Solutions to Two Sum:
    #
    #                    time       space    when to use
    #   brute force      O(n^2)     O(1)     small n, no extra memory
    #   hashing          O(n)       O(n)     unsorted input, original indices matter
    #   two pointers     O(n)       O(1)     input is already sorted
    #
    #   Sort + two pointers:  O(n log n) time, O(1) space
    #   — loses original indices unless you carry them through.
    #
    # For interview "can you do better than brute force?" answers,
    # hashing is almost always the expected response.
    # ---------------------------------------------------------------
