"""
template.py – Hashing Technique Reference Template

This file demonstrates the FOUR canonical hashing patterns:

    1. "Have I seen X?"                  — set of visited
    2. "Has X's partner been seen?"      — dict of value → position
    3. "How many of each?"               — frequency counter
    4. "What's X's group?"               — signature → list/set

All four share the same skeleton: insert into a hash structure as you
walk once through the input, and each query is an O(1) lookup.

Run this file to see each pattern in action.
"""

from collections import Counter, defaultdict


# =========================================================================
# Pattern 1: "Have I Seen X Before?"  — Set of Visited
# =========================================================================

def has_duplicate(arr):
    """
    Return True if `arr` contains any duplicate.

    Time Complexity:  O(n)
    Space Complexity: O(n)

    Canonical use of a `seen` set. Also solves Cycle detection (on
    linked lists where O(n) space is acceptable) and "find first
    repeating character" variants.
    """
    seen = set()
    for x in arr:
        if x in seen:
            return True
        seen.add(x)
    return False


# =========================================================================
# Pattern 2: "Has X's Partner Been Seen?"  — Dict of value → position
# =========================================================================

def two_sum(nums, target):
    """
    Return indices (i, j) such that nums[i] + nums[j] == target,
    or None if no such pair exists.

    Time Complexity:  O(n)
    Space Complexity: O(n)

    For each new x, we ask: "has `target - x` been seen already?"
    That's an O(1) dict lookup — dramatically better than the O(n²)
    nested-loop search.
    """
    seen = {}                                    # value → index
    for i, x in enumerate(nums):
        complement = target - x
        if complement in seen:
            return (seen[complement], i)
        seen[x] = i
    return None


# =========================================================================
# Pattern 3: "How Many of Each?"  — Frequency Counter
# =========================================================================

def most_frequent(items):
    """
    Return the most common item in `items` (first-seen on ties).

    Time Complexity:  O(n)
    Space Complexity: O(distinct items)

    Uses `max(d, key=d.get)` — iterates the dict's KEYS, ranked by
    their VALUE. Ties broken by insertion order (first-seen wins).
    """
    if not items:
        return None

    counts = {}
    for x in items:
        counts[x] = counts.get(x, 0) + 1

    return max(counts, key=counts.get)


def are_anagrams(s, t):
    """
    True iff s and t are anagrams (same multiset of characters).

    Time Complexity:  O(n)
    Space Complexity: O(alphabet)

    The `Counter(s) == Counter(t)` one-liner is the idiomatic version.
    """
    return Counter(s) == Counter(t)


# =========================================================================
# Pattern 4: "What's X's Group?"  — Signature-Based Grouping
# =========================================================================

def group_words_by_length(words):
    """
    Group strings by their length.

    Time Complexity:  O(total characters)
    Space Complexity: O(n)

    The "signature" is just `len(word)`. For more interesting groupings
    (anagrams, shifted strings, etc.) replace the signature with a
    different canonical form.
    """
    groups = defaultdict(list)                   # defaultdict avoids the `setdefault` boilerplate
    for word in words:
        groups[len(word)].append(word)
    return dict(groups)


def group_anagrams(words):
    """
    Group anagrams together. The signature is the sorted string.

    Time Complexity:  O(n · k log k) — n words, k avg length
    Space Complexity: O(n · k)
    """
    groups = defaultdict(list)
    for w in words:
        sig = "".join(sorted(w))
        groups[sig].append(w)
    return list(groups.values())


# =========================================================================
# Bonus: Prefix Sum + Hashing — Subarrays with a Given Sum
# =========================================================================

def count_subarrays_sum_k(nums, k):
    """
    Count contiguous subarrays of `nums` whose sum equals `k`.

    Time Complexity:  O(n)
    Space Complexity: O(n)

    Combines prefix sum with hashing — the single most powerful
    prefix-based trick. See Phase-02 / 02 / 03-Prefix-Sum.
    """
    seen = {0: 1}                                # prefix-sum → count, including empty prefix
    running = 0
    count = 0
    for x in nums:
        running += x
        if running - k in seen:
            count += seen[running - k]
        seen[running] = seen.get(running, 0) + 1
    return count


# =========================================================================
# Demonstration
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Pattern 1 — Set of Visited (has duplicate)")
    print("=" * 60)
    for arr in [[1, 2, 3, 1], [1, 2, 3], [], [7]]:
        print(f"   has_duplicate({arr}) = {has_duplicate(arr)}")
    print()

    print("=" * 60)
    print("Pattern 2 — Dict of Value → Index (Two Sum)")
    print("=" * 60)
    for nums, target in [([2, 7, 11, 15], 9), ([3, 2, 4], 6), ([1, 2, 3], 10)]:
        print(f"   two_sum({nums}, target={target}) = {two_sum(nums, target)}")
    print()

    print("=" * 60)
    print("Pattern 3 — Frequency Counter")
    print("=" * 60)
    print(f"   most_frequent(['a','b','a','c','a','b']) = {most_frequent(['a', 'b', 'a', 'c', 'a', 'b'])!r}")
    print(f"   are_anagrams('listen', 'silent') = {are_anagrams('listen', 'silent')}")
    print(f"   are_anagrams('abc', 'abd')       = {are_anagrams('abc', 'abd')}")
    print()

    print("=" * 60)
    print("Pattern 4 — Grouping by Signature")
    print("=" * 60)
    print(f"   by length: {group_words_by_length(['one', 'two', 'three', 'hi', 'four'])}")
    anagrams = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    print(f"   anagrams:  {[sorted(g) for g in sorted(anagrams, key=lambda g: sorted(g))]}")
    print()

    print("=" * 60)
    print("Bonus — Prefix Sum + Hashing (Subarrays Sum K)")
    print("=" * 60)
    for nums, k in [([1, 1, 1], 2), ([1, 2, 3], 3), ([1, -1, 1, -1], 0)]:
        print(f"   count_subarrays_sum_k({nums}, k={k}) = {count_subarrays_sum_k(nums, k)}")

    print("\nAll patterns demonstrated.")
