"""
merge-sort.py – Merge Sort (Top-Down Recursive, Standard Version)

The archetypal O(n log n) sort. Divide the array in half, recursively
sort each half, then MERGE the two sorted halves. See
Phase-02 / 01 / 02-Divide-Conquer / theory.md for the paradigm view.

---------------------------------------------------
Time:   O(n log n) on ALL inputs (best, average, worst).
Space:  O(n) for the merge buffer; O(log n) for recursion stack.
Stable: Yes (with `<=` in the merge).
In place: No — uses O(n) auxiliary memory.
Adaptive: No — the classical version always splits at the midpoint.

---------------------------------------------------
Why Merge Sort Matters Even When Quick Sort Is Faster:

    - **Guaranteed O(n log n).** Quick sort has O(n²) worst case; merge
      sort doesn't. On adversarial or worst-case inputs (pre-sorted
      arrays, all-equal arrays) merge sort's predictability wins.
    - **Stable.** Needed for multi-key sorts ("sort by name, then by age").
    - **External-memory friendly.** Merging streams from disk or tape
      is natural; quicksort's in-place partitioning isn't. This is
      why merge sort is the algorithm of choice for sorting data too
      big to fit in RAM.
    - **Parallelizable.** The two recursive calls are independent —
      one goroutine / thread each.
    - **Used inside Timsort.** Python's `list.sort()` merges runs using
      a merge sort variant — not quicksort.

---------------------------------------------------
The Algorithm:

    def merge_sort(arr):
        if len(arr) <= 1: return arr
        mid = len(arr) // 2
        left = merge_sort(arr[:mid])
        right = merge_sort(arr[mid:])
        return merge(left, right)

    def merge(left, right):
        two-pointer walk: take the smaller head each step

---------------------------------------------------
"""

# =========================================================================
# Top-Down Recursive Merge Sort
# =========================================================================

def merge_sort(arr):
    """
    Return a NEW sorted list. The input is not mutated.

    Time:   O(n log n)
    Space:  O(n) (plus O(log n) recursion)
    Stable: Yes
    """
    if len(arr) <= 1:
        return arr[:]

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left, right):
    """
    Merge two already-sorted lists into one sorted list.

    Uses `<=` (not `<`) so equal elements preserve left-first order —
    the source of merge sort's stability.

    Time:   O(len(left) + len(right))
    Space:  O(len(left) + len(right)) for the output
    """
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:                 # `<=` = stability
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


# =========================================================================
# In-Place-Style Merge Sort (Index-Based, Avoids Slice Copies)
# =========================================================================

def merge_sort_index_based(arr):
    """
    Sort `arr` in place (from the caller's view), but internally still
    uses an O(n) auxiliary buffer for merging. Avoids the repeated
    slice allocations of the classical version.

    Time:   O(n log n)
    Space:  O(n) auxiliary
    """
    if len(arr) <= 1:
        return arr

    def sort(lo, hi):
        if hi - lo <= 1:                        # 0 or 1 element
            return
        mid = (lo + hi) // 2
        sort(lo, mid)
        sort(mid, hi)
        merge_range(lo, mid, hi)

    def merge_range(lo, mid, hi):
        left = arr[lo:mid]
        right = arr[mid:hi]

        i = j = 0
        k = lo
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                arr[k] = left[i]; i += 1
            else:
                arr[k] = right[j]; j += 1
            k += 1
        while i < len(left):
            arr[k] = left[i]; i += 1; k += 1
        while j < len(right):
            arr[k] = right[j]; j += 1; k += 1

    sort(0, len(arr))
    return arr


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    arr = [38, 27, 43, 3, 9, 82, 10]

    print(f"Input:  {arr}")
    print(f"Sorted: {merge_sort(arr)}")
    print(f"Input unchanged (merge_sort is non-destructive): {arr}")
    print()

    # Test cases
    test_cases = [
        [38, 27, 43, 3, 9, 82, 10],
        [],
        [5],
        [1, 2, 3, 4, 5],                          # already sorted
        [5, 4, 3, 2, 1],                          # reverse sorted
        [3, 1, 3, 1, 3],                          # duplicates
        [0, -1, 2, -3, 4, -5],                    # negatives
        [7] * 20,                                 # all equal
    ]

    for i, data in enumerate(test_cases):
        expected = sorted(data)

        # top-down version (non-mutating)
        got = merge_sort(data)
        assert got == expected, f"Test {i+1} (top-down) failed"

        # index-based version (mutating)
        mut = data[:]
        merge_sort_index_based(mut)
        assert mut == expected, f"Test {i+1} (index-based) failed"

        print(f"Test {i+1} passed: len={len(data)}")

    # Stability: equal keys should keep input order
    pairs = [(1, "a"), (2, "b"), (1, "c"), (2, "d"), (1, "e")]
    # sort pairs by first element via a small merge-sort
    def merge_sort_pairs(arr):
        if len(arr) <= 1:
            return arr[:]
        mid = len(arr) // 2
        L = merge_sort_pairs(arr[:mid])
        R = merge_sort_pairs(arr[mid:])
        out = []
        i = j = 0
        while i < len(L) and j < len(R):
            if L[i][0] <= R[j][0]:
                out.append(L[i]); i += 1
            else:
                out.append(R[j]); j += 1
        out.extend(L[i:]); out.extend(R[j:])
        return out

    sorted_pairs = merge_sort_pairs(pairs)
    assert sorted_pairs == [(1, "a"), (1, "c"), (1, "e"), (2, "b"), (2, "d")]
    print(f"\nStability check passed: {sorted_pairs}")

    # Stress test
    import random
    random.seed(11)
    for _ in range(100):
        n = random.randint(0, 50)
        data = [random.randint(-100, 100) for _ in range(n)]
        assert merge_sort(data) == sorted(data)
    print("\nStress test: 100 random arrays matched sorted()")

    print("\nAll tests passed!")
