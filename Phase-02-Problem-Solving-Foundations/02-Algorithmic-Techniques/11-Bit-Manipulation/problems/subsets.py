"""
Problem: Subsets

Technique: Bit Manipulation — bitmask enumeration
Difficulty: Medium (LeetCode #78)

---------------------------------------------------
Problem Statement:

Given an integer array `nums` of unique elements, return ALL possible
subsets (the power set).

The solution set must not contain duplicate subsets. Order doesn't matter.

---------------------------------------------------
Why This Is a Canonical Bitmask Problem:

An n-element set has 2^n subsets. The integers 0 .. 2^n - 1 are, in
their binary representation, EXACTLY those 2^n subsets:

    bit k of mask is set  <->  nums[k] is in the subset

So "generate all subsets" is just:

    for mask in range(1 << n):
        build subset from set bits of mask

No recursion, no stack, no cleanup. One loop.

    Time Complexity:  O(n * 2^n)     — 2^n subsets, each of length ≤ n to build
    Space Complexity: O(n * 2^n)     — the output

Compare this to Phase-02 / 01 / 05-Backtracking / template.py's
`subsets` function: same Big-O, but backtracking pays function-call
overhead and stack manipulation; bitmask enumeration is a single tight
loop. Both are valid — the bitmask version is shorter and typically
faster in practice.

---------------------------------------------------
Example:

    nums = [1, 2, 3]

    2^3 = 8 subsets:
        mask 000 -> []
        mask 001 -> [1]
        mask 010 -> [2]
        mask 011 -> [1, 2]
        mask 100 -> [3]
        mask 101 -> [1, 3]
        mask 110 -> [2, 3]
        mask 111 -> [1, 2, 3]

---------------------------------------------------
"""

# -------------------------------------------------
# Approach 1: Bitmask Enumeration (The Point of This Module)
# -------------------------------------------------

def subsets_bitmask(nums):
    """
    Generate every subset by walking 0..2^n - 1.

    Time Complexity:  O(n * 2^n)
    Space Complexity: O(n * 2^n) for the output; O(n) for each subset
                       during construction
    """
    n = len(nums)
    result = []

    for mask in range(1 << n):
        subset = [nums[k] for k in range(n) if mask & (1 << k)]
        result.append(subset)

    return result


# -------------------------------------------------
# Approach 2: Backtracking (For Contrast — see 05-Backtracking)
# -------------------------------------------------

def subsets_backtracking(nums):
    """
    The classical backtracking solution.

    Time Complexity:  O(n * 2^n)
    Space Complexity: O(n) recursion + O(n * 2^n) output
    """
    result = []
    path = []

    def backtrack(start):
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1)
            path.pop()

    backtrack(0)
    return result


# -------------------------------------------------
# Approach 3: Iterative Cascade (Another Variant)
# -------------------------------------------------

def subsets_cascade(nums):
    """
    Start with [[]]. For each new element, DOUBLE the result list by
    adding copies with the new element appended.

    Time Complexity:  O(n * 2^n)
    Space Complexity: O(n * 2^n)

    A neat alternative that's easy to explain on a whiteboard.
    """
    result = [[]]
    for x in nums:
        result = result + [sub + [x] for sub in result]
    return result


# -------------------------------------------------
# Helper: Normalize for Order-Independent Comparison
# -------------------------------------------------

def normalize(subsets):
    """Sort each subset, then sort the list of subsets."""
    return sorted([sorted(s) for s in subsets])


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    nums = [1, 2, 3]

    print(f"nums = {nums}")
    print(f"subsets_bitmask:       {subsets_bitmask(nums)}")
    print(f"subsets_backtracking:  {subsets_backtracking(nums)}")
    print(f"subsets_cascade:       {subsets_cascade(nums)}")
    print()

    # Test cases — (nums, expected_normalized)
    test_cases = [
        (
            [1, 2, 3],
            [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]],
        ),
        (
            [0],
            [[], [0]],
        ),
        (
            [],
            [[]],
        ),
        (
            [5, -2, 8, 4],
            normalize(subsets_backtracking([5, -2, 8, 4])),   # compare against backtracking
        ),
    ]

    for i, (data, expected) in enumerate(test_cases):
        for fn in (subsets_bitmask, subsets_backtracking, subsets_cascade):
            got = normalize(fn(data))
            assert got == expected, (
                f"Test {i+1} ({fn.__name__}) failed on {data}: "
                f"expected {expected}, got {got}"
            )
        print(f"Test {i+1} passed: {data} -> {len(expected)} subsets")

    # All three should agree on a larger input
    big = list(range(6))                          # 2^6 = 64 subsets
    a = normalize(subsets_bitmask(big))
    b = normalize(subsets_backtracking(big))
    c = normalize(subsets_cascade(big))
    assert a == b == c
    assert len(a) == 2 ** len(big) == 64
    print(f"\nConsistency check on nums={big}: all three approaches agree "
          f"on {len(a)} subsets.")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Why Bitmasks Shine Here:
    #
    #   1. Zero recursion overhead — just a loop.
    #   2. Each mask IS the subset — no state to "enter/exit".
    #   3. Natural iteration over all subsets of any given mask:
    #
    #         sub = mask
    #         while sub:
    #             ...      # `sub` is a subset of mask
    #             sub = (sub - 1) & mask
    #
    #   That last trick is the foundation of bitmask DP (traveling
    #   salesman, assignment problem, partition-into-k-subsets DP).
    #   Once you can generate subsets of a mask, you can DP over them.
    # ---------------------------------------------------------------
