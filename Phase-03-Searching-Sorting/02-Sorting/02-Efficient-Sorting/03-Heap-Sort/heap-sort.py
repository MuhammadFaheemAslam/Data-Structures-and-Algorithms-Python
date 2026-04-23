"""
heap-sort.py – Heap Sort

An in-place O(n log n) sort built on top of a MAX-HEAP. Unlike merge
sort (which needs O(n) extra space) and quick sort (whose O(n²) worst
case forces randomization), heap sort has:

    Time:   **O(n log n) GUARANTEED** — no adversarial input
    Space:  O(1) — truly in place
    Stable: No

So heap sort is the **only comparison-based sort** that is both
in-place AND worst-case O(n log n). That's its niche.

---------------------------------------------------
Why Heap Sort Is Usually Not Chosen Despite Its Guarantees:

Quick sort is faster in practice (better cache behaviour); merge
sort is faster and stable. Heap sort pays for its guarantees with
a ~2× constant-factor overhead compared to quicksort.

When you see heap sort in the wild:
    - Embedded systems where worst-case guarantees matter.
    - As part of **introsort** (quick sort that degrades to heap sort
      when recursion depth exceeds 2·log₂ n — gives worst-case
      O(n log n) with quicksort's typical speed).
    - C++ `std::sort` is introsort on libstdc++.
    - Java's `Arrays.sort` for primitives is introsort / pdqsort.

---------------------------------------------------
The Algorithm:

    1. BUILD a max-heap out of the array in place.  (O(n))
    2. REPEATEDLY extract the max: swap arr[0] with arr[n-1],
       shrink the heap by 1, re-heapify from the root.  (n iterations
       × O(log n) each = O(n log n))

After the loop, the array is sorted ascending.

    def heap_sort(arr):
        build_max_heap(arr)
        for end in range(n-1, 0, -1):
            arr[0], arr[end] = arr[end], arr[0]
            sift_down(arr, 0, end)

The KEY operation is **sift-down** (a.k.a. heapify): given a binary
tree where only the root violates the max-heap property, fix the
whole tree in O(log n) by swapping the root down to its correct place.

---------------------------------------------------
Array-as-Heap Layout:

For a 0-indexed array representing a complete binary tree:

    parent(i) = (i - 1) // 2
    left(i)   = 2 * i + 1
    right(i)  = 2 * i + 2

The array is the tree, level by level:

    arr: [9, 5, 7, 2, 3, 1, 6]
         tree:
                     9
                   /   \
                  5     7
                 / \   / \
                2   3 1   6

A **max-heap** has every parent ≥ its children. To sort ASCENDING, we
use a max-heap: extract the MAX repeatedly and place it at the END.

---------------------------------------------------
"""

# =========================================================================
# Heap Sort — The Full Algorithm
# =========================================================================

def heap_sort(arr):
    """
    Sort `arr` in place using heap sort.

    Time:   O(n log n) guaranteed
    Space:  O(1)
    Stable: No

    Returns `arr` for convenience (mutated).
    """
    n = len(arr)
    if n <= 1:
        return arr

    # Phase 1: Build a max-heap (O(n) via Floyd's bottom-up algorithm)
    # Start at the last non-leaf and sift down.
    for i in range(n // 2 - 1, -1, -1):
        _sift_down(arr, i, n)

    # Phase 2: Repeatedly extract the max.
    # After each extraction, the "sorted" region grows at the end
    # and the heap shrinks.
    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]       # max → final position
        _sift_down(arr, 0, end)                   # restore heap in arr[:end]

    return arr


def _sift_down(arr, start, end):
    """
    Push arr[start] DOWN the max-heap arr[:end] until it reaches its
    correct position.

    Invariant: arr[start] is the only potential violator; the rest of
    arr[:end] is already a valid max-heap below `start`.

    Time: O(log n) — at most one step per tree level.
    """
    i = start
    while True:
        left  = 2 * i + 1
        right = 2 * i + 2
        largest = i

        if left < end and arr[left] > arr[largest]:
            largest = left
        if right < end and arr[right] > arr[largest]:
            largest = right

        if largest == i:
            break                                  # heap property satisfied

        arr[i], arr[largest] = arr[largest], arr[i]
        i = largest


# =========================================================================
# Sorting in DESCENDING Order — Use a Min-Heap
# =========================================================================

