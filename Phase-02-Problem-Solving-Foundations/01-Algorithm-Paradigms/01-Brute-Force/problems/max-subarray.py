"""
Problem: Maximum Subarray — Brute Force Edition

Paradigm: Brute Force (with a hint at Dynamic Programming)
Difficulty: Easy-Medium (LeetCode #53)

---------------------------------------------------
Problem Statement:

Given an integer array `nums`, find the CONTIGUOUS subarray with the
largest sum and return its sum.

    - Subarrays must be contiguous.
    - The subarray must be non-empty.
    - Elements may be negative.

---------------------------------------------------
The Brute Force Lens:

The search space is "all contiguous subarrays" — that is, every pair
(i, j) with i <= j, where the subarray is nums[i..j].

    - Number of subarrays: n * (n + 1) / 2 = O(n^2).
    - Cost to sum each subarray NAIVELY: O(n).
    - Naive brute force total: O(n^3).

We'll show three progressively better versions:

    O(n^3)  → full brute force: enumerate AND re-sum each subarray.
    O(n^2)  → keep a running sum while extending the right endpoint.
    O(n)    → Kadane's algorithm (DP insight; shown for contrast).

This is one of the classic "brute force tells you WHERE to optimize"
problems — each step reveals a small inefficiency in the previous one.

---------------------------------------------------
Example:

    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    -> 6       (the subarray [4, -1, 2, 1])

---------------------------------------------------
"""

# -------------------------------------------------
# Approach 1: Full Brute Force — O(n^3)
# -------------------------------------------------

def max_subarray_brute_force(nums):
    """
    Enumerate every (i, j) with i <= j and recompute sum(nums[i..j])
    from scratch for each one.

    Time Complexity:  O(n^3)
    Space Complexity: O(1)

    The inner sum() IS the inefficiency. It recomputes work that the
    outer loops already did one step earlier. That observation is what
    leads us to Approach 2.
    """
    if not nums:
        return 0

    n = len(nums)
    best = nums[0]

    for i in range(n):
        for j in range(i, n):
            current = sum(nums[i:j + 1])         # O(j - i + 1) – redundant!
            if current > best:
                best = current

    return best


# -------------------------------------------------
# Approach 2: Brute Force with Running Sum — O(n^2)
# -------------------------------------------------

def max_subarray_brute_force_running(nums):
    """
    Same enumeration as Approach 1, but we MAINTAIN a running sum as we
    extend j. Each inner iteration adds exactly ONE new element instead
    of re-summing the whole slice.

    Time Complexity:  O(n^2)
    Space Complexity: O(1)

    This is still brute force — we haven't pruned any candidates — but
    we've eliminated the redundant work inside the inner loop. That is
    the signature move of "smart brute force".
    """
    if not nums:
        return 0

    n = len(nums)
    best = nums[0]

    for i in range(n):
        current = 0
        for j in range(i, n):
            current += nums[j]                   # extend by one element
            if current > best:
                best = current

    return best


# -------------------------------------------------
# Approach 3: Kadane's Algorithm — O(n)
# -------------------------------------------------

def max_subarray_kadane(nums):
    """
    The DP insight: at each position, the best subarray ending HERE
    either (a) includes the previous best subarray, or (b) starts fresh
    at the current element. We never need to look further back than that.

        current = max(nums[i], current + nums[i])

    Track the running answer; return the best `current` we ever saw.

    Time Complexity:  O(n)
    Space Complexity: O(1)

    This is the "DP" version of the brute force. It's what the brute
    force becomes once you notice that extending the running sum from
    index i is equivalent across all left endpoints i — so you only
    need one running sum, not n of them.

    Covered properly in Phase-02 / 01 / 04-Dynamic-Programming.
    Shown here to make the optimization story concrete.
    """
    if not nums:
        return 0

    best = current = nums[0]
    for x in nums[1:]:
        current = max(x, current + x)            # extend or restart
        best = max(best, current)
    return best


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

    print(f"nums = {nums}")
    print()
    print(f"brute force O(n^3):         {max_subarray_brute_force(nums)}")
    print(f"brute force O(n^2) running: {max_subarray_brute_force_running(nums)}")
    print(f"Kadane's   O(n):            {max_subarray_kadane(nums)}")
    print()

    # Test cases – (nums, expected)
    test_cases = [
        ([-2, 1, -3, 4, -1, 2, 1, -5, 4],  6),   # [4, -1, 2, 1]
        ([1],                              1),
        ([5, 4, -1, 7, 8],                23),
        ([-1, -2, -3, -4],                -1),   # all negatives → single best element
        ([0],                              0),
        ([3, -2, 5, -1, 2],                7),   # [3, -2, 5, -1, 2]
    ]

    for i, (data, expected) in enumerate(test_cases):
        for fn in (
            max_subarray_brute_force,
            max_subarray_brute_force_running,
            max_subarray_kadane,
        ):
            got = fn(data)
            assert got == expected, (
                f"Test {i+1} ({fn.__name__}) failed on {data}: "
                f"expected {expected}, got {got}"
            )
        print(f"Test {i+1} passed: nums={data} -> {expected}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Story in One Table:
    #
    #   approach            work per (i, j)    outer cost    total
    #   --------            ---------------    ----------    -----
    #   Approach 1 O(n^3)   O(n) — full sum    O(n^2) pairs  O(n^3)
    #   Approach 2 O(n^2)   O(1) — running     O(n^2) pairs  O(n^2)
    #   Approach 3 O(n)     O(1)               O(n) states   O(n)
    #
    # Each step kills redundant work that the previous step exposed.
    # That's the whole point of starting with brute force: it tells
    # you EXACTLY which redundancy to eliminate next.
    # ---------------------------------------------------------------
