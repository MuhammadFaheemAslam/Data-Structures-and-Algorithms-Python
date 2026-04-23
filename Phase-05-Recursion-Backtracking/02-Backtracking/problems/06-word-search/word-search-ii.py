"""
Problem: Word Search II (Multiple Words via Trie)

Difficulty: Hard (LeetCode #212)

---------------------------------------------------
Problem Statement:

Given an `m × n` board of characters and a list of strings `words`,
return all `words[i]` that can be constructed by walking adjacent
cells (same rules as Word Search I — LC #79).

    board = [...],
    words = ["oath", "pea", "eat", "rain"]
    output = ["oath", "eat"]

---------------------------------------------------
The Naïve Approach (Word Search I for Each Word):

```python
return [w for w in words if word_search_i(board, w)]
```

For k words of length L on an m × n board:
    Time:  O(k · m · n · 4^L)

For k = 1000 and L = 10 on a 12 × 12 board, that's 10^14 —
unusable.

---------------------------------------------------
The Smart Approach: TRIE + ONE DFS

Build a **trie** containing all the words. Then do a single DFS
from each cell, advancing through the trie as we go. When we land
on a trie node that marks the end of a word, record it.

    Time:  O(m · n · 4^L)   — ONE DFS, not k
    Space: O(total characters in words)

The trie approach visits the board once (per starting cell) and
tracks ALL words simultaneously. A single character mismatch
prunes ALL word branches starting with that prefix.

---------------------------------------------------
Building the Trie:

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None            # stores the COMPLETE word at end nodes

root = TrieNode()
for word in words:
    node = root
    for ch in word:
        node = node.children.setdefault(ch, TrieNode())
    node.word = word                 # mark this node as a word's endpoint
```

The `node.word` trick: instead of a boolean "is this a word end?",
store the actual word so we can emit it directly.

---------------------------------------------------
"""


# =========================================================================
# TrieNode
# =========================================================================

class TrieNode:
    __slots__ = ("children", "word")

    def __init__(self):
        self.children = {}
        self.word = None                          # None unless this node ends a word


def build_trie(words):
    """Build a trie rooted at an anonymous TrieNode."""
    root = TrieNode()
    for w in words:
        node = root
        for ch in w:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.word = w
    return root


# =========================================================================
# Word Search II with Trie Pruning
# =========================================================================

def find_words(board, words):
    """
    Return all words in `words` that appear in the board by walking
    adjacent cells (no cell reuse per word).

    Time:  O(m · n · 4^L)
    Space: O(total characters in words)
    """
    if not board or not words:
        return []

    root = build_trie(words)
    m, n = len(board), len(board[0])
    found = set()

    def dfs(r, c, node):
        if not (0 <= r < m and 0 <= c < n):
            return
        ch = board[r][c]
        if ch not in node.children:
            return                                 # trie prune: no word has this prefix

        next_node = node.children[ch]
        if next_node.word is not None:
            found.add(next_node.word)
            # IMPORTANT: don't return — same node could be a prefix of
            # longer words (e.g., "eat" is also a prefix of "eating")
            next_node.word = None                  # optional: avoid re-adding

        # Mark visited
        board[r][c] = "#"
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            dfs(r + dr, c + dc, next_node)
        board[r][c] = ch                           # restore

        # OPTIMIZATION: prune this branch of the trie if it has no more
        # children and isn't a word itself. Saves time on subsequent
        # visits to this cell from other starting positions.
        if not next_node.children and next_node.word is None:
            node.children.pop(ch, None)

    for r in range(m):
        for c in range(n):
            dfs(r, c, root)

    return list(found)


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #212 canonical example
    board = [
        ["o", "a", "a", "n"],
        ["e", "t", "a", "e"],
        ["i", "h", "k", "r"],
        ["i", "f", "l", "v"],
    ]
    words = ["oath", "pea", "eat", "rain"]

    got = find_words([row[:] for row in board], words)
    assert set(got) == {"oath", "eat"}
    print(f"find_words(board, {words}) = {sorted(got)}")
    print()

    # Edge cases
    cases = [
        # (board, words, expected)
        # 2x2 grid: a b
        #           c d
        # Adjacencies: a↔b, a↔c, b↔d, c↔d  (no diagonal a↔d or b↔c)
        ([["a", "b"], ["c", "d"]],
         ["abd", "ab", "abcd"],
         {"ab", "abd"}),                       # "abcd" can't be formed — b and c not adjacent
        ([["a"]],
         ["a"],
         {"a"}),
        ([["a"]],
         ["b"],
         set()),
        ([["a", "a"]],
         ["aa", "aaa"],
         {"aa"}),                                  # "aaa" needs same cell twice
    ]

    for board, words, expected in cases:
        got = set(find_words([row[:] for row in board], words))
        assert got == expected, f"board={board}, words={words}: {got} != {expected}"
        print(f"   find_words(board, {words}) = {sorted(got)}")

    # Performance: large word list on a small board
    import random
    random.seed(42)

    m, n = 6, 6
    board = [[chr(ord("a") + random.randint(0, 3)) for _ in range(n)] for _ in range(m)]

    # Generate 200 random "words" of length 3-5
    words = list({
        "".join(random.choice("abcd") for _ in range(random.randint(3, 5)))
        for _ in range(200)
    })

    import time
    t0 = time.time()
    found = find_words([row[:] for row in board], words)
    elapsed = time.time() - t0
    print(f"\nFound {len(found)} of {len(words)} words on a 6×6 board in {elapsed:.3f}s")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Why the Trie Is the Right Data Structure:
    #
    #   Without a trie:
    #     - Each word search is independent → O(k) separate DFS calls.
    #     - Redundancy: two words sharing a prefix explore the same
    #       grid cells for those shared characters.
    #
    #   With a trie:
    #     - Shared prefixes share trie traversal.
    #     - A single DFS per starting cell covers all words at once.
    #     - Pruning removes dead branches (both grid- and trie-side).
    #
    # This generalizes: whenever you have MANY strings and need to
    # MATCH them against a corpus, a trie + shared traversal is
    # usually the right tool.
    # ---------------------------------------------------------------
