"""
Problem: Number of Islands

Difficulty: Medium (LeetCode #200)

---------------------------------------------------
Problem Statement:

Given an m×n grid of '1' (land) and '0' (water), return the number
of ISLANDS. An island is a maximal group of orthogonally-connected
land cells.

    Input:  [[1,1,0,0,0],
             [1,1,0,0,0],
             [0,0,1,0,0],
             [0,0,0,1,1]]
    Output: 3

---------------------------------------------------
Why This Is A Graph Problem:

The grid IS a graph:
    - Every land cell is a vertex.
    - Two cells are connected iff they're orthogonally adjacent AND
      both are land.

Counting islands = counting connected components of that graph.
We can reuse `connected-components.py`'s algorithm: scan every cell;
when we find unvisited land, BFS/DFS to mark its whole island, then
increment the count.

---------------------------------------------------
Three Implementations:

    1. BFS                                     — classic "flood fill with a queue"
    2. DFS (recursive)                         — shorter code, but watch recursion depth
    3. Union-Find (covered in Phase 10)        — useful if islands can MERGE dynamically

We do BFS and DFS here. Union-Find is in the Phase 10 materials.

---------------------------------------------------
Complexity:

    Time:  O(m·n)     — each cell visited O(1) times
    Space: O(m·n)     — BFS queue / recursion stack in worst case
"""

from collections import deque


# -------- BFS solution --------

def num_islands_bfs(grid):
    """
    Time: O(m·n), Space: O(m·n).

    The grid is MUTATED in place (land → '#') to mark "visited".
    If the caller needs the grid preserved, pass a copy.
    """
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    count = 0

    def bfs(r, c):
        """Mark the entire island containing (r, c) as visited."""
        queue = deque([(r, c)])
        grid[r][c] = "#"
        while queue:
            r, c = queue.popleft()
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1":
                    grid[nr][nc] = "#"
                    queue.append((nr, nc))

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                bfs(r, c)

    return count


# -------- DFS solution --------

def num_islands_dfs(grid):
    """
    Time: O(m·n), Space: O(m·n) — recursion stack.

    Also mutates in place.
    """
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])

    def dfs(r, c):
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] != "1":
            return
        grid[r][c] = "#"
        dfs(r + 1, c); dfs(r - 1, c); dfs(r, c + 1); dfs(r, c - 1)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                dfs(r, c)
    return count


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    def clone(g):
        return [row[:] for row in g]

    # LC examples
    g1 = [
        ["1", "1", "1", "1", "0"],
        ["1", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"],
    ]
    assert num_islands_bfs(clone(g1)) == 1
    assert num_islands_dfs(clone(g1)) == 1

    g2 = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    assert num_islands_bfs(clone(g2)) == 3
    assert num_islands_dfs(clone(g2)) == 3

    # Edge cases
    assert num_islands_bfs([]) == 0
    assert num_islands_bfs([[]]) == 0
    assert num_islands_bfs([["0"]]) == 0
    assert num_islands_bfs([["1"]]) == 1

    # All water
    assert num_islands_bfs([["0"] * 5 for _ in range(5)]) == 0

    # All land: one big island
    assert num_islands_bfs([["1"] * 5 for _ in range(5)]) == 1

    # Diagonals DON'T connect — only orthogonal adjacency counts
    diag = [
        ["1", "0", "1"],
        ["0", "1", "0"],
        ["1", "0", "1"],
    ]
    assert num_islands_bfs(clone(diag)) == 5

    # Randomized cross-check: BFS and DFS must agree
    import random
    random.seed(42)
    for _ in range(200):
        rows = random.randint(1, 15)
        cols = random.randint(1, 15)
        grid = [[random.choice(["0", "1"]) for _ in range(cols)] for _ in range(rows)]
        assert num_islands_bfs(clone(grid)) == num_islands_dfs(clone(grid))

    print("All tests passed!")
