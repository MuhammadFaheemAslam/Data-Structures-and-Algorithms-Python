"""
recursive.py – Recursive Binary Search

The same algorithm as iterative.py, written as a recursion. Useful
for understanding the divide-and-conquer structure of binary search;
in practice, prefer the iterative form (see iterative.py).

Divide:   pick mid = (lo + hi) // 2; compare arr[mid] with target.
Conquer:  recurse into ONE half — the one that could still contain target.
Combine:  nothing — the recursive call's answer IS the answer.

This structure is unusual for divide & conquer: only ONE subproblem,
not two. That's why binary search is O(log n) rather than O(n log n):

    T(n) = T(n/2) + O(1)     →     O(log n)

(See Phase-02 / 01 / 02-Divide-Conquer / theory.md for the master
theorem analysis.)
---------------------------------------------------
Recursion vs Iteration:

Same time complexity. Different constants.

                    Iterative         Recursive
    Time:           O(log n)          O(log n)
    Space:          O(1)              O(log n) — stack frames
    Idiomatic:      yes               educational only

In Python, recursion also risks hitting the default recursion limit
(~1000). For log-depth searches this is harmless unless n > 2^1000,
which is… unlikely. But for readability, the iterative form wins.

This file exists because binary search is traditionally TAUGHT as a
recursion first — the divide/conquer structure is easier to see.
After you've seen it, the iterative form reads naturally.

---------------------------------------------------
"""

# =========================================================================
# Recursive Binary Search — Inclusive [lo, hi] Range
# =========================================================================

def binary_search_recursive(arr, target):
    """
    Outer function — handles the initial call with the full range.

    Time Complexity:  O(log n)
    Space Complexity: O(log n) for the call stack

    Assumes `arr` is sorted ascending.
    """
    return _search(arr, target, 0, len(arr) - 1)


def _search(arr, target, lo, hi):
    """
    Inner recursive helper: search for `target` within arr[lo..hi]
    (INCLUSIVE on both ends).
    """
    # base case: empty range
    if lo > hi:
        return -1

    mid = lo + (hi - lo) // 2

    # found
    if arr[mid] == target:
        return mid

    # recurse into ONE half
    if arr[mid] < target:
        return _search(arr, target, mid + 1, hi)
    else:
        return _search(arr, target, lo, mid - 1)


# =========================================================================
# Recursive Binary Search — Exclusive [lo, hi) Range
# =========================================================================

def binary_search_recursive_exclusive(arr, target):
    """
    The [lo, hi) exclusive convention as a recursion.
    """
    def search(lo, hi):
        if lo >= hi:
            return -1

        mid = lo + (hi - lo) // 2

        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            return search(mid + 1, hi)
        return search(lo, mid)

    return search(0, len(arr))


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]

    print(f"arr = {arr}")
    print()
    print("Recursive binary_search:")
    for target in [1, 13, 19, 4, 20, 0, 10]:
        print(f"   binary_search_recursive(arr, {target:2}) = "
              f"{binary_search_recursive(arr, target)}")
    print()

    # Extensive test cases
    test_cases = [
        ([1, 3, 5, 7, 9],        5,   2),
        ([1, 3, 5, 7, 9],        1,   0),
        ([1, 3, 5, 7, 9],        9,   4),
        ([1, 3, 5, 7, 9],        4,   -1),
        ([1, 3, 5, 7, 9],        0,   -1),
        ([1, 3, 5, 7, 9],        10,  -1),
        ([],                     5,   -1),
        ([42],                   42,  0),
        ([42],                   10,  -1),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 7, 6),
    ]

    for i, (data, tgt, expected) in enumerate(test_cases):
        for fn in (binary_search_recursive, binary_search_recursive_exclusive):
            got = fn(data, tgt)
            assert got == expected, (
                f"Test {i+1} ({fn.__name__}) failed on {data}, target={tgt}: "
                f"expected {expected}, got {got}"
            )
        print(f"Test {i+1} passed: target={tgt} -> {expected}")

    # Recursion depth check — binary search should use ~log2(n) stack frames
    import sys
    # a large array — binary search should handle it well within the limit
    big = list(range(10_000))
    sys.setrecursionlimit(200)                    # ~log2(10_000) ≈ 14; 200 is overkill
    assert binary_search_recursive(big, 7500) == 7500
    sys.setrecursionlimit(1000)                   # restore default
    print("\nRecursion depth test: 10_000-element array fits in a small stack.")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Iterative vs Recursive — When to Prefer Which:
    #
    #   Iterative:
    #     - Production code.
    #     - Easier to adapt to the four boundary variations.
    #     - No risk of stack overflow.
    #     - O(1) space.
    #
    #   Recursive:
    #     - Teaching the divide-and-conquer structure.
    #     - Problems where the recursion is on a MORE COMPLEX state
    #       (e.g., binary search on a 2D matrix where mid is a pair).
    #
    # For plain sorted-array binary search, use iterative. Always.
    # ---------------------------------------------------------------
