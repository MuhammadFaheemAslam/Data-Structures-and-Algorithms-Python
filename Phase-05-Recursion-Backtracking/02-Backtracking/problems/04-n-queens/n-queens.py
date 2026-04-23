"""
Problem: N-Queens (Return One Solution)

Difficulty: Hard (LeetCode #51 variant — "find any one")

---------------------------------------------------
Problem Statement:

Place N queens on an N × N chessboard so that no two queens attack
each other. Return ONE valid placement (as a list of column indices,
one per row).

A queen attacks any square on the same:
    - row
    - column
    - diagonal (↘ or ↙)

Example: N = 4

    . Q . .
    . . . Q
    Q . . .
    . . Q .

Returns [1, 3, 0, 2] — queen in row 0 at col 1, row 1 at col 3, etc.

---------------------------------------------------
Why N-Queens Is the Canonical Backtracking Problem:

It's the simplest problem where BACKTRACKING WITH PRUNING is
essential. Brute force (try every board) is O(N^(N²)) — unusable
past N = 4. Backtracking with feasibility pruning is empirically
fast for N ≤ 14 or so.

The three constraints (row, col, diagonals) are the textbook case
for maintaining O(1) validity checks via set invariants.

---------------------------------------------------
Key Insights:

1. We ONE QUEEN PER ROW — the problem places exactly N queens,
   one per row by the pigeonhole principle.
2. State: partial placement (one col per row, for rows 0..k-1).
3. Feasibility: a new queen at (row, col) is valid iff:
       col not in used_cols
       (row - col) not in used_diag_ne       ← diagonals ↘
       (row + col) not in used_diag_nw       ← anti-diagonals ↙

All three are O(1) set lookups.

---------------------------------------------------
Complexity:

    Time: exponential in N; heavily pruned
    Space: O(N) for the board + O(N) for the three sets
"""


# =========================================================================
# Find ONE Valid Placement (Return First Found)
# =========================================================================

def solve_n_queens_one(n):
    """
    Return one valid N-queens placement, or None if impossible.

    Returns a list `cols` where cols[row] = column of queen in that row.

    Time:  exponential worst case; with pruning, fast for n ≤ 14
    Space: O(n)
    """
    if n == 0:
        return []
    if n in (2, 3):
        return None                                # no solution for n=2 or n=3

    cols = [-1] * n
    used_cols = set()
    used_diag1 = set()                             # row - col (↘ diagonals)
    used_diag2 = set()                             # row + col (↙ anti-diagonals)

    def backtrack(row):
        if row == n:
            return True                            # all rows placed → done

        for col in range(n):
            if col in used_cols:
                continue
            if (row - col) in used_diag1:
                continue
            if (row + col) in used_diag2:
                continue

            # CHOOSE
            cols[row] = col
            used_cols.add(col)
            used_diag1.add(row - col)
            used_diag2.add(row + col)

            # EXPLORE
            if backtrack(row + 1):
                return True                        # short-circuit on first solution

            # UN-CHOOSE
            cols[row] = -1
            used_cols.remove(col)
            used_diag1.remove(row - col)
            used_diag2.remove(row + col)

        return False

    return cols[:] if backtrack(0) else None


# =========================================================================
# Pretty-Print a Solution
# =========================================================================

def print_board(cols):
    """Print a textual board for a solution `cols`."""
    if cols is None:
        print("   (no solution)")
        return
    n = len(cols)
    for row in range(n):
        line = ["."] * n
        line[cols[row]] = "Q"
        print("   " + " ".join(line))


# =========================================================================
# Validator (For Testing)
# =========================================================================

def is_valid_board(cols):
    """True iff `cols` is a valid N-queens placement."""
    n = len(cols)
    seen_cols = set()
    seen_d1 = set()
    seen_d2 = set()
    for row, col in enumerate(cols):
        if col < 0 or col >= n:
            return False
        if col in seen_cols:
            return False
        if (row - col) in seen_d1:
            return False
        if (row + col) in seen_d2:
            return False
        seen_cols.add(col)
        seen_d1.add(row - col)
        seen_d2.add(row + col)
    return True


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Small cases
    cases = [
        (0,   []),             # trivially solved
        (1,   [0]),            # one queen
        (2,   None),           # no solution
        (3,   None),           # no solution
    ]

    for n, expected in cases:
        got = solve_n_queens_one(n)
        assert got == expected, f"n={n}: got {got}, expected {expected}"
        print(f"   solve_n_queens_one({n}) = {got}")
    print()

    # N = 4..12: should always find a valid solution
    for n in range(4, 13):
        sol = solve_n_queens_one(n)
        assert sol is not None, f"n={n}: no solution found"
        assert is_valid_board(sol), f"n={n}: invalid solution {sol}"

    print("Valid solutions found for n = 4..12")

    # Pretty-print a few
    print("\nOne solution for N = 4:")
    print_board(solve_n_queens_one(4))
    print("\nOne solution for N = 8:")
    print_board(solve_n_queens_one(8))

    print("\nAll tests passed!")
