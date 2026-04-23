"""
Problem: Sudoku Solver

Difficulty: Hard (LeetCode #37)

---------------------------------------------------
Problem Statement:

Fill in the empty cells of a 9×9 Sudoku board so that each row,
each column, and each 3×3 box contains the digits 1-9 exactly once.

Input: a 9×9 grid of digits '1'-'9' and '.' for empty cells.
Output: the board solved in place.

---------------------------------------------------
Why Sudoku Is the Perfect Constraint-Satisfaction Example:

Three overlapping constraints (row, column, box) interact to prune
the search space dramatically. A naïve brute force is 9^81 ≈ 2 × 10^77 —
completely impossible. With:

    - Feasibility pruning (only try legal digits)
    - Dead-end detection (a cell with 0 legal digits → fail)
    - MRV heuristic (fill the most-constrained cell first)

...the same problem solves in MILLISECONDS for standard puzzles.

This file demonstrates all three optimization techniques from
`../../optimization-techniques.md` on a single problem.

---------------------------------------------------
The Data Structures:

    rows[r]     — set of digits used in row r
    cols[c]     — set of digits used in column c
    boxes[b]    — set of digits used in box b, where b = (r // 3) * 3 + c // 3

All three sets are maintained as we place/remove digits. "Can I put
digit `d` in (r, c)?" is three O(1) set lookups.
"""


# =========================================================================
# Solution 1: Standard Backtracking (Left-to-Right, Top-to-Bottom)
# =========================================================================

def solve_sudoku_basic(board):
    """
    Solve the Sudoku in place using standard left-to-right backtracking.

    Time:  exponential worst case; fast in practice for well-formed puzzles
    Space: O(1) beyond the three constraint sets (fixed-size 9 each)
    """
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    empty = []                                     # (r, c) positions to fill

    # Scan the board to set up state
    for r in range(9):
        for c in range(9):
            if board[r][c] == ".":
                empty.append((r, c))
            else:
                d = board[r][c]
                rows[r].add(d)
                cols[c].add(d)
                boxes[_box(r, c)].add(d)

    def backtrack(idx):
        if idx == len(empty):
            return True                            # all empties filled

        r, c = empty[idx]
        b = _box(r, c)

        for d in "123456789":
            if d in rows[r]: continue
            if d in cols[c]: continue
            if d in boxes[b]: continue

            # Place
            board[r][c] = d
            rows[r].add(d); cols[c].add(d); boxes[b].add(d)

            if backtrack(idx + 1):
                return True

            # Undo
            board[r][c] = "."
            rows[r].remove(d); cols[c].remove(d); boxes[b].remove(d)

        return False

    backtrack(0)
    return board


# =========================================================================
# Solution 2: With MRV (Minimum Remaining Values) Heuristic
# =========================================================================

def solve_sudoku_mrv(board):
    """
    Same algorithm, but at each recursion pick the EMPTY CELL with
    the FEWEST legal digits (Minimum Remaining Values heuristic).

    Time:  exponential worst case; much faster than basic on hard puzzles
    Space: same

    For easy puzzles the basic and MRV versions are equally fast.
    For "hard" published Sudokus (those with ~23-25 clues), MRV can
    be 100× faster.
    """
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]

    for r in range(9):
        for c in range(9):
            if board[r][c] != ".":
                d = board[r][c]
                rows[r].add(d)
                cols[c].add(d)
                boxes[_box(r, c)].add(d)

    def find_mrv():
        """Return (r, c, legal_digits) for the most-constrained empty cell, or None if solved."""
        best = None
        best_count = 10
        for r in range(9):
            for c in range(9):
                if board[r][c] != ".":
                    continue
                b = _box(r, c)
                legal = set("123456789") - rows[r] - cols[c] - boxes[b]
                if len(legal) < best_count:
                    best_count = len(legal)
                    best = (r, c, legal)
                    if best_count == 0:
                        return best                # dead-end — return immediately
        return best

    def backtrack():
        mrv = find_mrv()
        if mrv is None:
            return True                            # solved — no empty cells

        r, c, legal = mrv
        if not legal:
            return False                            # dead-end

        b = _box(r, c)
        for d in legal:
            board[r][c] = d
            rows[r].add(d); cols[c].add(d); boxes[b].add(d)

            if backtrack():
                return True

            board[r][c] = "."
            rows[r].remove(d); cols[c].remove(d); boxes[b].remove(d)

        return False

    backtrack()
    return board


# =========================================================================
# Helpers
# =========================================================================

