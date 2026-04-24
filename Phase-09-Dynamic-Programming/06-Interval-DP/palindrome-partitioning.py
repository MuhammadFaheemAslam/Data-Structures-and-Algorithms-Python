"""
Problem: Palindrome Partitioning II (Minimum Cuts)

Difficulty: Hard (LeetCode #132)

---------------------------------------------------
Problem Statement:

Given a string `s`, partition it so that every substring of the
partition is a PALINDROME. Return the MINIMUM number of CUTS needed.

Example:
    "aab"    → 1   ("aa" | "b")
    "a"      → 0   (already a palindrome)
    "abacdc" → 1   ("a" | "bacdcb") — wait, "bacdcb" isn't a palindrome.
                   "aba" | "cdc" → 1 cut.

---------------------------------------------------
Two-Layer DP:

### Layer 1 — Palindrome Check (O(n²))

Precompute `is_pal[i][j] = True iff s[i..j] is a palindrome`:

    is_pal[i][j] = (s[i] == s[j]) AND (j - i < 2 OR is_pal[i+1][j-1])

Fill by LENGTH ascending so the diagonal is set before we read from it.

### Layer 2 — Min Cuts (O(n²))

    cuts[i] = min cuts needed for s[:i+1]

    cuts[i] = 0                                       if s[:i+1] is a palindrome
    cuts[i] = min over j in 0..i of:
        cuts[j-1] + 1                                 if s[j..i] is a palindrome

(Use cuts[-1] = -1 sentinel so the "no prior cut" case reduces to
`cuts[j-1] + 1 = 0`.)

---------------------------------------------------
Why Two Layers Not One:

If we did "cuts[i] = 1 + min over j of cuts[j-1] where s[j..i] is pal",
the palindrome check in the inner loop takes O(n) each time. That's
O(n³) total. Precomputing palindromicity once brings us to O(n²).

For n ≤ 2000 (LC's constraint), O(n²) is 4 million ops — tight but
fine. O(n³) = 8 billion, TLE.

---------------------------------------------------
Complexity:

    Time:  O(n²)
    Space: O(n²)  for is_pal;  O(n) for cuts
"""


def min_cuts(s):
    """
    Minimum cuts to partition s into palindromes.

    Time:  O(n²)
    Space: O(n²)
    """
    n = len(s)
    if n <= 1:
        return 0

    # is_pal[i][j] = True iff s[i..j] is a palindrome
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n):
        is_pal[i][i] = True
    for i in range(n - 1):
        is_pal[i][i + 1] = (s[i] == s[i + 1])
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            is_pal[i][j] = (s[i] == s[j]) and is_pal[i + 1][j - 1]

    # cuts[i] = min cuts for s[0..i]
    cuts = [0] * n
    for i in range(n):
        if is_pal[0][i]:
            cuts[i] = 0
            continue
        cuts[i] = i                                 # upper bound: cut after every char
        for j in range(1, i + 1):
            if is_pal[j][i]:
                cuts[i] = min(cuts[i], cuts[j - 1] + 1)

    return cuts[n - 1]


# -------- Alternative: Manacher-like centre expansion to compute is_pal --------

def min_cuts_center_expansion(s):
    """
    Same algorithm but uses center-expansion to build is_pal in O(n²),
    avoiding the DP on is_pal. Slightly cleaner in some presentations.
    """
    n = len(s)
    if n <= 1:
        return 0

    is_pal = [[False] * n for _ in range(n)]
    for center in range(n):
        # Odd-length palindromes centered at `center`
        l, r = center, center
        while l >= 0 and r < n and s[l] == s[r]:
            is_pal[l][r] = True
            l -= 1
            r += 1
        # Even-length palindromes centered between `center` and `center + 1`
        l, r = center, center + 1
        while l >= 0 and r < n and s[l] == s[r]:
            is_pal[l][r] = True
            l -= 1
            r += 1

    cuts = [0] * n
    for i in range(n):
        if is_pal[0][i]:
            cuts[i] = 0
            continue
        cuts[i] = i
        for j in range(1, i + 1):
            if is_pal[j][i]:
                cuts[i] = min(cuts[i], cuts[j - 1] + 1)

    return cuts[n - 1]


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #132 examples
    assert min_cuts("aab") == 1
    assert min_cuts("a") == 0
    assert min_cuts("ab") == 1                              # "a" | "b"
    assert min_cuts("aba") == 0                             # already palindrome
    assert min_cuts("") == 0
    assert min_cuts("abc") == 2                             # "a" | "b" | "c"
    assert min_cuts("aabb") == 1                            # "aa" | "bb"
    assert min_cuts("aabaa") == 0                           # already palindrome
    assert min_cuts("abacdc") == 1                          # "aba" | "cdc"

    # Longer
    assert min_cuts("abbab") == 1                           # "abba" + "b" OR "a" + "bbab"? "abba" | "b"
    assert min_cuts("coder") == 4                           # no palindromes > 1, cut between each

    # Cross-check two approaches
    import random
    random.seed(42)
    for _ in range(200):
        s = "".join(random.choice("abc") for _ in range(random.randint(0, 20)))
        assert min_cuts(s) == min_cuts_center_expansion(s)

    # Brute force: try every partition, count slices, take min cuts = min_slices - 1.
    def brute(s):
        if len(s) <= 1:
            return 0

        def is_palindrome(t):
            return t == t[::-1]

        from functools import cache

        @cache
        def min_slices_from(i):
            """Minimum number of palindrome slices to cover s[i:]."""
            if i == len(s):
                return 0
            best = float("inf")
            for j in range(i + 1, len(s) + 1):
                if is_palindrome(s[i:j]):
                    best = min(best, 1 + min_slices_from(j))
            return best

        return min_slices_from(0) - 1

    for _ in range(100):
        s = "".join(random.choice("ab") for _ in range(random.randint(0, 10)))
        assert min_cuts(s) == brute(s), f"mismatch on {s!r}"

    print("All tests passed!")
