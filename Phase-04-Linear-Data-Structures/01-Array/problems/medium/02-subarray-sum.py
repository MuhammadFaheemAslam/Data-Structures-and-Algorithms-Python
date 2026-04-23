"""
Problem 02: Maximum Subarray Sum (Kadane's Algorithm)

Difficulty: Medium (LeetCode #53)

---------------------------------------------------
Problem Statement:

Given an integer array `nums` (possibly containing negative numbers),
find the contiguous subarray with the largest sum and return that sum.

The subarray must be:
    - Contiguous
    - Non-empty
    - Can contain any mix of positive and negative numbers

    [-2, 1, -3, 4, -1, 2, 1, -5, 4]  →  6  (from [4, -1, 2, 1])

---------------------------------------------------
The Three Approaches:

    1. Brute force, re-sum each subarray      O(n³)
    2. Brute force with running sum           O(n²)
    3. Kadane's algorithm                     O(n)  ← The answer

Kadane's is one of the most elegant algorithms in existence — an O(n),
O(1)-space, single-pass solution to a problem whose brute force is cubic.
It's a perfect introduction to the "streaming DP" pattern.

---------------------------------------------------
Kadane's Insight:

At each position `i`, the best subarray ENDING AT i is either:

    (a) nums[i] alone (starting fresh here), or
    (b) the best subarray ending at i-1, extended by nums[i].

Pick whichever is larger:

    current = max(nums[i], current + nums[i])

Track the global maximum separately:

    best = max(best, current)

That's the entire algorithm. Two lines of real logic, O(n), O(1) space.

---------------------------------------------------
"""

# =========================================================================
# Approach 1: Brute Force (O(n³)) — Re-Sum Every Subarray
# =========================================================================

def max_subarray_brute_force(nums):
    """
    For each (i, j) with i ≤ j, compute sum(nums[i..j]) from scratch.

    Time:  O(n³)
    Space: O(1)

    Unusable past n ~ 500. Shown here as the starting point —
    Kadane's goal is to reveal the redundancy in this approach.
    """
    if not nums:
        return 0

    best = nums[0]
    n = len(nums)
    for i in range(n):
        for j in range(i, n):
            current = sum(nums[i:j + 1])
            if current > best:
                best = current
    return best


# =========================================================================
# Approach 2: Running Sum (O(n²)) — Avoid Re-Summing
# =========================================================================

def max_subarray_running_sum(nums):
    """
    Still check every (i, j) pair, but reuse the running sum as j grows.

    Time:  O(n²)
    Space: O(1)

    One order of magnitude better than Approach 1 — kills the redundant
    inner `sum()`. But still quadratic.
    """
    if not nums:
        return 0

    best = nums[0]
    n = len(nums)
    for i in range(n):
        current = 0
        for j in range(i, n):
            current += nums[j]
            if current > best:
                best = current
    return best


# =========================================================================
# Approach 3: Kadane's Algorithm (O(n)) — THE Answer
# =========================================================================

def max_subarray(nums):
    """
    Kadane's algorithm. One pass, O(1) space.

    Time:  O(n)
    Space: O(1)

    The `current` variable tracks the best subarray ending HERE.
    Either we extend it (current + nums[i]) or start fresh (nums[i]).
    Pick the larger. Update global `best` as we go.
    """
    if not nums:
        return 0

    current = best = nums[0]
    for x in nums[1:]:
        current = max(x, current + x)              # extend, or start fresh at x
        best = max(best, current)
    return best


# =========================================================================
# Approach 4: Kadane's with Subarray Bounds
# =========================================================================

def max_subarray_with_bounds(nums):
    """
    Kadane's, but also return the START and END indices of the best subarray.

    Time:  O(n)
    Space: O(1)

    The bookkeeping: whenever we "start fresh" (current = nums[i]), the
    candidate start moves to i. Whenever `best` updates, we snapshot
    the current start/end.
    """
    if not nums:
        return 0, -1, -1

    current = best = nums[0]
    start = end = best_start = best_end = 0

    for i in range(1, len(nums)):
        if nums[i] > current + nums[i]:
            # start fresh at i
            current = nums[i]
            start = i
        else:
            current = current + nums[i]
        end = i

        if current > best:
            best = current
            best_start, best_end = start, end

    return best, best_start, best_end


