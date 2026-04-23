"""
heapify.py – Heapify: Build a Heap in O(n)

Heap sort has two distinct phases:

    1. BUILD a max-heap from an unordered array.    (Floyd's: O(n))
    2. REPEATEDLY extract the max.                  (O(n log n))

Phase 1 looks like it should be O(n log n) — for each of the n
elements, we sift-down in O(log n). But a clever analysis shows
that the bottom-up heapify is actually **O(n)**. This file is
devoted to explaining and implementing that.

---------------------------------------------------
The Two Ways to Build a Heap:

### Top-Down (Insert One at a Time)

Start with an empty heap; call `heappush(x)` n times.

    Time: O(n log n)
    Space: O(n) (or in place)

Each push is O(log n); n pushes → O(n log n). Correct but slow.

### Bottom-Up (Floyd's Algorithm)

Use the array directly. Starting from the LAST NON-LEAF node and
walking UP to the root, call sift-down on each.

    Time: **O(n)** — surprising!
    Space: O(1)

Why O(n), not O(n log n)?

    - Leaves (bottom half of the array) need NO sift-down.
    - Level-one-above-leaves (next quarter) sift down at most 1 step.
    - Level-two-above-leaves (next eighth) sift down at most 2 steps.
    - ...
    - The root (1 node) sifts down log n steps.

Sum: n/2 · 0 + n/4 · 1 + n/8 · 2 + … + 1 · log n
   = O(n)

The geometric series converges — most nodes do NO work; the root does
O(log n) but it's just one node. Total: O(n).

This is the standard "build the heap once, all at once" technique.
Use Floyd's whenever you have all the elements upfront; top-down
push only for streaming input.

---------------------------------------------------
"""

# =========================================================================
# Floyd's Bottom-Up Heapify — O(n)
# =========================================================================

def build_max_heap(arr):
    """
    Turn `arr` into a max-heap in place using Floyd's algorithm.

    Time:   O(n)
    Space:  O(1)

    Starts at the last non-leaf index (n // 2 - 1) and sifts down
    toward the root.
    """
    n = len(arr)
    # the last non-leaf is at index (n // 2 - 1); nodes after it are leaves
    for i in range(n // 2 - 1, -1, -1):
        sift_down(arr, i, n)
    return arr


def sift_down(arr, start, end):
    """
    Push arr[start] DOWN the max-heap arr[:end] until it reaches its
    correct position.

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
            break

        arr[i], arr[largest] = arr[largest], arr[i]
        i = largest


# =========================================================================
# Top-Down Heap Construction — O(n log n)  (For Comparison)
# =========================================================================

def build_max_heap_topdown(arr):
    """
    Build a max-heap by inserting one element at a time.

    Time:   O(n log n)
    Space:  O(1)

    Slower than build_max_heap (Floyd's) asymptotically, but uses the
    same sift-down primitive. Shown for comparison.
    """
    n = len(arr)
    for i in range(1, n):
        _sift_up(arr, i)
    return arr


def _sift_up(arr, i):
    """
    Push arr[i] UP the max-heap until it reaches its correct position.

    Used by the top-down heap construction and by insertion-style heap
    operations (heappush).

    Time: O(log n)
    """
    while i > 0:
        parent = (i - 1) // 2
        if arr[i] > arr[parent]:
            arr[i], arr[parent] = arr[parent], arr[i]
            i = parent
        else:
            break


# =========================================================================
# Min-Heap Versions (for completeness)
# =========================================================================

def build_min_heap(arr):
    """Min-heap version of Floyd's algorithm."""
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        _sift_down_min(arr, i, n)
    return arr


def _sift_down_min(arr, start, end):
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
# Heap Validation (For Testing)
# =========================================================================

def is_max_heap(arr):
    """True iff `arr` (interpreted as a binary tree) is a max-heap."""
    n = len(arr)
    for i in range(n):
        left, right = 2 * i + 1, 2 * i + 2
        if left < n and arr[i] < arr[left]:
            return False
        if right < n and arr[i] < arr[right]:
            return False
    return True


def is_min_heap(arr):
    """True iff `arr` is a min-heap."""
    n = len(arr)
    for i in range(n):
        left, right = 2 * i + 1, 2 * i + 2
        if left < n and arr[i] > arr[left]:
            return False
        if right < n and arr[i] > arr[right]:
            return False
    return True


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    arr = [12, 11, 13, 5, 6, 7]
    print(f"Input:  {arr}")
    build_max_heap(arr)
    print(f"Max-heap (Floyd's):  {arr}")
    assert is_max_heap(arr)
    print()

    # Test cases — heap validity (NOT sortedness!)
    test_cases = [
        [12, 11, 13, 5, 6, 7],
        [],
        [1],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],                          # already a max-heap (reverse sorted)
        [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5],
        [0, -1, 2, -3, 4, -5],
        [7] * 20,                                 # all equal
    ]

    for i, data in enumerate(test_cases):
        # Floyd's O(n) version
        h1 = build_max_heap(data[:])
        assert is_max_heap(h1), f"Test {i+1} (Floyd's): {h1} is not a max-heap"

        # Top-down O(n log n) version
        h2 = build_max_heap_topdown(data[:])
        assert is_max_heap(h2), f"Test {i+1} (top-down): {h2} is not a max-heap"

        # Min-heap
        h3 = build_min_heap(data[:])
        assert is_min_heap(h3), f"Test {i+1} (min-heap): {h3} is not a min-heap"

        print(f"Test {i+1} passed: len={len(data)} — all three build correctly")

    # Timing — Floyd's O(n) vs top-down O(n log n)
    import time
    import random

    random.seed(0)
    n = 200_000
    data = [random.randint(0, 10**6) for _ in range(n)]

    t0 = time.time()
    build_max_heap(data[:])
    t_floyd = time.time() - t0

    t0 = time.time()
    build_max_heap_topdown(data[:])
    t_topdown = time.time() - t0

    print(f"\nTiming on n={n}:")
    print(f"   Floyd's (O(n)):        {t_floyd:.3f}s")
    print(f"   Top-down (O(n log n)): {t_topdown:.3f}s")

    # Stress test
    random.seed(42)
    for _ in range(200):
        n = random.randint(0, 100)
        data = [random.randint(-100, 100) for _ in range(n)]
        h1 = build_max_heap(data[:])
        assert is_max_heap(h1)
        h2 = build_min_heap(data[:])
        assert is_min_heap(h2)

    print("\nStress test: 200 random arrays produced valid heaps")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Key Insight:
    #
    #   Floyd's O(n) construction is one of the most elegant analyses
    #   in all of algorithms. The per-node cost decreases exponentially
    #   as you go down the tree — the leaves do 0 work, and while the
    #   root does O(log n) work, it's ONLY ONE NODE.
    #
    #   Sum: n/2 · 0 + n/4 · 1 + n/8 · 2 + ... = O(n).
    #
    # This same analysis appears again in:
    #   - Building a segment tree (O(n)).
    #   - Building a disjoint-set forest via union-by-rank (amortized).
    #   - The "heavy path" analysis in balanced-tree structures.
    # ---------------------------------------------------------------
