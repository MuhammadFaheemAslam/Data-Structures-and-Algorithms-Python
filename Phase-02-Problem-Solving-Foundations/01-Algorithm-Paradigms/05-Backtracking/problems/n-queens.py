"""
Problem: N-Queens

Paradigm: Backtracking — the canonical constraint-satisfaction problem
Difficulty: Hard (LeetCode #51)

---------------------------------------------------
Problem Statement:

Place `n` queens on an `n × n` chessboard so that no two queens attack
each other. A queen attacks along any row, column, or diagonal.

Return:
    - All distinct solutions (each as a list of column indices, one per row).
    - The TOTAL count of solutions (LeetCode #52).

---------------------------------------------------
The Backtracking Lens:

The decision tree is:

    Row 0: try placing a queen in columns 0, 1, 2, ..., n-1.
    Row 1: for each of those, try every non-attacking column.
    Row 2: ... and so on.

Without pruning this is O(n^n) — totally unusable for n > 6 or so.
With constraint pruning (column / diagonal tracking in O(1) per check)
it drops to empirically fast: n=10 runs in milliseconds, n=14 in
about a second.

This is the PURE form of backtracking:
    - A clean decision tree (one decision per row).
    - Hard feasibility constraints.
    - Aggressive O(1) pruning via precomputed "used" sets.

---------------------------------------------------
The Three Key Pruning Sets:

    cols:       which columns already contain a queen
    diag1:      which "\\" diagonals are occupied    (indexed by row - col)
    diag2:      which "/" diagonals are occupied     (indexed by row + col)

Why these indices?

    - On a "\\" diagonal (top-left to bottom-right), `row - col` is CONSTANT.
      So all cells on the same "\\" diagonal share a single diag1 value.
    - On a "/" diagonal (top-right to bottom-left), `row + col` is CONSTANT.
      Same logic, different formula.

With these three sets, "is placing a queen at (r, c) safe?" becomes three
O(1) set membership checks. That is what makes N-Queens practical.

---------------------------------------------------
Example:

    n = 4

    Two solutions:
        [1, 3, 0, 2]            [2, 0, 3, 1]

            . Q . .                 . . Q .
            . . . Q                 Q . . .
            Q . . .                 . . . Q
            . . Q .                 . Q . .

---------------------------------------------------
"""

# -------------------------------------------------
# Solve N-Queens — Return All Solutions
# -------------------------------------------------

def solve_n_queens(n):
    """
    Return every valid placement for n queens as a list of column indices.

    Each solution `cols` is a list of length n, where cols[r] is the
    column of the queen on row r.

    Time Complexity:  Exponential in general; practical for n ≤ 14.
    Space Complexity: O(n) recursion stack + O(solutions * n) output.
    """
    result = []
    queens = []                                 # queens[r] = column of queen in row r

    # Constraint-tracking sets — all O(1) membership checks
    used_cols = set()
    used_diag1 = set()                          # row - col
    used_diag2 = set()                          # row + col

    def backtrack(row):
        if row == n:
            result.append(queens[:])            # SNAPSHOT
            return

        for col in range(n):
            # feasibility pruning — three O(1) checks
            if col in used_cols:          continue
            if (row - col) in used_diag1: continue
            if (row + col) in used_diag2: continue

            # CHOOSE
            queens.append(col)
            used_cols.add(col)
            used_diag1.add(row - col)
            used_diag2.add(row + col)

            # EXPLORE
            backtrack(row + 1)

            # UN-CHOOSE
            queens.pop()
            used_cols.remove(col)
            used_diag1.remove(row - col)
            used_diag2.remove(row + col)

    backtrack(0)
    return result


# -------------------------------------------------
# Count Solutions Only (LeetCode #52)
# -------------------------------------------------

def count_n_queens(n):
    """
    Return just the COUNT of valid placements. Same algorithm as above,
    but we don't allocate space for each solution — only increment a counter.

    Time Complexity:  Exponential; faster than `solve_n_queens` by a
                      constant factor (no list-copying).
    Space Complexity: O(n)
    """
    count = 0
    used_cols = set()
    used_diag1 = set()
    used_diag2 = set()

    def backtrack(row):
        nonlocal count
        if row == n:
            count += 1
            return

        for col in range(n):
            if col in used_cols:          continue
            if (row - col) in used_diag1: continue
            if (row + col) in used_diag2: continue

            used_cols.add(col)
            used_diag1.add(row - col)
            used_diag2.add(row + col)

            backtrack(row + 1)

            used_cols.remove(col)
            used_diag1.remove(row - col)
            used_diag2.remove(row + col)

    backtrack(0)
    return count


# -------------------------------------------------
# Pretty-Print a Solution as a Board
# -------------------------------------------------

def board_strings(queens):
    """
    Convert a list of column indices into a list of board row strings.

    Example: queens = [1, 3, 0, 2]
    -> [".Q..", "...Q", "Q...", "..Q."]
    """
    n = len(queens)
    return [
        "." * col + "Q" + "." * (n - col - 1)
        for col in queens
    ]


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    n = 4
    solutions = solve_n_queens(n)
    print(f"N = {n}: {len(solutions)} solution(s)")
    for i, sol in enumerate(solutions):
        print(f"\n  Solution {i + 1}: columns = {sol}")
        for row_str in board_strings(sol):
            print(f"    {row_str}")

    print()

    # Known solution counts for small n (OEIS A000170)
    expected_counts = {
        0: 1, 1: 1, 2: 0, 3: 0, 4: 2, 5: 10, 6: 4,
        7: 40, 8: 92, 9: 352, 10: 724,
    }

    for n in sorted(expected_counts):
        got_all   = len(solve_n_queens(n))
        got_count = count_n_queens(n)
        expected  = expected_counts[n]

        assert got_all == expected, (
            f"solve_n_queens({n}) returned {got_all}, expected {expected}"
        )
        assert got_count == expected, (
            f"count_n_queens({n}) returned {got_count}, expected {expected}"
        )
        print(f"Test n={n}: {got_all} solution(s)   ✓")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Why N-Queens Is the Canonical Backtracking Problem:
    #
    #   1. Clear decision tree (one queen per row).
    #   2. Simple but aggressive pruning via three O(1) sets.
    #   3. The "choose → explore → un-choose" pattern shows up exactly
    #      once per recursion level, making the shape clean.
    #   4. Without pruning it's O(n^n) → impossible.
    #      With pruning it runs in milliseconds for n=10.
    #
    # Together, these make N-Queens the clearest demonstration that
    # backtracking = brute force + aggressive pruning.
    # ---------------------------------------------------------------
