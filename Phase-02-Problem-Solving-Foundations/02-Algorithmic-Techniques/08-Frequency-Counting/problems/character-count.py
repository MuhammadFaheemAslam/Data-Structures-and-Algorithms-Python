"""
Problem: Character Counts — Valid Anagram and First Unique Character

Technique: Frequency Counting — multiset equality and single-scan queries
Difficulty: Easy (LeetCode #242 and #387)

---------------------------------------------------
Problem Statements:

Valid Anagram (LeetCode #242):
    Given two strings `s` and `t`, return True if `t` is an anagram of
    `s` — i.e., both strings contain the same multiset of characters.

First Unique Character (LeetCode #387):
    Given a string `s`, return the INDEX of the first character that
    appears exactly once in the string. Return -1 if no unique character
    exists.

Both problems are archetypal frequency-counting problems. Together
they showcase the two most common query types:

    1. "Do two multisets match?"         (anagram check)
    2. "What's the first thing appearing exactly once?"  (first unique)

---------------------------------------------------
The Frequency-Counting Lens:

Valid Anagram:
    Two strings are anagrams iff `Counter(s) == Counter(t)`. One line.
    O(n) time, O(|alphabet|) space.

First Unique Character:
    Build a Counter of characters, then walk `s` again and return the
    first index whose character has count 1.
    Two passes over `s`, each O(n). Total: O(n) time.

Both problems benefit from the **array-of-26** representation when the
input is lowercase a-z only:

    counts = [0] * 26
    for ch in s:
        counts[ord(ch) - ord("a")] += 1

Faster and uses constant space (since the alphabet is fixed).

---------------------------------------------------
Examples:

    is_anagram("anagram", "nagaram")    -> True
    is_anagram("rat", "car")            -> False

    first_unique_char("leetcode")       -> 0       ('l')
    first_unique_char("loveleetcode")   -> 2       ('v')
    first_unique_char("aabb")           -> -1

---------------------------------------------------
"""

from collections import Counter


# ==========================================================================
# Valid Anagram (LeetCode #242)
# ==========================================================================

# -------------------------------------------------
# Approach 1: Counter Equality (Idiomatic)
# -------------------------------------------------

def is_anagram_counter(s, t):
    """
    Count characters in both strings; equal multisets iff anagrams.

    Time Complexity:  O(n + m)
    Space Complexity: O(|alphabet|)
    """
    return Counter(s) == Counter(t)


# -------------------------------------------------
# Approach 2: Array-of-26 (Faster for Lowercase a-z)
# -------------------------------------------------

def is_anagram_fixed_alphabet(s, t):
    """
    Use a 26-slot array instead of a Counter. Faster and uses constant
    space. Assumes lowercase a-z only.

    Time Complexity:  O(n + m)
    Space Complexity: O(1)   — fixed-size array, not O(|alphabet|)

    We don't build two arrays — we INCREMENT from `s` and DECREMENT
    from `t`. If `s` and `t` are anagrams, every slot ends at zero.
    """
    if len(s) != len(t):
        return False

    counts = [0] * 26
    for c1, c2 in zip(s, t):
        counts[ord(c1) - ord("a")] += 1
        counts[ord(c2) - ord("a")] -= 1

    return all(c == 0 for c in counts)


# -------------------------------------------------
# Approach 3: Sort Both (Simpler, Slower)
# -------------------------------------------------

def is_anagram_sort(s, t):
    """
    Sort both strings; equal iff anagrams.

    Time Complexity:  O(n log n)
    Space Complexity: O(n)

    Works for any characters, no alphabet assumptions. But slower than
    the counter approach.
    """
    return sorted(s) == sorted(t)


# ==========================================================================
# First Unique Character (LeetCode #387)
# ==========================================================================

# -------------------------------------------------
# Approach 1: Counter + Second Pass
# -------------------------------------------------

def first_unique_char_counter(s):
    """
    Build a Counter, then scan `s` once more for the first char with
    count 1.

    Time Complexity:  O(n)
    Space Complexity: O(|alphabet|)
    """
    counts = Counter(s)
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return i
    return -1


# -------------------------------------------------
# Approach 2: Array-of-26 + Second Pass
# -------------------------------------------------

def first_unique_char_fixed_alphabet(s):
    """
    Same algorithm but with a 26-slot array.

    Time Complexity:  O(n)
    Space Complexity: O(1)
    """
    counts = [0] * 26
    for ch in s:
        counts[ord(ch) - ord("a")] += 1
    for i, ch in enumerate(s):
        if counts[ord(ch) - ord("a")] == 1:
            return i
    return -1


# -------------------------------------------------
# Approach 3: Brute Force — O(n²)
# -------------------------------------------------

def first_unique_char_brute_force(s):
    """
    For each character, rescan to see if it appears elsewhere.

    Time Complexity:  O(n²)
    Space Complexity: O(1)

    Included only for validation on small inputs.
    """
    for i, ch in enumerate(s):
        if s.count(ch) == 1:                      # one O(n) scan per position
            return i
    return -1


# ==========================================================================
# Test the Functions
# ==========================================================================

if __name__ == "__main__":
    # --- Valid Anagram tests ---
    print("=" * 60)
    print("Valid Anagram")
    print("=" * 60)

    anagram_cases = [
        ("anagram", "nagaram",     True),
        ("rat",     "car",         False),
        ("",        "",            True),                # empty strings
        ("a",       "a",           True),
        ("a",       "b",           False),
        ("aacc",    "ccac",        False),               # counts must match
        ("abcdef",  "fedcba",      True),
    ]

    for s, t, expected in anagram_cases:
        for fn in (is_anagram_counter, is_anagram_fixed_alphabet, is_anagram_sort):
            got = fn(s, t)
            assert got == expected, (
                f"{fn.__name__}({s!r}, {t!r}) = {got}, expected {expected}"
            )
        print(f"   is_anagram({s!r:10}, {t!r:10}) = {expected}")
    print()

    # --- First Unique Character tests ---
    print("=" * 60)
    print("First Unique Character")
    print("=" * 60)

    unique_cases = [
        ("leetcode",        0),
        ("loveleetcode",    2),
        ("aabb",           -1),
        ("",               -1),
        ("z",               0),
        ("abcdefghij",      0),                          # all unique
        ("aabccdd",         2),                          # 'b' is first unique, at index 2
        ("dddccdbba",       8),                          # counts: d=4, c=2, b=2, a=1 → 'a' at index 8
    ]

    for s, expected in unique_cases:
        for fn in (
            first_unique_char_counter,
            first_unique_char_fixed_alphabet,
            first_unique_char_brute_force,
        ):
            got = fn(s)
            assert got == expected, (
                f"{fn.__name__}({s!r}) = {got}, expected {expected}"
            )
        print(f"   first_unique_char({s!r:15}) = {expected}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Pattern to Remember:
    #
    #   Both problems are solved by the same two moves:
    #
    #     1. Build a frequency map in one pass.
    #     2. Query it in O(1) per lookup during a second pass.
    #
    # That's the whole module. Valid Anagram compares two maps for
    # equality; First Unique Character looks up counts during a scan.
    # Every "string frequency" interview problem is a variant.
    # ---------------------------------------------------------------
