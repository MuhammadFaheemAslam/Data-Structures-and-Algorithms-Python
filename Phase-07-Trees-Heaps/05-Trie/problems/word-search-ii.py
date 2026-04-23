"""
Problem: Word Search II

Difficulty: Hard (LeetCode #212)

---------------------------------------------------
Problem Statement:

Given an m×n board of characters and a list of target words, return
all words that can be formed by tracing a path on the board where:

    - each letter is visited at most once per word;
    - moves are to the 4 orthogonal neighbours;
    - consecutive letters on the path spell out the target word.

Example:
    board = [
        ['o','a','a','n'],
        ['e','t','a','e'],
        ['i','h','k','r'],
        ['i','f','l','v']
    ]
    words = ["oath","pea","eat","rain"]
    → ["oath", "eat"]                              (pea and rain aren't on the board)

---------------------------------------------------
Why This Is A Trie Problem:

Naïve solution — DFS from each board cell for EACH target word —
is O(W · m · n · 4^L) where W = number of words, L = max length.
With many words, the 4^L search is repeated W times.

Better — BUILD A TRIE of all target words, then do ONE DFS from each
cell, walking the trie in lock-step with the board. When we reach a
trie node marked `is_end`, we've found a word. PRUNE: if a board
character isn't in the current trie node's children, bail early.

This turns "W · 4^L" into "one 4^L search that finds ALL words".

---------------------------------------------------
Additional optimizations:

1. STORE THE WORD on the `is_end` node (or replace the flag with the
   word string). Saves reconstructing it when we find a match.

2. DELETE found words from the trie. Prevents duplicate reports AND
   reduces the search space for the remaining DFS.

3. PRUNE DEAD BRANCHES after deletion. If a node has no children AND
   isn't an end-mark, it serves no purpose — remove it from its
   parent. This is the "leaf pruning" step that keeps the trie tight.

Together these earn the "fastest LC #212 submission" tier.

---------------------------------------------------
Complexity:

    Time:  O(m · n · 4^L) — bounded by total DFS exploration.
    Space: O(Σ|words|) for the trie + O(L) recursion.
"""


def find_words(board, words):
    """
    Return every word in `words` that can be traced on `board`.

    Time:  O(m·n · 4^L), Space: O(Σ|words|).
    """
    if not board or not words:
        return []

    # Build a trie. Store the WHOLE WORD at the end-node so we can report it
    # without having to reconstruct it from the DFS state.
    root = {}
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = w

    rows, cols = len(board), len(board[0])
    found = []

    def dfs(r, c, parent):
        ch = board[r][c]
        node = parent.get(ch)
        if node is None:
            return

        # Found a word?
        matched = node.pop("$", None)
        if matched is not None:
            found.append(matched)

        # Mark cell visited by mutating the board
        board[r][c] = "#"

        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != "#":
                dfs(nr, nc, node)

        # Restore cell
        board[r][c] = ch

        # Prune: if the child is empty, remove it from its parent
        if not node:
            parent.pop(ch, None)

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, root)

    return found


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #212 example
    board = [
        ['o', 'a', 'a', 'n'],
        ['e', 't', 'a', 'e'],
        ['i', 'h', 'k', 'r'],
        ['i', 'f', 'l', 'v']
    ]
    words = ["oath", "pea", "eat", "rain"]
    assert sorted(find_words([row[:] for row in board], words)) == ["eat", "oath"]

    # Smaller cases
    assert find_words([["a", "b"], ["c", "d"]], ["abcd"]) == []  # need adjacency
    assert find_words([["a", "b"], ["c", "d"]], ["acdb"]) == ["acdb"]
    assert find_words([["a"]], ["a"]) == ["a"]
    assert find_words([["a"]], ["b"]) == []
    assert find_words([], ["any"]) == []
    assert find_words([["a", "b"]], []) == []

    # Can't reuse a cell
    assert find_words([["a", "b"]], ["aba"]) == []              # can't step back

    # Same word once even if findable multiple ways
    board = [["a", "a"], ["a", "a"]]
    words = ["aaaa"]                                              # 4-cell cycle path exists
    result = find_words([row[:] for row in board], words)
    assert result == ["aaaa"]

    # Different word forms — each returned once
    board = [
        ["a", "b", "c"],
        ["a", "e", "d"],
        ["a", "f", "g"],
    ]
    words = ["abe", "cde", "fed", "abcd"]
    result = sorted(find_words([row[:] for row in board], words))
    # abe: a(0,0)→b(0,1)→e(1,1) ✓
    # cde: c(0,2)→d(1,2)→e(1,1) ✓
    # fed: f(2,1)→e(1,1)→d(1,2) ✓
    # abcd: a(0,0)→b(0,1)→c(0,2)→d(1,2) ✓
    assert result == sorted(["abe", "cde", "fed", "abcd"])

    # Stress: compare against a correct-but-slow reference
    def brute_find_words(board, words):
        rows = len(board)
        cols = len(board[0]) if board else 0
        found = []
        for w in words:
            if brute_in_board(board, w, rows, cols):
                found.append(w)
        return found

    def brute_in_board(board, word, rows, cols):
        visited = set()
        def dfs(r, c, i):
            if i == len(word):
                return True
            if (r, c) in visited or not (0 <= r < rows and 0 <= c < cols):
                return False
            if board[r][c] != word[i]:
                return False
            visited.add((r, c))
            found = any(dfs(r + dr, c + dc, i + 1) for dr, dc in ((-1,0),(1,0),(0,-1),(0,1)))
            visited.remove((r, c))
            return found
        return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))

    import random
    random.seed(42)
    for _ in range(50):
        rows = random.randint(1, 4)
        cols = random.randint(1, 4)
        board = [[random.choice("abcd") for _ in range(cols)] for _ in range(rows)]
        words = []
        for _ in range(random.randint(1, 5)):
            L = random.randint(1, 6)
            words.append("".join(random.choice("abcd") for _ in range(L)))

        fast = sorted(find_words([row[:] for row in board], words))
        slow = sorted(brute_find_words(board, words))
        # Remove duplicates in slow (brute checks each word; fast already dedupes)
        slow = sorted(set(slow))
        fast = sorted(set(fast))
        assert fast == slow, f"mismatch: board={board}, words={words}"

    print("All tests passed!")
