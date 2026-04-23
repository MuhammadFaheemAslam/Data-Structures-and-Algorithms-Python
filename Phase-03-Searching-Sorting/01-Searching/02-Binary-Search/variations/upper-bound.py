"""
upper-bound.py – First Index with arr[i] > target

Upper bound is the STRICT counterpart of lower bound.

    upper_bound(arr, target) = smallest i such that arr[i] > target
                             = the RIGHTMOST insertion point for `target`
                               into a sorted array (preserves order).

Equivalently — this is Python's `bisect.bisect_right(arr, target)`.

---------------------------------------------------
Lower Bound vs Upper Bound:

    arr    = [1, 3, 3, 5, 7, 7, 9]
    target = 3

    lower_bound → 1    (first index where arr[i] >= 3)
    upper_bound → 3    (first index where arr[i] >  3)

The two bounds together pick out the RANGE of indices equal to target:

    [lower_bound, upper_bound)      ← half-open, INCLUSIVE on left

For target = 3 above: [1, 3) → indices 1 and 2 (the two 3s). Count:
upper_bound − lower_bound == 2.

---------------------------------------------------
The Template (Exclusive-hi):

    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] <= target:
            lo = mid + 1
        else:
            hi = mid                    # arr[mid] is a candidate answer
    return lo

The only difference from lower_bound is the comparison: `<=` here vs
`<` there. That one character change flips the tie-breaking from
"leftmost" to "rightmost".

---------------------------------------------------
Example:

    arr = [1, 3, 3, 5, 7, 7, 9]
    upper_bound(arr, 3) → 3    (insert right of all 3s, before 5)
    upper_bound(arr, 4) → 3    (same as lower_bound when target absent)
    upper_bound(arr, 0) → 0    (before everything)
    upper_bound(arr, 10) → 7   (one past end)

---------------------------------------------------
"""

# =========================================================================
# Upper Bound — Iterative
# =========================================================================

def upper_bound(arr, target):
    """
    Return the smallest index `i` with arr[i] > target, or len(arr)
    if no such index exists.

    Time Complexity:  O(log n)
    Space Complexity: O(1)
    """
    lo, hi = 0, len(arr)

    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] <= target:
            lo = mid + 1                          # mid <= target: exclude it
        else:
            hi = mid                              # mid > target: candidate

    return lo


# =========================================================================
# Useful Derivatives
# =========================================================================

def count_at_most(arr, target):
    """
    Count how many elements in the sorted array are <= target.

    That's just `upper_bound(arr, target)` — one binary search.
    """
    return upper_bound(arr, target)


def count_equal(arr, target):
    """
    Count how many elements in the sorted array are equal to `target`.

    upper_bound - lower_bound is the range width.
    """
    # inline lower_bound to avoid a cross-module import
    def _lower(arr, target):
        lo, hi = 0, len(arr)
        while lo < hi:
            mid = lo + (hi - lo) // 2
            if arr[mid] < target:
                lo = mid + 1
            else:
                hi = mid
        return lo

    return upper_bound(arr, target) - _lower(arr, target)


def count_in_range(arr, lo_target, hi_target):
    """
    Count elements in the sorted array that are in the range
    [lo_target, hi_target] (INCLUSIVE on both ends).

    count_in_range = count(arr[i] <= hi_target) - count(arr[i] < lo_target)
                   = upper_bound(arr, hi_target) - lower_bound(arr, lo_target)
    """
    def _lower(arr, target):
        lo, hi = 0, len(arr)
        while lo < hi:
            mid = lo + (hi - lo) // 2
            if arr[mid] < target:
                lo = mid + 1
            else:
                hi = mid
        return lo

    return upper_bound(arr, hi_target) - _lower(arr, lo_target)


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    from bisect import bisect_right

    arr = [1, 3, 3, 5, 7, 7, 9]
    print(f"arr = {arr}")
    print()
    for target in [3, 4, 0, 10, 7, 9]:
        got = upper_bound(arr, target)
        builtin = bisect_right(arr, target)
        assert got == builtin
        print(f"   upper_bound(arr, {target:2}) = {got}   (bisect_right: {builtin})")
    print()

    # Test cases — verify against Python's bisect_right
    test_cases = [
        ([1, 3, 3, 5, 7, 7, 9],  3,   3),
        ([1, 3, 3, 5, 7, 7, 9],  4,   3),
        ([1, 3, 3, 5, 7, 7, 9],  0,   0),
        ([1, 3, 3, 5, 7, 7, 9],  10,  7),
        ([1, 3, 3, 5, 7, 7, 9],  1,   1),
        ([1, 3, 3, 5, 7, 7, 9],  9,   7),
        ([],                     5,   0),
        ([5],                    5,   1),
        ([5],                    3,   0),
        ([5],                    7,   1),
        ([1, 1, 1, 1],           1,   4),
        ([1, 1, 1, 1],           0,   0),
    ]

    for i, (data, tgt, expected) in enumerate(test_cases):
        got = upper_bound(data, tgt)
        assert got == expected == bisect_right(data, tgt), (
            f"Test {i+1} failed on {data}, target={tgt}: "
            f"expected {expected}, got {got}"
        )
        print(f"Test {i+1} passed: target={tgt} -> {expected}")

    # Derivatives
    print()
    print("Derivatives:")
    arr = [1, 3, 3, 5, 7, 7, 9]
    print(f"   count_at_most({arr}, 5)      = {count_at_most(arr, 5)}")
    print(f"   count_equal({arr}, 3)        = {count_equal(arr, 3)}")
    print(f"   count_equal({arr}, 7)        = {count_equal(arr, 7)}")
    print(f"   count_equal({arr}, 4)        = {count_equal(arr, 4)}  (not present)")
    print(f"   count_in_range({arr}, 3, 7)  = {count_in_range(arr, 3, 7)}")
    print(f"   count_in_range({arr}, 4, 6)  = {count_in_range(arr, 4, 6)}")

    assert count_at_most(arr, 5) == 4
    assert count_equal(arr, 3) == 2
    assert count_equal(arr, 7) == 2
    assert count_equal(arr, 4) == 0
    assert count_in_range(arr, 3, 7) == 5           # 3, 3, 5, 7, 7
    assert count_in_range(arr, 4, 6) == 1           # just 5

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Lower Bound + Upper Bound = Binary Search Complete:
    #
    #   With these two as primitives, you can answer:
    #
    #     first occurrence            = lower_bound (if match)
    #     last occurrence             = upper_bound - 1 (if match)
    #     number equal to target      = upper_bound - lower_bound
    #     number less than target     = lower_bound
    #     number at most target       = upper_bound
    #     count in [lo, hi] range     = upper_bound(hi) - lower_bound(lo)
    #     smallest > target           = upper_bound (returns the index)
    #     largest <= target           = upper_bound - 1
    #
    # Almost all "binary search with twists" problems collapse to one
    # or two calls to these two functions. Memorize the templates;
    # the rest is composition.
    # ---------------------------------------------------------------
