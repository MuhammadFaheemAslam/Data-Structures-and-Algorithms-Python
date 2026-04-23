"""
iterative-merge.py – Bottom-Up Merge Sort (No Recursion)

The same algorithm as the top-down version, but expressed as ITERATIVE
doubling instead of recursion:

    Pass 1: merge adjacent pairs of size-1 blocks → size-2 sorted blocks
    Pass 2: merge adjacent pairs of size-2 blocks → size-4 sorted blocks
    Pass 3: merge adjacent pairs of size-4 blocks → size-8 sorted blocks
    ...continue until the block size reaches n.

After ⌈log₂ n⌉ passes the whole array is sorted.

---------------------------------------------------
Same Big-O as Top-Down:

    Time:   O(n log n)
    Space:  O(n) auxiliary merge buffer
    Stable: Yes

But with three practical advantages:

    1. **No recursion** — no stack frames, no recursion-depth limit.
    2. **Cache-friendlier** on some architectures — we work on
       contiguous chunks pass-by-pass.
    3. **Parallel-friendlier** — all the pairs at a given block size
       are INDEPENDENT, so they're trivial to parallelize across
       threads without the recursive structure.

Disadvantage:

    - Slightly clunkier code, especially the "handle the leftover
      odd block at the end of each pass" case.

---------------------------------------------------
The Algorithm:

    width = 1
    while width < n:
        for lo in range(0, n, 2 * width):
            mid = min(lo + width, n)
            hi = min(lo + 2 * width, n)
            merge(arr, lo, mid, hi)
        width *= 2

---------------------------------------------------
"""

# =========================================================================
# Bottom-Up (Iterative) Merge Sort
# =========================================================================

def iterative_merge_sort(arr):
    """
    Bottom-up merge sort. Mutates `arr` in place and returns it.

    Time:   O(n log n)
    Space:  O(n) auxiliary
    Stable: Yes
    """
    n = len(arr)
    if n <= 1:
        return arr

    width = 1
    while width < n:
        # merge every adjacent pair of blocks at the current width
        for lo in range(0, n, 2 * width):
            mid = min(lo + width, n)              # edge case: last block may be short
            hi = min(lo + 2 * width, n)
            if mid < hi:                          # is there anything to merge?
                _merge_range(arr, lo, mid, hi)

        width *= 2

    return arr


def _merge_range(arr, lo, mid, hi):
    """
    Merge arr[lo..mid] and arr[mid..hi] in place, using an auxiliary buffer.

    Time:   O(hi - lo)
    """
    left = arr[lo:mid]
    right = arr[mid:hi]

    i = j = 0
    k = lo
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:                   # stable
            arr[k] = left[i]; i += 1
        else:
            arr[k] = right[j]; j += 1
        k += 1
    while i < len(left):
        arr[k] = left[i]; i += 1; k += 1
    while j < len(right):
        arr[k] = right[j]; j += 1; k += 1


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    arr = [38, 27, 43, 3, 9, 82, 10]
    print(f"Input:  {arr}")
    iterative_merge_sort(arr)
    print(f"Sorted: {arr}")
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
        list(range(100, 0, -1)),                   # 100-element reverse
        [random_val for random_val in [42, 17, 29, 38, 5, 91, 3, 64, 27, 48]],
    ]

    for i, data in enumerate(test_cases):
        expected = sorted(data)
        mut = data[:]
        got = iterative_merge_sort(mut)
        assert got == expected, f"Test {i+1} failed on {data}"
        print(f"Test {i+1} passed: len={len(data)}")

    # Test against a non-power-of-two length (trickiest edge case)
    for odd_len in [3, 5, 7, 9, 11, 13, 100, 1001]:
        data = list(range(odd_len, 0, -1))        # reverse-sorted
        got = iterative_merge_sort(data)
        assert got == list(range(1, odd_len + 1)), f"Failed on len {odd_len}"
    print(f"\nNon-power-of-two lengths: OK ({odd_len} elements max)")

    # Stability check
    pairs = [(1, "a"), (2, "b"), (1, "c"), (2, "d"), (1, "e")]
    def iter_merge_sort_pairs(arr):
        arr = list(arr)
        n = len(arr)
        width = 1
        while width < n:
            for lo in range(0, n, 2 * width):
                mid = min(lo + width, n)
                hi = min(lo + 2 * width, n)
                if mid >= hi:
                    continue
                left = arr[lo:mid]
                right = arr[mid:hi]
                i = j = 0
                k = lo
                while i < len(left) and j < len(right):
                    if left[i][0] <= right[j][0]:
                        arr[k] = left[i]; i += 1
                    else:
                        arr[k] = right[j]; j += 1
                    k += 1
                while i < len(left):
                    arr[k] = left[i]; i += 1; k += 1
                while j < len(right):
                    arr[k] = right[j]; j += 1; k += 1
            width *= 2
        return arr

    sorted_pairs = iter_merge_sort_pairs(pairs)
    assert sorted_pairs == [(1, "a"), (1, "c"), (1, "e"), (2, "b"), (2, "d")]
    print(f"Stability check passed: {sorted_pairs}")

    # Stress test
    import random
    random.seed(33)
    for _ in range(200):
        n = random.randint(0, 100)
        data = [random.randint(-200, 200) for _ in range(n)]
        assert iterative_merge_sort(data[:]) == sorted(data)
    print("\nStress test: 200 random arrays matched sorted()")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Top-Down vs Bottom-Up — Which Should You Use?
    #
    #   In Python, either works. The top-down version is shorter and
    #   clearer. The bottom-up version matters when:
    #
    #     - Recursion is forbidden (some embedded systems).
    #     - You're parallelizing and want independent work items.
    #     - You're implementing an external-memory merge sort (disk
    #       runs get merged in pass-by-pass waves).
    #
    # Timsort is bottom-up. Most textbook examples are top-down.
    # ---------------------------------------------------------------
