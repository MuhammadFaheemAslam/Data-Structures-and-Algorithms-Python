"""
Problem: Longest Palindromic Substring

Difficulty: Medium (LeetCode #5)

---------------------------------------------------
Problem Statement:

Given a string `s`, return the LONGEST PALINDROMIC SUBSTRING of `s`.
(Substring means CONTIGUOUS, not subsequence.)

Example:
    "babad"  →  "bab" or "aba"     (both valid length-3 palindromes)
    "cbbd"   →  "bb"
    "a"      →  "a"
    "racecar" → "racecar"

---------------------------------------------------
Three Classical Approaches:

### 1. O(n²) DP — "is s[i..j] a palindrome?"

    dp[i][j] = True iff s[i..j] is a palindrome.
    dp[i][j] = (s[i] == s[j]) AND (j - i <= 1 OR dp[i+1][j-1])

Fill by LENGTH ascending (all len-1 palindromes first, then len-2, …).
Track the largest (i, j) seen.

O(n²) time, O(n²) space.

### 2. O(n²) EXPAND AROUND CENTER — the usual interview answer

For each possible CENTER (every index + every gap-between-indices),
expand outward while s[l] == s[r]. Total work is still O(n²) but
with a tiny constant factor and O(1) extra space.

### 3. O(n) Manacher's algorithm

A masterful algorithm that reuses previous palindrome extents to
avoid re-checking characters. Conceptually the "longest-palindrome
Z-algorithm". We SKETCH the idea here; the full implementation is
in Phase 12 (strings).

We implement (1) and (2). Manacher's is out of scope for THIS module.

---------------------------------------------------
Complexity:

    DP:              Time O(n²), Space O(n²).
    Expand center:   Time O(n²), Space O(1).
    Manacher's:      Time O(n),  Space O(n).        (Phase 12)
"""


# -------- Expand around center (recommended) --------

def longest_palindrome(s):
    """
    Return one of the longest palindromic substrings.

    Time: O(n²), Space: O(1).
    """
    if not s:
        return ""

    def expand(l, r):
        """Expand outward while s[l] == s[r]; return the palindrome."""
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        return s[l + 1:r]

    best = ""
    for i in range(len(s)):
        # Odd-length palindrome centered at i
        p1 = expand(i, i)
        # Even-length palindrome centered between i and i+1
        p2 = expand(i, i + 1)
        for p in (p1, p2):
            if len(p) > len(best):
                best = p
    return best


# -------- DP version (for cross-check) --------

def longest_palindrome_dp(s):
    """
    Classic 2D DP: dp[i][j] = s[i..j] is a palindrome.

    Time: O(n²), Space: O(n²).
    """
    n = len(s)
    if n == 0:
        return ""

    dp = [[False] * n for _ in range(n)]
    best_lo, best_hi = 0, 0

    # Length 1
    for i in range(n):
        dp[i][i] = True

    # Length 2
    for i in range(n - 1):
        if s[i] == s[i + 1]:
            dp[i][i + 1] = True
            best_lo, best_hi = i, i + 1

    # Length 3+
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j] and dp[i + 1][j - 1]:
                dp[i][j] = True
                if length > best_hi - best_lo + 1:
                    best_lo, best_hi = i, j

    return s[best_lo:best_hi + 1]


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #5 examples
    assert longest_palindrome("babad") in ("bab", "aba")
    assert longest_palindrome("cbbd") == "bb"
    assert longest_palindrome("a") == "a"
    assert longest_palindrome("ac") in ("a", "c")
    assert longest_palindrome("") == ""

    # Known palindromes
    assert longest_palindrome("racecar") == "racecar"
    assert longest_palindrome("abcba") == "abcba"
    assert longest_palindrome("abba") == "abba"
    assert longest_palindrome("aaaa") == "aaaa"

    # Both approaches find palindromes of the SAME LENGTH on every input
    import random
    random.seed(42)
    for _ in range(500):
        s = "".join(random.choice("abc") for _ in range(random.randint(0, 25)))
        a = longest_palindrome(s)
        b = longest_palindrome_dp(s)
        assert len(a) == len(b), f"mismatch: s={s!r}, expand={a!r}, dp={b!r}"
        # Both are palindromes
        assert a == a[::-1]
        assert b == b[::-1]
        # Both are substrings of s
        assert a in s
        assert b in s

    # Brute force: every substring
    def brute(s):
        best = ""
        for i in range(len(s)):
            for j in range(i, len(s)):
                sub = s[i:j + 1]
                if sub == sub[::-1] and len(sub) > len(best):
                    best = sub
        return best

    for _ in range(100):
        s = "".join(random.choice("ab") for _ in range(random.randint(0, 15)))
        expected_len = len(brute(s))
        assert len(longest_palindrome(s)) == expected_len
        assert len(longest_palindrome_dp(s)) == expected_len

    print("All tests passed!")
