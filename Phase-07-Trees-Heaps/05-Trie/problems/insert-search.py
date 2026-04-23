"""
Problem: Implement Trie (Prefix Tree)

Difficulty: Medium (LeetCode #208)

---------------------------------------------------
Problem Statement:

Implement a Trie class with these three operations:

    insert(word)
    search(word)          → True iff `word` was inserted
    startsWith(prefix)    → True iff ANY inserted word starts with `prefix`

This is the minimum-viable trie — no delete, no enumeration — and it's
frequently used as a LEAD-IN to harder trie problems.

---------------------------------------------------
Why The `is_end` Flag Is Essential:

Consider inserting "apple" but NOT "app". After insertion, the path
`a → p → p` exists in the tree (because "apple" passes through those
nodes). Without an `is_end` flag, you can't distinguish:

    search("app")      → should be FALSE   (never inserted)
    startsWith("app")  → should be TRUE    (prefix of "apple")

The flag lets search return true ONLY when we land on an `is_end` node.

---------------------------------------------------
The Follow-Up (LC #211 — Add and Search Word):

Same problem but `search` accepts wildcards `'.'` that match any
character. The wildcard is solved with DFS: at a `'.'`, recurse into
EVERY child of the current node. O(26^L) worst case but fast in
practice because only the active branches are explored.

We include `MagicDictionary` at the bottom as a similar variant.

---------------------------------------------------
Complexity (for LC #208):

    insert:      O(L)
    search:      O(L)
    startsWith:  O(L)

L = length of the word or prefix.
"""


class Trie:
    """Minimum-viable LC #208 implementation."""

    def __init__(self):
        self._root = {}
        # Sentinel key inside a node to mark "a word ends here".
        # Using a dict-as-node avoids the class-per-node overhead.
        self._END = "$"

    def insert(self, word):
        """O(L)."""
        node = self._root
        for ch in word:
            if ch not in node:
                node[ch] = {}
            node = node[ch]
        node[self._END] = True

    def search(self, word):
        """O(L). True iff `word` was inserted."""
        node = self._walk(word)
        return node is not None and self._END in node

    def starts_with(self, prefix):
        """O(L). True iff some inserted word starts with `prefix`."""
        return self._walk(prefix) is not None

    def _walk(self, s):
        node = self._root
        for ch in s:
            if ch not in node:
                return None
            node = node[ch]
        return node


# =========================================================================
# LC #211 — Add and Search with wildcards
# =========================================================================

class WordDictionary:
    """
    LC #211. Same shape as Trie, but `search` supports `.` wildcard.

    Time:  insert O(L), search O(26^L) worst-case (only one `.`? O(26·L)).
    Space: O(Σ|words|).
    """

    def __init__(self):
        self._root = {}
        self._END = "$"

    def add_word(self, word):
        node = self._root
        for ch in word:
            if ch not in node:
                node[ch] = {}
            node = node[ch]
        node[self._END] = True

    def search(self, word):
        return self._dfs(self._root, word, 0)

    def _dfs(self, node, word, i):
        if i == len(word):
            return self._END in node
        ch = word[i]
        if ch == ".":
            # Try every child
            return any(
                self._dfs(child, word, i + 1)
                for key, child in node.items()
                if key != self._END
            )
        if ch not in node:
            return False
        return self._dfs(node[ch], word, i + 1)


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #208 example
    t = Trie()
    t.insert("apple")
    assert t.search("apple") is True
    assert t.search("app") is False
    assert t.starts_with("app") is True
    t.insert("app")
    assert t.search("app") is True

    # Edge cases
    t2 = Trie()
    t2.insert("")                                  # empty word — marks root as end
    assert t2.search("") is True
    assert t2.starts_with("") is True

    t3 = Trie()
    assert t3.search("anything") is False
    assert t3.starts_with("") is True              # empty prefix always matches

    # LC #211 example
    wd = WordDictionary()
    wd.add_word("bad")
    wd.add_word("dad")
    wd.add_word("mad")
    assert wd.search("pad") is False
    assert wd.search("bad") is True
    assert wd.search(".ad") is True                # matches bad/dad/mad
    assert wd.search("b..") is True                # bad
    assert wd.search("..") is False                # no 2-letter words
    assert wd.search("...") is True
    assert wd.search("....") is False

    # Stress: WordDictionary with mixed adds and wildcard searches
    import random
    random.seed(42)
    wd = WordDictionary()
    words = set()
    for _ in range(500):
        w = "".join(random.choice("abc") for _ in range(random.randint(1, 5)))
        wd.add_word(w)
        words.add(w)

    # Exact search must match membership
    for _ in range(500):
        q = "".join(random.choice("abc") for _ in range(random.randint(1, 5)))
        assert wd.search(q) == (q in words)

    # Wildcard search: answer is True iff any stored word matches the pattern
    for _ in range(500):
        q = "".join(random.choice("abc.") for _ in range(random.randint(1, 5)))
        expected = any(len(w) == len(q) and all(qc == "." or qc == wc
                                                 for qc, wc in zip(q, w))
                        for w in words)
        assert wd.search(q) == expected, f"wildcard search failed on {q!r}"

    print("All tests passed!")
