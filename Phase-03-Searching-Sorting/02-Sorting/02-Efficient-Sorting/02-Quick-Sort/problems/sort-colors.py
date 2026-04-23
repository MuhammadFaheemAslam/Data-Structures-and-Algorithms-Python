"""
Problem: Sort Colors (Dutch National Flag)

Technique: Three-way partition in a single pass
Difficulty: Medium (LeetCode #75)

---------------------------------------------------
Problem Statement:

Given an array `nums` with n elements, each either 0 (red), 1 (white),
or 2 (blue), sort them IN PLACE so that all 0s come first, then all 1s,
then all 2s.

**Must be a one-pass, O(1)-space algorithm.** No counting sort, no
library sort function.

---------------------------------------------------
The Dutch National Flag Algorithm:

This is the problem Dijkstra invented 3-way partitioning for (1976).
The solution is exactly the 3-way partition from `three-way.py`,
specialized to pivot == 1.

Maintain three regions via two pointers:

    arr[0  .. lo-1]   all 0s    (red — already placed)
    arr[lo .. i-1]    all 1s    (white — already placed)
    arr[i  .. hi]     UNPROCESSED
    arr[hi+1 .. n-1]  all 2s    (blue — already placed)

Scan with `i`:
    if arr[i] == 0:  swap with arr[lo], lo += 1, i += 1
    if arr[i] == 2:  swap with arr[hi], hi -= 1  (don't advance i!)
    if arr[i] == 1:  i += 1

When `i > hi`, we're done.

---------------------------------------------------
Time:   O(n)
Space:  O(1)
Stable: No (but the problem doesn't require stability)

This is **faster than quick sort** on this specialized input (no
recursion, one pass). A 2-line variant also solves LC #75 using
counting sort in two passes — see below.

---------------------------------------------------
Example:

    [2, 0, 2, 1, 1, 0]
    → [0, 0, 1, 1, 2, 2]

---------------------------------------------------
"""

# =========================================================================
# Approach 1: Dutch National Flag (One-Pass, In-Place) — O(n), O(1)
# =========================================================================

def sort_colors(nums):
    """
    In-place sort of {0, 1, 2} values via the Dutch National Flag
    algorithm.

    Time:   O(n)
    Space:  O(1)

    Returns `nums` for convenience (mutated).
    """
    lo = 0
    hi = len(nums) - 1
    i = 0

    while i <= hi:
        if nums[i] == 0:
            nums[lo], nums[i] = nums[i], nums[lo]
            lo += 1
            i += 1
        elif nums[i] == 2:
            nums[hi], nums[i] = nums[i], nums[hi]
            hi -= 1
            # DON'T advance i — the swapped-in value is unprocessed
        else:                                      # nums[i] == 1
            i += 1

    return nums


# =========================================================================
# Approach 2: Counting Sort (Two Passes) — Simpler, O(n), O(1)
# =========================================================================

def sort_colors_counting(nums):
    """
    Count how many 0s, 1s, 2s there are; overwrite the array.

    Time:   O(n)
    Space:  O(1)    (fixed 3-slot count array)

    Two passes — not strictly one-pass, but O(1) space and dead simple.
    For most practical purposes this is just as good.
    """
    counts = [0, 0, 0]
    for x in nums:
        counts[x] += 1

    i = 0
    for value, cnt in enumerate(counts):
        for _ in range(cnt):
            nums[i] = value
            i += 1

    return nums


# =========================================================================
# Approach 3: Sorted (Cheating, But Valid for Validation)
# =========================================================================

def sort_colors_sorted(nums):
    """Uses Python's built-in sort. O(n log n). For cross-validation only."""
    nums.sort()
    return nums


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    nums = [2, 0, 2, 1, 1, 0]
    print(f"Input:  {nums}")
    sort_colors(nums)
    print(f"Sorted (Dutch National Flag): {nums}")
    print()

    # Test cases
    test_cases = [
        [2, 0, 2, 1, 1, 0],
        [2, 0, 1],
        [1, 2, 0],
        [0, 0, 0],
        [1, 1, 1],
        [2, 2, 2],
        [0, 1, 2],
        [2, 1, 0],
        [],
        [1],
        [0],
        [2],
        [0, 2, 1, 2, 0, 1, 0, 2, 1, 0],
        [1, 2, 0, 0, 2, 1, 0, 1, 2, 0, 2, 1, 0, 1],
    ]

    for i, data in enumerate(test_cases):
        expected = sorted(data)

        # All three approaches must agree
        for fn in (sort_colors, sort_colors_counting, sort_colors_sorted):
            got = fn(data[:])
            assert got == expected, (
                f"Test {i+1} ({fn.__name__}) failed on {data}: "
                f"expected {expected}, got {got}"
            )

        print(f"Test {i+1} passed: {data} -> {expected}")

    # Stress test
    import random
    random.seed(42)
    for _ in range(500):
        n = random.randint(0, 100)
        data = [random.randint(0, 2) for _ in range(n)]
        expected = sorted(data)
        assert sort_colors(data[:]) == expected
        assert sort_colors_counting(data[:]) == expected

    print("\nStress test: 500 random inputs — both approaches matched sorted()")

    # Demonstrate the one-pass property
    print()
    print("One-pass demonstration — tracking the scan index:")
    arr = [2, 0, 2, 1, 1, 0]
    lo = 0
    hi = len(arr) - 1
    i = 0
    print(f"   Start:  {arr}   lo={lo}, hi={hi}, i={i}")
    while i <= hi:
        if arr[i] == 0:
            arr[lo], arr[i] = arr[i], arr[lo]
            lo += 1
            i += 1
        elif arr[i] == 2:
            arr[hi], arr[i] = arr[i], arr[hi]
            hi -= 1
        else:
            i += 1
        print(f"   Step:   {arr}   lo={lo}, hi={hi}, i={i}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Variants and Generalizations:
    #
    #   - **Sort k colors:** with k distinct values, 3-way partition
    #     becomes k-way partition. The problem degrades to O(n log k)
    #     (recursive 3-way quicksort on k-valued arrays).
    #
    #   - **Partition around any value:** same algorithm, pivot != 1.
    #     See ../three-way.py.
    #
    #   - **LC #75 follow-up:** "Can you do it in one pass and O(1)
    #     extra space?" → the Dutch National Flag algorithm, i.e.,
    #     the `sort_colors` function above.
    # ---------------------------------------------------------------