def heap_sort_descending(arr):
    """
    Sort `arr` in DESCENDING order via a MIN-heap.

    Algorithm: build a MIN-heap. Each extraction places the current
    minimum at the END of the shrinking heap region — so the back of
    the array fills up with SMALLEST → LARGEST, which means reading
    the array left-to-right gives LARGEST → SMALLEST: descending.

    (Mirror of heap_sort, which uses a MAX-heap and produces ascending.)
    """
    n = len(arr)
    if n <= 1:
        return arr

    # Build min-heap
    for i in range(n // 2 - 1, -1, -1):
        _sift_down_min(arr, i, n)

    # Repeatedly extract the min to the end of the heap region.
    # Each extraction moves the current min to position `end`, then
    # shrinks the heap by 1.
    #
    # After the loop: arr[i] contains the (n - i)-th smallest → arr
    # is sorted DESCENDING (largest at front, smallest at back).
    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        _sift_down_min(arr, 0, end)

    return arr


def _sift_down_min(arr, start, end):
    """Sift-down for a MIN-heap."""
    i = start
    while True:
        left  = 2 * i + 1
        right = 2 * i + 2
        smallest = i

        if left < end and arr[left] < arr[smallest]:
            smallest = left
        if right < end and arr[right] < arr[smallest]:
            smallest = right

        if smallest == i:
            break

        arr[i], arr[smallest] = arr[smallest], arr[i]
        i = smallest


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    arr = [12, 11, 13, 5, 6, 7]
    print(f"Input:  {arr}")
    heap_sort(arr)
    print(f"Sorted: {arr}")
    print()

    # Test cases
    test_cases = [
        [12, 11, 13, 5, 6, 7],
        [],
        [1],
        [1, 2, 3, 4, 5],                          # already sorted
        [5, 4, 3, 2, 1],                          # reverse sorted
        [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5],        # duplicates
        [0, -1, 2, -3, 4, -5],                    # negatives
        [7] * 20,                                 # all equal
    ]

    for i, data in enumerate(test_cases):
        expected = sorted(data)
        got = heap_sort(data[:])
        assert got == expected, f"Test {i+1} failed on {data}"
        print(f"Test {i+1} passed: {data} -> {got}")

    # Descending
    print()
    print("Descending-order variant:")
    for data in [[3, 1, 4, 1, 5, 9, 2, 6], [], [1, 2, 3]]:
        got = heap_sort_descending(data[:])
        expected = sorted(data, reverse=True)
        assert got == expected
        print(f"   heap_sort_descending({data}) = {got}")

    # Performance note — heap sort is guaranteed O(n log n) even on
    # adversarial inputs that kill fixed-pivot quicksort.
    import time
    n = 10_000
    for label, data in [
        ("random",        [n - i for i in range(n)]),
        ("sorted",        list(range(n))),
        ("reverse sorted", list(range(n, 0, -1))),
        ("all equal",     [42] * n),
    ]:
        t0 = time.time()
        heap_sort(data[:])
        print(f"   heap_sort ({label:<16}, n={n}): {time.time() - t0:.4f}s  (guaranteed O(n log n))")

    # Stress test
    import random
    random.seed(42)
    for _ in range(200):
        n = random.randint(0, 80)
        data = [random.randint(-100, 100) for _ in range(n)]
        assert heap_sort(data[:]) == sorted(data)

    print("\nStress test: 200 random arrays matched sorted()")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Heap Sort vs Merge Sort vs Quick Sort:
    #
    #                   Merge        Quick (random)    Heap
    #   Worst case      O(n log n)   O(n²)             **O(n log n)**
    #   Average         O(n log n)   O(n log n)        O(n log n)
    #   Space           O(n)         O(log n)          **O(1)**
    #   Stable          Yes          No                No
    #   In place        No           Yes               **Yes**
    #   Cache behaviour Good         **Excellent**     Poor (random jumps)
    #
    # Heap sort is the ONLY one that's both in-place AND worst-case O(n log n).
    # Its niche is embedded / real-time systems where guarantees matter.
    #
    # For everyday code: Timsort (Python), pdqsort (Rust), or introsort (C++)
    # — hybrid algorithms that COMPOSE quicksort + heap sort + insertion sort
    # to get the best of all worlds.
    # ---------------------------------------------------------------
