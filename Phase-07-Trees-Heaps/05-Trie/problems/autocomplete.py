"""
Problem: Autocomplete — Top-K Suggestions From A Prefix

Difficulty: Medium (LeetCode #642 / #1268 style)

---------------------------------------------------
Problem Statement:

Design a data structure that supports:

    add(word, frequency)                           — add/update a word's usage frequency
    suggest(prefix) -> list[str]                   — top-k most frequent words starting with `prefix`;
                                                     tiebreak lexicographically; return at most k
                                                     words, or fewer if the trie has fewer matches.

Example:
    a.add("apple", 5)
    a.add("apricot", 2)
    a.add("app", 8)
    a.suggest("ap")  → ["app", "apple", "apricot"]      (k = 3, freqs 8, 5, 2)
    a.suggest("apx") → []                                (no match)

---------------------------------------------------
The Design Choice:

There are two ways to implement this:

    A) Trie + DFS under the prefix node, collecting all (word, freq)
       and picking top-k. O(S + k log S) where S = total matching
       characters. Simple, correct, but slow when the prefix matches
       millions of words.

    B) Trie + per-node INDEX of top-k most frequent descendants.
       Each node stores a pre-sorted list of its top-k subtree words.
       `suggest` becomes O(L + k): walk to prefix, return cached list.

(A) is the interview answer — clear, concise, fits any scale typical
for interviews. (B) is what a production search backend would do, and
shows up in some hard problems (LC #1268).

We implement (A), which is sufficient for LC and shows off trie
enumeration. A hint at how (B) changes the code is at the end of this
file.

---------------------------------------------------
Complexity of (A):

    add:          O(L).
    suggest(p):   O(L + M log k)  — L to walk; M matches to collect; k-heap
                                    pick. M ≤ n (total words).
"""

import heapq


class Autocomplete:
    """Trie-backed autocomplete with (frequency, lexicographic) ordering."""

    def __init__(self, k=3):
        self._root = {}
        self._END = "$"                            # sentinel key for word-end & freq
        self._k = k

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    def add(self, word, frequency=1):
        """Add or update `word`'s frequency. O(L)."""
        node = self._root
        for ch in word:
            if ch not in node:
                node[ch] = {}
            node = node[ch]
        node[self._END] = frequency                # overwrite-or-set

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    def suggest(self, prefix):
        """
        Top-`k` most-frequent words starting with `prefix`; tiebreak lexicographic.

        Time:  O(L + M log k) where M = number of matching words.
        Space: O(M) for collection + O(k) for heap.
        """
        # Walk to prefix node
        node = self._root
        for ch in prefix:
            if ch not in node:
                return []
            node = node[ch]

        # Collect (freq, word) from the subtree
        matches = []
        self._collect(node, list(prefix), matches)

        # Top-k by freq DESC, then lexicographic ASC
        # heapq is a min-heap, so we invert freq to get "top-k largest"
        # Tiebreak: heapq compares tuples element-wise; for ascending-lex
        # ties, we want the SMALLER string first, so keep string as-is.
        return [
            w for _, w in heapq.nsmallest(
                self._k, matches, key=lambda fw: (-fw[0], fw[1])
            )
        ]

    def _collect(self, node, path, out):
        """DFS under `node`, collecting every (freq, word) pair."""
        if self._END in node:
            out.append((node[self._END], "".join(path)))
        for ch in node:
            if ch == self._END:
                continue
            path.append(ch)
            self._collect(node[ch], path, out)
            path.pop()


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Canonical example
    a = Autocomplete(k=3)
    a.add("apple", 5)
    a.add("apricot", 2)
    a.add("app", 8)
    assert a.suggest("ap") == ["app", "apple", "apricot"]
    assert a.suggest("app") == ["app", "apple"]
    assert a.suggest("apx") == []
    assert a.suggest("") == ["app", "apple", "apricot"]

    # Lexicographic tie-break when freq ties
    a = Autocomplete(k=3)
    a.add("alpha", 5)
    a.add("beta", 5)
    a.add("gamma", 5)
    assert a.suggest("") == ["alpha", "beta", "gamma"]

    # Update by re-adding
    a = Autocomplete(k=2)
    a.add("cat", 1)
    a.add("car", 5)
    assert a.suggest("c") == ["car", "cat"]
    a.add("cat", 10)                               # bumped
    assert a.suggest("c") == ["cat", "car"]

    # k larger than matches
    a = Autocomplete(k=10)
    a.add("sun", 1)
    a.add("moon", 1)
    assert sorted(a.suggest("")) == ["moon", "sun"]
    assert len(a.suggest("")) == 2

    # Empty structure
    empty = Autocomplete()
    assert empty.suggest("any") == []
    assert empty.suggest("") == []

    # Stress: a dictionary of random words, correct top-k across random prefixes
    import random
    random.seed(42)
    words_freq = {}
    for _ in range(2000):
        w = "".join(random.choice("abcde") for _ in range(random.randint(1, 6)))
        words_freq[w] = random.randint(1, 100)     # last-write-wins, matches .add semantics

    a = Autocomplete(k=5)
    for w, f in words_freq.items():
        a.add(w, f)

    # Brute-force ground truth
    def brute(prefix):
        matching = [(f, w) for w, f in words_freq.items() if w.startswith(prefix)]
        matching.sort(key=lambda fw: (-fw[0], fw[1]))
        return [w for _, w in matching[:5]]

    for _ in range(500):
        p = "".join(random.choice("abcde") for _ in range(random.randint(0, 4)))
        assert a.suggest(p) == brute(p), f"mismatch on prefix {p!r}"

    print("All tests passed!")

    # ---------------------------------------------------------------
    # The Production Optimization (Approach B):
    #
    #   Add a per-node field `top_k`: a sorted list (by our ordering)
    #   of up to k (freq, word) pairs for the subtree. On `add`, walk
    #   down AND merge the new entry into `top_k` of every node on
    #   the path; bump out the current worst if we exceed k.
    #
    #   `suggest(prefix)` then walks to the prefix node and RETURNS
    #   THAT NODE'S top_k directly: O(L + k).
    #
    #   Overhead per add: O(L · k) instead of O(L). Usually a
    #   worthwhile trade when suggest QPS >> add QPS — i.e. almost
    #   every production autocomplete.
    # ---------------------------------------------------------------
