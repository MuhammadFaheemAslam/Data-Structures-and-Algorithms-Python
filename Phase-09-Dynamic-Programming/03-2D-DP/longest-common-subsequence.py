"""
Problem: Longest Common Subsequence

Difficulty: Medium (LeetCode #1143)

---------------------------------------------------
Problem Statement:

Given two strings `s1` and `s2`, find the length of their longest
COMMON SUBSEQUENCE. A subsequence drops characters without changing
relative order (no contiguity required).

Example:
    s1 = "abcde", s2 = "ace" → 3           (LCS = "ace")
    s1 = "abc",   s2 = "abc" → 3           (equal)
    s1 = "abc",   s2 = "def" → 0

---------------------------------------------------
The State:

    dp[i][j] = LCS length of s1[:i] and s2[:j]

Base: `dp[0][*] = dp[*][0] = 0` (empty string has no LCS with anything).

Transition:
    if s1[i-1] == s2[j-1]:   dp[i][j] = dp[i-1][j-1] + 1
    else:                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])

Intuition: when the current characters match, extend the LCS of the
shorter prefixes. Otherwise, skip one character from either string
and take the larger LCS.

---------------------------------------------------
Reconstructing The Subsequence:

After filling `dp`, walk BACKWARDS from (m, n) to (0, 0):
    - If s1[i-1] == s2[j-1]: append that char, move to (i-1, j-1).
    - Else move to whichever neighbour (i-1, j) or (i, j-1) has the
      larger dp.

Reverse the collected chars to get the LCS.

---------------------------------------------------
Applications:

- `diff` — line-level LCS of two files identifies unchanged lines.
- Version control (git diff, SVN diff, patch generation).
- Bioinformatics — DNA/protein sequence alignment.
- Plagiarism detection, spell-check suggestions.

---------------------------------------------------
Complexity:

    Time:  O(m·n)
    Space: O(min(m, n)) with rolling rows (space-opt version)
           O(m·n) if you need to RECONSTRUCT the actual LCS string
"""


# -------- O(m·n) time, O(m·n) space — with reconstruction --------

def lcs_length(s1, s2):
    """
    Length of LCS of s1 and s2. O(m·n) time and space.
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]


def lcs_string(s1, s2):
    """
    Return one LCS of s1 and s2 as a string. There may be multiple
    LCS's of the same length; we return whichever the backtracking finds.

    Time: O(m·n), Space: O(m·n) (the full dp table is needed to backtrack).
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Reconstruct
    out = []
    i, j = m, n
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            out.append(s1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(out))


# -------- O(m·n) time, O(min(m, n)) space — LC submission version --------

def lcs_length_optimized(s1, s2):
    """
    Only length, not the string. O(min(m, n)) space via rolling row.
    """
    if len(s1) < len(s2):
        s1, s2 = s2, s1
    m, n = len(s1), len(s2)

    dp = [0] * (n + 1)
    for i in range(1, m + 1):
        prev_diag = 0                              # dp[i-1][0]
        for j in range(1, n + 1):
            temp = dp[j]                           # save dp[i-1][j]
            if s1[i - 1] == s2[j - 1]:
                dp[j] = prev_diag + 1
            else:
                dp[j] = max(dp[j], dp[j - 1])
            prev_diag = temp
    return dp[n]


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #1143 examples
    assert lcs_length("abcde", "ace") == 3
    assert lcs_length("abc", "abc") == 3
    assert lcs_length("abc", "def") == 0

    # Classic textbook examples
    assert lcs_length("ABCBDAB", "BDCAB") == 4                  # BDAB or BCAB
    assert lcs_length("AGGTAB", "GXTXAYB") == 4                 # GTAB

    # Empty inputs
    assert lcs_length("", "") == 0
    assert lcs_length("abc", "") == 0
    assert lcs_length("", "abc") == 0

    # Reconstruction is VALID: every returned LCS is a subseq of both
    def is_subseq(t, s):
        i = 0
        for ch in s:
            if i < len(t) and ch == t[i]:
                i += 1
        return i == len(t)

    import random
    random.seed(42)
    for _ in range(200):
        n1 = random.randint(0, 20)
        n2 = random.randint(0, 20)
        s1 = "".join(random.choice("abc") for _ in range(n1))
        s2 = "".join(random.choice("abc") for _ in range(n2))

        length = lcs_length(s1, s2)
        optimized = lcs_length_optimized(s1, s2)
        got_str = lcs_string(s1, s2)

        assert length == optimized
        assert len(got_str) == length
        assert is_subseq(got_str, s1)
        assert is_subseq(got_str, s2)

    # Brute: enumerate every subsequence of s1 (only for tiny inputs)
    def brute(s1, s2):
        best = 0
        for mask in range(1 << len(s1)):
            sub = "".join(s1[i] for i in range(len(s1)) if (mask >> i) & 1)
            if is_subseq(sub, s2):
                best = max(best, len(sub))
        return best

    for _ in range(50):
        s1 = "".join(random.choice("ab") for _ in range(random.randint(0, 10)))
        s2 = "".join(random.choice("ab") for _ in range(random.randint(0, 10)))
        assert lcs_length(s1, s2) == brute(s1, s2)

    print("All tests passed!")
