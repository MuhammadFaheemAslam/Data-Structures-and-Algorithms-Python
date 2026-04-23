"""
Problem: Top K Frequent Elements

Difficulty: Medium (LeetCode #347)

---------------------------------------------------
Problem Statement:

Given an integer array `nums` and integer `k`, return the `k` most
frequent elements. You may return the answer in any order.

Example:
    nums = [1, 1, 1, 2, 2, 3], k = 2   →  [1, 2]
    nums = [1], k = 1                  →  [1]

Follow-up: can you solve it in better than O(n log n)?

---------------------------------------------------
Three Classical Solutions:

    1. Sort by frequency                O(n log n) time, O(n) space
    2. Heap of size k                   O(n log k) time, O(n) space
    3. Bucket sort by frequency         O(n) time, O(n) space  ← optimal

All three start the same way — COUNT frequencies with a hash map.
That's where Phase 06 comes in: the counting step is a perfect
HashMap use-case. The choice of step TWO (sort vs heap vs bucket)
is what separates the solutions.

---------------------------------------------------
Why Bucket Sort Is O(n):

The key insight: a frequency is bounded by `n` (no element appears
more than n times, because the array has only n elements). So we
can build a fixed-size array `buckets[0..n]` where `buckets[f]` is
the list of elements with frequency `f`.

Fill the buckets from the frequency map (O(unique_elements)), then
walk backwards from buckets[n] to buckets[0] collecting elements
until we have k. Total work: O(n).

This is a special case of COUNTING SORT — applicable because the
"keys we're sorting by" (frequencies) are bounded integers.

---------------------------------------------------
Complexity summary:

    Solution            Time         Space   Notes
    ---------------------------------------------------
    Sort                O(n log n)   O(n)    simplest
    Heap of size k      O(n log k)   O(n+k)  best for k ≪ n
    Bucket sort         O(n)         O(n)    optimal, slightly trickier
"""

from collections import Counter
import heapq


# =========================================================================
# Solution 1: Sort by frequency — O(n log n)
# =========================================================================

def top_k_sort(nums, k):
    """
    Count, then sort unique elements by descending frequency, take top k.

    Time:  O(n log n).
    Space: O(n).
    """
    counts = Counter(nums)
    return [x for x, _ in counts.most_common(k)]   # Counter.most_common uses heap internally


# =========================================================================
# Solution 2: Min-Heap of size k — O(n log k)
# =========================================================================

def top_k_heap(nums, k):
    """
    Keep a MIN-heap of size k, keyed by frequency. The heap always
    contains the current top-k candidates; its smallest-frequency
    element is evicted when a larger one appears.

    Time:  O(n log k) — n pushes, each bounded by log k.
    Space: O(n + k).
    """
    counts = Counter(nums)

    heap = []                                      # min-heap of (freq, value)
    for value, freq in counts.items():
        if len(heap) < k:
            heapq.heappush(heap, (freq, value))
        elif freq > heap[0][0]:
            heapq.heapreplace(heap, (freq, value))

    return [value for _freq, value in heap]


# =========================================================================
# Solution 3: Bucket Sort — O(n)
# =========================================================================

def top_k_bucket(nums, k):
    """
    Place each unique element in bucket[freq]. Walk buckets from high
    frequency to low, collecting until we have k.

    Time:  O(n).
    Space: O(n).
    """
    counts = Counter(nums)
    n = len(nums)

    # bucket[f] holds elements that appear f times (f in 1..n)
    buckets = [[] for _ in range(n + 1)]
    for value, freq in counts.items():
        buckets[freq].append(value)

    result = []
    for freq in range(n, 0, -1):
        for value in buckets[freq]:
            result.append(value)
            if len(result) == k:
                return result
    return result                                  # reached only if k > unique count


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #347 examples
    cases = [
        ([1, 1, 1, 2, 2, 3], 2, {1, 2}),
        ([1], 1, {1}),
        ([4, 4, 1, 1, 2, 3], 2, {4, 1}),
        ([-1, -1, -2, -2, -2, 3, 3, 3, 3], 2, {-2, 3}),
    ]

    for nums, k, expected_set in cases:
        for solver in (top_k_sort, top_k_heap, top_k_bucket):
            got = solver(nums, k)
            assert set(got) == expected_set, (
                f"{solver.__name__}({nums}, {k}) = {got}; expected {expected_set}"
            )
            assert len(got) == k

    # Ties: when multiple elements share the k-th frequency, any of them
    # is acceptable. Check only that the returned set's frequencies are
    # at least as high as any other element's.
    import random
    random.seed(42)
    for _ in range(200):
        n = random.randint(1, 100)
        nums = [random.randint(0, 20) for _ in range(n)]
        k = random.randint(1, min(len(set(nums)), 5))
        counts = Counter(nums)

        for solver in (top_k_sort, top_k_heap, top_k_bucket):
            got = solver(nums, k)
            assert len(got) == k
            got_freqs = [counts[x] for x in got]
            # Every NOT-returned element must have frequency <= min returned freq
            min_returned = min(got_freqs)
            for other in counts:
                if other not in got:
                    assert counts[other] <= min_returned, (
                        f"{solver.__name__}: {other}({counts[other]}) beats "
                        f"returned min freq {min_returned}"
                    )

    print("All tests passed on 200 random inputs.")

    # ---- Timing demo: heap vs bucket on a large input ----
    import time
    import random
    random.seed(0)
    big = [random.randint(0, 10_000) for _ in range(1_000_000)]
    k = 10

    for solver in (top_k_sort, top_k_heap, top_k_bucket):
        t0 = time.time()
        result = solver(big, k)
        elapsed = time.time() - t0
        print(f"   {solver.__name__:<16}: {elapsed * 1000:6.1f} ms   top-{k} = {sorted(result)}")

    # ---------------------------------------------------------------
    # Pick Your Poison:
    #
    #   - top_k_sort is a one-liner (`Counter(nums).most_common(k)`),
    #     and for interview purposes perfectly acceptable unless the
    #     follow-up explicitly asks for sub-n-log-n.
    #
    #   - top_k_heap is the "I know what I'm doing" answer: O(n log k)
    #     is a real win when k is small and n is huge.
    #
    #   - top_k_bucket is O(n) and shows you recognize that
    #     "frequencies are bounded by n" — a canonical counting-sort
    #     insight. This is the answer graders love.
    # ---------------------------------------------------------------
