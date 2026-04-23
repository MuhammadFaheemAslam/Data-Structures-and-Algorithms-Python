"""
Problem: Find Peak Element

Technique: Binary Search on a NON-MONOTONIC array
Difficulty: Medium (LeetCode #162)

---------------------------------------------------
Problem Statement:

A peak element is one strictly greater than its neighbours. Given an
input array `nums` where `nums[-1] = nums[n] = -∞` (conceptual
boundaries), find ANY peak and return its index. You may assume no
two adjacent elements are equal.

Must run in **O(log n)**.

---------------------------------------------------
Why This Is a Surprising Binary Search:

The array is NOT SORTED. How can binary search possibly work?

The trick is that binary search doesn't need global order — it only
needs a monotonic decision rule at each step. For this problem, the
rule is:

    Look at arr[mid] vs arr[mid + 1]:
        - If arr[mid] < arr[mid + 1]:
              there MUST be a peak somewhere in [mid+1 .. n-1].
        - If arr[mid] > arr[mid + 1]:
              there MUST be a peak somewhere in [lo .. mid].

Either way, we halve the range.

Why is the MUST true? Because:

    Case 1 (arr[mid] < arr[mid+1]):
        Starting at mid, we can walk rightward — values keep increasing.
        Eventually they stop (hit the boundary, which is -∞). The
        last index where we stopped increasing is a peak.

    Case 2 (arr[mid] > arr[mid+1]):
        Walking leftward from mid, values keep being ≥ arr[mid] (at
        least mid itself). Eventually that sequence stops — that's a peak.

So a peak always exists in whichever direction is "uphill" from mid.
Binary search on that invariant → O(log n).

---------------------------------------------------
The Algorithm:

    lo, hi = 0, n - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < arr[mid + 1]:
            lo = mid + 1              # peak is to the right
        else:
            hi = mid                  # peak is at mid or to the left
    return lo

When lo == hi, that's the peak.

Time:  O(log n)
Space: O(1)

---------------------------------------------------
The Lesson:

Binary search applies whenever you can establish a **monotonic
invariant** that lets you pick "left half" or "right half" at each
step. The array doesn't need to be sorted — just the DECISION RULE
has to be monotone.

This is the same idea as Phase-02 / 02 / 05-Binary-Search-on-Answer:
binary searching OVER A PROPERTY, not over the input's values.

---------------------------------------------------
Example:

    nums = [1, 2, 3, 1]           → peak at index 2
    nums = [1, 2, 1, 3, 5, 6, 4]  → peak at index 1 OR index 5 (any valid)

---------------------------------------------------
"""

# =========================================================================
# Solution: Binary Search on "Uphill Direction" — O(log n)
# =========================================================================

def find_peak(nums):
    """
    Return the index of ANY peak element in `nums`.

    Time Complexity:  O(log n)
    Space Complexity: O(1)

    Assumes no two adjacent elements are equal (LC #162's precondition).
    """
    lo, hi = 0, len(nums) - 1

    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] < nums[mid + 1]:
            # we're going uphill → a peak lies to the right
            lo = mid + 1
        else:
            # we're going downhill (or flat) → a peak is at mid or left
            hi = mid

    return lo


# =========================================================================
# Linear Search Reference — O(n)
# =========================================================================

def find_peak_linear(nums):
    """
    Simple scan for any index where nums[i] > both neighbours.

    Time Complexity:  O(n)
    Space Complexity: O(1)

    Used for validation.
    """
    n = len(nums)
    for i in range(n):
        left_ok  = i == 0   or nums[i - 1] < nums[i]
        right_ok = i == n-1 or nums[i + 1] < nums[i]
        if left_ok and right_ok:
            return i
    return -1


# =========================================================================
# Test the Functions
# =========================================================================

def is_peak(nums, i):
    """Validate that index i is indeed a peak in nums."""
    n = len(nums)
    left_ok  = i == 0   or nums[i - 1] < nums[i]
    right_ok = i == n-1 or nums[i + 1] < nums[i]
    return left_ok and right_ok


if __name__ == "__main__":
    # Classic examples
    print(f"find_peak([1, 2, 3, 1])               = {find_peak([1, 2, 3, 1])}   (expected 2)")
    print(f"find_peak([1, 2, 1, 3, 5, 6, 4])      = {find_peak([1, 2, 1, 3, 5, 6, 4])}   (expected 1 or 5)")
    print()

    # Test cases — verify the returned index IS a peak
    test_cases = [
        [1, 2, 3, 1],
        [1, 2, 1, 3, 5, 6, 4],
        [1],                                      # single-element = always a peak
        [1, 2],                                   # right-end peak
        [2, 1],                                   # left-end peak
        [1, 2, 3, 4, 5],                          # monotone increasing — peak is last
        [5, 4, 3, 2, 1],                          # monotone decreasing — peak is first
        [1, 3, 2, 4, 1, 5],                       # multiple valid peaks
    ]

    for i, nums in enumerate(test_cases):
        got = find_peak(nums)
        assert 0 <= got < len(nums), f"Test {i+1}: index out of range: {got}"
        assert is_peak(nums, got), (
            f"Test {i+1}: {nums}, returned index {got} is not a peak"
        )
        print(f"Test {i+1} passed: {nums} -> peak at index {got} (value {nums[got]})")

    # Stress test — random inputs
    import random
    random.seed(8)
    for _ in range(500):
        n = random.randint(1, 30)
        # build an array with no equal adjacent pairs
        nums = []
        while len(nums) < n:
            x = random.randint(0, 100)
            if not nums or nums[-1] != x:
                nums.append(x)

        got = find_peak(nums)
        linear = find_peak_linear(nums)
        assert is_peak(nums, got), f"stress: {nums}: returned {got} (value {nums[got]}) is not a peak"
        # both should point at SOME peak — they may differ
        assert is_peak(nums, linear), f"stress (linear): {nums}: returned {linear} not a peak"

    print("\nStress test: 500 random arrays — all returned peaks are valid")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Takeaway:
    #
    #   Binary search is defined by a MONOTONIC DECISION RULE, not by
    #   a sorted input. Whenever you can define "if X holds at mid,
    #   the answer lies to one specific side", you can binary-search
    #   over that rule — even on unsorted or structured data.
    #
    # Related problems using this mental model:
    #   - Find Peak in a 2D Matrix (LC #1901)
    #   - Find Local Minimum (symmetric to this problem)
    #   - First Bad Version (LC #278)
    #   - Koko Eating Bananas (see Phase-02 / 02 / 05-Binary-Search-on-Answer)
    # ---------------------------------------------------------------
