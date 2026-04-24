"""
space-optimization.py — Rolling Array Technique

Many DP solutions have the form:

    dp[i] = f(dp[i-1], dp[i-2], ...)

If the recurrence only looks back a BOUNDED number of previous
values, we can drop the full `dp[0..n]` array and keep just those
few. This reduces space from O(n) to O(1) without changing time.

The same idea extends to 2D: if `dp[i][j]` only depends on `dp[i-1][*]`
and `dp[i][*]`, we keep only TWO ROWS (or even one, with careful
indexing) — space drops from O(mn) to O(min(m, n)).

This file demonstrates the technique on two problems:

    1. Climb Stairs (1D) — O(n) → O(1) space
    2. Longest Common Subsequence (2D) — O(mn) → O(min(m, n)) space

These patterns recur everywhere. Once you can do this reduction by
reflex, you'll save memory on most DP interviews for free.
"""


# =========================================================================
# 1D example: Climb Stairs
# =========================================================================
# LC #70: How many distinct ways to climb n stairs, taking 1 or 2 steps?
#
#   dp[i] = dp[i-1] + dp[i-2]          (Fibonacci)
#   only depends on the previous 2 values → O(1) space suffices
# =========================================================================

def climb_stairs_full(n):
    """Full tabulation — O(n) space. Plain-vanilla version for comparison."""
    if n <= 2:
        return n
    dp = [0] * (n + 1)
    dp[1], dp[2] = 1, 2
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]


def climb_stairs_rolling(n):
    """Rolling two variables — O(1) space."""
    if n <= 2:
        return n
    a, b = 1, 2                                     # a = ways(i-2), b = ways(i-1)
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b


# =========================================================================
# 2D example: Longest Common Subsequence
# =========================================================================
# LC #1143: length of LCS of two strings.
#
#   dp[i][j] = LCS of s1[:i] and s2[:j]
#   Recurrence:
#      dp[i][j] = dp[i-1][j-1] + 1           if s1[i-1] == s2[j-1]
#               = max(dp[i-1][j], dp[i][j-1])  otherwise
#
#   dp[i][j] only depends on dp[i-1][j-1], dp[i-1][j], dp[i][j-1] — i.e. the
#   CURRENT ROW and the PREVIOUS ROW. Keep just those two rows.
# =========================================================================

def lcs_full(s1, s2):
    """Full DP table — O(mn) time, O(mn) space."""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]


def lcs_two_rows(s1, s2):
    """Two rolling rows — O(mn) time, O(n) space."""
    # Small optimization: make s2 the shorter string so the rolling dim is smaller
    if len(s1) < len(s2):
        s1, s2 = s2, s1
    m, n = len(s1), len(s2)
    prev = [0] * (n + 1)
    curr = [0] * (n + 1)
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev, curr = curr, prev
        # Reset curr (previously prev) to ensure a clean slate for next row.
        # Not strictly required here because we overwrite every cell, but
        # it's a safety net against bugs with sparse overwrites.
    return prev[n]                                  # we swapped, so `prev` holds the final row


def lcs_one_row(s1, s2):
    """
    Single row + one scalar — O(mn) time, O(n) space.

    Uses the insight that within a single row-scan, each cell needs:
        - dp[i-1][j]     = previous-row value at j    (we have this in `dp[j]`)
        - dp[i][j-1]     = current-row value at j-1   (we have this in `dp[j-1]`)
        - dp[i-1][j-1]   = previous-row value at j-1  (we need to remember this!)

    So we keep a scalar `prev_diag` that holds dp[i-1][j-1] as we move left-to-right.

    Same asymptotics as two-rows; trades a bit of code clarity for half the memory.
    """
    if len(s1) < len(s2):
        s1, s2 = s2, s1
    m, n = len(s1), len(s2)
    dp = [0] * (n + 1)
    for i in range(1, m + 1):
        prev_diag = 0                               # dp[i-1][0] = 0
        for j in range(1, n + 1):
            temp = dp[j]                            # save dp[i-1][j] before overwriting
            if s1[i - 1] == s2[j - 1]:
                dp[j] = prev_diag + 1
            else:
                dp[j] = max(dp[j], dp[j - 1])
            prev_diag = temp                        # dp[i-1][j-1] for NEXT j
    return dp[n]


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    import random

    # Climb stairs
    for n in range(0, 30):
        assert climb_stairs_full(n) == climb_stairs_rolling(n)
    # Known values
    assert climb_stairs_rolling(0) == 0
    assert climb_stairs_rolling(1) == 1
    assert climb_stairs_rolling(2) == 2
    assert climb_stairs_rolling(3) == 3
    assert climb_stairs_rolling(4) == 5
    assert climb_stairs_rolling(10) == 89

    # LCS correctness
    cases = [
        ("abcde", "ace", 3),
        ("abc", "abc", 3),
        ("abc", "def", 0),
        ("", "abc", 0),
        ("abc", "", 0),
        ("", "", 0),
        ("ABCBDAB", "BDCAB", 4),                   # classic textbook example
        ("AGGTAB", "GXTXAYB", 4),                   # LCS = GTAB
    ]
    for s1, s2, expected in cases:
        assert lcs_full(s1, s2) == expected
        assert lcs_two_rows(s1, s2) == expected
        assert lcs_one_row(s1, s2) == expected

    # Stress: random strings
    random.seed(42)
    for _ in range(200):
        n1 = random.randint(0, 25)
        n2 = random.randint(0, 25)
        s1 = "".join(random.choice("abc") for _ in range(n1))
        s2 = "".join(random.choice("abc") for _ in range(n2))
        a = lcs_full(s1, s2)
        b = lcs_two_rows(s1, s2)
        c = lcs_one_row(s1, s2)
        assert a == b == c, f"mismatch on s1={s1!r}, s2={s2!r}: {a}, {b}, {c}"

    # Memory demonstration
    import tracemalloc

    # Both versions compute the same thing; observe peak memory.
    m, n = 400, 400
    s1 = "a" * m
    s2 = "a" * n

    tracemalloc.start()
    lcs_full(s1, s2)
    _current, peak_full = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tracemalloc.start()
    lcs_one_row(s1, s2)
    _current, peak_one = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"LCS on {m}×{n} strings:")
    print(f"   full table:      peak {peak_full / 1024:7.1f} KiB")
    print(f"   one-row:         peak {peak_one / 1024:7.1f} KiB")
    print(f"   reduction: {peak_full / peak_one:.1f}×")

    print("\nAll tests passed!")
