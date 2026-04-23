"""
iterative.py – Iterative Binary Search (The Textbook Version)

Binary Search is the canonical **divide & conquer** search algorithm:

    - Precondition: the array is SORTED.
    - Each step compares the target with the middle element and
      DISCARDS HALF the remaining search range.
    - Result: O(log n) time, O(1) space.

This file implements the iterative version — a while loop over a
shrinking [lo, hi] range. The recursive version is in recursive.py,
the boundary-finding variants are in variations/, and the twisted
applications are in problems/.

The iterative version should be your default. It's shorter, has no
recursion overhead, and fits the "nothing fancy, just a loop" shape
that's easy to adapt to the four boundary variations.

---------------------------------------------------
The Algorithm:

    lo, hi = 0, n - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target: return mid
        if arr[mid] < target:  lo = mid + 1
        else:                   hi = mid - 1
    return -1

Four things to get right:
    1. Inclusive vs exclusive hi. This file uses INCLUSIVE hi.
    2. Loop condition. lo <= hi for inclusive hi; lo < hi for exclusive.
    3. mid update. `lo = mid + 1` and `hi = mid - 1` (both move PAST mid).
    4. Base case return. -1 when the range is empty.

Messing up any one of these gives an infinite loop or a ±1 error.
Memorize the template and it's a five-line function forever.

---------------------------------------------------
The Integer-Overflow Trap:

In C/C++, `(lo + hi) // 2` can OVERFLOW when lo and hi are both near
INT_MAX. The safer formula is `lo + (hi - lo) // 2` — same value,
no overflow. Python's ints are arbitrary-precision so it doesn't
matter here, but you should know the idiom. It's a common interview
follow-up.

---------------------------------------------------
"""

# =========================================================================
# Basic Iterative Binary Search
# =========================================================================

def binary_search(arr, target):
    """
    Return the index of `target` in sorted `arr`, or -1 if not present.

    Time Complexity:  O(log n)
    Space Complexity: O(1)

    Assumes `arr` is sorted in ascending order.
    """
    lo, hi = 0, len(arr) - 1

    while lo <= hi:
        mid = lo + (hi - lo) // 2                 # overflow-safe form
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            lo = mid + 1                          # target is to the right
        else:
            hi = mid - 1                          # target is to the left

    return -1


# =========================================================================
# Exclusive-hi Variant (the [lo, hi) convention)
# =========================================================================

def binary_search_exclusive(arr, target):
    """
    The [lo, hi) exclusive-hi convention, which some prefer because
    it matches Python's slice semantics.

    Watch the differences:
        - hi starts at len(arr), not len(arr) - 1.
        - Loop is `while lo < hi`, not `<=`.
        - `hi = mid`, not `mid - 1`.

    Time Complexity:  O(log n)
    Space Complexity: O(1)
    """
    lo, hi = 0, len(arr)

    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid                              # exclude mid in the next iteration

    return -1


# =========================================================================
# Search with a Custom Comparator
# =========================================================================

def binary_search_by_key(arr, target, key):
    """
    Binary search on a list sorted by some key function.

    Example:
        users = [("alice", 30), ("bob", 25), ("carol", 40)]  # sorted by age
        binary_search_by_key(users, 25, key=lambda u: u[1])
        → 1

    The array must be sorted by `key(x)` in ascending order.

    Time Complexity:  O(log n * cost of key)
    Space Complexity: O(1)
    """
    lo, hi = 0, len(arr) - 1

    while lo <= hi:
        mid = lo + (hi - lo) // 2
        k = key(arr[mid])
        if k == target:
            return mid
        if k < target:
            lo = mid + 1
        else:
            hi = mid - 1

    return -1


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]

    print(f"arr = {arr}")
    print()

    print("Basic binary_search:")
    for target in [1, 13, 19, 4, 20, 0, 10]:
        print(f"   binary_search(arr, {target:2}) = {binary_search(arr, target)}")
    print()

    print("Exclusive-hi version (same result):")
    for target in [1, 13, 19, 4]:
        print(f"   binary_search_exclusive(arr, {target:2}) = "
              f"{binary_search_exclusive(arr, target)}")
    print()

    print("With key function:")
    users = [("alice", 25), ("bob", 30), ("carol", 40)]
    print(f"   users (by age): {users}")
    print(f"   binary_search_by_key(users, 30, age) = "
          f"{binary_search_by_key(users, 30, key=lambda u: u[1])}")
    print()

    # Test cases — cross-verify both versions
    test_cases = [
        ([1, 3, 5, 7, 9], 5, 2),
        ([1, 3, 5, 7, 9], 1, 0),
        ([1, 3, 5, 7, 9], 9, 4),
        ([1, 3, 5, 7, 9], 4, -1),                 # between elements
        ([1, 3, 5, 7, 9], 0, -1),                 # below min
        ([1, 3, 5, 7, 9], 10, -1),                # above max
        ([], 5, -1),                               # empty
        ([42], 42, 0),                             # single element hit
        ([42], 10, -1),                            # single element miss
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 7, 6),  # even length
    ]

    for i, (data, tgt, expected) in enumerate(test_cases):
        for fn in (binary_search, binary_search_exclusive):
            got = fn(data, tgt)
            assert got == expected, (
                f"Test {i+1} ({fn.__name__}) failed on {data}, target={tgt}: "
                f"expected {expected}, got {got}"
            )
        print(f"Test {i+1} passed: target={tgt} -> {expected}")

    # Stress test — compare against linear search on random inputs
    import random
    random.seed(42)
    for _ in range(200):
        n = random.randint(0, 50)
        sorted_arr = sorted(random.sample(range(-100, 100), n))
        target = random.randint(-120, 120)

        bs = binary_search(sorted_arr, target)
        expected = sorted_arr.index(target) if target in sorted_arr else -1
        assert bs == expected, f"stress: {sorted_arr}, target={target}: {bs} != {expected}"

    print("\nStress test: 200 random sorted arrays matched linear search")
    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Two Conventions:
    #
    #   [lo, hi] inclusive:            [lo, hi) exclusive:
    #     hi = n - 1                     hi = n
    #     while lo <= hi:                while lo < hi:
    #         ...                            ...
    #         hi = mid - 1                   hi = mid
    #
    # Pick ONE and use it everywhere. Mixing them is the fastest way
    # to write a binary-search bug.
    #
    # This repo uses INCLUSIVE hi throughout — it matches most
    # textbooks and the C++ STL's `std::binary_search`. The exclusive
    # form matches Python's `bisect` module.
    # ---------------------------------------------------------------
