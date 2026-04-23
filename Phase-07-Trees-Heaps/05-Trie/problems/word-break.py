"""
Problem: Word Break

Difficulty: Medium (LeetCode #139)

---------------------------------------------------
Problem Statement:

Given a string `s` and a dictionary `words`, return True iff `s` can
be SEGMENTED into a space-separated sequence of one or more dictionary
words. Words may be reused.

Example:
    s = "applepenapple", words = ["apple", "pen"] → True
    s = "catsandog", words = ["cats","dog","sand","and","cat"] → False

---------------------------------------------------
Why Trie + DP Together?

The natural formulation is DP:

    dp[i] = True iff s[0..i] can be segmented.
    dp[0] = True.
    dp[i] = OR over all j < i of (dp[j] AND s[j..i] in words).

With a SET for dictionary lookup, the inner check is O(L) per substring
(hashing). Total: O(n² · L).

With a TRIE, you can REUSE the trie walk for every starting position.
From position j, walk the trie through s[j], s[j+1], ...; at each
`is_end` you hit, mark `dp[j + depth]` as True. Visits each character
at most once per starting position. Overall O(n²) — a factor of L
saved on the common-prefix case.

For short inputs the difference is negligible; for long strings with
many overlapping dictionary prefixes, the trie version is noticeably
faster.

---------------------------------------------------
Two Approaches Below:

    1. Plain DP with a `set` dictionary.         Simpler.
    2. DP with a TRIE.                            Demonstrates the speedup.

Both return True/False. Constructing the actual segmentation (LC #140
"Word Break II") requires remembering predecessors and reconstructing.
"""

# -------- Solution 1: set + DP --------

def word_break_set(s, words):
    """
    Time:  O(n² · L_avg) (n = len(s), L_avg = avg dict-word length during hashing).
    Space: O(n) for DP, O(Σ|words|) for the set.
    """
    word_set = set(words)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    max_len = max((len(w) for w in words), default=0)

    for i in range(1, n + 1):
        # Only check substrings ending at i with length ≤ max_len
        lo = max(0, i - max_len)
        for j in range(lo, i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    return dp[n]


# -------- Solution 2: trie + DP --------

class _TrieNode:
    __slots__ = ("children", "is_end")

    def __init__(self):
        self.children = {}
        self.is_end = False


def _build_trie(words):
    root = _TrieNode()
    for w in words:
        node = root
        for ch in w:
            if ch not in node.children:
                node.children[ch] = _TrieNode()
            node = node.children[ch]
        node.is_end = True
    return root


def word_break_trie(s, words):
    """
    For each reachable position j (dp[j] == True), walk the TRIE from j
    through s[j], s[j+1], ...; whenever we hit an `is_end`, mark that
    endpoint in dp.

    Time:  O(n²) worst case.
    Space: O(Σ|words|) for trie + O(n) for dp.
    """
    n = len(s)
    if n == 0:
        return True
    root = _build_trie(words)

    dp = [False] * (n + 1)
    dp[0] = True

    for j in range(n):
        if not dp[j]:
            continue
        node = root
        k = j
        while k < n and s[k] in node.children:
            node = node.children[s[k]]
            k += 1
            if node.is_end:
                dp[k] = True

    return dp[n]


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    cases = [
        ("leetcode", ["leet", "code"], True),
        ("applepenapple", ["apple", "pen"], True),
        ("catsandog", ["cats", "dog", "sand", "and", "cat"], False),
        ("", ["any", "thing"], True),                              # empty string trivially breakable
        ("aaa", ["a"], True),
        ("aaa", ["aa"], False),                                    # can't segment odd length with pieces of size 2
        ("aaaaaaa", ["aaaa", "aa"], False),                         # 7 isn't 4+anything-of-2s
        ("aaaaaaaa", ["aaaa", "aa"], True),                         # 8 = 4+4 or 2+2+2+2 or 4+2+2 etc.
        ("a" * 50, ["a"], True),
        ("aaaaaaaaaaaaab", ["a", "aa", "aaa"], False),              # no way to end with 'b'
    ]

    for s, words, expected in cases:
        assert word_break_set(s, words) == expected, f"set failed on ({s!r}, {words})"
        assert word_break_trie(s, words) == expected, f"trie failed on ({s!r}, {words})"

    # Stress: random inputs compared across the two solutions
    import random
    random.seed(42)
    for _ in range(200):
        words = ["".join(random.choice("abc") for _ in range(random.randint(1, 3)))
                  for _ in range(random.randint(1, 6))]
        s = "".join(random.choice("abc") for _ in range(random.randint(0, 20)))
        assert word_break_set(s, words) == word_break_trie(s, words), (
            f"disagreement: s={s!r}, words={words}"
        )

    # Timing: trie wins for many overlapping dict words
    import time

    # A pathological-ish input for the set version: worst-case n² substring lookups
    s = "a" * 150 + "b"
    words = ["a" * k for k in range(1, 20)]        # overlapping prefixes
    for solver in (word_break_set, word_break_trie):
        t0 = time.time()
        for _ in range(100):
            solver(s, words)
        elapsed = time.time() - t0
        print(f"   {solver.__name__:<20}: {elapsed * 1000:6.1f} ms  (100 runs)")

    print("\nAll tests passed!")
