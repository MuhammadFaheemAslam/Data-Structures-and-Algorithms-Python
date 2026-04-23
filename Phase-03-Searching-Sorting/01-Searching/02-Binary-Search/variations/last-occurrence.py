"""
last-occurrence.py – Find the Last Occurrence of a Target

Mirror of first-occurrence.py: return the RIGHTMOST index at which
`target` appears in a sorted array (or -1 if not present).

---------------------------------------------------
The Trick:

Symmetric to first-occurrence. When arr[mid] == target, save the
index and keep searching in the RIGHT half (a still-later occurrence
might exist).

Equivalently: find the UPPER BOUND (first index with arr[i] > target)
and return `upper_bound - 1` if that index's value is the target.

---------------------------------------------------
Example:

    arr = [1, 2, 2, 2, 3, 3, 3, 5]
    last_occurrence(arr, 2) → 3
    last_occurrence(arr, 3) → 6
    last_occurrence(arr, 4) → -1

---------------------------------------------------
"""

# =========================================================================
# Last Occurrence — Save-on-Match Approach
# =========================================================================

def last_occurrence(arr, target):
    """
    Return the rightmost index at which `target` occurs, or -1 if not
    present.

    Time Complexity:  O(log n)
    Space Complexity: O(1)
    """
    lo, hi = 0, len(arr) - 1
    result = -1

    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            result = mid                          # record; keep looking right
            lo = mid + 1
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1

    return result


# =========================================================================
# Last Occurrence via Upper Bound (Alternative)
# =========================================================================

def last_occurrence_via_upper_bound(arr, target):
    """
    Upper bound returns the leftmost index with arr[i] > target.
    Subtract 1; if that index's value equals target, it's the answer.
    """
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] <= target:
            lo = mid + 1
        else:
            hi = mid

    idx = lo - 1
    if idx >= 0 and arr[idx] == target:
        return idx
    return -1


# =========================================================================
# Bonus: Combine with first_occurrence — Count of a Target
# =========================================================================

def count_occurrences(arr, target):
    """
    Count how many times `target` appears in the sorted array.

    Classic application of first + last occurrence:
        count = (last_occ - first_occ + 1) if both exist, else 0

    Time Complexity:  O(log n)
    """
    # inline first_occurrence for a self-contained function
    lo, hi = 0, len(arr) - 1
    first = -1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            first = mid; hi = mid - 1
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1

    if first == -1:
        return 0

    last = last_occurrence(arr, target)
    return last - first + 1


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    arr = [1, 2, 2, 2, 3, 3, 3, 5]
    print(f"arr = {arr}")
    print()

    for target in [2, 3, 5, 1, 4, 6]:
        print(f"   last_occurrence(arr, {target}) = {last_occurrence(arr, target)}")
    print()

    print("count_occurrences combines first + last:")
    for target in [2, 3, 5, 1, 4, 6]:
        print(f"   count_occurrences(arr, {target}) = {count_occurrences(arr, target)}")
    print()

    test_cases = [
        ([1, 2, 2, 2, 3],                2,   3),
        ([1, 2, 2, 2, 3, 3, 3, 5],       3,   6),
        ([1, 1, 1, 1, 1],                1,   4),         # all equal — last is n-1
        ([1, 2, 3],                      2,   1),
        ([1, 2, 3],                      4,   -1),
        ([],                             5,   -1),
        ([5],                            5,   0),
        ([5],                            3,   -1),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9],    1,   0),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9],    9,   8),
    ]

    for i, (data, tgt, expected) in enumerate(test_cases):
        for fn in (last_occurrence, last_occurrence_via_upper_bound):
            got = fn(data, tgt)
            assert got == expected, (
                f"Test {i+1} ({fn.__name__}) failed on {data}, target={tgt}: "
                f"expected {expected}, got {got}"
            )
        print(f"Test {i+1} passed: target={tgt} -> {expected}")

    # count_occurrences
    count_cases = [
        ([1, 2, 2, 2, 3],                2,   3),
        ([1, 2, 2, 2, 3, 3, 3, 5],       3,   3),
        ([1, 1, 1, 1, 1],                1,   5),
        ([1, 2, 3],                      4,   0),
        ([],                             5,   0),
    ]
    for arr, target, expected in count_cases:
        assert count_occurrences(arr, target) == expected

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # When You Need This:
    #
    #   "Find First and Last Position of Element in Sorted Array" (LC #34)
    #   "Count of Elements Smaller Than Target"
    #   "Number of Occurrences of a Value in a Sorted Array" — this file
    #
    # First + Last together give you any "range of this value" query
    # in O(log n) with O(1) space.
    # ---------------------------------------------------------------
