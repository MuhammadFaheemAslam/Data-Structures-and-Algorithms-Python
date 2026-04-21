"""
Problem 03: Group Anagrams

Difficulty: Easy-Medium (LeetCode #49)

---------------------------------------------------
Problem Statement:

Given a list of strings, group the strings that are anagrams of each other.

Two strings are anagrams if one can be rearranged to form the other
(same letters, same counts, possibly different order).

Return a list of groups. The order of groups does not matter.

This problem highlights the other core dict pattern: GROUPING.
The trick is picking the right "signature" to use as the dict key —
two strings are anagrams iff they share the same signature.

---------------------------------------------------
Example:

Input:
    ["eat", "tea", "tan", "ate", "nat", "bat"]

Output:
    [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]

---------------------------------------------------
"""

# -------------------------------------------------
# Approach 1: Sorted String as the Signature (Interview Friendly)
# -------------------------------------------------

def group_anagrams_sorted_key(words):
    """
    Two strings are anagrams iff their sorted characters are equal.
    Use the sorted string (as a tuple or str) as the dict key.

    Time Complexity: O(n * k log k)
        n = number of words, k = max word length
        – sorting each word costs k log k
    Space Complexity: O(n * k) – the groups and the keys
    """
    groups = {}                           # signature -> list of words
    for w in words:
        key = "".join(sorted(w))
        groups.setdefault(key, []).append(w)
    return list(groups.values())


# -------------------------------------------------
# Approach 2: Character-Count Tuple as the Signature (Faster for Long Words)
# -------------------------------------------------

def group_anagrams_count_key(words):
    """
    For each word, build a 26-slot tuple of letter counts.
    Two anagrams produce identical tuples.

    Time Complexity: O(n * k)   – counting is linear in word length
                                  (no log k factor from sorting)
    Space Complexity: O(n * 26) = O(n)

    Tuples are HASHABLE – that's what lets us use them as dict keys.
    A list of counts would raise TypeError here.

    Assumes lowercase ASCII letters. Generalize with a dict-of-counts
    converted to frozenset of (char, count) pairs if needed.
    """
    groups = {}
    for w in words:
        counts = [0] * 26
        for ch in w:
            counts[ord(ch) - ord("a")] += 1
        key = tuple(counts)               # tuple IS hashable; list IS NOT
        groups.setdefault(key, []).append(w)
    return list(groups.values())


# -------------------------------------------------
# Approach 3: defaultdict (Cleanest Version)
# -------------------------------------------------

def group_anagrams_defaultdict(words):
    """
    `collections.defaultdict(list)` auto-creates an empty list the first
    time a key is accessed. Saves the setdefault() boilerplate.

    Time Complexity: O(n * k log k)   (same as Approach 1)
    Space Complexity: O(n * k)
    """
    from collections import defaultdict
    groups = defaultdict(list)
    for w in words:
        groups["".join(sorted(w))].append(w)
    return list(groups.values())


# -------------------------------------------------
# Approach 4: Brute Force – Compare Every Pair (Anti-Pattern)
# -------------------------------------------------

def group_anagrams_bruteforce(words):
    """
    For each word, scan existing groups; if it's an anagram of any
    group's first element, add it there; otherwise start a new group.

    Time Complexity: O(n^2 * k log k)
    Space Complexity: O(n * k)

    Included to highlight what the dict version buys you: direct O(1)
    lookup by signature, no scanning.
    """
    def is_anagram(a, b):
        return sorted(a) == sorted(b)

    groups = []
    for w in words:
        placed = False
        for g in groups:
            if is_anagram(g[0], w):
                g.append(w)
                placed = True
                break
        if not placed:
            groups.append([w])
    return groups


# -------------------------------------------------
# Helpers for Testing (Groups Are Order-Independent)
# -------------------------------------------------

def normalize(groups):
    """
    Sort each group, then sort the list of groups — so equality checks
    don't depend on which order anagrams happened to appear.
    """
    return sorted([sorted(g) for g in groups])


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    words = ["eat", "tea", "tan", "ate", "nat", "bat"]

    print(f"Input: {words}")
    print()
    print("group_anagrams_sorted_key:  ", group_anagrams_sorted_key(words))
    print("group_anagrams_count_key:   ", group_anagrams_count_key(words))
    print("group_anagrams_defaultdict: ", group_anagrams_defaultdict(words))
    print("group_anagrams_bruteforce:  ", group_anagrams_bruteforce(words))
    print()

    # Test cases – (words, expected_normalized_groups)
    test_cases = [
        (
            ["eat", "tea", "tan", "ate", "nat", "bat"],
            [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]],
        ),
        (
            [""],
            [[""]],
        ),
        (
            ["a"],
            [["a"]],
        ),
        (
            ["abc", "cab", "bca", "xyz", "zxy", "xxx"],
            [["abc", "bca", "cab"], ["xxx"], ["xyz", "zxy"]],
        ),
        (
            [],
            [],
        ),
    ]

    for i, (data, expected) in enumerate(test_cases):
        for fn in (
            group_anagrams_sorted_key,
            group_anagrams_count_key,
            group_anagrams_defaultdict,
            group_anagrams_bruteforce,
        ):
            got = normalize(fn(data))
            assert got == expected, (
                f"Test {i+1} ({fn.__name__}) failed on {data}: "
                f"expected {expected}, got {got}"
            )
        print(f"Test {i+1} passed: {data} -> {expected}")

    print("\nAll tests passed!")
