"""
Problem: Subarray Sum Equals K

Technique: Prefix Sum + Hashing
Difficulty: Medium (LeetCode #560)

---------------------------------------------------
Problem Statement:

Given an integer array `nums` and an integer `k`, return the TOTAL
NUMBER of contiguous subarrays whose sum equals `k`.

Note:
    - `nums` may contain negatives (so sliding window won't work —
      the running sum isn't monotone).
    - Count overlapping subarrays separately.

---------------------------------------------------
The Prefix-Sum + Hashing Lens:

Brute force: for each (i, j) with i <= j, compute sum(nums[i..j]) →
O(n^2) or O(n^3). For n = 20_000 (the LeetCode limit), the O(n^2)
version is 400M operations — too slow.

Prefix sum alone gets each range sum to O(1) but still requires
enumerating O(n^2) pairs. We need another idea.

The key identity:

    sum(nums[i..j]) = prefix[j+1] - prefix[i]

We want this to equal k, so:

    prefix[j+1] - prefix[i] = k
    prefix[i]               = prefix[j+1] - k

For each j, we want to count how many prior positions i have
prefix[i] = (current_prefix - k).

That's a classic hash-map lookup: while walking through the array once,
maintain a dict `seen[value] = how many positions had prefix == value`.
At each step, add `seen[running - k]` to the answer.

    Time:   O(n)    — one pass, O(1) dict ops
    Space:  O(n)    — the dict

---------------------------------------------------
Important: seen[0] = 1

The "empty prefix" has sum 0 and occurs once (before the first element).

Without `seen[0] = 1`, subarrays starting at index 0 are missed —
their prefix-so-far equals k, so we're asking "has any prior prefix
been 0?" and the answer must be "yes, the empty one."

This is the single most common bug in this problem.

---------------------------------------------------
Example:

    nums = [1, 1, 1], k = 2
    -> 2     # [1,1] at positions (0,1), and [1,1] at positions (1,2)

    nums = [1, 2, 3], k = 3
    -> 2     # [1,2] and [3]

    nums = [1, -1, 1, -1], k = 0
    -> 4     # [1,-1], [1,-1], [-1,1], [1,-1,1,-1]

---------------------------------------------------
"""

# -------------------------------------------------
# The Prefix-Sum + Hashing Solution — O(n)
# -------------------------------------------------

def subarray_sum(nums, k):
    """
    Count contiguous subarrays of `nums` whose sum equals `k`.

    Time Complexity:  O(n)
    Space Complexity: O(n)
    """
    seen = {0: 1}                                 # prefix-sum → count (must include empty prefix)
    running = 0
    count = 0

    for x in nums:
        running += x
        needed = running - k                      # prefix value we'd need to see
        if needed in seen:
            count += seen[needed]
        seen[running] = seen.get(running, 0) + 1

    return count


# -------------------------------------------------
# Prefix Sum Alone — O(n^2), To Show the Middle Step
# -------------------------------------------------

def subarray_sum_prefix_only(nums, k):
    """
    Prefix sum without hashing. Every pair (i, j) checked, but each
    range sum is O(1).

    Time Complexity:  O(n^2)
    Space Complexity: O(n)

    Useful as the conceptual stepping stone: it shows why prefix sum
    alone isn't enough, and motivates the dict lookup.
    """
    n = len(nums)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]

    count = 0
    for j in range(n + 1):
        for i in range(j):
            if prefix[j] - prefix[i] == k:
                count += 1

    return count


# -------------------------------------------------
# Brute Force — O(n^3) Reference
# -------------------------------------------------

def subarray_sum_brute_force(nums, k):
    """
    Re-sum every subarray from scratch. Purely for validation.

    Time Complexity:  O(n^3)
    Space Complexity: O(1)
    """
    count = 0
    n = len(nums)
    for i in range(n):
        for j in range(i, n):
            if sum(nums[i:j + 1]) == k:
                count += 1
    return count


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    # Classic cases
    classics = [
        ([1, 1, 1],              2,  2),
        ([1, 2, 3],              3,  2),
        ([1, -1, 1, -1],         0,  4),
        ([3, 4, 7, 2, -3, 1, 4, 2], 7,  4),
    ]

    for nums, k, expected in classics:
        for fn in (subarray_sum, subarray_sum_prefix_only, subarray_sum_brute_force):
            got = fn(nums, k)
            assert got == expected, (
                f"{fn.__name__}({nums}, {k}) = {got}, expected {expected}"
            )
        print(f"   subarray_sum({nums}, {k}) = {expected}")
    print()

    # More test cases — edge cases
    test_cases = [
        ([],                     0,  0),          # empty
        ([],                     5,  0),
        ([0],                    0,  1),          # single zero
        ([0, 0, 0],              0,  6),          # every non-empty subarray sums to 0
        ([5],                    5,  1),
        ([5],                    3,  0),
        ([1, 2, 3, 4, 5],        15, 1),          # whole array
        ([-1, -1, 1],            0,  1),
        ([1, 0, 1, 0, 1],        2,  4),          # multiple ways
    ]

    for i, (nums, k, expected) in enumerate(test_cases):
        got = subarray_sum(nums, k)
        assert got == expected, (
            f"Test {i+1} failed on {nums}, k={k}: expected {expected}, got {got}"
        )
        # cross-check with brute force for inputs it can handle
        if len(nums) <= 20:
            bf = subarray_sum_brute_force(nums, k)
            assert got == bf, f"Test {i+1}: hash ({got}) disagrees with brute force ({bf})"
        print(f"Test {i+1} passed: nums={nums}, k={k} -> {expected}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Variations on the Same Pattern:
    #
    #   Same prefix + hash structure, different key:
    #
    #     Subarray Sum Equals K (LC #560)       key = prefix_sum
    #     Continuous Subarray Sum (#523)        key = prefix_sum % k
    #     Subarrays Divisible by K (#974)       key = prefix_sum % k
    #     Contiguous Array (#525)               key = prefix(#ones - #zeros)
    #     Count Nice Subarrays (#1248)          key = prefix(#odd numbers)
    #
    #   All of these are four-line variants of this function. Learn the
    #   shape once, recognize it forever.
    # ---------------------------------------------------------------
