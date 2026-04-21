"""
Problem: Two Sum — Brute Force Edition

Paradigm: Brute Force
Difficulty: Easy (LeetCode #1)

---------------------------------------------------
Problem Statement:

Given a list of integers `nums` and a target integer `target`, return the
INDICES (i, j) with i < j such that nums[i] + nums[j] == target.

You may assume exactly one such pair exists. Return None if no pair exists.

---------------------------------------------------
The Brute Force Lens:

The search space is "all pairs of indices (i, j) with i < j".
    - Size of search space: n * (n - 1) / 2 = O(n^2).
    - Validation cost per candidate: O(1)  (just an addition).

So the brute force is O(n^2) time, O(1) space.

This IS the paradigm's canonical example — the "all pairs" skeleton from
template.py, specialized to the Two Sum problem. The entire algorithm
is three lines of real logic; everything else is bookkeeping.

---------------------------------------------------
Example:

    nums   = [2, 7, 11, 15]
    target = 9
    -> (0, 1)     because 2 + 7 == 9

---------------------------------------------------
"""

# -------------------------------------------------
# The Brute Force Solution (All Pairs)
# -------------------------------------------------

def two_sum_brute_force(nums, target):
    """
    Check every pair (i, j) with i < j. Return the first pair whose
    values sum to `target`.

    Time Complexity:  O(n^2)
    Space Complexity: O(1)

    This is the canonical O(n^2) "search the entire pair space" shape.
    Slow for large n, but correct by construction and trivial to reason about.
    """
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return (i, j)
    return None


# -------------------------------------------------
# A Slightly Less Naive Brute Force
# -------------------------------------------------

def two_sum_brute_force_with_early_exit(nums, target):
    """
    Same O(n^2) worst case, but we stop at the very first match.
    Useful when most inputs have the pair near the start — the
    asymptotic bound doesn't change, but the constant factor does.

    Time Complexity:  O(n^2) worst case
    Space Complexity: O(1)
    """
    for i, a in enumerate(nums):
        for j in range(i + 1, len(nums)):
            if a + nums[j] == target:
                return (i, j)                    # early return on first hit
    return None


# -------------------------------------------------
# For Contrast: the O(n) Hashing Solution
# -------------------------------------------------

def two_sum_hash(nums, target):
    """
    Included only for contrast with the brute force. This is the solution
    Phase-02 / 02 / 07-Hashing-Technique will teach properly.

    The insight: instead of searching the rest of the list for the partner
    of each element, record each element we've seen into a dict keyed by
    value; then for each new element just ask "is my partner already there?"

    Time Complexity:  O(n)
    Space Complexity: O(n)

    The speedup comes from REPLACING A SEARCH WITH A LOOKUP — the single
    most important trick in algorithmic optimization.
    """
    seen = {}                                     # value -> index
    for i, x in enumerate(nums):
        complement = target - x
        if complement in seen:
            return (seen[complement], i)
        seen[x] = i
    return None


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    nums = [2, 7, 11, 15]
    target = 9

    print(f"nums   = {nums}")
    print(f"target = {target}")
    print()
    print(f"brute force (nested loops): {two_sum_brute_force(nums, target)}")
    print(f"brute force (early exit):   {two_sum_brute_force_with_early_exit(nums, target)}")
    print(f"hash map (O(n), contrast):  {two_sum_hash(nums, target)}")
    print()

    # Test cases – (nums, target, expected)
    test_cases = [
        ([2, 7, 11, 15],      9,  (0, 1)),
        ([3, 2, 4],           6,  (1, 2)),
        ([3, 3],              6,  (0, 1)),
        ([1, 5, 9, 14],       23, (2, 3)),
        ([-3, 4, 3, 90],      0,  (0, 2)),        # negatives
        ([1, 2, 3],           10, None),          # no solution
        ([],                  5,  None),          # empty input
        ([5],                 5,  None),          # single element
    ]

    for i, (data, tgt, expected) in enumerate(test_cases):
        for fn in (
            two_sum_brute_force,
            two_sum_brute_force_with_early_exit,
            two_sum_hash,
        ):
            got = fn(data, tgt)
            assert got == expected, (
                f"Test {i+1} ({fn.__name__}) failed on {data} target={tgt}: "
                f"expected {expected}, got {got}"
            )
        print(f"Test {i+1} passed: nums={data}, target={tgt} -> {expected}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Reflection:
    #
    # Both approaches return the same answer. The difference is ONLY
    # in the cost at scale:
    #
    #   n = 100:    brute force = 10_000 ops   |  hash map = 100 ops
    #   n = 10_000: brute force = 100_000_000  |  hash map = 10_000
    #
    # This is why "can I replace a nested loop with a dict lookup?"
    # is the single most valuable question to ask when optimizing code.
    # ---------------------------------------------------------------
