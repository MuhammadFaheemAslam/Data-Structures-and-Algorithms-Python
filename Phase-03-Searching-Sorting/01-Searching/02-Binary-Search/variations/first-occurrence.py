"""
first-occurrence.py – Find the First Occurrence of a Target

Standard binary search returns SOME index where `target` sits — not
necessarily the leftmost when duplicates exist. For example:

    arr = [1, 2, 2, 2, 3]
    binary_search(arr, 2)  →  could return 1, 2, OR 3

Often we want the LEFTMOST occurrence — the first index `i` with
arr[i] == target. This is the "first occurrence" variation.

---------------------------------------------------
The Trick:

When arr[mid] == target, we don't return immediately. Instead we
RECORD that mid is a valid answer and keep searching in the LEFT
half (because a still-earlier occurrence might exist).

The two changes from plain binary search:

    1. On a match, don't return. Save the index and continue leftward.
    2. When `lo > hi`, return the saved index (or -1 if nothing matched).

Equivalently, we can find the LOWER BOUND (first index with arr[i] >=
target) and check whether that index holds the target. See lower-bound.py.

---------------------------------------------------
Example:

    arr = [1, 2, 2, 2, 3, 3, 3, 5]
    first_occurrence(arr, 2) → 1
    first_occurrence(arr, 3) → 4
    first_occurrence(arr, 4) → -1

---------------------------------------------------
"""

# =========================================================================
# First Occurrence — Save-on-Match Approach
# =========================================================================

def first_occurrence(arr, target):
    """
    Return the leftmost index at which `target` occurs, or -1 if not
    present.

    Time Complexity:  O(log n)
    Space Complexity: O(1)
    """
    lo, hi = 0, len(arr) - 1
    result = -1

    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            result = mid                          # record; keep looking left
            hi = mid - 1
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1

    return result


# =========================================================================
# First Occurrence via Lower Bound (Alternative Implementation)
# =========================================================================

def first_occurrence_via_lower_bound(arr, target):
    """
    Lower bound returns the leftmost index with arr[i] >= target.
    If that index's value equals target, it's our answer; else -1.

    Same O(log n), different mental model. Useful when you already
    have a `lower_bound` helper available.
    """
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid

    if lo < len(arr) and arr[lo] == target:
        return lo
    return -1


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    arr = [1, 2, 2, 2, 3, 3, 3, 5]
    print(f"arr = {arr}")
    print()
    for target in [2, 3, 5, 1, 4, 6, 0]:
        print(f"   first_occurrence(arr, {target}) = {first_occurrence(arr, target)}")
    print()

    test_cases = [
        ([1, 2, 2, 2, 3],                2,   1),
        ([1, 2, 2, 2, 3, 3, 3, 5],       3,   4),
        ([1, 1, 1, 1, 1],                1,   0),         # all equal — first is 0
        ([2, 2, 2, 2, 2],                2,   0),
        ([1, 2, 3],                      2,   1),         # single occurrence
        ([1, 2, 3],                      4,   -1),        # not present
        ([],                             5,   -1),
        ([5],                            5,   0),
        ([5],                            3,   -1),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9],    1,   0),         # first element
        ([1, 2, 3, 4, 5, 6, 7, 8, 9],    9,   8),         # last element
    ]

    for i, (data, tgt, expected) in enumerate(test_cases):
        for fn in (first_occurrence, first_occurrence_via_lower_bound):
            got = fn(data, tgt)
            assert got == expected, (
                f"Test {i+1} ({fn.__name__}) failed on {data}, target={tgt}: "
                f"expected {expected}, got {got}"
            )
        print(f"Test {i+1} passed: target={tgt} -> {expected}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # When You Need This:
    #
    #   "Find the first bad version" (LC #278)
    #   "Find the index of the first occurrence in a string" (LC #28)
    #   "Search Range in Sorted Array" (LC #34 — combine with last-occurrence)
    #   "Smallest Letter Greater Than Target" (LC #744 — lower bound)
    #
    # Any time the question asks for "the first" or "the earliest"
    # something in a sorted structure, this is your template.
    # ---------------------------------------------------------------
