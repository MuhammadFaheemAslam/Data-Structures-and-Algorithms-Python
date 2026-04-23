"""
Problem: Anagram — Three Variants

Difficulty: Easy → Medium

---------------------------------------------------
Covered in this file:

    1. is_anagram(s, t)              — same characters, any order (LC #242)
    2. group_anagrams(words)         — group words that are anagrams of each other (LC #49)
    3. find_all_anagrams(s, p)       — all starting indices of anagrams of p within s (LC #438)

All three reduce to **multiset equality on character counts** — the
canonical frequency-counting pattern.

---------------------------------------------------
The Core Test: Are Two Strings Anagrams?

Two strings are anagrams iff they have the same MULTISET of characters.
Three ways to check:

    a) Sort both → compare.      O(n log n) time, O(n) space.
    b) Counter comparison.        O(n) time, O(k) space (k = alphabet).
    c) Array-of-26.              O(n) time, O(1) space (constant-size array).

(b) and (c) both beat (a) asymptotically. (c) is the fastest in
practice when the alphabet is fixed (e.g., lowercase a-z).
"""

from collections import Counter, defaultdict


# =========================================================================
# 1. Is Anagram (LC #242) — Three Approaches
# =========================================================================

def is_anagram_sort(s, t):
    """
    Sort both strings and compare.

    Time:  O(n log n)
    Space: O(n) — sorted() returns a new list
    """
    if len(s) != len(t):
        return False
    return sorted(s) == sorted(t)


def is_anagram_counter(s, t):
    """
    Counter comparison — the idiomatic one-liner.

    Time:  O(n)
    Space: O(alphabet)
    """
    return Counter(s) == Counter(t)


def is_anagram_fixed_alphabet(s, t):
    """
    26-slot array for lowercase a-z — fastest in practice.

    Time:  O(n)
    Space: O(1) — a constant-sized 26-slot array

    Trick: increment from s, decrement from t. If they're anagrams,
    every slot ends at 0.
    """
    if len(s) != len(t):
        return False

    counts = [0] * 26
    for a, b in zip(s, t):
        counts[ord(a) - ord("a")] += 1
        counts[ord(b) - ord("a")] -= 1

    return all(c == 0 for c in counts)


# =========================================================================
# 2. Group Anagrams (LC #49)
# =========================================================================

def group_anagrams_sorted_key(words):
    """
    Signature = sorted(word). Words with the same sorted-key are anagrams.

    Time:  O(n · k log k)    n = # words, k = average word length
    Space: O(n · k)
    """
    groups = defaultdict(list)
    for w in words:
        key = "".join(sorted(w))
        groups[key].append(w)
    return list(groups.values())


def group_anagrams_count_key(words):
    """
    Signature = tuple of 26 letter counts. Works for lowercase a-z.

    Time:  O(n · k)
    Space: O(n)

    Slightly faster than sorted-key for long words; assumes fixed alphabet.
    """
    groups = defaultdict(list)
    for w in words:
        counts = [0] * 26
        for c in w:
            counts[ord(c) - ord("a")] += 1
        groups[tuple(counts)].append(w)        # tuple, not list — hashable key
    return list(groups.values())


# =========================================================================
# 3. Find All Anagrams in a String (LC #438) — Sliding Window
# =========================================================================

def find_all_anagrams(s, p):
    """
    Return all starting indices in `s` where a substring of length |p|
    is an anagram of `p`.

        s = "cbaebabacd", p = "abc"
        → [0, 6]
        (at index 0: "cba" ↔ "abc"; at index 6: "bac" ↔ "abc")

    Technique: SLIDING WINDOW of size len(p).
        - Maintain a character-count for the current window.
        - Compare window count to p's count each step.
        - Slide right: add entering, remove leaving, compare, emit on match.

    Time:  O(n)       where n = len(s)
    Space: O(k)       k = alphabet size (26 for lowercase a-z)
    """
    n, m = len(s), len(p)
    if m > n:
        return []

    p_count = Counter(p)
    window_count = Counter(s[:m])

    result = []
    if window_count == p_count:
        result.append(0)

    for i in range(m, n):
        # add new right-edge character
        window_count[s[i]] += 1
        # remove the character that just left the window
        left_char = s[i - m]
        window_count[left_char] -= 1
        if window_count[left_char] == 0:
            del window_count[left_char]           # keep the dict clean for equality

        if window_count == p_count:
            result.append(i - m + 1)

    return result


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    # 1. is_anagram
    print("1. is_anagram — three implementations:")
    cases = [
        ("listen", "silent",  True),
        ("rat",    "car",     False),
        ("a",      "a",       True),
        ("",       "",        True),
        ("ab",     "abc",     False),             # length mismatch
        ("aab",    "aba",     True),
        ("anagram","nagaram", True),
    ]
    for s, t, expected in cases:
        for fn in (is_anagram_sort, is_anagram_counter, is_anagram_fixed_alphabet):
            got = fn(s, t)
            assert got == expected, f"{fn.__name__}({s!r}, {t!r}): {got} != {expected}"
        print(f"   is_anagram({s!r:10}, {t!r:10}) = {expected}")
    print()

    # 2. group_anagrams
    print("2. group_anagrams:")
    words = ["eat", "tea", "tan", "ate", "nat", "bat"]
    for fn in (group_anagrams_sorted_key, group_anagrams_count_key):
        got = fn(words)
        # normalize for comparison: sort within + sort across groups
        normalized = sorted([sorted(g) for g in got])
        expected = [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]
        assert normalized == expected, f"{fn.__name__}: {normalized} != {expected}"
        print(f"   {fn.__name__}(words) = {normalized}")
    print()

    # 3. find_all_anagrams (sliding window)
    print("3. find_all_anagrams (LC #438):")
    anagram_cases = [
        ("cbaebabacd",  "abc",  [0, 6]),
        ("abab",        "ab",   [0, 1, 2]),
        ("",            "abc",  []),
        ("abc",         "",     [i for i in range(4)]),    # len-0 pattern matches every position
                                                            # including the end
        ("aaaa",        "a",    [0, 1, 2, 3]),
        ("abcde",       "fgh",  []),
        ("af",          "be",   []),
    ]
    for s, p, expected in anagram_cases:
        got = find_all_anagrams(s, p)
        assert got == expected, f"find_all_anagrams({s!r}, {p!r}): {got} != {expected}"
        print(f"   find_all_anagrams({s!r:15}, {p!r:5}) = {got}")
    print()

    # Stress test — compare fixed-alphabet version against Counter version
    import random
    random.seed(42)
    for _ in range(300):
        n = random.randint(0, 20)
        s = "".join(random.choice("abc") for _ in range(n))
        t = "".join(random.choice("abc") for _ in range(n))

        a = is_anagram_sort(s, t)
        b = is_anagram_counter(s, t)
        c = is_anagram_fixed_alphabet(s, t)
        assert a == b == c

    print("Stress test: 300 random pairs — all three is_anagram variants agree")
    print("\nAll tests passed!")
