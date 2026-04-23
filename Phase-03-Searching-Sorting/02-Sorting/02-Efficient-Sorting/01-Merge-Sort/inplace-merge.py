"""
inplace-merge.py – In-Place Merge (Rotations, No Auxiliary Array)

Standard merge sort uses O(n) auxiliary space for the merge buffer.
Eliminating that buffer — truly in-place merge — is HARD. Pure in-place
merge sort exists but either:

    - Uses O(n log² n) time with a block-rotation merge (shown here), or
    - Uses O(n log n) time with complex buffer-management tricks that
      sacrifice constant factors (and stability).

In practice, NO production sort uses in-place merge sort. The memory
savings don't justify the algorithmic complexity. This file exists to
show what the trick LOOKS like — it's a classic CS exercise.

---------------------------------------------------
The Algorithm:

    To merge arr[lo..mid] and arr[mid..hi] (both sorted) IN PLACE:

        while both halves have elements:
            if arr[lo] <= arr[mid]:
                lo += 1          # left head already in place
            else:
                # arr[mid] should go to position `lo`. But we can't
                # swap — that destroys left-half order. Instead ROTATE:
                #   shift arr[lo..mid-1] right by one, pulling arr[mid] to arr[lo].
                rotate(arr, lo, mid + 1)
                lo += 1
                mid += 1

Each rotation is O(mid - lo). Total merge work: O(n²) in the worst
case, giving overall O(n² · log n). That's worse than plain merge
sort with a buffer.

A cleverer approach — **block rotations** — achieves O(n · log² n):
split the array into blocks of size √n and exchange blocks using
cyclic rotations. We skip that here; it's a rabbit hole.

---------------------------------------------------
Why It Matters Historically:

In-place merge sort was the Holy Grail of sorting theory for decades.
The existence of an O(n log n), in-place, stable sort was only proved
in the 2000s with a tangled mess of book-keeping. Industrial sorts
(Timsort, pdqsort) sidestep the problem by accepting O(n) auxiliary
memory — almost always a good tradeoff.

---------------------------------------------------
"""

# =========================================================================
# Rotation Helper
# =========================================================================

def _rotate(arr, lo, hi):
    """
    Right-rotate arr[lo..hi] by one position.

    Before:  arr[lo], arr[lo+1], ..., arr[hi-1]
    After:   arr[hi-1], arr[lo], ..., arr[hi-2]

    In other words: move the last element of the range to the front,
    shifting everything else right.

    Time:   O(hi - lo)
    """
    value = arr[hi - 1]
    for i in range(hi - 1, lo, -1):
        arr[i] = arr[i - 1]
    arr[lo] = value


# =========================================================================
# In-Place Merge (Rotation-Based)
# =========================================================================

def inplace_merge(arr, lo, mid, hi):
    """
    Merge arr[lo..mid] (sorted) and arr[mid..hi] (sorted) in place.

    Time:   O((hi - lo)²) worst case due to rotations.
    Space:  O(1)
    Stable: Yes

    Interface: modifies arr directly; no return.
    """
    while lo < mid and mid < hi:
        if arr[lo] <= arr[mid]:
            lo += 1                               # left head already in place
        else:
            # arr[mid] < arr[lo] — bring arr[mid] to position lo
            # by rotating arr[lo..mid+1] right by one.
            _rotate(arr, lo, mid + 1)
            lo += 1
            mid += 1                              # the boundary moved too


# =========================================================================
# In-Place Merge Sort (For Demonstration)
# =========================================================================

def inplace_merge_sort(arr):
    """
    Merge sort using the rotation-based in-place merge.

    Time:   O(n² log n) worst case  — DON'T ship this.
    Space:  O(1) auxiliary beyond the recursion stack.
    Stable: Yes

    The O(n² log n) comes from: log n levels of recursion, each doing
    O(n²) work for the merge (due to rotations). Included as a
    curiosity; do not use on inputs larger than ~1000.
    """
    def sort(lo, hi):
        if hi - lo <= 1:
            return
        mid = (lo + hi) // 2
        sort(lo, mid)
        sort(mid, hi)
        inplace_merge(arr, lo, mid, hi)

    sort(0, len(arr))
    return arr


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    # Test the merge helper alone
    print("Testing inplace_merge on pre-split arrays:")
    cases = [
        # (arr, lo, mid, hi, expected)
        ([1, 3, 5, 2, 4, 6], 0, 3, 6, [1, 2, 3, 4, 5, 6]),
        ([1, 5, 8, 2, 3, 9], 0, 3, 6, [1, 2, 3, 5, 8, 9]),
        ([2, 4, 6, 1, 3, 5], 0, 3, 6, [1, 2, 3, 4, 5, 6]),
        ([1, 2, 3, 4, 5, 6], 0, 3, 6, [1, 2, 3, 4, 5, 6]),   # already merged
        ([4, 5, 6, 1, 2, 3], 0, 3, 6, [1, 2, 3, 4, 5, 6]),   # worst case
    ]
    for arr, lo, mid, hi, expected in cases:
        work = arr[:]
        inplace_merge(work, lo, mid, hi)
        assert work == expected, f"inplace_merge({arr}) -> {work}, expected {expected}"
        print(f"   inplace_merge({arr}, {lo}, {mid}, {hi}) -> {work}")

    print()

    # Test full in-place merge sort
    print("Testing full in-place merge sort:")
    test_cases = [
        [38, 27, 43, 3, 9, 82, 10],
        [],
        [5],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [3, 1, 3, 1, 3],
        [0, -1, 2, -3, 4, -5],
        [7] * 10,
    ]

    for i, data in enumerate(test_cases):
        expected = sorted(data)
        got = inplace_merge_sort(data[:])
        assert got == expected, f"Test {i+1} failed on {data}"
        print(f"Test {i+1} passed: len={len(data)}")

    # Stability check
    pairs = [(1, "a"), (2, "b"), (1, "c"), (2, "d"), (1, "e")]
    def inplace_merge_sort_pairs(arr):
        arr = list(arr)
        def inmerge(lo, mid, hi):
            while lo < mid and mid < hi:
                if arr[lo][0] <= arr[mid][0]:
                    lo += 1
                else:
                    value = arr[mid]
                    for i in range(mid, lo, -1):
                        arr[i] = arr[i - 1]
                    arr[lo] = value
                    lo += 1
                    mid += 1

        def sort(lo, hi):
            if hi - lo <= 1:
                return
            mid = (lo + hi) // 2
            sort(lo, mid)
            sort(mid, hi)
            inmerge(lo, mid, hi)

        sort(0, len(arr))
        return arr

    sorted_pairs = inplace_merge_sort_pairs(pairs)
    assert sorted_pairs == [(1, "a"), (1, "c"), (1, "e"), (2, "b"), (2, "d")]
    print(f"\nStability check passed: {sorted_pairs}")

    # Stress test (kept small because of the O(n² log n) cost)
    import random
    random.seed(7)
    for _ in range(50):
        n = random.randint(0, 25)
        data = [random.randint(-50, 50) for _ in range(n)]
        assert inplace_merge_sort(data[:]) == sorted(data)

    print("\nStress test: 50 small random arrays matched sorted()")

    print("\nAll tests passed!")
