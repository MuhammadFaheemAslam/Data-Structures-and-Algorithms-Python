"""
template-bottomup.py – Bottom-Up Dynamic Programming Template (Tabulation)

Bottom-up DP = fill a table from smallest subproblem to largest, in a loop.

The shape:

    1. Define the DP table dimensions.
    2. Initialize the base case cell(s).
    3. Loop from smaller states to larger, filling each cell from the recurrence.
    4. Return the final cell.

This file shows the pattern three ways — mirroring template-topdown.py so
you can see both implementations side by side:

    1. Fibonacci        — 1D table + the O(1)-space optimization.
    2. Climbing Stairs  — 1D, same shape as Fibonacci.
    3. Unique Paths     — 2D grid table + the O(n)-space optimization.

Run this file to see each template's output.
"""

# =========================================================================
# Template 1: Fibonacci (1D)
# =========================================================================

def fib_tabulation(n):
    """
    Bottom-up fibonacci via a 1D table.

    Time Complexity:  O(n)
    Space Complexity: O(n)
    """
    if n < 2:
        return n

    dp = [0] * (n + 1)
    dp[0], dp[1] = 0, 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]           # the recurrence, filled directly
    return dp[n]


def fib_space_optimized(n):
    """
    The recurrence only uses the last TWO values, so we don't need a full
    table — just two rolling variables.

    Time Complexity:  O(n)
    Space Complexity: O(1)    ← this is why bottom-up often wins

    This optimization — "keep only as many prior states as the recurrence
    reads" — applies to almost every 1D DP. Always check whether you can
    take it.
    """
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


# =========================================================================
# Template 2: Climbing Stairs (1D, Constrained)
# =========================================================================

def climb_stairs_tabulation(n):
    """
    Same recurrence as Fibonacci, different bases.

    Time Complexity:  O(n)
    Space Complexity: O(n)  — reducible to O(1), exactly as for Fibonacci.
    """
    if n <= 1:
        return 1

    dp = [0] * (n + 1)
    dp[0] = dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]


def climb_stairs_space_optimized(n):
    """
    O(1) space, same pattern as fib_space_optimized.
    """
    if n <= 1:
        return 1
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b


# =========================================================================
# Template 3: Unique Paths (2D Grid DP)
# =========================================================================

def unique_paths_tabulation(m, n):
    """
    Fill an m × n table where dp[i][j] = number of paths to (i, j).

    Time Complexity:  O(m * n)
    Space Complexity: O(m * n)

    Correct loop order: fill row-by-row, column-by-column. Each cell
    reads only `dp[i-1][j]` and `dp[i][j-1]`, both of which are already
    filled by the time we reach (i, j).
    """
    if m == 0 or n == 0:
        return 0

    dp = [[1] * n for _ in range(m)]            # base: first row/column = 1

    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]

    return dp[m - 1][n - 1]


def unique_paths_space_optimized(m, n):
    """
    We only ever read the PREVIOUS row — throw away everything else.
    Drops memory from O(m * n) to O(n).

    Time Complexity:  O(m * n)
    Space Complexity: O(n)

    This "roll the 2D table into a 1D array" trick appears in almost
    every grid DP problem.
    """
    if m == 0 or n == 0:
        return 0

    row = [1] * n
    for _ in range(1, m):
        for j in range(1, n):
            row[j] += row[j - 1]                # row[j-1] = current row's left neighbour
                                                # row[j]   = previous row's cell (not yet overwritten)
    return row[n - 1]


# =========================================================================
# Generic Bottom-Up Skeleton (The Pattern)
# =========================================================================
#
# def dp_bottom_up(input):
#     dp = allocate_table(based_on_state_size)
#     initialize_base_cases(dp)
#
#     for state in smallest_to_largest_order(all_states):
#         dp[state] = combine(
#             dp[smaller_state_1],
#             dp[smaller_state_2],
#             ...
#         )
#
#     return dp[final_state]
#
# Two subtleties:
#   - Loop order must respect the dependency graph (fill smaller first).
#   - "Allocate table" is where you decide the space optimization.


# =========================================================================
# Demonstration
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Template 1 — Fibonacci (Bottom-Up)")
    print("=" * 60)
    for n in [0, 1, 2, 5, 10, 20, 50, 100]:
        a = fib_tabulation(n)
        b = fib_space_optimized(n)
        print(f"   fib({n:3}): tabulation={a}, O(1)-space={b}")
    print()

    print("=" * 60)
    print("Template 2 — Climbing Stairs (Bottom-Up)")
    print("=" * 60)
    for n in [0, 1, 2, 3, 4, 5, 10, 20]:
        a = climb_stairs_tabulation(n)
        b = climb_stairs_space_optimized(n)
        print(f"   climb_stairs({n:3}): tabulation={a}, O(1)-space={b}")
    print()

    print("=" * 60)
    print("Template 3 — Unique Paths (2D Bottom-Up)")
    print("=" * 60)
    for m, n in [(1, 1), (2, 2), (3, 3), (3, 7), (10, 10)]:
        a = unique_paths_tabulation(m, n)
        b = unique_paths_space_optimized(m, n)
        print(f"   unique_paths({m:2}, {n:2}): 2D-table={a}, O(n)-space={b}")
