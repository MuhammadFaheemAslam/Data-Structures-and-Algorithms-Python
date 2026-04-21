"""
template.py – Frequency Counting Reference Template

This file demonstrates the four core frequency-counting operations plus
one specialized algorithm:

    1. Build a Counter
    2. Query (most frequent, top-k, uniqueness)
    3. Compare two Counters (multiset equality)
    4. Counter arithmetic (+, -, &, |)
    5. Boyer-Moore Voting (the O(1)-space majority trick)

Run this file to see each template's output.
"""

from collections import Counter
import heapq


# =========================================================================
# Operation 1: Build
# =========================================================================

def build_counter(items):
    """
    Build a Counter from any iterable.

    Time Complexity:  O(n)
    Space Complexity: O(distinct)
    """
    return Counter(items)


def build_counter_manual(items):
    """
    Equivalent using a plain dict + .get() — works in any Python version
    and is the "implement it from scratch" interview answer.
    """
    counts = {}
    for x in items:
        counts[x] = counts.get(x, 0) + 1
    return counts


# =========================================================================
# Operation 2: Query
# =========================================================================

def most_frequent_value(counts):
    """
    Return the key with the largest value.

    Time Complexity:  O(distinct)
    """
    if not counts:
        return None
    return max(counts, key=counts.get)


def top_k_frequent(items, k):
    """
    Return the k most-frequent items (order: most-frequent first).

    Time Complexity:  O(n + distinct * log k) using a size-K heap.
    Space Complexity: O(distinct + k)

    Counter.most_common(k) is the idiomatic version and does the same
    thing.
    """
    counts = Counter(items)

    # size-k min-heap, keyed by count
    heap = []
    for val, cnt in counts.items():
        if len(heap) < k:
            heapq.heappush(heap, (cnt, val))
        elif cnt > heap[0][0]:
            heapq.heapreplace(heap, (cnt, val))

    return [val for _, val in sorted(heap, reverse=True)]


def first_unique(items):
    """
    Return the first item appearing exactly once, or None if none exists.

    Two-pass pattern: count, then scan.
    Time Complexity:  O(n)
    """
    counts = Counter(items)
    for x in items:
        if counts[x] == 1:
            return x
    return None


# =========================================================================
# Operation 3: Compare (Multiset Equality)
# =========================================================================

def is_anagram(s, t):
    """
    True iff s and t are anagrams (same multiset of characters).

    Time Complexity:  O(n)
    """
    return Counter(s) == Counter(t)


# =========================================================================
# Operation 4: Arithmetic
# =========================================================================

def counter_arithmetic_demo(a, b):
    """
    Show the four Counter arithmetic operators and what each means.
    """
    return {
        "add":            a + b,              # elementwise sum
        "subtract":       a - b,              # clipped at 0
        "intersection":   a & b,              # pointwise min
        "union":          a | b,              # pointwise max
    }


# =========================================================================
# Operation 5: Boyer-Moore Voting (Majority Element, O(1) Space)
# =========================================================================

def majority_element(nums):
    """
    Return the element appearing MORE than n/2 times.
    Assumes one such element exists (LeetCode #169's guarantee).

    Time Complexity:  O(n)
    Space Complexity: O(1)   — no counter needed

    See theory.md for the intuition — each non-candidate "pairs off"
    with a candidate vote; the majority survives the tournament.
    """
    candidate = None
    count = 0

    for x in nums:
        if count == 0:
            candidate = x
        count += 1 if x == candidate else -1

    return candidate


# =========================================================================
# Demonstration
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Operation 1 — Build")
    print("=" * 60)
    items = ["a", "b", "a", "c", "a", "b"]
    c = build_counter(items)
    print(f"   build_counter({items}) = {c}")
    print(f"   build_counter_manual same result: {build_counter_manual(items)}")
    print()

    print("=" * 60)
    print("Operation 2 — Query")
    print("=" * 60)
    print(f"   most_frequent_value({dict(c)}) = {most_frequent_value(c)!r}")
    print(f"   top_k_frequent({items}, 2)     = {top_k_frequent(items, 2)}")
    print(f"   first_unique({items})          = {first_unique(items)!r}")
    print()

    print("=" * 60)
    print("Operation 3 — Compare (Multiset Equality)")
    print("=" * 60)
    print(f"   is_anagram('listen', 'silent') = {is_anagram('listen', 'silent')}")
    print(f"   is_anagram('abc', 'abd')       = {is_anagram('abc', 'abd')}")
    print()

    print("=" * 60)
    print("Operation 4 — Arithmetic")
    print("=" * 60)
    a = Counter("aabbc")
    b = Counter("abc")
    ops = counter_arithmetic_demo(a, b)
    print(f"   a = {dict(a)}")
    print(f"   b = {dict(b)}")
    for name, result in ops.items():
        print(f"   {name:14}: {dict(result)}")
    print()

    print("=" * 60)
    print("Operation 5 — Boyer-Moore Voting")
    print("=" * 60)
    cases = [
        ([3, 2, 3], 3),
        ([2, 2, 1, 1, 1, 2, 2], 2),
        ([1], 1),
        ([4, 4, 4, 5, 4], 4),
    ]
    for nums, expected in cases:
        got = majority_element(nums)
        assert got == expected, f"{nums} -> {got}, expected {expected}"
        print(f"   majority_element({nums}) = {got}")

    print("\nAll tests passed!")
