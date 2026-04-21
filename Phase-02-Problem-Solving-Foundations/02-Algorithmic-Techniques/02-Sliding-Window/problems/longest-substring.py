"""
Problem: Longest Substring Without Repeating Characters

Technique: Sliding Window (VARIABLE size, LONGEST flavour)
Difficulty: Medium (LeetCode #3)

---------------------------------------------------
Problem Statement:

Given a string `s`, find the length of the longest substring that
contains no repeated characters.

    Input:   "abcabcbb"
    Output:  3      # "abc"

---------------------------------------------------
The Sliding-Window Lens:

Brute force: for every (i, j) pair, check if s[i..j] has repeats →
O(n^3) (n^2 substrings × O(n) repeat check). Clearly unusable.

Sliding window:

    - Expand `right` one character at a time.
    - Maintain a SET (or dict) of characters currently in the window.
    - If the new character is already in the window, SHRINK from the
      left until it isn't.
    - Record the window length at each step.

The critical invariant: the window [left..right] NEVER contains a
duplicate. The moment a duplicate would appear (because we just added
one), we shrink from the left to remove the old copy.

This is the textbook LONGEST-flavour variable-window problem.

Time Complexity:  O(n)   — each character enters and leaves the window once
Space Complexity: O(min(n, alphabet_size))

---------------------------------------------------
Two Implementations:

We show two versions:

    1. Set-based:      shrink one char at a time until the duplicate is gone.
    2. Dict-based:     jump `left` directly past the last position of the
                       duplicate, using a "char → last seen index" map.

Version 2 is slightly faster (constant-factor) and often preferred in
interviews for its elegance. Both are O(n).

---------------------------------------------------
"""

# -------------------------------------------------
# Approach 1: Set-Based Window (Shrink One at a Time)
# -------------------------------------------------

def length_of_longest_substring_set(s):
    """
    Sliding-window with a character set.

    When the new character is already in `seen`, shrink `left` one step
    at a time until it's gone, then add the new character.

    Time Complexity:  O(n) — each char added and removed at most once
    Space Complexity: O(min(n, alphabet))
    """
    seen = set()
    left = 0
    best = 0

    for right in range(len(s)):
        # shrink until s[right] can be added without duplication
        while s[right] in seen:
            seen.remove(s[left])
            left += 1

        seen.add(s[right])
        best = max(best, right - left + 1)

    return best


# -------------------------------------------------
# Approach 2: Dict-Based Window (Jump `left` Forward)
# -------------------------------------------------

def length_of_longest_substring_dict(s):
    """
    Sliding-window with a "char → last-seen-index" dict.

    When s[right] is a duplicate of a character INSIDE the current window,
    move `left` directly to `last_seen[s[right]] + 1` — skipping past the
    old copy in one jump instead of shrinking one step at a time.

    Important: only jump `left` if the old copy is actually INSIDE the
    window (i.e., last_seen[c] >= left). If it's already before `left`,
    it's no longer in the window and irrelevant.

    Time Complexity:  O(n)
    Space Complexity: O(min(n, alphabet))
    """
    last_seen = {}          # char -> index of its last occurrence
    left = 0
    best = 0

    for right, c in enumerate(s):
        if c in last_seen and last_seen[c] >= left:
            left = last_seen[c] + 1             # jump past old copy

        last_seen[c] = right
        best = max(best, right - left + 1)

    return best


# -------------------------------------------------
# Brute Force for Verification
# -------------------------------------------------

def length_of_longest_substring_brute_force(s):
    """
    Check every substring — O(n^3). Only for validating on small inputs.
    """
    best = 0
    for i in range(len(s)):
        seen = set()
        for j in range(i, len(s)):
            if s[j] in seen:
                break
            seen.add(s[j])
            if j - i + 1 > best:
                best = j - i + 1
    return best


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    for s in ["abcabcbb", "bbbbb", "pwwkew", "", "a", "dvdf"]:
        a = length_of_longest_substring_set(s)
        b = length_of_longest_substring_dict(s)
        c = length_of_longest_substring_brute_force(s)
        assert a == b == c, f"disagreement on {s!r}: {a}, {b}, {c}"
        print(f"   {s!r:15}  -> {a}")
    print()

    # Test cases — (s, expected)
    test_cases = [
        ("abcabcbb",    3),      # "abc"
        ("bbbbb",       1),      # "b"
        ("pwwkew",      3),      # "wke"
        ("",            0),
        ("a",           1),
        ("au",          2),
        ("dvdf",        3),      # "vdf"
        ("abba",        2),      # "ab" or "ba" — classic jump-too-far trap
        ("tmmzuxt",     5),      # "mzuxt"
        ("anviaj",      5),      # "nviaj"
    ]

    for i, (s, expected) in enumerate(test_cases):
        for fn in (
            length_of_longest_substring_set,
            length_of_longest_substring_dict,
            length_of_longest_substring_brute_force,
        ):
            got = fn(s)
            assert got == expected, (
                f"Test {i+1} ({fn.__name__}) failed on {s!r}: "
                f"expected {expected}, got {got}"
            )
        print(f"Test {i+1} passed: {s!r} -> {expected}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Sneaky Test Case — "abba":
    #
    #   A wrong implementation of Approach 2 might set:
    #       left = last_seen[c] + 1
    #   unconditionally, without the "is the old copy actually inside
    #   the window?" check. On "abba":
    #
    #       right=3, c='a':  last_seen['a'] = 0, but left is already 2
    #                        (after seeing the duplicate 'b').
    #                        Setting left = 0 + 1 = 1 would MOVE LEFT
    #                        BACKWARD — violating the sliding-window
    #                        invariant.
    #
    #   Always guard with:   `if last_seen[c] >= left:`
    #   This is the single most common bug in this problem.
    # ---------------------------------------------------------------