# =========================================================================
# Approach 5: Divide & Conquer (O(n log n)) — Included for Interest
# =========================================================================

def max_subarray_divide_conquer(nums):
    """
    Divide the array in half. The max subarray is one of:
        (a) entirely in the left half,
        (b) entirely in the right half, or
        (c) CROSSING the midpoint.

    Case (c) is the clever part: expand outward from the midpoint
    tracking the best prefix sum going left and best suffix sum going
    right. Add them together.

    Time:  O(n log n)
    Space: O(log n) recursion

    Not the best algorithm for this problem — Kadane's is strictly
    better. Shown to illustrate that Divide & Conquer applies even
    to problems where a single-pass DP wins.
    """
    if not nums:
        return 0

    def helper(lo, hi):
        if lo == hi:
            return nums[lo]

        mid = (lo + hi) // 2

        # Case (a) and (b)
        left_max = helper(lo, mid)
        right_max = helper(mid + 1, hi)

        # Case (c): best subarray crossing mid
        # Best sum ending at mid (going leftward)
        left_sum = float("-inf")
        s = 0
        for i in range(mid, lo - 1, -1):
            s += nums[i]
            left_sum = max(left_sum, s)

        # Best sum starting at mid + 1 (going rightward)
        right_sum = float("-inf")
        s = 0
        for i in range(mid + 1, hi + 1):
            s += nums[i]
            right_sum = max(right_sum, s)

        cross = left_sum + right_sum

        return max(left_max, right_max, cross)

    return helper(0, len(nums) - 1)


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    expected = 6
    print(f"nums = {nums}")
    print(f"   brute force O(n³):        {max_subarray_brute_force(nums)}")
    print(f"   running sum O(n²):        {max_subarray_running_sum(nums)}")
    print(f"   Kadane O(n):              {max_subarray(nums)}")
    print(f"   Kadane with bounds:       {max_subarray_with_bounds(nums)}")
    print(f"   Divide & conquer:         {max_subarray_divide_conquer(nums)}")
    print()

    # Test cases — (nums, expected_sum)
    test_cases = [
        ([-2, 1, -3, 4, -1, 2, 1, -5, 4],  6),         # canonical
        ([1],                              1),
        ([5, 4, -1, 7, 8],                23),
        ([-1, -2, -3, -4],                -1),         # all negatives → best single
        ([0],                              0),
        ([-1],                            -1),
        ([3, -2, 5, -1, 2],                7),
        ([1, 2, 3, 4, 5],                  15),        # all positive — whole array
        ([-5, -4, -3, -2, -1],            -1),         # all negatives → biggest
    ]

    for i, (data, expected) in enumerate(test_cases):
        for fn in (max_subarray_brute_force, max_subarray_running_sum,
                   max_subarray, max_subarray_divide_conquer):
            got = fn(data)
            assert got == expected, (
                f"Test {i+1} ({fn.__name__}): expected {expected}, got {got}"
            )
        best, s, e = max_subarray_with_bounds(data)
        assert best == expected
        # Sanity-check the bounds actually represent the claimed sum
        if data:
            assert sum(data[s:e + 1]) == best, (
                f"bounds wrong: data[{s}:{e+1}] sums to {sum(data[s:e+1])}, not {best}"
            )

        print(f"Test {i+1} passed: {data} -> {expected}")

    # Stress test — compare Kadane with brute force on small inputs
    import random
    random.seed(42)
    for _ in range(300):
        n = random.randint(0, 30)
        data = [random.randint(-100, 100) for _ in range(n)]
        if n == 0:
            continue
        expected = max_subarray_brute_force(data)
        for fn in (max_subarray_running_sum, max_subarray, max_subarray_divide_conquer):
            assert fn(data) == expected

    print("\nStress test: 300 random arrays — all four approaches agree")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Related Problems:
    #
    #   - Maximum Product Subarray (LC #152)     — track max AND min
    #   - Best Time to Buy and Sell Stock (LC #121) — a DP variant
    #   - Maximum Circular Subarray (LC #918)    — Kadane on wrap-around
    #   - Maximum Subarray of Length K           — sliding window
    #
    # All four are elaborations of Kadane's insight. Master the
    # "extend or start fresh" pattern and they all open up.
    # ---------------------------------------------------------------