def _box(r, c):
    """Return the 3×3-box index for cell (r, c), in range 0..8."""
    return (r // 3) * 3 + (c // 3)


def print_board(board):
    """Pretty-print a 9×9 Sudoku grid."""
    for r in range(9):
        if r % 3 == 0 and r > 0:
            print("   ------+-------+------")
        row = []
        for c in range(9):
            if c % 3 == 0 and c > 0:
                row.append("|")
            row.append(board[r][c])
        print("   " + " ".join(row))


def is_valid_solution(board):
    """Check that a filled board is a valid solution (no duplicates)."""
    for i in range(9):
        row = [board[i][c] for c in range(9)]
        col = [board[r][i] for r in range(9)]
        box = [board[3 * (i // 3) + r][3 * (i % 3) + c] for r in range(3) for c in range(3)]
        for group in (row, col, box):
            if sorted(group) != list("123456789"):
                return False
    return True


def clone(board):
    return [row[:] for row in board]


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #37 example puzzle
    lc_puzzle = [
        ["5", "3", ".",  ".", "7", ".",  ".", ".", "."],
        ["6", ".", ".",  "1", "9", "5",  ".", ".", "."],
        [".", "9", "8",  ".", ".", ".",  ".", "6", "."],
        ["8", ".", ".",  ".", "6", ".",  ".", ".", "3"],
        ["4", ".", ".",  "8", ".", "3",  ".", ".", "1"],
        ["7", ".", ".",  ".", "2", ".",  ".", ".", "6"],
        [".", "6", ".",  ".", ".", ".",  "2", "8", "."],
        [".", ".", ".",  "4", "1", "9",  ".", ".", "5"],
        [".", ".", ".",  ".", "8", ".",  ".", "7", "9"],
    ]

    for solver in (solve_sudoku_basic, solve_sudoku_mrv):
        board = clone(lc_puzzle)
        solver(board)
        assert is_valid_solution(board)

    print("LC #37 example puzzle — solved and validated:")
    board = clone(lc_puzzle)
    solve_sudoku_mrv(board)
    print_board(board)
    print()

    # A HARDER puzzle (known minimum-clue Sudoku with 17 clues)
    hard_puzzle = [
        [".", ".", ".",  ".", ".", ".",  ".", ".", "1"],
        [".", ".", ".",  ".", ".", "2",  ".", "3", "."],
        [".", ".", ".",  "4", ".", ".",  ".", ".", "."],
        [".", ".", ".",  ".", ".", ".",  "5", ".", "."],
        "4 .. 1 .6 ... 6 .7 ..".split(),
        [".", ".", ".",  ".", ".", ".",  ".", ".", "."],
        [".", ".", ".",  ".", ".", ".",  ".", ".", "."],
        [".", ".", ".",  ".", ".", ".",  ".", ".", "."],
        [".", ".", ".",  ".", ".", ".",  ".", ".", "."],
    ]
    # skip the hard puzzle as the representation above isn't quite well-formed;
    # use another well-formed one instead:
    hard_puzzle = [
        ["8", ".", ".",  ".", ".", ".",  ".", ".", "."],
        [".", ".", "3",  "6", ".", ".",  ".", ".", "."],
        [".", "7", ".",  ".", "9", ".",  "2", ".", "."],
        [".", "5", ".",  ".", ".", "7",  ".", ".", "."],
        [".", ".", ".",  ".", "4", "5",  "7", ".", "."],
        [".", ".", ".",  "1", ".", ".",  ".", "3", "."],
        [".", ".", "1",  ".", ".", ".",  ".", "6", "8"],
        [".", ".", "8",  "5", ".", ".",  ".", "1", "."],
        [".", "9", ".",  ".", ".", ".",  "4", ".", "."],
    ]
    # "World's hardest Sudoku" (Arto Inkala)

    import time
    for solver_name, solver in [("basic", solve_sudoku_basic), ("mrv", solve_sudoku_mrv)]:
        board = clone(hard_puzzle)
        t0 = time.time()
        solver(board)
        elapsed = time.time() - t0
        assert is_valid_solution(board)
        print(f"   {solver_name:<6}: solved in {elapsed:.3f}s")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The MRV Heuristic Is Transformative:
    #
    #   On EASY puzzles, both solvers are effectively instant.
    #
    #   On HARD puzzles (the 17-clue minimum Sudokus, "world's hardest"
    #   puzzles by Arto Inkala), MRV can be 10-100× faster than the
    #   basic top-left-to-bottom-right scan.
    #
    # The idea generalizes to ANY constraint-satisfaction problem:
    # "always commit to the variable with the fewest choices first."
    # Graph colouring, scheduling, cryptarithms — all benefit from
    # this single heuristic.
    # ---------------------------------------------------------------
