"""
Problem: N-Queens II — Count Only

Difficulty: Hard (LeetCode #52)

---------------------------------------------------
Problem Statement:

Return the NUMBER of valid N-queens placements, not the placements
themselves.

---------------------------------------------------
Why Count-Only Matters:

If you only need the COUNT, you don't have to allocate and copy
each solution. Just increment a counter when you reach a full
placement. For large N, this saves significant memory (and some
constant-factor time).

---------------------------------------------------
The Bitmask Optimization:

For larger N (say, N = 13 or 14), we can use BIT MASKS instead of
Python sets for the three constraints. Each mask is an integer
whose bits indicate "column X is used" / "diagonal Y is used." Set
operations become single bitwise ops — very fast.

    cols      : bit `c` set iff column `c` has a queen
    diag_ne   : bit `r - c` set (shifted to non-negative) iff taken
    diag_nw   : bit `r + c` set

Given these three masks, the AVAILABLE columns in row `r` are:

    available = ~(cols | (diag_ne << 1) | (diag_nw >> 1)) & ALL

The left-shift on `diag_ne` propagates the diagonal constraint one
column to the right for the next row. The right-shift on `diag_nw`
is symmetric.

This is a beautiful piece of bit manipulation — see the
`total_n_queens_bitmask` implementation below.

---------------------------------------------------
"""


# =========================================================================
# 1. Set-Based (Same as n-queens.py but Counting)
# =========================================================================

def total_n_queens_sets(n):
    """
    Count valid placements using three Python sets.

    Time:  exponential, heavily pruned
    Space: O(n) sets
    """
    if n == 0:
        return 1
    if n in (2, 3):
        return 0

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
            if col in used_cols:           continue
            if (row - col) in used_diag1:  continue
            if (row + col) in used_diag2:  continue

            used_cols.add(col)
            used_diag1.add(row - col)
            used_diag2.add(row + col)

            backtrack(row + 1)

            used_cols.remove(col)
            used_diag1.remove(row - col)
            used_diag2.remove(row + col)

    backtrack(0)
    return count


# =========================================================================
# 2. Bitmask-Based (Faster for Larger N)
# =========================================================================

def total_n_queens_bitmask(n):
    """
    Count placements using bitmasks instead of sets. Same algorithm,
    much smaller constant factor.

    Time:  exponential worst case, ~2-5× faster than sets in practice
    Space: O(n) recursion (no large sets)

    Key trick:
        - `cols`: bit c set iff column c is in use
        - `diag_ne`: bit set per occupied ↘ diagonal, shifted left each row
        - `diag_nw`: bit set per occupied ↙ diagonal, shifted right each row

    On each level, `available = ~(cols | diag_ne | diag_nw) & ((1 << n) - 1)`
    gives a bitmask of columns we can use. We iterate through set bits.
    """
    if n == 0:
        return 1
    if n in (2, 3):
        return 0

    all_cols = (1 << n) - 1                       # all n bits set
    count = 0

    def backtrack(cols, diag_ne, diag_nw):
        nonlocal count

        if cols == all_cols:
            count += 1
            return

        # available = bits of columns that are NOT in any of the three masks
        available = ~(cols | diag_ne | diag_nw) & all_cols

        while available:
            bit = available & -available          # isolate the lowest available column
            available ^= bit                      # clear it from available

            backtrack(
                cols | bit,
                (diag_ne | bit) << 1 & all_cols,
                (diag_nw | bit) >> 1,
            )

    backtrack(0, 0, 0)
    return count


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # OEIS A000170
    expected = {
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
        11: 2680,
        12: 14200,
    }

    for n, exp in expected.items():
        a = total_n_queens_sets(n)
        b = total_n_queens_bitmask(n)
        assert a == exp, f"sets(n={n}) = {a}, expected {exp}"
        assert b == exp, f"bitmask(n={n}) = {b}, expected {exp}"
        print(f"   n = {n:2}:  {exp} solutions (both impls agree)")
    print()

    # Timing at N = 12
    import time

    t0 = time.time()
    total_n_queens_sets(12)
    t_sets = time.time() - t0

    t0 = time.time()
    total_n_queens_bitmask(12)
    t_bits = time.time() - t0

    print(f"Timing (n = 12):")
    print(f"   set-based:    {t_sets:.3f}s")
    print(f"   bitmask:      {t_bits:.3f}s")
    print(f"   speedup:      {t_sets / max(t_bits, 1e-9):.1f}×")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The N-Queens Trilogy:
    #
    #     n-queens.py        → find ONE solution (short-circuit)
    #     n-queens-all.py    → find ALL solutions (enumerate)
    #     n-queens-count.py  → count only (no allocation)
    #
    # Same algorithm; three different base-case behaviours:
    #     - return True on first solution   (existence)
    #     - append to result, continue      (enumeration)
    #     - increment counter, continue     (counting)
    #
    # This is a general pattern — the same backtracking skeleton
    # answers four question types (existence, enumeration, counting,
    # optimization) by just changing what happens at the base case.
    # ---------------------------------------------------------------
