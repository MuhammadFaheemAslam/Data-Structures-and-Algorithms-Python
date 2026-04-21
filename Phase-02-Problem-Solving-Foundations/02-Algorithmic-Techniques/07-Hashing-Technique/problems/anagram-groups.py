"""
Problem: Group Anagrams (Hashing — Grouping by Signature)

Technique: Hashing — pattern 4: signature-based grouping
Difficulty: Easy-Medium (LeetCode #49)

---------------------------------------------------
Problem Statement:

Given a list of strings, group the strings that are anagrams of each other.

Two strings are anagrams if one can be rearranged to form the other
(same letters, same counts, possibly different order).

Return a list of groups. The order of groups does not matter; the
order of strings within each group does not matter.

---------------------------------------------------
The Hashing Lens:

Brute force: for each word, scan existing groups, check "is this an
anagram of any existing member?" → O(n² · k log k) where k = max word
length.

Hashing insight — SIGNATURE-BASED GROUPING:

    Two strings are anagrams iff they share a SIGNATURE — a canonical
    form that's identical for all anagrams.

Two common signatures:

    1. Sorted string:    "eat", "tea", "ate"  all → "aet"
    2. Letter-count tuple: "eat", "tea", "ate" all → (1, 0, 0, ..., 1, 0, 1, ...)

Use the signature as a dict key. Every new word computes its signature
in O(k) or O(k log k), then appends to `groups[signature]` in O(1).

    Time:  O(n · k log k)  with sorted-string signature
           O(n · k)         with letter-count tuple signature
    Space: O(n · k)

---------------------------------------------------
Why the Letter-Count Signature MUST Be a Tuple:

Lists aren't hashable in Python — you can't use them as dict keys.
So while the count array `[0]*26` is a natural representation, you
must convert it to a tuple before using it as a key:

    key = tuple(counts)

Forgetting this raises:
    TypeError: unhashable type: 'list'

It's the single most common bug when writing this solution from scratch.

---------------------------------------------------
Example:

    Input:  ["eat", "tea", "tan", "ate", "nat", "bat"]
    Output: [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]

---------------------------------------------------
"""

from collections import defaultdict


# -------------------------------------------------
# Approach 1: Sorted String as Signature (Interview-Standard)
# -------------------------------------------------

def group_anagrams_sorted(words):
    """
    Signature = sorted characters.

    Time Complexity:  O(n · k log k)
    Space Complexity: O(n · k)

    Clean, short, works for any characters.
    """
    groups = defaultdict(list)
    for w in words:
        sig = "".join(sorted(w))
        groups[sig].append(w)
    return list(groups.values())


# -------------------------------------------------
# Approach 2: Letter-Count Tuple as Signature (Faster for Long Words)
# -------------------------------------------------

def group_anagrams_counts(words):
    """
    Signature = tuple of 26 letter counts.

    Time Complexity:  O(n · k)   — no sort, just a count pass per word
    Space Complexity: O(n · 26) = O(n)

    Slightly faster than Approach 1 when k is large. Assumes lowercase
    a-z; generalize to a Counter-of-tuples-of-items for arbitrary
    characters.
    """
    groups = defaultdict(list)
    for w in words:
        counts = [0] * 26
        for ch in w:
            counts[ord(ch) - ord("a")] += 1
        sig = tuple(counts)                         # MUST be a tuple (hashable)
        groups[sig].append(w)
    return list(groups.values())


# -------------------------------------------------
# Brute Force Reference (Anti-Pattern)
# -------------------------------------------------

def group_anagrams_brute_force(words):
    """
    For each word, scan existing groups for an anagram match.

    Time Complexity:  O(n² · k log k)
    Space Complexity: O(n · k)

    Slow enough to fail on large inputs. Included only to validate the
    hashing solutions on small inputs.
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
# Normalize for Comparison (Order-Independent)
# -------------------------------------------------

def normalize(groups):
    """Sort each group, then sort the list of groups."""
    return sorted([sorted(g) for g in groups])


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    words = ["eat", "tea", "tan", "ate", "nat", "bat"]

    print(f"Input: {words}")
    print(f"group_anagrams_sorted:      {normalize(group_anagrams_sorted(words))}")
    print(f"group_anagrams_counts:      {normalize(group_anagrams_counts(words))}")
    print(f"group_anagrams_brute_force: {normalize(group_anagrams_brute_force(words))}")
    print()

    # Test cases — (input, expected_normalized_groups)
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
        (
            ["aaa", "aaa", "aaa"],
            [["aaa", "aaa", "aaa"]],                # duplicates preserved in a single group
        ),
    ]

    for i, (data, expected) in enumerate(test_cases):
        for fn in (group_anagrams_sorted, group_anagrams_counts, group_anagrams_brute_force):
            got = normalize(fn(data))
            assert got == expected, (
                f"Test {i+1} ({fn.__name__}) failed on {data}: "
                f"expected {expected}, got {got}"
            )
        print(f"Test {i+1} passed: {data} -> {expected}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The General "Group by Signature" Pattern:
    #
    # Any problem of the form "group these items such that equivalent
    # ones end up together" is a signature-hashing problem. The only
    # question is: "what IS the signature?"
    #
    #   Group anagrams           → sorted string / letter-count tuple
    #   Group people by birthdate → (year, month, day)
    #   Group files by extension  → path.rsplit(".", 1)[-1]
    #   Group points by quadrant  → (sign(x), sign(y))
    #   Group similar shapes      → len(vertices)
    #   Group shifted strings     → differences between consecutive chars
    #
    # Same skeleton:
    #       groups = defaultdict(list)
    #       for item in items:
    #           groups[signature(item)].append(item)
    #       return list(groups.values())
    #
    # Once you've solved group_anagrams once, you've solved them all.
    # ---------------------------------------------------------------
