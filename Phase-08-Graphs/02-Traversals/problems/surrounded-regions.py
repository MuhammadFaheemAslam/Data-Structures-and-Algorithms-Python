"""
Problem: Surrounded Regions

Difficulty: Medium (LeetCode #130)

---------------------------------------------------
Problem Statement:

Given an m×n board of 'X' and 'O', FLIP every 'O' that is completely
surrounded by 'X' into 'X'. An 'O' is "surrounded" iff its region
does NOT touch the border of the board.

    Before:              After:
    X X X X              X X X X
    X O O X              X X X X
    X X O X              X X X X
    X O X X              X O X X

The bottom-left 'O' is NOT captured because it's on the border.

---------------------------------------------------
The Trick — Think Backwards:

Instead of looking for surrounded regions directly, find the
UN-surrounded ones and mark them SAFE. The UN-surrounded 'O's are
exactly those REACHABLE from a border 'O' via 4-directional moves.

    1. Walk the border. Every 'O' there starts a flood-fill that
       marks every reachable 'O' as safe (use '#' as a sentinel).
    2. After all border flood-fills, every remaining 'O' is
       surrounded. Convert:
           '#' → 'O'   (unsurrounded; restored)
           'O' → 'X'   (surrounded; captured)

Two passes over the grid, each O(m·n).

---------------------------------------------------
Why This "Reverse" Framing Is Powerful:

A direct attack — "find each region, decide if it's surrounded" —
forces you to classify each region AFTER collecting it. The reverse
framing naturally separates the two classes in one pass. The same
trick appears in:

    - "Number of enclaves" (LC #1020)
    - "Pacific Atlantic Water Flow" (LC #417) — do two floods,
      one from each ocean's border, then intersect
    - Many "water on a boundary" grid puzzles

When a problem says "doesn't touch the border", that's your hint
to start FROM the border.

---------------------------------------------------
Complexity:

    Time:  O(m·n)
    Space: O(m·n) — BFS queue or recursion stack in the worst case
"""

from collections import deque


def solve(board):
    """
    Mutates `board` in place per LC #130's contract.

    Time: O(m·n), Space: O(m·n).
    """
    if not board or not board[0]:
        return

    rows, cols = len(board), len(board[0])

    def bfs_from(r, c):
        if board[r][c] != "O":
            return
        queue = deque([(r, c)])
        board[r][c] = "#"
        while queue:
            r, c = queue.popleft()
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == "O":
                    board[nr][nc] = "#"
                    queue.append((nr, nc))

    # Flood-fill from every border 'O'
    for r in range(rows):
        bfs_from(r, 0)
        bfs_from(r, cols - 1)
    for c in range(cols):
        bfs_from(0, c)
        bfs_from(rows - 1, c)

    # Sweep: '#' → 'O', 'O' → 'X'
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == "#":
                board[r][c] = "O"
            elif board[r][c] == "O":
                board[r][c] = "X"


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #130 example
    board = [
        ["X", "X", "X", "X"],
        ["X", "O", "O", "X"],
        ["X", "X", "O", "X"],
        ["X", "O", "X", "X"],
    ]
    solve(board)
    assert board == [
        ["X", "X", "X", "X"],
        ["X", "X", "X", "X"],
        ["X", "X", "X", "X"],
        ["X", "O", "X", "X"],                     # bottom-left 'O' is on border
    ]

    # Trivial cases
    solve([])                                      # empty → no-op
    solve([[]])

    board = [["X"]]
    solve(board)
    assert board == [["X"]]

    board = [["O"]]
    solve(board)
    assert board == [["O"]]                        # single 'O' on border stays

    # All 'O' — nothing is surrounded
    board = [["O"] * 5 for _ in range(5)]
    solve(board)
    assert board == [["O"] * 5 for _ in range(5)]

    # All 'O' EXCEPT border is 'X': inner O's captured
    board = [
        ["X", "X", "X"],
        ["X", "O", "X"],
        ["X", "X", "X"],
    ]
    solve(board)
    assert board == [
        ["X", "X", "X"],
        ["X", "X", "X"],
        ["X", "X", "X"],
    ]

    # Inner region connected to border via a corridor → safe
    board = [
        ["X", "O", "X", "X"],
        ["X", "O", "O", "X"],
        ["X", "X", "O", "X"],
        ["X", "X", "X", "X"],
    ]
    expected = [row[:] for row in board]            # every 'O' reachable from border → unchanged
    solve(board)
    assert board == expected

    # Two regions: one on border (safe), one interior (captured)
    board = [
        ["X", "O", "X", "X", "X"],
        ["X", "X", "X", "O", "X"],
        ["X", "X", "X", "O", "X"],
        ["X", "X", "X", "X", "X"],
    ]
    solve(board)
    assert board == [
        ["X", "O", "X", "X", "X"],
        ["X", "X", "X", "X", "X"],                 # interior O's became X
        ["X", "X", "X", "X", "X"],
        ["X", "X", "X", "X", "X"],
    ]

    # Stress: compare against a brute-force component classifier
    def brute_solve(board):
        if not board or not board[0]:
            return
        rows, cols = len(board), len(board[0])
        # Collect all O-components; check if any cell is on border
        visited = [[False] * cols for _ in range(rows)]
        def bfs(r, c):
            comp = []
            on_border = False
            q = deque([(r, c)])
            visited[r][c] = True
            while q:
                r, c = q.popleft()
                comp.append((r, c))
                if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                    on_border = True
                for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < rows and 0 <= nc < cols and
                            board[nr][nc] == "O" and not visited[nr][nc]):
                        visited[nr][nc] = True
                        q.append((nr, nc))
            return comp, on_border

        for r in range(rows):
            for c in range(cols):
                if board[r][c] == "O" and not visited[r][c]:
                    comp, on_border = bfs(r, c)
                    if not on_border:
                        for rr, cc in comp:
                            board[rr][cc] = "X"

    import random
    random.seed(42)
    for _ in range(100):
        rows = random.randint(1, 8)
        cols = random.randint(1, 8)
        board = [[random.choice(["O", "X"]) for _ in range(cols)] for _ in range(rows)]
        a = [row[:] for row in board]
        b = [row[:] for row in board]
        solve(a)
        brute_solve(b)
        assert a == b, f"mismatch on {board}"

    print("All tests passed!")
