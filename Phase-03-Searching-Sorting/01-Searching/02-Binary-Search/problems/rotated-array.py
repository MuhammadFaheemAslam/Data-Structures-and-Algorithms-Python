"""
Problem: Search in Rotated Sorted Array

Technique: Binary Search on a PARTIALLY-SORTED array
Difficulty: Medium (LeetCode #33; #81 with duplicates)

---------------------------------------------------
Problem Statement:

A sorted (ascending, distinct) array is ROTATED at some pivot unknown
to you. For example:

    original:  [0, 1, 2, 4, 5, 6, 7]
    rotated:   [4, 5, 6, 7, 0, 1, 2]    (pivot at index 4)

Given the rotated array `nums` and a `target`, return the index of
`target`, or -1 if not present. You must do it in **O(log n)** time
— ruling out linear search.

---------------------------------------------------
Why This Is a Classic:

Plain binary search relies on the array being fully sorted. A rotated
array isn't — but it has a weaker property that still lets us halve
the search range at each step:

    At ANY midpoint `mid`, one of the two halves [lo..mid] or
    [mid..hi] IS fully sorted.

Which one? The one whose endpoints are non-decreasing. Concretely:

    - If arr[lo] <= arr[mid], the LEFT half is sorted.
    - Otherwise the RIGHT half is sorted.

(With distinct values, those two cases are disjoint. With duplicates
— LC #81 — a third case arises where arr[lo] == arr[mid] == arr[hi]
and we can't tell; then we just shrink both ends by 1. The worst case
degrades to O(n) in that variant.)

Once we know which half is sorted, we can check whether `target` lies
inside that sorted half's range. If yes, recurse there; if no, recurse
in the other half.

---------------------------------------------------
The Algorithm (Distinct Values):

    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid

        if arr[lo] <= arr[mid]:                  # LEFT half is sorted
            if arr[lo] <= target < arr[mid]:
                hi = mid - 1                     # target lives in sorted left
            else:
                lo = mid + 1                     # must be in unsorted right
        else:                                    # RIGHT half is sorted
            if arr[mid] < target <= arr[hi]:
                lo = mid + 1                     # target lives in sorted right
            else:
                hi = mid - 1                     # must be in unsorted left

Time:  O(log n) with distinct values
Space: O(1)

---------------------------------------------------
Example:

    nums = [4, 5, 6, 7, 0, 1, 2], target = 0 → 4
    nums = [4, 5, 6, 7, 0, 1, 2], target = 3 → -1
    nums = [1],                   target = 0 → -1

---------------------------------------------------
"""

# =========================================================================
# Solution: Modified Binary Search — O(log n)
# =========================================================================

def search_rotated(nums, target):
    """
    Search for `target` in a rotated sorted array with DISTINCT values.

    Time Complexity:  O(log n)
    Space Complexity: O(1)
    """
    lo, hi = 0, len(nums) - 1

    while lo <= hi:
        mid = lo + (hi - lo) // 2

        if nums[mid] == target:
            return mid

        # Which half is sorted?
        if nums[lo] <= nums[mid]:
            # LEFT half [lo..mid] is sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1                      # target is in the sorted left
            else:
                lo = mid + 1
        else:
            # RIGHT half [mid..hi] is sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1                      # target is in the sorted right
            else:
                hi = mid - 1

    return -1


# =========================================================================
# Variant: Rotated Sorted Array with Duplicates (LeetCode #81)
# =========================================================================

def search_rotated_with_duplicates(nums, target):
    """
    Same problem but the array may contain duplicates.

    Time Complexity:  O(log n) average, O(n) worst case — because the
                      "unclear which half is sorted" branch shrinks by 1.
    Space Complexity: O(1)

    Returns True iff target is present (rather than an index — LC #81's
    signature). Change to an index if you need it.
    """
    lo, hi = 0, len(nums) - 1

    while lo <= hi:
        mid = lo + (hi - lo) // 2

        if nums[mid] == target:
            return True

        # Ambiguous: arr[lo] == arr[mid] == arr[hi] leaves us unable
        # to identify the sorted half. Shrink both ends by 1 and retry.
        if nums[lo] == nums[mid] == nums[hi]:
            lo += 1
            hi -= 1
        elif nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1

    return False


