"""
bubble-sort.py – Bubble Sort (Classical Version)

The "first sort anyone learns." Repeatedly scan the array and swap
adjacent elements that are out of order. After each full pass, the
largest remaining element has "bubbled" to the end. Repeat until
nothing swaps.

---------------------------------------------------
Time:   O(n²) worst and average; O(n²) best WITHOUT early-exit.
Space:  O(1) — in place.
Stable: Yes — equal elements keep their relative order, provided we
        use `>` (not `>=`) in the swap condition.

---------------------------------------------------
The Algorithm:

    for i in range(n - 1):
        for j in range(n - 1 - i):          # already-sorted tail shrinks
            if arr[j] > arr[j + 1]:
                swap(arr[j], arr[j + 1])

After iteration `i`, the last `i + 1` elements are in final position.
Hence the inner loop can stop at `n - 1 - i`.

---------------------------------------------------
Why Teach It at All?

Bubble sort is genuinely bad in practice — the CS community has been
trying to retire it for decades. But it remains in every textbook because:

    1. It's the SIMPLEST sort to explain. Two lines of pseudocode.
    2. It demonstrates STABILITY and IN-PLACE sorting on small examples.
    3. It's a clean baseline for optimization: see optimized-bubble.py
       for how a two-line tweak turns it into O(n) on already-sorted data.
    4. Interviewers still ask about it.

Use it ONLY for pedagogy. Real code: Python's `sorted()` is Timsort —
orders of magnitude faster.

---------------------------------------------------
"""

# =========================================================================
# Bubble Sort — Classical
# =========================================================================

def bubble_sort(arr):
    """
    In-place bubble sort.

    Time:   O(n²)    — even on already-sorted input (no early exit).
    Space:  O(1)
    Stable: Yes

    Returns `arr` for convenience (same object, mutated).
    """
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


# =========================================================================
# Non-Mutating Variant — Returns a New List
# =========================================================================

def bubble_sort_copy(arr):
    """Same algorithm, but returns a new sorted list without mutating input."""
    return bubble_sort(list(arr))


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    # Basic demo
    arr = [64, 34, 25, 12, 22, 11, 90]
    original = list(arr)
    bubble_sort(arr)
    print(f"Input:  {original}")
    print(f"Sorted: {arr}")
    print()

    # Test cases
    test_cases = [
        [64, 34, 25, 12, 22, 11, 90],
        [],
        [1],
        [1, 2, 3, 4, 5],                          # already sorted
        [5, 4, 3, 2, 1],                          # reverse sorted
        [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5],        # duplicates
        [0, -1, 2, -3, 4, -5],                    # negatives
        [7, 7, 7, 7, 7],                          # all equal
        [3, 2],                                   # 2-element
    ]

    for i, data in enumerate(test_cases):
        expected = sorted(data)
        got = bubble_sort(list(data))
        assert got == expected, f"Test {i+1} failed on {data}: expected {expected}, got {got}"
        print(f"Test {i+1} passed: {data} -> {got}")

    # Stability check — sort pairs by first element; second element order must be preserved
    pairs = [(1, "a"), (2, "b"), (1, "c"), (2, "d"), (1, "e")]
    # key-only bubble sort for stability testing
    def bubble_sort_pairs(arr):
        n = len(arr)
        arr = list(arr)
        for i in range(n - 1):
            for j in range(n - 1 - i):
                if arr[j][0] > arr[j + 1][0]:     # compare FIRST element only
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

    sorted_pairs = bubble_sort_pairs(pairs)
    expected_stable = [(1, "a"), (1, "c"), (1, "e"), (2, "b"), (2, "d")]
    assert sorted_pairs == expected_stable, (
        "Bubble sort should be stable — equal keys should keep input order"
    )
    print(f"\nStability check: {pairs}")
    print(f"   sorted:   {sorted_pairs}")

    # Stress test
    import random
    random.seed(5)
    for _ in range(100):
        n = random.randint(0, 30)
        data = [random.randint(-100, 100) for _ in range(n)]
        assert bubble_sort(list(data)) == sorted(data)
    print("\nStress test: 100 random arrays matched sorted()")

    print("\nAll tests passed!")
