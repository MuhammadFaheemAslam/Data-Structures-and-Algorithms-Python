"""
lower-bound.py – First Index with arr[i] >= target

The most useful binary-search variation after plain-old search.

    lower_bound(arr, target) = smallest i such that arr[i] >= target
                             = the index where `target` would be inserted
                               into `arr` to keep it sorted, preferring
                               the LEFTMOST insertion point for ties.

Equivalently — this is Python's `bisect.bisect_left(arr, target)`.

---------------------------------------------------
Why It's So Useful:

Lower bound answers a whole family of questions:

    1. First index with arr[i] >= target        — directly.
    2. First index with arr[i] > target         — upper_bound (see upper-bound.py).
    3. Number of elements < target              — just `lower_bound(arr, target)`.
    4. Is `target` present?                     — check arr[lower_bound(...)] == target.
    5. First occurrence of target (if present)  — check the above and return.
    6. Closest value to target                  — inspect lower_bound(...) and the one before.
    7. Insert while maintaining sorted order    — insert at lower_bound(...).

Being able to implement this variant cleanly is the boundary between
"knows binary search" and "uses binary search in real problems".

---------------------------------------------------
The Template (Exclusive-hi, the Cleanest Form):

    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid                  # arr[mid] is a CANDIDATE answer
    return lo                         # lo == hi is the final answer

The key move: when arr[mid] >= target, we DON'T discard mid — we
keep it in the range by setting `hi = mid` (NOT `mid - 1`). That
lets mid remain a candidate for the answer.

---------------------------------------------------
Return Value:

lower_bound returns a value in [0, n] — INCLUSIVE of n. If target is
greater than every element, lower_bound returns n (one past the last
index). This is intentional and useful: it's the correct "insert at
the end" position.

Check `idx < n` before accessing arr[idx].

---------------------------------------------------
Example:

    arr = [1, 3, 3, 5, 7, 7, 9]
    lower_bound(arr, 3) → 1       (first 3 is at index 1)
    lower_bound(arr, 4) → 3       (insert 4 before the 5 at index 3)
    lower_bound(arr, 0) → 0       (before everything)
    lower_bound(arr, 10) → 7      (one past the end)

---------------------------------------------------
"""

# =========================================================================
# Lower Bound — Iterative
# =========================================================================

def lower_bound(arr, target):
    """
    Return the smallest index `i` with arr[i] >= target. If no such
    index exists (target is greater than every element), returns len(arr).

    Time Complexity:  O(log n)
    Space Complexity: O(1)
    """
    lo, hi = 0, len(arr)

    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] < target:
            lo = mid + 1                          # mid is too small — exclude
        else:
            hi = mid                              # mid is a candidate — keep

    return lo


# =========================================================================
# Useful Derivatives
# =========================================================================

def count_less_than(arr, target):
    """
    Count how many elements in the sorted array are STRICTLY less
    than `target`.

    This is just `lower_bound(arr, target)` — no extra work.
    """
    return lower_bound(arr, target)


def contains_target(arr, target):
    """
    Check whether `target` is present, using lower_bound.

    Compare to iterative.py's binary_search — same Big-O, this version
    is composed with lower_bound rather than a standalone loop.
    """
    idx = lower_bound(arr, target)
    return idx < len(arr) and arr[idx] == target


def insert_sorted(arr, x):
    """
    Insert `x` into sorted `arr` at its lower-bound position.
    Returns the new list (doesn't mutate).

    Useful as the "maintain sorted order on each insert" operation —
    though for repeated insertions you'd want a balanced BST or
    `SortedList` from the `sortedcontainers` library.
    """
    idx = lower_bound(arr, x)
    return arr[:idx] + [x] + arr[idx:]


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    from bisect import bisect_left

    arr = [1, 3, 3, 5, 7, 7, 9]
    print(f"arr = {arr}")
    print()
    for target in [3, 4, 0, 10, 7, 9]:
        got = lower_bound(arr, target)
        builtin = bisect_left(arr, target)
        assert got == builtin
        print(f"   lower_bound(arr, {target:2}) = {got}   (bisect_left: {builtin})")
    print()

    # Test cases — verify against Python's bisect_left
    test_cases = [
        # (arr, target, expected)
        ([1, 3, 3, 5, 7, 7, 9],  3,   1),
        ([1, 3, 3, 5, 7, 7, 9],  4,   3),
        ([1, 3, 3, 5, 7, 7, 9],  0,   0),
        ([1, 3, 3, 5, 7, 7, 9],  10,  7),
        ([1, 3, 3, 5, 7, 7, 9],  1,   0),
        ([1, 3, 3, 5, 7, 7, 9],  9,   6),
        ([],                     5,   0),
        ([5],                    5,   0),
        ([5],                    3,   0),
        ([5],                    7,   1),
        ([1, 1, 1, 1],           1,   0),
        ([1, 1, 1, 1],           2,   4),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5, 4),
    ]

    for i, (data, tgt, expected) in enumerate(test_cases):
        got = lower_bound(data, tgt)
        builtin = bisect_left(data, tgt)
        assert got == expected == builtin, (
            f"Test {i+1} failed on {data}, target={tgt}: "
            f"expected {expected}, got {got} (bisect says {builtin})"
        )
        print(f"Test {i+1} passed: target={tgt} -> {expected}")

    # Derivatives
    print()
    print("Derivatives:")
    print(f"   count_less_than([1, 3, 3, 5, 7, 7, 9], 5) = {count_less_than([1, 3, 3, 5, 7, 7, 9], 5)}")
    print(f"   contains_target([1, 3, 5], 3) = {contains_target([1, 3, 5], 3)}")
    print(f"   contains_target([1, 3, 5], 4) = {contains_target([1, 3, 5], 4)}")
    print(f"   insert_sorted([1, 3, 5, 7], 4) = {insert_sorted([1, 3, 5, 7], 4)}")

    assert count_less_than([1, 3, 3, 5, 7, 7, 9], 5) == 3
    assert contains_target([1, 3, 5], 3) is True
    assert contains_target([1, 3, 5], 4) is False
    assert insert_sorted([1, 3, 5, 7], 4) == [1, 3, 4, 5, 7]

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Lower Bound Is the Most Reusable Binary-Search Variant:
    #
    #   Almost every "is X present / how many are less / what's the
    #   closest" question reduces to a call to lower_bound. Master
    #   this one implementation and you've covered most binary-search
    #   interview problems.
    #
    # In Python, use `bisect_left` for production code. Implement
    # lower_bound yourself when you need to customize the comparison
    # or the data structure (e.g., binary searching on an ANSWER rather
    # than an array — see Phase-02 / 02 / 05-Binary-Search-on-Answer).
    # ---------------------------------------------------------------
