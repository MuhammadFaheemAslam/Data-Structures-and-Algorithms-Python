"""
Problem: Minimum Path Sum

Difficulty: Medium (LeetCode #64)

---------------------------------------------------
Problem Statement:

Given an m×n grid of non-negative numbers, find a path from
top-left to bottom-right that MINIMIZES the sum of numbers along
the path. You can only move right or down.

    Input:  [[1, 3, 1],
             [1, 5, 1],
             [4, 2, 1]]

    Path with minimum sum: 1 → 3 → 1 → 1 → 1  = 7

---------------------------------------------------
The Recurrence:

    dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])

Each cell's best total is its own value plus the smaller of the two
"how did I get here?" options.

Base cases:
    dp[0][0] = grid[0][0]
    dp[0][j] = dp[0][j-1] + grid[0][j]        (first row: only from left)
    dp[i][0] = dp[i-1][0] + grid[i][0]        (first col: only from above)

---------------------------------------------------
Space Optimization:

Each cell only needs the value directly ABOVE (same column, previous
row) and directly LEFT (same row, previous column). A single row
suffices if we scan left-to-right:
    - `dp[j]` currently holds the PREVIOUS ROW's value at column j.
    - Once we update it, it becomes the CURRENT ROW's value.
    - At that point, `dp[j-1]` is the CURRENT ROW at column j-1
      (same row, just updated).

Space: O(n).

---------------------------------------------------
Complexity:

    Time:  O(m·n)
    Space: O(min(m, n)) with the rolling-row trick
"""


def min_path_sum(grid):
    """
    Minimum path sum from top-left to bottom-right, RIGHT/DOWN only.

    Time: O(m·n), Space: O(min(m, n)).
    """
    if not grid or not grid[0]:
        return 0

    m, n = len(grid), len(grid[0])
    # Ensure dp[] is the shorter dimension for memory
    if m < n:
        # Transpose conceptually by iterating the other way
        # (Easier: just keep a row of length n as-is — O(n) is fine.)
        pass

    dp = [0] * n
    dp[0] = grid[0][0]
    # Initialize first row
    for j in range(1, n):
        dp[j] = dp[j - 1] + grid[0][j]

    for i in range(1, m):
        dp[0] += grid[i][0]                        # first column: only from above
        for j in range(1, n):
            dp[j] = grid[i][j] + min(dp[j], dp[j - 1])

    return dp[-1]


# -------- O(m·n) space — verbose but clearer --------

def min_path_sum_tab(grid):
    """Full dp[i][j] table. Easier to step through for learning."""
    if not grid or not grid[0]:
        return 0

    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = grid[0][0]
    for j in range(1, n):
        dp[0][j] = dp[0][j - 1] + grid[0][j]
    for i in range(1, m):
        dp[i][0] = dp[i - 1][0] + grid[i][0]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = grid[i][j] + min(dp[i - 1][j], dp[i][j - 1])
    return dp[-1][-1]


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #64 example
    assert min_path_sum([[1, 3, 1], [1, 5, 1], [4, 2, 1]]) == 7
    assert min_path_sum([[1, 2, 3], [4, 5, 6]]) == 12

    # Edge cases
    assert min_path_sum([]) == 0
    assert min_path_sum([[]]) == 0
    assert min_path_sum([[42]]) == 42
    assert min_path_sum([[1, 2, 3, 4, 5]]) == 15                # single row
    assert min_path_sum([[1], [2], [3], [4]]) == 10             # single column

    # Cross-check full-table vs optimized
    import random
    random.seed(42)
    for _ in range(200):
        m = random.randint(1, 20)
        n = random.randint(1, 20)
        grid = [[random.randint(0, 99) for _ in range(n)] for _ in range(m)]
        assert min_path_sum(grid) == min_path_sum_tab(grid)

    # Brute force — DFS, exponential but correct on small grids
    def brute(grid):
        m, n = len(grid), len(grid[0])
        def dfs(i, j):
            if i == m - 1 and j == n - 1:
                return grid[i][j]
            best = float("inf")
            if i + 1 < m:
                best = min(best, dfs(i + 1, j))
            if j + 1 < n:
                best = min(best, dfs(i, j + 1))
            return grid[i][j] + best
        return dfs(0, 0)

    for _ in range(50):
        m = random.randint(1, 6)
        n = random.randint(1, 6)
        grid = [[random.randint(0, 20) for _ in range(n)] for _ in range(m)]
        assert min_path_sum(grid) == brute(grid)

    print("All tests passed!")
