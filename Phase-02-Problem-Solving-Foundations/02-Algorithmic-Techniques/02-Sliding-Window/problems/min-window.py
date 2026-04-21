"""
Problem: Minimum Window Substring

Technique: Sliding Window (VARIABLE size, SHORTEST flavour) + dict state
Difficulty: Hard (LeetCode #76)

---------------------------------------------------
Problem Statement:

Given strings `s` and `t`, return the minimum window (shortest contiguous
substring) of `s` that contains EVERY character of `t`, including
multiplicities.

If no such window exists, return the empty string.

---------------------------------------------------
Why This Is the Hardest Classic Sliding-Window Problem:

Two things make this problem trickier than the other variable-window
templates:

    1. The "valid window" predicate is RICH: not "no duplicates" or
       "sum ≥ target", but "contains at least the right count of every
       character of t". Naively, checking that would be O(|alphabet|)
       per step.

    2. It's the SHORTEST-flavour pattern — expand until valid, then
       shrink as much as possible while still valid, AND update the
       answer inside the shrink.

We solve both with the classic "have / need" counter trick:

    need  = len(t)                  # number of char-occurrences still missing
    count = Counter(t)              # char → how many more of this we still need

    When adding a char that we NEED (count[c] > 0), decrement `need`.
    When removing a char that we'd then NEED (count[c] becomes > 0), increment `need`.

    The window is valid ↔ need == 0.

That gives us O(1) validity checks, so the whole algorithm is O(|s| + |t|).

---------------------------------------------------
Example:

    s = "ADOBECODEBANC", t = "ABC"
    -> "BANC"           # shortest window of s containing A, B, and C

---------------------------------------------------
"""

from collections import Counter


# -------------------------------------------------
# The Sliding-Window Solution — O(|s| + |t|)
# -------------------------------------------------

def min_window(s, t):
    """
    Return the shortest substring of `s` containing every character of
    `t` (including multiplicities). Returns "" if no valid window exists.

    Time Complexity:  O(|s| + |t|)
    Space Complexity: O(|t|)  — the `need` counter
    """
    if not s or not t or len(s) < len(t):
        return ""

    need = Counter(t)                        # char → still-missing count
    missing = len(t)                         # total characters still missing

    left = 0
    best_len = float("inf")
    best_range = (0, 0)

    for right, c in enumerate(s):
        # expand right edge — does this char help satisfy the requirement?
        if need[c] > 0:
            missing -= 1
        need[c] -= 1

        # if window is valid, try to shrink from the left
        while missing == 0:
            if right - left + 1 < best_len:
                best_len = right - left + 1
                best_range = (left, right + 1)

            # remove s[left]
            left_char = s[left]
            need[left_char] += 1
            if need[left_char] > 0:           # we now MISS this char
                missing += 1
            left += 1

    return s[best_range[0]:best_range[1]] if best_len != float("inf") else ""


# -------------------------------------------------
# Brute Force for Verification
# -------------------------------------------------

def min_window_brute_force(s, t):
    """
    Check every substring of `s` and return the shortest that contains
    every char of `t` (with multiplicities).

    Time Complexity:  O(|s|^3 * |t|)   — worst case
    Space Complexity: O(|t|)

    Only for validating the sliding-window implementation on small inputs.
    """
    if not s or not t or len(s) < len(t):
        return ""

    need = Counter(t)

    def contains_all(sub):
        have = Counter(sub)
        for c, cnt in need.items():
            if have[c] < cnt:
                return False
        return True

    best = ""
    for i in range(len(s)):
        for j in range(i + len(t), len(s) + 1):
            sub = s[i:j]
            if contains_all(sub) and (best == "" or len(sub) < len(best)):
                best = sub
    return best


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    s, t = "ADOBECODEBANC", "ABC"
    print(f"s = {s!r}, t = {t!r}")
    print(f"min_window:             {min_window(s, t)!r}")
    print(f"min_window_brute_force: {min_window_brute_force(s, t)!r}")
    print()

    # Test cases — (s, t, expected)
    #
    # Note: when multiple valid windows of the same length exist, our
    # sliding-window returns the FIRST such window encountered. The
    # brute force returns the same.
    test_cases = [
        ("ADOBECODEBANC",       "ABC",      "BANC"),
        ("a",                   "a",        "a"),
        ("a",                   "aa",       ""),             # insufficient chars
        ("aa",                  "aa",       "aa"),
        ("",                    "a",        ""),
        ("abc",                 "",         ""),             # empty target
        ("abcdef",              "f",        "f"),
        ("abcdef",              "gh",       ""),
        ("AAABBBCCC",           "ABC",      "ABBBC"),        # first valid window
        ("aaflslflsldkalskaaa", "aaa",      "aaa"),
        ("bba",                 "ab",       "ba"),
    ]

    for i, (s, t, expected) in enumerate(test_cases):
        for fn in (min_window, min_window_brute_force):
            got = fn(s, t)
            # for "empty target", any empty window counts; standardize on ""
            if not t:
                got = ""
            assert got == expected, (
                f"Test {i+1} ({fn.__name__}) failed on s={s!r}, t={t!r}: "
                f"expected {expected!r}, got {got!r}"
            )
        print(f"Test {i+1} passed: s={s!r}, t={t!r} -> {expected!r}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Why the `missing` Counter Is So Important:
    #
    #   A naive check of "does this window contain all of t?" would
    #   scan the entire `need` dict at every step — O(|alphabet|) per
    #   step, making the whole algorithm O(|s| * |alphabet|).
    #
    #   Tracking `missing` as a SINGLE INT that we update incrementally
    #   gives us O(1) validity checks. It's a small bookkeeping trick,
    #   but it's THE difference between a sliding-window solution and
    #   an almost-but-not-quite one.
    #
    #   Whenever you build a variable-window solution with a dict state,
    #   ask: "can I summarize validity as an int that I update in O(1)?"
    #   If yes, you'll get a clean O(n) algorithm. If not, your window
    #   state is under-designed.
    # ---------------------------------------------------------------
