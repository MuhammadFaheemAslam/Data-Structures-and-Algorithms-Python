"""
Problem: Regular Expression Matching

Difficulty: Hard (LeetCode #10)

---------------------------------------------------
Problem Statement:

Given a string `s` and a pattern `p`, return True iff the pattern
matches the ENTIRE string. Pattern supports:

    '.'  matches any single character
    '*'  matches ZERO OR MORE of the preceding element

Examples:
    s = "aa",     p = "a"       → False   (p matches only one 'a')
    s = "aa",     p = "a*"      → True    ('a*' = "" or "a" or "aa"...)
    s = "ab",     p = ".*"      → True    ('.*' = any sequence)
    s = "aab",    p = "c*a*b"   → True    ('c*' = "", 'a*' = "aa")
    s = "mississippi", p = "mis*is*p*." → False

---------------------------------------------------
Why DP (Not A Regex Library)?

Yes, Python's `re` would solve this. But the problem is asking you to
IMPLEMENT regex matching from scratch. The algorithmic heart is:

    dp[i][j] = True iff s[:i] matches p[:j]

Recurrence — look at the LAST pattern char:

    if p[j-1] != '*':
        # Either exact-char match or '.'; must consume one s char.
        match = (i > 0 and (p[j-1] == s[i-1] or p[j-1] == '.'))
        dp[i][j] = dp[i-1][j-1] and match

    else:  # p[j-1] == '*'
        # '*' modifies p[j-2]. Two cases:
        # (a) Use zero copies: drop "X*" from pattern
        dp[i][j] = dp[i][j-2]
        # (b) Use >=1 copy: if p[j-2] matches s[i-1], eat that s char
        if i > 0 and (p[j-2] == s[i-1] or p[j-2] == '.'):
            dp[i][j] |= dp[i-1][j]

Base: dp[0][0] = True (empty matches empty).
      dp[0][j] = True ONLY when pattern can vanish (e.g. "a*" or "a*b*c*").

---------------------------------------------------
Subtle Points:

    1. "*" ALWAYS follows another character in the pattern (guarantee).
    2. "a*b*c*" should match "" — handle this in the base row.
    3. The "zero copies" case of `*` makes an adjacent-column jump
       (dp[i][j-2]), not diagonal. Missing this is the #1 bug.

---------------------------------------------------
Complexity:

    Time:  O(m·n)
    Space: O(m·n)  (can be reduced to O(n) with care)
"""


def is_match(s, p):
    """
    Full regex match per LC #10 rules.

    Time:  O(m·n)
    Space: O(m·n)
    """
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True

    # Base row: empty s, pattern must vanish (like "a*b*c*")
    for j in range(1, n + 1):
        if p[j - 1] == "*":
            dp[0][j] = dp[0][j - 2]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == "*":
                # Zero copies of the char before '*'
                dp[i][j] = dp[i][j - 2]
                # One-or-more copies: if previous pattern char matches current s char
                if p[j - 2] == s[i - 1] or p[j - 2] == ".":
                    dp[i][j] = dp[i][j] or dp[i - 1][j]
            else:
                # Literal or '.' — must consume one s char
                if p[j - 1] == s[i - 1] or p[j - 1] == ".":
                    dp[i][j] = dp[i - 1][j - 1]

    return dp[m][n]


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #10 examples
    assert is_match("aa", "a") is False
    assert is_match("aa", "a*") is True
    assert is_match("ab", ".*") is True
    assert is_match("aab", "c*a*b") is True
    assert is_match("mississippi", "mis*is*p*.") is False

    # More cases
    assert is_match("", "") is True
    assert is_match("", "a*") is True
    assert is_match("", "a*b*c*") is True
    assert is_match("", "a") is False
    assert is_match("a", "") is False
    assert is_match("a", ".") is True
    assert is_match("a", "a") is True
    assert is_match("abc", "abc") is True
    assert is_match("abc", "a.c") is True
    assert is_match("abc", "ab*c") is True
    assert is_match("ac", "ab*c") is True
    assert is_match("abbc", "ab*c") is True

    # The zero-copies case
    assert is_match("b", "a*b") is True
    assert is_match("aab", "a*b") is True

    # '.*' matches anything
    for s in ["", "a", "abcde", "hello world"]:
        assert is_match(s, ".*") is True

    # Greedy vs non-greedy doesn't matter — we check all partitions
    assert is_match("aaa", "a*a") is True
    assert is_match("aaa", "a*aa") is True

    # Cross-check against Python's `re.fullmatch`
    import re
    import random
    random.seed(42)
    for _ in range(500):
        # Generate a small valid pattern
        alphabet = "abcd"
        p_parts = []
        for _ in range(random.randint(0, 6)):
            ch = random.choice(list(alphabet) + ["."])
            p_parts.append(ch)
            if random.random() < 0.4:
                p_parts.append("*")
        p = "".join(p_parts)
        s = "".join(random.choice(alphabet) for _ in range(random.randint(0, 8)))

        expected = re.fullmatch(p, s) is not None
        got = is_match(s, p)
        assert got == expected, f"mismatch: s={s!r}, p={p!r}: got {got}, expected {expected}"

    print("All tests passed!")
