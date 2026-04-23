"""
selection-sort.py – Selection Sort

At each pass, SELECT the minimum of the unsorted tail and place it
at the start of the tail. After i passes, arr[:i] is sorted and in
final position.

---------------------------------------------------
Time:   O(n²) best / average / worst — NOT adaptive.
Space:  O(1)
Stable: **No** — swapping the selected min with arr[i] can jump
        an equal element past another equal element.
Swaps:  O(n) — exactly n − 1 swaps, regardless of input.

The **O(n) swap count** is selection sort's one genuine advantage.
If swaps are extremely expensive (e.g., writing to flash memory, or
moving heavy objects in a physical system), selection sort does the
minimum possible number. Compare bubble/insertion sort's O(n²) swaps.

---------------------------------------------------
The Algorithm:

    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        swap(arr[i], arr[min_idx])

Scan the unsorted tail for the minimum; swap it into position i.

---------------------------------------------------
"""

# =========================================================================
# Selection Sort — Classical
# =========================================================================

def selection_sort(arr):
    """
    In-place selection sort.

    Time:   O(n²)    — always, regardless of input
    Space:  O(1)
    Stable: No
    Swaps:  Exactly n - 1
    """
    n = len(arr)
    for i in range(n - 1):
        # find the index of the minimum in arr[i..n-1]
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        # place it at position i
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


# =========================================================================
# Double-Ended Variant: Pick Both Min and Max Per Pass
# =========================================================================

def selection_sort_bidirectional(arr):
    """
    Pick both the min AND the max per pass. Place min at the start,
    max at the end of the unsorted range.

    Halves the number of outer-loop iterations, from n - 1 to n / 2.

    Time:   O(n²)    — same Big-O; ~2x smaller constant
    Space:  O(1)
    Stable: No

    Sometimes called "double selection sort" or "cocktail selection
    sort". A small improvement; still impractical.
    """
    n = len(arr)
    lo, hi = 0, n - 1

    while lo < hi:
        min_idx = lo
        max_idx = lo
        for j in range(lo, hi + 1):
            if arr[j] < arr[min_idx]:
                min_idx = j
            if arr[j] > arr[max_idx]:
                max_idx = j

        # place min at lo
        arr[lo], arr[min_idx] = arr[min_idx], arr[lo]

        # if the max was at lo (now moved to min_idx), correct max_idx
        if max_idx == lo:
            max_idx = min_idx

        arr[hi], arr[max_idx] = arr[max_idx], arr[hi]

        lo += 1
        hi -= 1

    return arr


# =========================================================================
# Stable Selection Sort — By Shifting Instead of Swapping
# =========================================================================

def selection_sort_stable(arr):
    """
    Stable selection sort: when the minimum is found, INSERT it at
    position i by shifting everything else right — instead of the
    direct swap that breaks stability.

    Time:   O(n²) — but with WORSE constant factor due to shifting
    Space:  O(1)
    Stable: Yes
    Swaps:  O(n²) — loses the "O(n) swaps" advantage of standard
            selection sort

    Included for educational contrast. In practice, if you need a
    stable O(n²) sort, use insertion sort — it's faster AND stable.
    """
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j

        # shift everything from i to min_idx - 1 one step right;
        # put the original arr[min_idx] at position i
        value = arr[min_idx]
        for k in range(min_idx, i, -1):
            arr[k] = arr[k - 1]
        arr[i] = value

    return arr


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    arr = [64, 25, 12, 22, 11]
    original = list(arr)
    selection_sort(arr)
    print(f"Input:  {original}")
    print(f"Sorted: {arr}")
    print()

    # Test cases
    test_cases = [
        [64, 25, 12, 22, 11],
        [],
        [1],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5],
        [0, -1, 2, -3, 4, -5],
        [7, 7, 7, 7, 7],
    ]

    for i, data in enumerate(test_cases):
        expected = sorted(data)
        for fn in (selection_sort, selection_sort_bidirectional, selection_sort_stable):
            got = fn(list(data))
            assert got == expected, (
                f"Test {i+1} ({fn.__name__}) failed on {data}: "
                f"expected {expected}, got {got}"
            )
        print(f"Test {i+1} passed: {data} -> {expected}")

    # Stability check — the plain version is NOT stable; the stable version IS
    pairs = [(1, "a"), (2, "b"), (1, "c"), (2, "d"), (1, "e")]

    def selection_sort_pairs_plain(arr):
        arr = list(arr)
        n = len(arr)
        for i in range(n - 1):
            min_idx = i
            for j in range(i + 1, n):
                if arr[j][0] < arr[min_idx][0]:
                    min_idx = j
            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return arr

    def selection_sort_pairs_stable(arr):
        arr = list(arr)
        n = len(arr)
        for i in range(n - 1):
            min_idx = i
            for j in range(i + 1, n):
                if arr[j][0] < arr[min_idx][0]:
                    min_idx = j
            value = arr[min_idx]
            for k in range(min_idx, i, -1):
                arr[k] = arr[k - 1]
            arr[i] = value
        return arr

    plain_result = selection_sort_pairs_plain(pairs)
    stable_result = selection_sort_pairs_stable(pairs)
    expected_stable = [(1, "a"), (1, "c"), (1, "e"), (2, "b"), (2, "d")]

    print(f"\nStability check:")
    print(f"   input:            {pairs}")
    print(f"   plain (unstable): {plain_result}")
    print(f"   stable variant:   {stable_result}")
    assert stable_result == expected_stable, "Stable variant failed stability check"
    # plain MAY or may not be in the stable order — usually isn't

    # Stress test
    import random
    random.seed(7)
    for _ in range(100):
        n = random.randint(0, 40)
        data = [random.randint(-100, 100) for _ in range(n)]
        expected = sorted(data)
        for fn in (selection_sort, selection_sort_bidirectional, selection_sort_stable):
            assert fn(list(data)) == expected
    print("\nStress test: 100 random arrays — all three variants agree with sorted()")

    print("\nAll tests passed!")
