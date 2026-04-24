"""
Problem: Edit Distance (Levenshtein Distance)

Difficulty: Hard (LeetCode #72)

---------------------------------------------------
Problem Statement:

Given two strings `word1` and `word2`, return the minimum number of
OPERATIONS to convert one into the other. Operations are:

    - INSERT a character
    - DELETE a character
    - REPLACE a character

Examples:
    word1 = "horse", word2 = "ros"          → 3
        (horse → rorse → rose → ros)

    word1 = "intention", word2 = "execution" → 5

---------------------------------------------------
The State:

    dp[i][j] = min ops to convert word1[:i] into word2[:j]

Base cases:
    dp[0][j] = j         (insert j chars into empty word1)
    dp[i][0] = i         (delete i chars from word1 to get empty word2)

Transition — three options when advancing:

    if word1[i-1] == word2[j-1]:
        dp[i][j] = dp[i-1][j-1]            # no op needed, just match
    else:
        dp[i][j] = 1 + min(
            dp[i-1][j],                    # DELETE word1[i-1]
            dp[i][j-1],                    # INSERT word2[j-1] into word1
            dp[i-1][j-1]                   # REPLACE word1[i-1] with word2[j-1]
        )

Each edit advances one or both pointers; we take the cheapest.

---------------------------------------------------
Why This Matters:

- SPELL-CHECK & AUTOCORRECT — "what's the closest dictionary word to
  this typo?"
- Bioinformatics — DNA sequence alignment with substitutions/indels.
- `diff` algorithms — LCS and edit distance are inverses in a sense
  (longer common subsequence → fewer edits needed).
- FUZZY SEARCH — ranked by edit distance to the query.

---------------------------------------------------
Complexity:

    Time:  O(m·n)
    Space: O(min(m, n)) with rolling rows
"""


# -------- O(m·n) time, O(m·n) space — tabulated, easier to reason about --------

def edit_distance(word1, word2):
    """
    Min edits to transform word1 into word2.

    Time: O(m·n), Space: O(m·n).
    """
    m, n = len(word1), len(word2)
    # Initialize base cases
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],                  # delete
                    dp[i][j - 1],                  # insert
                    dp[i - 1][j - 1],              # replace
                )
    return dp[m][n]


# -------- O(m·n) time, O(min(m, n)) space --------

def edit_distance_optimized(word1, word2):
    """
    Rolling-row variant. O(min(m, n)) space.
    """
    if len(word1) < len(word2):
        word1, word2 = word2, word1                # keep the shorter one as the rolling dim
    m, n = len(word1), len(word2)

    dp = list(range(n + 1))                        # dp[j] = edit-dist of "" → word2[:j] = j
    for i in range(1, m + 1):
        prev_diag = dp[0]                          # dp[i-1][0]
        dp[0] = i                                  # dp[i][0] = i
        for j in range(1, n + 1):
            temp = dp[j]                           # save dp[i-1][j] before overwriting
            if word1[i - 1] == word2[j - 1]:
                dp[j] = prev_diag
            else:
                dp[j] = 1 + min(dp[j - 1], dp[j], prev_diag)
            prev_diag = temp
    return dp[n]


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #72 examples
    assert edit_distance("horse", "ros") == 3
    assert edit_distance("intention", "execution") == 5

    # Trivial
    assert edit_distance("", "") == 0
    assert edit_distance("abc", "") == 3
    assert edit_distance("", "abc") == 3
    assert edit_distance("abc", "abc") == 0
    assert edit_distance("a", "b") == 1
    assert edit_distance("kitten", "sitting") == 3             # classic Levenshtein example

    # Cross-check optimized vs full
    import random
    random.seed(42)
    for _ in range(200):
        n1 = random.randint(0, 20)
        n2 = random.randint(0, 20)
        w1 = "".join(random.choice("abc") for _ in range(n1))
        w2 = "".join(random.choice("abc") for _ in range(n2))
        assert edit_distance(w1, w2) == edit_distance_optimized(w1, w2)

    # Symmetry: edit_distance(a, b) == edit_distance(b, a)
    for _ in range(100):
        a = "".join(random.choice("abcd") for _ in range(random.randint(0, 10)))
        b = "".join(random.choice("abcd") for _ in range(random.randint(0, 10)))
        assert edit_distance(a, b) == edit_distance(b, a)

    # Triangle inequality: d(a, c) ≤ d(a, b) + d(b, c)
    for _ in range(100):
        a = "".join(random.choice("abc") for _ in range(random.randint(0, 6)))
        b = "".join(random.choice("abc") for _ in range(random.randint(0, 6)))
        c = "".join(random.choice("abc") for _ in range(random.randint(0, 6)))
        assert edit_distance(a, c) <= edit_distance(a, b) + edit_distance(b, c)

    print("All tests passed!")
