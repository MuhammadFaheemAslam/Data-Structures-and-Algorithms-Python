"""
Problem: N-Queens (Return ALL Solutions)

Difficulty: Hard (LeetCode #51)

---------------------------------------------------
Problem Statement:

Place N queens on an N × N chessboard so no two queens attack.
Return EVERY valid placement (not just one).

---------------------------------------------------
Almost Identical to `n-queens.py`:

The only change is at the base case: record the solution and
CONTINUE searching instead of short-circuiting.

    if row == n:
        result.append(cols[:])
        return                 # keep exploring other branches
    ...

The rest of the algorithm (three-set pruning, iteration over columns)
is identical.

---------------------------------------------------
Known Solution Counts (OEIS A000170):

    n:  1  2  3  4  5   6   7   8   9    10   11   12    13
    count: 1  0  0  2  10   4  40  92  352  724  2680 14200  73712

n = 8 (the original chess variant) has 92 distinct solutions,
which reduce to 12 fundamental solutions once rotations and
reflections are accounted for.
"""


def solve_n_queens_all(n):
    """
    Return ALL valid N-queens placements.

    Each solution is a list `cols[0..n-1]` with cols[row] = queen's column.

    Time:  exponential (but the number of SOLUTIONS is much less than n!)
    Space: O(number of solutions × n)
    """
    if n == 0:
        return [[]]
    if n in (2, 3):
        return []

    result = []
    cols = [-1] * n
    used_cols = set()
    used_diag1 = set()
    used_diag2 = set()

    def backtrack(row):
        if row == n:
            result.append(cols[:])
            return

        for col in range(n):
            if col in used_cols:           continue
            if (row - col) in used_diag1:  continue
            if (row + col) in used_diag2:  continue

            cols[row] = col
            used_cols.add(col)
            used_diag1.add(row - col)
            used_diag2.add(row + col)

            backtrack(row + 1)

            cols[row] = -1
            used_cols.remove(col)
            used_diag1.remove(row - col)
            used_diag2.remove(row + col)

    backtrack(0)
    return result


# =========================================================================
# Format a Solution as a Board String List (LC #51's Output Format)
# =========================================================================

def format_solution(cols):
    """Convert a cols[] solution to a list of N strings of '.' / 'Q'."""
    n = len(cols)
    return [
        "." * cols[row] + "Q" + "." * (n - cols[row] - 1)
        for row in range(n)
    ]


# =========================================================================
# Test
# =========================================================================

def is_valid(cols):
    n = len(cols)
    seen_cols = set()
    seen_d1 = set()
    seen_d2 = set()
    for row, col in enumerate(cols):
        if col in seen_cols:    return False
        if (row - col) in seen_d1: return False
        if (row + col) in seen_d2: return False
        seen_cols.add(col)
        seen_d1.add(row - col)
        seen_d2.add(row + col)
    return True


if __name__ == "__main__":
    # OEIS A000170 values
    expected_counts = {
        0: 1,
        1: 1,
        2: 0,
        3: 0,
        4: 2,
        5: 10,
        6: 4,
        7: 40,
        8: 92,
        9: 352,
        10: 724,
    }

    for n, expected in expected_counts.items():
        sols = solve_n_queens_all(n)
        assert len(sols) == expected, f"n={n}: got {len(sols)}, expected {expected}"
        for s in sols:
            assert is_valid(s)
        print(f"   n = {n:2}:  {expected} solutions")
    print()

    # Display all solutions for N = 4
    print("All 2 solutions for N = 4:\n")
    for i, cols in enumerate(solve_n_queens_all(4), 1):
        print(f"Solution {i}:")
        for line in format_solution(cols):
            print(f"   {line}")
        print()

    print("All tests passed!")