# =========================================================================
# For Contrast: Linear Scan — O(n)
# =========================================================================

def search_rotated_linear(nums, target):
    """Linear scan for validation. O(n)."""
    for i, x in enumerate(nums):
        if x == target:
            return i
    return -1


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    nums = [4, 5, 6, 7, 0, 1, 2]
    print(f"nums = {nums}")
    for t in [0, 3, 4, 7, 2, 6]:
        got = search_rotated(nums, t)
        print(f"   search_rotated(nums, {t:2}) = {got}")
    print()

    # Test cases — (nums, target, expected)
    test_cases = [
        ([4, 5, 6, 7, 0, 1, 2],        0,    4),
        ([4, 5, 6, 7, 0, 1, 2],        3,   -1),
        ([4, 5, 6, 7, 0, 1, 2],        4,    0),
        ([4, 5, 6, 7, 0, 1, 2],        2,    6),
        ([1],                          0,   -1),
        ([1],                          1,    0),
        ([],                           5,   -1),
        ([1, 3],                       3,    1),
        ([3, 1],                       1,    1),         # pivot at 1
        ([1, 2, 3, 4, 5],              3,    2),         # no rotation
        ([5, 1, 3],                    5,    0),
        ([5, 1, 3],                    3,    2),
        ([5, 1, 3],                    1,    1),
        ([4, 5, 6, 7, 8, 1, 2, 3],     8,    4),
        ([4, 5, 6, 7, 8, 1, 2, 3],     3,    7),
    ]

    for i, (data, tgt, expected) in enumerate(test_cases):
        got = search_rotated(data, tgt)
        linear = search_rotated_linear(data, tgt)
        assert got == expected, (
            f"Test {i+1}: nums={data}, target={tgt}: "
            f"expected {expected}, got {got}"
        )
        assert got == linear, (
            f"Test {i+1}: binary ({got}) vs linear ({linear}) disagree"
        )
        print(f"Test {i+1} passed: nums={data}, target={tgt} -> {got}")

    # Stress test — random rotations
    import random
    random.seed(11)
    for _ in range(500):
        n = random.randint(0, 30)
        base = sorted(random.sample(range(100), n))
        rot = random.randint(0, n) if n else 0
        rotated = base[rot:] + base[:rot]
        target = random.randint(-10, 110)

        got = search_rotated(rotated, target)
        linear = search_rotated_linear(rotated, target)
        assert got == linear, f"stress: {rotated}, target={target}: {got} vs {linear}"
    print("\nStress test: 500 random rotations matched linear scan")

    # Variant with duplicates
    print()
    print("Variant — with duplicates:")
    dup_cases = [
        ([2, 5, 6, 0, 0, 1, 2],    0,  True),
        ([2, 5, 6, 0, 0, 1, 2],    3,  False),
        ([1, 0, 1, 1, 1],          0,  True),            # ambiguous case
        ([1, 1, 1, 1, 1],          2,  False),           # all same
    ]
    for nums, target, expected in dup_cases:
        got = search_rotated_with_duplicates(nums, target)
        assert got == expected, f"dup: {nums}, target={target}: {got}"
        print(f"   {nums}, target={target} -> {got}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Why This Is a Classic:
    #
    #   It generalizes binary search beyond the "fully sorted" case
    #   to the BROADER class of "monotone-structured" arrays.
    #
    # Once you see the "at any midpoint, one half is sorted" invariant,
    # a family of problems becomes approachable:
    #
    #   - Find Minimum in Rotated Sorted Array (LC #153)
    #   - Find Rotation Count
    #   - Search in Rotated Matrix (2D variant)
    #
    # All of them are "binary search + one extra fact about the input"
    # problems.
    # ---------------------------------------------------------------
