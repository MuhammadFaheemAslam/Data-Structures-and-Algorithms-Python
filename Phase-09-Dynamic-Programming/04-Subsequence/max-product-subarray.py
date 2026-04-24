"""
Problem: Maximum Product Subarray

Difficulty: Medium (LeetCode #152)

---------------------------------------------------
Problem Statement:

Given an integer array `nums`, find a CONTIGUOUS subarray (at least
one number) that has the largest PRODUCT, and return that product.

Example:
    [2, 3, -2, 4]   →  6    ([2, 3])
    [-2, 0, -1]     →  0    (empty isn't allowed; 0 beats -2 or -1)
    [-2, 3, -4]     →  24   (-2 * 3 * -4 — all three, negatives cancel)

---------------------------------------------------
Why It's NOT Just "Kadane For Sum":

Kadane's algorithm for MAX SUM is linear: `cur = max(x, cur + x)`.
For PRODUCTS it breaks: a negative running product can become
LARGEST after multiplying by another negative. So the "obvious"
running max isn't enough.

The fix: TRACK BOTH THE MAX AND MIN running products ending at i.
When we see a negative number, the previous MIN becomes the next MAX
(and vice versa). We take the max over the whole array at the end.

    cur_max_i = max(x, cur_max_{i-1} * x, cur_min_{i-1} * x)
    cur_min_i = min(x, cur_max_{i-1} * x, cur_min_{i-1} * x)

    answer = max over i of cur_max_i

Zeros break the chain (reset to x). Our formulas handle this
automatically since `max(0, 0 * prev, 0 * prev) = 0`.

---------------------------------------------------
Complexity:

    Time:  O(n)
    Space: O(1)

---------------------------------------------------
Pattern — "Track Two Extremes":

This trick generalizes. When a transformation (negation, rotation,
reciprocal) can SWAP max and min, you often need to track both.
See also:
    - max-sum subarray under constraints
    - max/min queries on sliding windows
    - some bitmask DP variants
"""


def max_product(nums):
    """
    Maximum product of a contiguous non-empty subarray.

    Time: O(n), Space: O(1).
    """
    if not nums:
        raise ValueError("empty array")            # LC guarantees ≥ 1 element

    cur_max = cur_min = best = nums[0]
    for x in nums[1:]:
        # If x is negative, swap cur_max and cur_min — negatives flip roles
        if x < 0:
            cur_max, cur_min = cur_min, cur_max
        cur_max = max(x, cur_max * x)
        cur_min = min(x, cur_min * x)
        best = max(best, cur_max)
    return best


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #152 examples
    assert max_product([2, 3, -2, 4]) == 6
    assert max_product([-2, 0, -1]) == 0
    assert max_product([-2, 3, -4]) == 24
    assert max_product([0, 2]) == 2
    assert max_product([-2]) == -2
    assert max_product([-2, -3, -4]) == 12                     # all three
    assert max_product([-2, 3, 1, -1, 2]) == 12                # -2*3*1*-1*2 = 12 (watch the signs)
    # Subarrays of [2,-5,-2,-4,3]: three negatives total (odd), so the
    # full-array product is NEGATIVE (-240). The max comes from an even-
    # negative-count subarray: [-2,-4,3] = 24.
    assert max_product([2, -5, -2, -4, 3]) == 24

    # Brute force
    def brute(nums):
        best = nums[0]
        for i in range(len(nums)):
            p = 1
            for j in range(i, len(nums)):
                p *= nums[j]
                best = max(best, p)
        return best

    # Small stress tests
    import random
    random.seed(42)
    for _ in range(500):
        n = random.randint(1, 15)
        nums = [random.randint(-5, 5) for _ in range(n)]
        expected = brute(nums)
        got = max_product(nums)
        assert got == expected, f"mismatch: nums={nums}, got {got}, expected {expected}"

    # Edge cases
    assert max_product([1]) == 1
    assert max_product([0]) == 0
    assert max_product([-1]) == -1
    assert max_product([0, 0, 0]) == 0
    assert max_product([1, 2, 3, 4, 5]) == 120
    assert max_product([-1, -2, -3, -4, -5]) == 120            # all negatives, even count OK
    assert max_product([-1, -2, -3, -4, 0, 5]) == 24           # first 4 → 24, then 0 resets

    print("All tests passed!")
