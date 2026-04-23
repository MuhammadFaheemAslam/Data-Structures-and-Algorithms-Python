"""
Problem: Merge K Sorted Lists

Difficulty: Hard (LeetCode #23)

---------------------------------------------------
Problem Statement:

Given an array of k sorted lists, merge them into a single sorted list.
Return the result as a flat list. (LC #23 uses linked lists; we use
arrays here — the algorithm is identical.)

    Input:  [[1,4,5], [1,3,4], [2,6]]
    Output: [1,1,2,3,4,4,5,6]

---------------------------------------------------
Three Solutions:

    1. Concatenate and sort         O(N log N) where N = total elements. Dumb but easy.
    2. Pairwise merging             O(N log k) time — divide and conquer.
    3. Min-heap of heads            O(N log k) time — ELEGANT.

(2) and (3) have the same Big-O. The heap version is easier to
explain in an interview and generalizes to "merge k INFINITE streams".

---------------------------------------------------
The Heap Algorithm:

Seed a min-heap with the FIRST element of each list, tagged with
(value, list_index, element_index). Repeatedly:
    - Pop the smallest. Append it to the output.
    - Advance the pointer of the popped list. If it has more, push
      the new head into the heap.

Each of N total elements is pushed and popped exactly once. Heap
size is at most k. So N pushes + N pops, each O(log k) → O(N log k).

---------------------------------------------------
Why (list_index, element_index) and not just (value, element):

Python's heap compares TUPLES element-by-element. If two values are
equal, it tries to compare the SECOND element — which, in LC, might
be a `ListNode` object that isn't orderable. Including the list
INDEX (which is an int) breaks ties without reaching the node.

This is the "Python heapq gotcha" — almost every LC #23 attempt
trips over it once.
"""

import heapq


# -------- Solution 1: concatenate + sort (baseline) --------

def merge_k_sort(lists):
    """Time O(N log N), Space O(N)."""
    out = []
    for lst in lists:
        out.extend(lst)
    out.sort()
    return out


# -------- Solution 2: pairwise divide & conquer --------

def merge_k_pairwise(lists):
    """
    Repeatedly merge pairs of lists. After log k rounds, only one list remains.
    Time:  O(N log k).
    Space: O(N).
    """
    if not lists:
        return []
    # Round-by-round pair merge
    while len(lists) > 1:
        merged = []
        for i in range(0, len(lists), 2):
            if i + 1 < len(lists):
                merged.append(_merge_two(lists[i], lists[i + 1]))
            else:
                merged.append(lists[i])
        lists = merged
    return lists[0]


def _merge_two(a, b):
    """Merge two sorted lists. O(|a| + |b|)."""
    out = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return out


# -------- Solution 3: min-heap of heads --------

def merge_k_heap(lists):
    """
    Heap of (value, list_index, elem_index) triples.

    Time:  O(N log k).
    Space: O(k) for the heap + O(N) for the output.
    """
    heap = []
    for li, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], li, 0))

    out = []
    while heap:
        val, li, ei = heapq.heappop(heap)
        out.append(val)
        if ei + 1 < len(lists[li]):
            heapq.heappush(heap, (lists[li][ei + 1], li, ei + 1))
    return out


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #23 example
    cases = [
        ([[1, 4, 5], [1, 3, 4], [2, 6]], [1, 1, 2, 3, 4, 4, 5, 6]),
        ([], []),
        ([[]], []),
        ([[], [], []], []),
        ([[1]], [1]),
        ([[1, 2, 3]], [1, 2, 3]),
        ([[1], [0]], [0, 1]),
        ([[1, 2], [3, 4], [5, 6]], [1, 2, 3, 4, 5, 6]),
    ]
    for lists, expected in cases:
        assert merge_k_sort(lists) == expected
        assert merge_k_pairwise(lists) == expected
        assert merge_k_heap(lists) == expected

    # Randomized
    import random
    random.seed(42)
    for _ in range(200):
        k = random.randint(0, 20)
        lists = []
        for _ in range(k):
            size = random.randint(0, 20)
            lists.append(sorted(random.randint(-100, 100) for _ in range(size)))
        expected = sorted(sum(lists, []))
        assert merge_k_sort(lists) == expected
        assert merge_k_pairwise(lists) == expected
        assert merge_k_heap(lists) == expected

    # Timing
    import time
    k = 100
    m = 1000                                       # each list has m elements
    random.seed(0)
    lists = [sorted(random.randint(0, 10**9) for _ in range(m)) for _ in range(k)]

    for solver in (merge_k_sort, merge_k_pairwise, merge_k_heap):
        t0 = time.time()
        out = solver(lists)
        elapsed = time.time() - t0
        print(f"   {solver.__name__:<20}: {elapsed * 1000:6.1f} ms   (output len {len(out)})")

    print("\nAll tests passed!")
