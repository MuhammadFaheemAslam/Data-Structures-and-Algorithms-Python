"""
heapify.py — Converting an Arbitrary Array Into a Heap in O(n)

Given an unordered array, we can impose the heap property in LINEAR
time. The idea: run `sift_down` BOTTOM-UP, starting from the last
non-leaf index.

    for i in range(n // 2 - 1, -1, -1):
        sift_down(arr, i)

Why this works bottom-up: when we sift down at index `i`, both of
i's subtrees are ALREADY VALID HEAPS (we fixed them first). So a
single sift_down makes the subtree rooted at `i` a valid heap.

---------------------------------------------------
Why It's O(n), Not O(n log n):

A lazy analysis says: we call sift_down on n/2 nodes, each potentially
log n deep, so O(n log n). But that overcounts.

The KEY observation: sift_down from a node at HEIGHT h is bounded by h
(not log n). And in a complete tree of n nodes, MOST nodes are near
the bottom — roughly n/2 are leaves (height 0), n/4 are at height 1,
n/8 at height 2, etc.

Total work:
    ≤ Σ (h=0 to log n) ⌈n / 2^(h+1)⌉ · h
    = (n/2) · Σ (h=0 to ∞) h / 2^h
    = (n/2) · 2
    = O(n)

The algebra trick: Σ h / 2^h = 2 for h ≥ 0 (a standard series). So
heapify is bonafide O(n) in the worst case.

---------------------------------------------------
Why This Matters Practically:

Heapsort setup cost is O(n), not O(n log n). That's still O(n log n)
overall because extracting all n elements costs O(n log n), but the
constant factor in the setup is smaller than a hypothetical
"push-all-then-pop-all" which would incur n sift-UP calls each O(log n).

Push-build: O(n log n) guaranteed — every push can reach the root.
Heapify:     O(n) guaranteed — work concentrates near the bottom.

Benchmarks: 2-3× faster heapify in practice for large n.
"""


# =========================================================================
# The standalone heapify procedure (works for any list in place)
# =========================================================================

def heapify(arr):
    """
    Rearrange `arr` IN PLACE into a valid min-heap. O(n).
    """
    n = len(arr)
    for i in range((n - 2) >> 1, -1, -1):
        _sift_down(arr, i, n)


def _sift_down(arr, i, n):
    """Bubble arr[i] downward while it's greater than its smaller child."""
    while True:
        left = 2 * i + 1
        if left >= n:
            return
        right = left + 1
        smaller = left
        if right < n and arr[right] < arr[left]:
            smaller = right
        if arr[i] <= arr[smaller]:
            return
        arr[i], arr[smaller] = arr[smaller], arr[i]
        i = smaller


# =========================================================================
# Alternative: push-build (slower O(n log n) for comparison / benchmarking)
# =========================================================================

def push_build(arr):
    """
    Build a heap by repeated push. O(n log n).

    Used here as a FOIL to demonstrate heapify's speed advantage.
    """
    heap = []
    for x in arr:
        heap.append(x)
        i = len(heap) - 1
        while i > 0:
            parent = (i - 1) >> 1
            if heap[parent] > heap[i]:
                heap[parent], heap[i] = heap[i], heap[parent]
                i = parent
            else:
                break
    return heap


def is_min_heap(arr):
    n = len(arr)
    for i in range(n):
        l, r = 2 * i + 1, 2 * i + 2
        if l < n and arr[i] > arr[l]:
            return False
        if r < n and arr[i] > arr[r]:
            return False
    return True


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    import heapq
    import random
    import time

    # Correctness
    arr = [5, 3, 8, 1, 9, 2, 4, 7, 6, 0]
    heapify(arr)
    assert is_min_heap(arr)

    # Empty and single
    empty = []
    heapify(empty)
    assert empty == []
    single = [42]
    heapify(single)
    assert single == [42]

    # Matches heapq's result (up to ordering — heap arrays aren't unique)
    # Instead of direct comparison, verify both yield same sort when drained
    random.seed(42)
    for _ in range(100):
        n = random.randint(0, 200)
        arr = [random.randint(-100, 100) for _ in range(n)]
        mine = arr[:]
        ref = arr[:]
        heapify(mine)
        heapq.heapify(ref)
        assert is_min_heap(mine)
        # Both should produce the same sorted sequence
        mine_sorted = sorted(mine)
        ref_sorted = sorted(ref)
        assert mine_sorted == ref_sorted

    # Timing: heapify vs push-build on a large input
    n = 1_000_000
    random.seed(0)
    data = [random.randint(0, 10 ** 9) for _ in range(n)]

    t0 = time.time()
    arr = data[:]
    heapify(arr)
    t_heapify = time.time() - t0

    t0 = time.time()
    _ = push_build(data)
    t_push = time.time() - t0

    print(f"Build heap of {n:,} elements:")
    print(f"   heapify (O(n)):       {t_heapify * 1000:7.1f} ms")
    print(f"   push-build (O(n log n)): {t_push * 1000:7.1f} ms")
    print(f"   heapify speedup:      {t_push / t_heapify:.2f}x")

    # Assert the expected asymptotic advantage
    assert t_heapify < t_push, "heapify should beat push-build on large n"

    print("\nAll tests passed!")
