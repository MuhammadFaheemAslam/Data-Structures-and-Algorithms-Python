"""
Problem 02: Two Sum

Difficulty: Easy (LeetCode #1 – the single most famous interview problem)

---------------------------------------------------
Problem Statement:

Given a list of integers `nums` and a target integer `target`, return the
INDICES of the two numbers that add up to `target`.

You may assume exactly one such pair exists, and you may not use the
same element twice. Return the two indices as a tuple (i, j) with i < j.

If no pair exists, return None.

This problem is the canonical demonstration of how a dict (hash map) turns
an O(n^2) brute-force search into an O(n) single-pass solution.

---------------------------------------------------
Example:

Input:
    nums = [2, 7, 11, 15]
    target = 9

Output:
    (0, 1)         # nums[0] + nums[1] == 2 + 7 == 9

---------------------------------------------------
"""

# -------------------------------------------------
# Approach 1: Hash Map, Single Pass (The Answer)
# -------------------------------------------------

def two_sum_hash(nums, target):
    """
    Walk the list once. For each number x at index i:
      - Compute its COMPLEMENT: target - x.
      - If the complement is already in our dict, we found the pair.
      - Otherwise, record x -> i and continue.

    Time Complexity: O(n)       – one pass, O(1) dict ops
    Space Complexity: O(n)      – the `seen` dict, worst case

    This is the version to write in an interview.
    """
    seen = {}                             # value -> index
    for i, x in enumerate(nums):
        complement = target - x
        if complement in seen:
            return (seen[complement], i)
        seen[x] = i
    return None


# -------------------------------------------------
# Approach 2: Brute Force (Anti-Pattern)
# -------------------------------------------------

def two_sum_bruteforce(nums, target):
    """
    Compare every pair of indices.

    Time Complexity: O(n^2)
    Space Complexity: O(1)

    Included to make the speedup concrete. For n = 10,000 this is
    ~50 million comparisons; the hash-map version is ~10,000 dict ops.
    """
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return (i, j)
    return None


# -------------------------------------------------
# Approach 3: Sort + Two Pointers (Loses Original Indices)
# -------------------------------------------------

def two_sum_sorted(nums, target):
    """
    If we were allowed to return the VALUES (not the indices), we could
    sort and use two pointers.

    Time Complexity: O(n log n) – dominated by sorting
    Space Complexity: O(n)      – new list of (value, original_index) pairs

    Because the problem asks for indices, we must carry them through.
    The hash-map approach is cleaner AND strictly faster.
    """
    indexed = sorted(enumerate(nums), key=lambda pair: pair[1])
    lo, hi = 0, len(indexed) - 1
    while lo < hi:
        total = indexed[lo][1] + indexed[hi][1]
        if total == target:
            i, j = indexed[lo][0], indexed[hi][0]
            return (min(i, j), max(i, j))
        if total < target:
            lo += 1
        else:
            hi -= 1
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
    print(f"two_sum_hash:       {two_sum_hash(nums, target)}")
    print(f"two_sum_bruteforce: {two_sum_bruteforce(nums, target)}")
    print(f"two_sum_sorted:     {two_sum_sorted(nums, target)}")
    print()

    # Test cases – (nums, target, expected)
    test_cases = [
        ([2, 7, 11, 15],    9,  (0, 1)),
        ([3, 2, 4],         6,  (1, 2)),
        ([3, 3],            6,  (0, 1)),      # duplicates allowed at different indices
        ([1, 5, 9, 14],     23, (2, 3)),
        ([-3, 4, 3, 90],    0,  (0, 2)),      # negative numbers
        ([1, 2, 3],         10, None),         # no solution
    ]

    for i, (data, tgt, expected) in enumerate(test_cases):
        for fn in (two_sum_hash, two_sum_bruteforce, two_sum_sorted):
            got = fn(data, tgt)
            assert got == expected, (
                f"Test {i+1} ({fn.__name__}) failed on {data} target={tgt}: "
                f"expected {expected}, got {got}"
            )
        print(f"Test {i+1} passed: nums={data}, target={tgt} -> {expected}")

    print("\nAll tests passed!")
