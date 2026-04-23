"""
Problem: Word Search (Single Word)

Difficulty: Medium (LeetCode #79)

---------------------------------------------------
Problem Statement:

Given an `m × n` grid of characters and a string `word`, return
True iff `word` can be constructed by WALKING adjacent cells of
the grid, where "adjacent" means horizontally or vertically
neighbouring (no diagonals). The same cell may not be used more
than once.

    grid = [["A","B","C","E"],
            ["S","F","C","S"],
            ["A","D","E","E"]]

    word = "ABCCED"     → True   (walk A → B → C → C → E → D)
    word = "SEE"        → True
    word = "ABCB"       → False  (no way to avoid revisiting B)

---------------------------------------------------
Why This Is a Backtracking Problem:

At each cell, we have up to 4 choices (N, S, E, W). We'd like to
FILTER those choices by which ones match the next character of
`word`, and we'd like to PRUNE paths that visit already-used cells.
That's backtracking.

The interesting twist: we need to MARK cells as visited during
exploration and UNMARK them on the way back up — a textbook
apply/revert pair.

---------------------------------------------------
The Template:

    for each starting cell:
        if dfs(r, c, word_index=0):
            return True
    return False

    def dfs(r, c, word_index):
        if word_index == len(word):
            return True

        if out_of_bounds(r, c) or grid[r][c] != word[word_index]:
            return False

        saved = grid[r][c]
        grid[r][c] = "#"                         # mark visited (in place)

        for each neighbour (nr, nc):
            if dfs(nr, nc, word_index + 1):
                return True

        grid[r][c] = saved                       # unmark
        return False

The "mark in place by overwriting" trick avoids needing a separate
`visited` set — saving O(m · n) memory. We restore on the way back
up, so the grid is unchanged when the function returns.

---------------------------------------------------
Time:   O(m · n · 4^L) where L = len(word)
Space:  O(L) recursion stack
"""


# =========================================================================
# Solution: Backtracking with In-Place Visited Marking
# =========================================================================

def exists(board, word):
    """
    True iff `word` can be constructed by walking adjacent cells.

    Time:  O(m · n · 4^L) where L = len(word)
    Space: O(L) recursion stack
    """
    if not board or not word:
        return False

    m, n = len(board), len(board[0])

    def dfs(r, c, i):
        # i = index in `word` that we're trying to match at (r, c)
        if i == len(word):
            return True

        # Bounds + character check
        if not (0 <= r < m and 0 <= c < n):
            return False
        if board[r][c] != word[i]:
            return False

        # CHOOSE: mark this cell as visited by overwriting
        saved = board[r][c]
        board[r][c] = "#"                         # sentinel; not a valid grid char

        # EXPLORE: try each of the four neighbors
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if dfs(r + dr, c + dc, i + 1):
                board[r][c] = saved               # must restore BEFORE returning
                return True

        # UN-CHOOSE: restore the cell
        board[r][c] = saved
        return False

    # Try every cell as the start
    for r in range(m):
        for c in range(n):
            if dfs(r, c, 0):
                return True
    return False


# =========================================================================
# Alternative: Using a Visited Set
# =========================================================================

def exists_with_visited(board, word):
    """
    Same algorithm, but uses a `visited` set instead of in-place
    marking. Doesn't mutate the board.

    Time:  same O(m · n · 4^L)
    Space: O(L) for visited + O(L) stack
    """
    if not board or not word:
        return False

    m, n = len(board), len(board[0])
    visited = set()

    def dfs(r, c, i):
        if i == len(word):
            return True
        if not (0 <= r < m and 0 <= c < n):
            return False
        if (r, c) in visited:
            return False
        if board[r][c] != word[i]:
            return False

        visited.add((r, c))
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if dfs(r + dr, c + dc, i + 1):
                visited.remove((r, c))
                return True
        visited.remove((r, c))
        return False

    for r in range(m):
        for c in range(n):
            if dfs(r, c, 0):
                return True
    return False


# =========================================================================
# Pruning: Skip If the Word Has Characters Not in the Grid
# =========================================================================

def exists_with_pruning(board, word):
    """
    Same algorithm with an early-exit optimization: if ANY letter
    in `word` doesn't appear anywhere in the grid, no match is
    possible — return False immediately.

    Also: if the first letter of `word` is RARER in the grid than
    the last letter, REVERSE `word` before searching. Starting from
    rarer cells reduces the number of starting positions.

    These small heuristics can yield 10× speedups on adversarial inputs.
    """
    if not board or not word:
        return False

    from collections import Counter

    # Count grid characters
    grid_count = Counter(c for row in board for c in row)

    # Early exit: word contains a character not in grid
    for c in word:
        if c not in grid_count:
            return False
        if Counter(word)[c] > grid_count[c]:      # word needs more of c than grid has
            return False

    # Reverse `word` if its first letter is more common than its last
    if grid_count[word[0]] > grid_count[word[-1]]:
        word = word[::-1]

    return exists(board, word)


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #79 canonical example
    board = [["A", "B", "C", "E"],
             ["S", "F", "C", "S"],
             ["A", "D", "E", "E"]]

    cases = [
        ("ABCCED",  True),
        ("SEE",     True),
        ("ABCB",    False),
        ("A",       True),
        ("Z",       False),
        ("ADEES",   True),
        ("",        False),                        # empty word → convention: False
    ]

    for word, expected in cases:
        b = [row[:] for row in board]              # fresh copy per test (exists mutates)
        got = exists(b, word)
        # Verify board is restored
        assert b == board, f"board not restored after searching {word!r}"
        assert got == expected, f"exists({word!r}) = {got}, expected {expected}"
        print(f"   exists(board, {word!r}) = {got}")
    print()

    # Verify the other two implementations agree
    for word, expected in cases:
        b1 = [row[:] for row in board]
        b2 = [row[:] for row in board]
        b3 = [row[:] for row in board]

        a = exists(b1, word)
        b = exists_with_visited(b2, word)
        c = exists_with_pruning(b3, word)
        assert a == b == c == expected

    print("All three implementations agree on the test set.")

    # Larger stress test
    import random
    random.seed(42)
    for _ in range(50):
        m = random.randint(1, 5)
        n = random.randint(1, 5)
        grid = [[random.choice("ABC") for _ in range(n)] for _ in range(m)]
        word_len = random.randint(0, 8)
        word = "".join(random.choice("ABCD") for _ in range(word_len))

        g1 = [row[:] for row in grid]
        g2 = [row[:] for row in grid]
        a = exists(g1, word)
        b = exists_with_visited(g2, word)
        assert a == b, f"mismatch on grid={grid}, word={word!r}"

    print("\nStress test: 50 random boards — in-place and set-based implementations agree")

    print("\nAll tests passed!")
