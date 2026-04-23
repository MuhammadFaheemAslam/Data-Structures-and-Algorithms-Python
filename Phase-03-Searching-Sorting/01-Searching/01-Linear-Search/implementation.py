"""
implementation.py – Linear Search

The simplest possible search algorithm: walk the array from start to
end, returning the position of the first (or every) occurrence of the
target. O(n) time, O(1) space.

Linear Search is:
    - Trivially correct. No preconditions.
    - The FASTEST algorithm for UNSORTED data (you have to look at
      each element at least once).
    - The baseline every other search beats by exploiting STRUCTURE
      that linear search doesn't use (sortedness, hashing, skip pointers).

This file implements several common variants:

    1. linear_search              — first occurrence, iterative
    2. linear_search_all          — every occurrence
    3. linear_search_recursive    — same algorithm, written recursively
    4. linear_search_with_key     — search with a custom key function
    5. find_min_linear / find_max_linear — single-pass min/max

Run this file to see each variant's output.
"""

# =========================================================================
# 1. First Occurrence (Iterative)
# =========================================================================

def linear_search(arr, target):
    """
    Return the index of the first occurrence of `target` in `arr`,
    or -1 if not found.

    Time:  O(n) worst case, O(1) best case (target is at arr[0])
    Space: O(1)
    """
    for i, x in enumerate(arr):
        if x == target:
            return i
    return -1


# =========================================================================
# 2. All Occurrences
# =========================================================================

def linear_search_all(arr, target):
    """
    Return a list of every index at which `target` occurs in `arr`.

    Time:  O(n) — we must scan the whole array regardless of finds.
    Space: O(k) where k = number of matches.
    """
    return [i for i, x in enumerate(arr) if x == target]


# =========================================================================
# 3. Recursive Version
# =========================================================================

def linear_search_recursive(arr, target, i=0):
    """
    Same algorithm, written recursively.

    Time:  O(n)
    Space: O(n) for the call stack.

    Educational only — the recursion adds nothing over the loop. In
    Python, deep recursion will also hit the default recursion limit
    (~1000) for large arrays.
    """
    if i >= len(arr):
        return -1
    if arr[i] == target:
        return i
    return linear_search_recursive(arr, target, i + 1)


# =========================================================================
# 4. Search with a Custom Key
# =========================================================================

def linear_search_with_key(arr, target, key):
    """
    Return the index of the first element `x` such that `key(x) == target`.

    Useful when searching lists of objects / tuples by one field.

        users = [("alice", 30), ("bob", 25), ("carol", 30)]
        linear_search_with_key(users, 25, key=lambda u: u[1])  -> 1
    """
    for i, x in enumerate(arr):
        if key(x) == target:
            return i
    return -1


# =========================================================================
# 5. Single-Pass Min and Max
# =========================================================================

def find_min_linear(arr):
    """
    Return (index, value) of the minimum element via a single pass.
    Raises ValueError on empty input (matches Python's built-in min()).

    Time:  O(n)
    Space: O(1)
    """
    if not arr:
        raise ValueError("find_min_linear() arg is empty")

    best_i = 0
    best_v = arr[0]
    for i in range(1, len(arr)):
        if arr[i] < best_v:
            best_v = arr[i]
            best_i = i
    return best_i, best_v


def find_max_linear(arr):
    """Mirror of find_min_linear — returns (index, value) of the maximum."""
    if not arr:
        raise ValueError("find_max_linear() arg is empty")

    best_i = 0
    best_v = arr[0]
    for i in range(1, len(arr)):
        if arr[i] > best_v:
            best_v = arr[i]
            best_i = i
    return best_i, best_v


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]

    print(f"arr = {arr}")
    print()

    # 1. First occurrence
    print("First Occurrence:")
    print(f"   linear_search(arr, 4)   = {linear_search(arr, 4)}")
    print(f"   linear_search(arr, 5)   = {linear_search(arr, 5)}   (first of multiple 5s)")
    print(f"   linear_search(arr, 99)  = {linear_search(arr, 99)}  (not found)")
    print()

    # 2. All occurrences
    print("All Occurrences:")
    print(f"   linear_search_all(arr, 5)  = {linear_search_all(arr, 5)}")
    print(f"   linear_search_all(arr, 1)  = {linear_search_all(arr, 1)}")
    print(f"   linear_search_all(arr, 99) = {linear_search_all(arr, 99)}")
    print()

    # 3. Recursive
    print("Recursive:")
    print(f"   linear_search_recursive(arr, 9) = {linear_search_recursive(arr, 9)}")
    print()

    # 4. With key function
    print("With Key Function:")
    users = [("alice", 30), ("bob", 25), ("carol", 30), ("dan", 40)]
    print(f"   users = {users}")
    print(f"   linear_search_with_key(users, 25, key=age) = "
          f"{linear_search_with_key(users, 25, key=lambda u: u[1])}")
    print(f"   linear_search_with_key(users, 'dan', key=name) = "
          f"{linear_search_with_key(users, 'dan', key=lambda u: u[0])}")
    print()

    # 5. Min/Max
    print("Min / Max:")
    print(f"   find_min_linear(arr) = {find_min_linear(arr)}")
    print(f"   find_max_linear(arr) = {find_max_linear(arr)}")
    print()

    # Test cases — assertions for each variant
    assert linear_search([1, 2, 3], 2) == 1
    assert linear_search([1, 2, 3], 5) == -1
    assert linear_search([], 1) == -1
    assert linear_search([7], 7) == 0

    assert linear_search_all([1, 2, 1, 3, 1], 1) == [0, 2, 4]
    assert linear_search_all([1, 2, 3], 5) == []
    assert linear_search_all([], 1) == []

    assert linear_search_recursive([1, 2, 3, 4, 5], 3) == 2
    assert linear_search_recursive([1, 2, 3], 99) == -1

    assert linear_search_with_key([("a", 1), ("b", 2)], 2, key=lambda x: x[1]) == 1

    assert find_min_linear([3, 1, 4, 1, 5, 9]) == (1, 1)      # first min
    assert find_max_linear([3, 1, 4, 1, 5, 9]) == (5, 9)

    # Edge cases
    try:
        find_min_linear([])
    except ValueError:
        pass
    else:
        raise AssertionError("find_min_linear([]) should raise")

    print("All tests passed!")

    # ---------------------------------------------------------------
    # When to Use Linear Search:
    #
    #   - Data is UNSORTED and will only be searched once.
    #   - Data is very small (n ≤ ~50).
    #   - Structure of data doesn't support binary/hash (e.g., linked
    #     list traversal, stream processing).
    #   - You need a FIRST (or ALL) match by some complex predicate
    #     that isn't just equality.
    #
    # When NOT to use Linear Search:
    #
    #   - Data is sorted    → Binary Search — O(log n).
    #   - Data will be searched many times → Hashing — O(1) per query.
    #   - Data is huge and on disk    → Skip list / B-tree / index.
    # ---------------------------------------------------------------
