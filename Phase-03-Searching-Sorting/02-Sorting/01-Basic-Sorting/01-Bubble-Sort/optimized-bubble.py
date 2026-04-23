"""
optimized-bubble.py – Bubble Sort with Two Common Optimizations

The classical bubble sort is O(n²) on every input — including already-
sorted arrays. Two simple optimizations improve that:

    1. **Early-exit flag:** if a full pass makes no swaps, the array
       is sorted — stop immediately. This makes bubble sort O(n) on
       ALREADY-SORTED data. Worst case is still O(n²).

    2. **Bounded tail:** track the position of the LAST swap in each
       pass; the suffix after that position is already sorted, so the
       next pass can terminate there. A tighter bound than the
       classic `n - 1 - i`.

With BOTH, bubble sort is **adaptive** — O(n) best case, O(n²) worst.
Still bad in practice, but a real illustration of "a two-line fix can
turn a bad algorithm into a less-bad one".

---------------------------------------------------
This File Shows:

    1. bubble_sort_early_exit     — just the swapped flag
    2. bubble_sort_bounded        — just the last-swap-position trick
    3. bubble_sort_optimized      — both optimizations combined
    4. comparison timing vs the classical version on several inputs

Run this file to see the speedup on best-case inputs.
"""

import time


# =========================================================================
# Optimization 1: Early Exit (Swapped Flag)
# =========================================================================

def bubble_sort_early_exit(arr):
    """
    Classical bubble sort with an early-exit flag.

    Time:   O(n) best (already sorted), O(n²) average/worst.
    Space:  O(1)
    Stable: Yes

    The `swapped` flag records whether ANY swap happened in the pass.
    If none did, the array must already be sorted — break out.
    """
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break                                 # the array is sorted
    return arr


# =========================================================================
# Optimization 2: Bounded Tail (Last-Swap Position)
# =========================================================================

def bubble_sort_bounded(arr):
    """
    Track the position of the LAST swap in each pass; next pass stops there.

    Time:   O(n²) worst case, but often much less in practice.
    Space:  O(1)
    Stable: Yes

    Why: after a pass, everything to the right of the last swap is
    already in its final position. So the next pass can ignore it.
    This is STRICTLY better than the classical `n - 1 - i` bound on
    average inputs.
    """
    n = len(arr)
    end = n - 1                                    # last index to inspect

    while end > 0:
        new_end = 0
        for j in range(end):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                new_end = j                        # last swap position
        end = new_end

    return arr


# =========================================================================
# Optimization 3: Both Combined
# =========================================================================

def bubble_sort_optimized(arr):
    """
    Early-exit + bounded-tail.

    Time:   O(n) best, O(n²) worst.
    Space:  O(1)
    Stable: Yes

    The best version of bubble sort. Still bad compared to Timsort —
    this is "as good as bubble sort gets."
    """
    n = len(arr)
    end = n - 1

    while end > 0:
        new_end = 0
        for j in range(end):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                new_end = j
        if new_end == 0:
            break                                 # no swaps → sorted
        end = new_end

    return arr


# =========================================================================
# Classical Version (For Timing Comparison)
# =========================================================================

def bubble_sort_classic(arr):
    """Plain bubble sort for performance comparison."""
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


# =========================================================================
# Test and Time
# =========================================================================

if __name__ == "__main__":
    # Correctness
    test_cases = [
        [64, 34, 25, 12, 22, 11, 90],
        [],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5],
    ]

    for i, data in enumerate(test_cases):
        expected = sorted(data)
        for fn in (bubble_sort_early_exit, bubble_sort_bounded, bubble_sort_optimized):
            got = fn(list(data))
            assert got == expected, f"Test {i+1} ({fn.__name__}) failed on {data}"
        print(f"Test {i+1} passed: {data} -> {expected}")

    # Timing — best-case inputs (already sorted)
    print("\nBest-case speedup (already-sorted input, n = 5000):")
    sorted_arr = list(range(5000))

    t0 = time.time()
    bubble_sort_classic(list(sorted_arr))
    t_classic = time.time() - t0

    t0 = time.time()
    bubble_sort_early_exit(list(sorted_arr))
    t_early = time.time() - t0

    print(f"   classic:                {t_classic:.3f}s  (O(n²) regardless of input)")
    print(f"   with early-exit:        {t_early:.3f}s  (O(n) on sorted — huge speedup)")
    assert t_early * 10 < t_classic, "Early exit should be dramatically faster here"

    # Timing — worst-case inputs (reverse sorted)
    print("\nWorst-case (reverse-sorted input, n = 2000):")
    reverse_arr = list(range(2000, 0, -1))

    t0 = time.time()
    bubble_sort_classic(list(reverse_arr))
    t_classic = time.time() - t0

    t0 = time.time()
    bubble_sort_optimized(list(reverse_arr))
    t_opt = time.time() - t0

    print(f"   classic:                {t_classic:.3f}s")
    print(f"   optimized:              {t_opt:.3f}s")
    print("   (both O(n²) on reverse-sorted; bounded-tail saves constants)")

    # Stress — all four variants must agree
    import random
    random.seed(42)
    for _ in range(100):
        n = random.randint(0, 40)
        data = [random.randint(-100, 100) for _ in range(n)]
        expected = sorted(data)
        for fn in (bubble_sort_classic, bubble_sort_early_exit,
                   bubble_sort_bounded, bubble_sort_optimized):
            assert fn(list(data)) == expected

    print("\nStress test: 100 random arrays — all four variants agree\n")
    print("All tests passed!")
