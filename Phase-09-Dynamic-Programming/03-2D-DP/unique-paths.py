"""
Problem: Unique Paths (I and II)

Difficulty:
    Medium (LeetCode #62 — unobstructed grid)
    Medium (LeetCode #63 — with obstacles)

---------------------------------------------------
Problem Statement:

A robot starts at the top-left of an m×n grid, can move only RIGHT
or DOWN, and wants to reach the bottom-right. How many distinct
paths?

    LC #62: empty grid.
    LC #63: some cells are obstacles (1s), which cannot be passed.

Examples:
    LC #62:  m=3, n=7 → 28
    LC #63:  [[0,0,0], [0,1,0], [0,0,0]] → 2

---------------------------------------------------
LC #62 — Direct Recurrence:

    dp[i][j] = dp[i-1][j] + dp[i][j-1]

Each cell is reached from either above or from the left. Base case:
`dp[0][*]` and `dp[*][0]` are all 1 (only one way — keep going
right or down).

This is a classic 2D tabulation. Space can be reduced to O(n) by
keeping only one row — we show this below.

LC #62 also has a CLOSED-FORM solution: C(m+n-2, m-1) — the number
of ways to arrange (m-1) downs and (n-1) rights. But DP is what's
asked here, and we compute it anyway for cross-checking.

---------------------------------------------------
LC #63 — With Obstacles:

Same recurrence, but `dp[i][j] = 0` if the cell is an obstacle.
Requires careful handling of the first row/col: once we hit an
obstacle, everything after it in that row/col is unreachable.

---------------------------------------------------
Complexity:

    Time:  O(m·n)
    Space: O(min(m, n)) with the rolling-row optimization
"""

import math


# -------- LC #62: unique paths (no obstacles) --------

def unique_paths(m, n):
    """
    Count distinct paths from top-left to bottom-right, RIGHT/DOWN only.

    Time:  O(m·n), Space: O(min(m, n)).
    """
    if m < n:
        m, n = n, m                                 # roll the smaller dimension
    dp = [1] * n                                    # first row: all 1s
    for _ in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j - 1]
    return dp[-1]


# -------- LC #62 bonus: closed-form via binomial --------

def unique_paths_combinatorial(m, n):
    """C(m+n-2, m-1). O(min(m, n)) with math.comb (which is itself O(k))."""
    return math.comb(m + n - 2, m - 1)


# -------- LC #63: with obstacles --------

def unique_paths_with_obstacles(obstacleGrid):
    """
    Count paths avoiding cells where grid[i][j] == 1.

    Time:  O(m·n), Space: O(n).
    """
    if not obstacleGrid or not obstacleGrid[0]:
        return 0

    m, n = len(obstacleGrid), len(obstacleGrid[0])
    if obstacleGrid[0][0] == 1:
        return 0

    dp = [0] * n
    dp[0] = 1
    for i in range(m):
        for j in range(n):
            if obstacleGrid[i][j] == 1:
                dp[j] = 0
            elif j > 0:
                dp[j] += dp[j - 1]
            # j == 0: dp[0] carries forward from previous row, already correct
    return dp[-1]


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #62 examples
    assert unique_paths(3, 7) == 28
    assert unique_paths(3, 2) == 3
    assert unique_paths(7, 3) == 28                             # symmetric
    assert unique_paths(1, 1) == 1
    assert unique_paths(1, 10) == 1                              # one row, one path
    assert unique_paths(10, 1) == 1
    assert unique_paths(3, 3) == 6                              # DR, DR, RD, RR, ...

    # Cross-check with closed form
    import random
    random.seed(42)
    for _ in range(50):
        m, n = random.randint(1, 20), random.randint(1, 20)
        assert unique_paths(m, n) == unique_paths_combinatorial(m, n)

    # LC #63 examples
    assert unique_paths_with_obstacles([[0, 0, 0], [0, 1, 0], [0, 0, 0]]) == 2
    assert unique_paths_with_obstacles([[0, 1], [0, 0]]) == 1
    assert unique_paths_with_obstacles([[1, 0]]) == 0            # start blocked
    assert unique_paths_with_obstacles([[0, 1]]) == 0            # end blocked
    assert unique_paths_with_obstacles([[0]]) == 1               # single cell, no obstacle
    assert unique_paths_with_obstacles([[1]]) == 0               # single cell, blocked
    assert unique_paths_with_obstacles([[0, 0], [1, 1], [0, 0]]) == 0  # middle row blocked

    # Bigger obstacle grid
    grid = [
        [0, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    # Let's count: brute force by DFS
    def brute_with_obstacles(grid):
        m, n = len(grid), len(grid[0])
        if grid[0][0] == 1 or grid[-1][-1] == 1:
            return 0
        def dfs(i, j):
            if i == m - 1 and j == n - 1:
                return 1
            count = 0
            if i + 1 < m and grid[i + 1][j] == 0:
                count += dfs(i + 1, j)
            if j + 1 < n and grid[i][j + 1] == 0:
                count += dfs(i, j + 1)
            return count
        return dfs(0, 0)

    assert unique_paths_with_obstacles(grid) == brute_with_obstacles(grid)

    # Stress: fast vs brute (small grids only — brute is exponential)
    for _ in range(100):
        m, n = random.randint(1, 6), random.randint(1, 6)
        grid = [[1 if random.random() < 0.2 else 0 for _ in range(n)] for _ in range(m)]
        assert unique_paths_with_obstacles(grid) == brute_with_obstacles(grid)

    print("All tests passed!")
