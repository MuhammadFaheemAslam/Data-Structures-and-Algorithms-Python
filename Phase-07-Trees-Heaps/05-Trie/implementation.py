"""
implementation.py — Trie (prefix tree)

A trie built from dict-backed nodes. Supports insert, search,
starts_with, delete, and prefix enumeration.

---------------------------------------------------
Node layout:

    class TrieNode:
        children: dict[char, TrieNode]
        is_end:   bool

---------------------------------------------------
API:

    t = Trie()
    t.insert("apple")
    t.search("apple")       # True   — full word present
    t.search("app")         # False  — prefix but not a complete word
    t.starts_with("app")    # True
    t.delete("apple")
    list(t.words_with_prefix("app"))    # generator of full words
"""


class TrieNode:
    __slots__ = ("children", "is_end")

    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    """Prefix tree over strings (any hashable 'character' as a key)."""

    def __init__(self):
        self._root = TrieNode()
        self._size = 0                             # number of distinct words

    def __len__(self):
        return self._size

    # ------------------------------------------------------------------
    # Core operations
    # ------------------------------------------------------------------

    def insert(self, word):
        """O(L). Insert `word`. Duplicate is a no-op."""
        node = self._root
        for ch in word:
            nxt = node.children.get(ch)
            if nxt is None:
                nxt = TrieNode()
                node.children[ch] = nxt
            node = nxt
        if not node.is_end:
            node.is_end = True
            self._size += 1

    def search(self, word):
        """O(L). True iff `word` was previously inserted (full-word match)."""
        node = self._find_node(word)
        return node is not None and node.is_end

    def starts_with(self, prefix):
        """O(L). True iff ANY stored word starts with `prefix`."""
        return self._find_node(prefix) is not None

    def _find_node(self, s):
        """Walk the trie; return the node at the end of `s`, or None."""
        node = self._root
        for ch in s:
            nxt = node.children.get(ch)
            if nxt is None:
                return None
            node = nxt
        return node

    # ------------------------------------------------------------------
    # Delete — with dead-branch pruning
    # ------------------------------------------------------------------

    def delete(self, word):
        """
        O(L). Delete `word` from the trie. No-op if absent.

        After unmarking `is_end`, we optionally prune any node that
        has no children and is not an end-mark for another word. This
        keeps the trie compact.
        """
        self._delete(self._root, word, 0)

    def _delete(self, node, word, i):
        """Recursive helper. Returns True if the child pointer to `node` can be pruned."""
        if i == len(word):
            if not node.is_end:
                return False                       # word wasn't here — nothing to do
            node.is_end = False
            self._size -= 1
            # Prune if this node has no children (no other words depend on it)
            return not node.children

        ch = word[i]
        child = node.children.get(ch)
        if child is None:
            return False                           # word not present

        should_prune = self._delete(child, word, i + 1)

        if should_prune:
            del node.children[ch]
            # We can prune ourselves if we're now empty AND we're not a word-end
            return not node.is_end and not node.children

        return False

    # ------------------------------------------------------------------
    # Prefix enumeration
    # ------------------------------------------------------------------

    def words_with_prefix(self, prefix):
        """
        Yield every stored word starting with `prefix`, in lexicographic order.

        Time:  O(L + S) where S is total length of matching words.
        Space: O(L + max_word_length) for the recursion + path buffer.
        """
        start = self._find_node(prefix)
        if start is None:
            return

        buf = list(prefix)

        def dfs(node):
            if node.is_end:
                yield "".join(buf)
            for ch in sorted(node.children):
                buf.append(ch)
                yield from dfs(node.children[ch])
                buf.pop()

        yield from dfs(start)

    # ------------------------------------------------------------------
    # Pythonic-ish interface
    # ------------------------------------------------------------------

    def __contains__(self, word):
        return self.search(word)

    def __iter__(self):
        """Yield every stored word in lexicographic order."""
        yield from self.words_with_prefix("")


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Basics
    t = Trie()
    t.insert("apple")
    assert t.search("apple")
    assert not t.search("app")                     # prefix only, not a full word
    assert t.starts_with("app")
    t.insert("app")
    assert t.search("app")
    assert len(t) == 2

    # Duplicate insert is a no-op
    t.insert("apple")
    assert len(t) == 2

    # Delete
    t.delete("apple")
    assert not t.search("apple")
    assert t.search("app")                         # "app" remains
    assert t.starts_with("app")                    # still prefix for "app" itself
    assert len(t) == 1

    # Delete missing is a no-op
    t.delete("zebra")
    assert len(t) == 1

    # Prefix enumeration
    t = Trie()
    for w in ["car", "cart", "care", "cars", "carry", "cap", "cab", "dog"]:
        t.insert(w)
    assert sorted(t.words_with_prefix("car")) == ["car", "care", "carry", "cars", "cart"]
    assert list(t.words_with_prefix("carr")) == ["carry"]
    assert list(t.words_with_prefix("z")) == []

    # Full iteration in sorted order
    assert list(t) == ["cab", "cap", "car", "care", "carry", "cars", "cart", "dog"]

    # __contains__
    assert "car" in t
    assert "zebra" not in t

    # Stress: compare against a plain Python set
    import random
    random.seed(42)
    words = [
        "".join(random.choice("abcde") for _ in range(random.randint(1, 8)))
        for _ in range(2000)
    ]

    trie = Trie()
    seen = set()
    for w in words:
        trie.insert(w)
        seen.add(w)
    assert len(trie) == len(seen)
    assert set(trie) == seen

    # Random searches
    for _ in range(1000):
        w = "".join(random.choice("abcde") for _ in range(random.randint(1, 10)))
        assert trie.search(w) == (w in seen)

    # starts_with: a prefix is valid iff SOME word in the set begins with it
    for _ in range(500):
        p = "".join(random.choice("abcde") for _ in range(random.randint(1, 5)))
        expected = any(w.startswith(p) for w in seen)
        assert trie.starts_with(p) == expected

    # Random deletions
    for w in random.sample(list(seen), 200):
        trie.delete(w)
        seen.discard(w)
    assert len(trie) == len(seen)
    assert set(trie) == seen

    print("All tests passed!")
