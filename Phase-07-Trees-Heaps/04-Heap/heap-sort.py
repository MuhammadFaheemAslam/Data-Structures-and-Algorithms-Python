"""
heap-sort.py — In-Place Heapsort, O(n log n) Worst-Case

Heapsort proceeds in two phases:

    1. HEAPIFY — convert `arr` into a MAX-heap in O(n).
    2. EXTRACT — swap arr[0] with arr[last], shrink the heap by one,
                 sift-down the new root. Repeat until the heap shrinks
                 to empty. The SWAPPED-OUT maxes land in sorted order
                 at the end of the array.

Using a MAX-heap (not min) lets us produce an ASCENDING sort in the
same array — each extract places the current max at the back, and we
shrink toward the front.

---------------------------------------------------
Complexity:

    Time:  O(n log n) worst case — guaranteed, unlike quicksort.
    Space: O(1) extra — in place.
    Stable: NO — heap siftings re-order equal keys unpredictably.

---------------------------------------------------
Heapsort vs Its Competitors:

| Algorithm     | Time avg/worst | Space | Stable | Notes                          |
|---------------|----------------|-------|--------|--------------------------------|
| Heapsort      | n log n / n log n | O(1)  | no    | Guaranteed worst case; cache-unfriendly |
| Quicksort     | n log n / n²   | O(log n) | no | Fastest in practice (cache); worst case is very rare |
| Merge sort    | n log n / n log n | O(n)  | yes   | Stable; not in-place              |
| Tim sort      | n log n / n log n | O(n)  | yes   | Python's default; real-world wins |

Heapsort is rarely the FASTEST, but it's the only in-place O(n log n)
WORST CASE — useful when you can't tolerate quicksort's O(n²) blowup
and can't afford merge sort's O(n) extra space. It's what you'd pick
for an embedded or security-sensitive sort.

---------------------------------------------------
Why It's Seldom The Production Default:

The ~3× cache miss rate (compared to tim-sort / introsort) wins the
practical contest in languages that ship a standard sort. But
understanding heapsort is understanding heaps — the two stand
together.
"""


def heap_sort(arr):
    """
    Sort `arr` ASCENDING in place using heapsort. Returns `arr` for chaining.

    Time: O(n log n), Space: O(1).
    """
    n = len(arr)

    # Phase 1: build a MAX-heap in place (bottom-up sift-down)
    for i in range((n - 2) >> 1, -1, -1):
        _sift_down_max(arr, i, n)

    # Phase 2: repeatedly extract max to the back
    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]        # swap max to end
        _sift_down_max(arr, 0, end)                # fix the heap on arr[:end]

    return arr


def _sift_down_max(arr, i, n):
    """Sift `arr[i]` down within the heap of size `n` (max-heap variant)."""
    while True:
        left = 2 * i + 1
        if left >= n:
            return
        right = left + 1
        larger = left
        if right < n and arr[right] > arr[left]:
            larger = right
        if arr[i] >= arr[larger]:
            return
        arr[i], arr[larger] = arr[larger], arr[i]
        i = larger


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    import random

    # Basic
    assert heap_sort([]) == []
    assert heap_sort([1]) == [1]
    assert heap_sort([3, 1, 2]) == [1, 2, 3]
    assert heap_sort([5, 5, 5]) == [5, 5, 5]
    assert heap_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]
    assert heap_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    # Correctness on random inputs
    random.seed(42)
    for _ in range(200):
        n = random.randint(0, 200)
        arr = [random.randint(-100, 100) for _ in range(n)]
        expected = sorted(arr)
        assert heap_sort(arr[:]) == expected

    # In-place proof: original list object is modified
    arr = [4, 2, 1, 3]
    ret = heap_sort(arr)
    assert ret is arr
    assert arr == [1, 2, 3, 4]

    # Timing on a moderate input (no sanity threshold — just visibility)
    import time
    n = 200_000
    random.seed(0)
    data = [random.randint(0, 10 ** 9) for _ in range(n)]

    t0 = time.time()
    heap_sort(data[:])
    t_hs = time.time() - t0

    t0 = time.time()
    sorted(data)                                   # Python's Timsort (C)
    t_py = time.time() - t0

    print(f"Sort {n:,} ints:")
    print(f"   heap_sort (pure-Python): {t_hs * 1000:7.1f} ms")
    print(f"   sorted()  (Timsort, C):  {t_py * 1000:7.1f} ms")
    print(f"   (Timsort is ~{t_hs / t_py:.0f}× faster due to C impl + cache-friendly algorithm)")

    print("\nAll tests passed!")
