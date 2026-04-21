"""
Problem: Merge Sort

Paradigm: Divide & Conquer
Difficulty: Easy-Medium (foundational algorithm)

---------------------------------------------------
Problem Statement:

Sort an array of comparable values in ascending order.
Return a new sorted list (this implementation is NOT in place).

---------------------------------------------------
The Divide & Conquer Lens:

Merge sort is the canonical D&C sorting algorithm. The three steps:

    Divide:  split the array in half.
    Conquer: recursively sort each half.
    Combine: merge two sorted halves into one sorted array  ← O(n)

Recurrence:     T(n) = 2 * T(n/2) + O(n)
Master theorem: a = 2, b = 2, d = 1  →  d == log_b(a)  →  O(n log n)

Key properties:
    - Guaranteed O(n log n) — unlike quicksort, NO bad worst case.
    - Stable — equal elements keep their original relative order.
    - Needs O(n) extra space for the merge buffer.

---------------------------------------------------
Example:

    [38, 27, 43, 3, 9, 82, 10]
    -> [3, 9, 10, 27, 38, 43, 82]

---------------------------------------------------
"""

# -------------------------------------------------
# The Merge Sort Algorithm
# -------------------------------------------------

def merge_sort(arr):
    """
    Sort `arr` using Divide & Conquer.

    Time Complexity:  O(n log n)  — ALL cases (best, worst, average)
    Space Complexity: O(n)        — merge buffers

    Unlike quicksort, there is no pathological input. The array is split
    the same way regardless of values, so the recurrence is always
    T(n) = 2T(n/2) + O(n).
    """
    # base case: a list of 0 or 1 elements is already sorted
    if len(arr) <= 1:
        return arr[:]                           # return a copy

    # divide: split at the middle
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])                # conquer left
    right = merge_sort(arr[mid:])               # conquer right

    # combine: merge two sorted lists
    return _merge(left, right)


def _merge(left, right):
    """
    Combine step of merge sort.

    Given two already-sorted lists, return a single sorted list containing
    all their elements.

    Time Complexity:  O(len(left) + len(right))
    Space Complexity: O(len(left) + len(right))

    The two-pointer walk is what keeps merge sort linear in each level
    of the recursion — and therefore O(n log n) overall.
    """
    merged = []
    i = j = 0

    # walk both lists with two pointers
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:                 # `<=` keeps the sort stable
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # one list is exhausted; append whatever's left of the other
    merged.extend(left[i:])
    merged.extend(right[j:])

    return merged


# -------------------------------------------------
# In-Place Variant (Sort By Index Ranges)
# -------------------------------------------------

def merge_sort_in_place(arr):
    """
    A version that sorts `arr` in place (mutating it), avoiding the
    repeated slice copies of the classic implementation.

    Still uses O(n) auxiliary space for the merge buffer — merge sort
    cannot be done in TRUE O(1) space without complex rearrangements.

    Time Complexity:  O(n log n)
    Space Complexity: O(n)
    """
    def sort(lo, hi):
        if hi - lo <= 1:                        # 0 or 1 element
            return

        mid = (lo + hi) // 2
        sort(lo, mid)
        sort(mid, hi)
        merge_range(lo, mid, hi)

    def merge_range(lo, mid, hi):
        left = arr[lo:mid]                      # auxiliary buffers
        right = arr[mid:hi]

        i = j = 0
        k = lo
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            arr[k] = left[i]; i += 1; k += 1
        while j < len(right):
            arr[k] = right[j]; j += 1; k += 1

    sort(0, len(arr))


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    data = [38, 27, 43, 3, 9, 82, 10]

    print(f"input:  {data}")
    print(f"sorted: {merge_sort(data)}")
    print(f"input still: {data}   (merge_sort is non-destructive)")
    print()

    # Test cases – covering edge cases
    test_cases = [
        [38, 27, 43, 3, 9, 82, 10],             # typical
        [],                                      # empty
        [5],                                     # single element
        [1, 2, 3, 4, 5],                         # already sorted
        [5, 4, 3, 2, 1],                         # reverse sorted
        [3, 1, 3, 1, 3],                         # duplicates
        [0, -1, 2, -3, 4, -5],                   # negatives
        [7] * 20,                                # all equal
    ]

    for i, data in enumerate(test_cases):
        expected = sorted(data)

        got = merge_sort(data)
        assert got == expected, f"Test {i+1} (merge_sort) failed on {data}"

        mutable_copy = data[:]
        merge_sort_in_place(mutable_copy)
        assert mutable_copy == expected, (
            f"Test {i+1} (merge_sort_in_place) failed on {data}"
        )

        print(f"Test {i+1} passed: {data} -> {expected}")

    # Verify stability on a custom comparable
    pairs = [(1, "a"), (2, "b"), (1, "c"), (2, "d"), (1, "e")]
    stable_sorted = merge_sort(pairs)
    assert stable_sorted == [(1, "a"), (1, "c"), (1, "e"), (2, "b"), (2, "d")], (
        "Merge sort should be stable — equal keys must keep input order"
    )
    print(f"\nStability check passed: {pairs} -> {stable_sorted}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Why Merge Sort Matters:
    #
    #   - Guaranteed O(n log n) — no adversarial input makes it slow.
    #   - Stable — preserves order of equal elements.
    #   - External-memory friendly — merges stream naturally, so merge
    #     sort is the algorithm of choice for data that doesn't fit
    #     in RAM (see: Timsort, Python's built-in sort).
    #
    # Python's `sorted()` and `list.sort()` use **Timsort**, which is
    # a merge-sort variant that exploits pre-sorted runs in real data.
    # ---------------------------------------------------------------
