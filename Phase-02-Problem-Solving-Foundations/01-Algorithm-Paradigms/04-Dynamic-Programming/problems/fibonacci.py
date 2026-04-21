"""
Problem: Fibonacci Number

Paradigm: Dynamic Programming — the canonical "why DP exists" problem
Difficulty: Easy (LeetCode #509, and every DP textbook ever written)

---------------------------------------------------
Problem Statement:

The Fibonacci sequence is defined as:

    F(0) = 0
    F(1) = 1
    F(n) = F(n-1) + F(n-2)   for n >= 2

Given `n`, return F(n).

---------------------------------------------------
Why This Problem Matters:

Fibonacci is the shortest possible demonstration of WHY DP exists.
The recurrence is so trivial you already know it; the entire lesson is
in how the implementation evolves from O(2^n) to O(1).

We show four versions, each of which removes redundant work the previous
one was doing:

    1. Naive recursion              — O(2^n)  time, O(n) stack
    2. Top-down memoization         — O(n)    time, O(n) memo + stack
    3. Bottom-up tabulation         — O(n)    time, O(n) table
    4. Bottom-up, space-optimized   — O(n)    time, O(1) space

This is the full DP optimization arc in miniature. Every DP problem you
ever see is some variant of this progression.

---------------------------------------------------
"""

from functools import cache


# -------------------------------------------------
# Approach 1: Naive Recursion — O(2^n)
# -------------------------------------------------

def fib_naive(n):
    """
    Direct translation of the recurrence with no caching.

    Time Complexity:  O(2^n)   — each call spawns two more, up to depth n
    Space Complexity: O(n)     — recursion stack

    Correct. Completely unusable past n ~ 35. The recursion tree is
    overwhelmingly full of DUPLICATE work:

        fib(5) = fib(4) + fib(3)
               = (fib(3) + fib(2)) + (fib(2) + fib(1))
               ...

    fib(2) is computed 3 times, fib(1) 5 times, fib(0) 3 times, and
    it only gets worse exponentially. This redundancy is what DP kills.
    """
    if n < 2:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


# -------------------------------------------------
# Approach 2: Top-Down DP — O(n), Memoization
# -------------------------------------------------

@cache
def fib_topdown(n):
    """
    Same recursion, but @cache turns each subproblem into a one-time
    computation. Repeat calls to fib_topdown(k) return the cached
    result instead of re-exploring the subtree.

    Time Complexity:  O(n)   — each subproblem solved once
    Space Complexity: O(n)   — cache + recursion stack

    Conceptually the simplest DP: take your correct recursion, add a
    cache, and it's suddenly polynomial. The algorithm IS the recurrence.
    """
    if n < 2:
        return n
    return fib_topdown(n - 1) + fib_topdown(n - 2)


# -------------------------------------------------
# Approach 3: Bottom-Up DP — O(n), Tabulation
# -------------------------------------------------

def fib_bottomup(n):
    """
    Fill a table from smallest to largest, in a loop.

    Time Complexity:  O(n)
    Space Complexity: O(n)   — the table

    No recursion — no stack to overflow, no function-call overhead.
    The recurrence is exactly the same as Approach 2, just expressed
    iteratively.
    """
    if n < 2:
        return n

    dp = [0] * (n + 1)
    dp[0], dp[1] = 0, 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]


# -------------------------------------------------
# Approach 4: Space-Optimized — O(n) Time, O(1) Space
# -------------------------------------------------

def fib_space_optimized(n):
    """
    The recurrence only looks at the LAST TWO values. Keep just those.

    Time Complexity:  O(n)
    Space Complexity: O(1)

    This optimization applies to any DP whose recurrence has bounded
    lookback. Always ask: "How many previous values does my recurrence
    actually use?" That's how much memory you really need.
    """
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


# -------------------------------------------------
# Bonus: Matrix Exponentiation — O(log n)
# -------------------------------------------------

def fib_matrix_power(n):
    """
    The Fibonacci recurrence can be expressed as a matrix power:

        | F(n+1) |   | 1 1 |^n   | F(1) |
        | F(n)   | = | 1 0 |     | F(0) |

    Using fast matrix exponentiation (divide & conquer squaring),
    this computes F(n) in O(log n) time.

    Time Complexity:  O(log n)
    Space Complexity: O(log n)  recursion depth

    Useful only for extremely large n — the DP versions handle n up to
    ~100_000 in well under a second.
    """
    def mat_mult(A, B):
        return [
            [A[0][0] * B[0][0] + A[0][1] * B[1][0],
             A[0][0] * B[0][1] + A[0][1] * B[1][1]],
            [A[1][0] * B[0][0] + A[1][1] * B[1][0],
             A[1][0] * B[0][1] + A[1][1] * B[1][1]],
        ]

    def mat_pow(M, p):
        if p == 1:
            return M
        half = mat_pow(M, p // 2)
        squared = mat_mult(half, half)
        return squared if p % 2 == 0 else mat_mult(squared, M)

    if n == 0:
        return 0
    M = mat_pow([[1, 1], [1, 0]], n)
    return M[0][1]                              # = F(n)


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    # Known Fibonacci values for sanity
    expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]

    print("Comparing all approaches on small n:")
    print(f"   {'n':>3}  {'naive':>8}  {'topdown':>8}  {'bottomup':>8}  {'O(1)':>8}  {'matrix':>8}")
    for n, exp in enumerate(expected):
        vals = [
            fib_naive(n),
            fib_topdown(n),
            fib_bottomup(n),
            fib_space_optimized(n),
            fib_matrix_power(n),
        ]
        assert all(v == exp for v in vals), f"Disagreement on fib({n}): {vals}"
        print(f"   {n:>3}  {vals[0]:>8}  {vals[1]:>8}  {vals[2]:>8}  {vals[3]:>8}  {vals[4]:>8}")
    print()

    # Try a larger n — naive would time out, but the DP versions breeze through.
    big_n = 200
    expected_big = fib_space_optimized(big_n)
    assert fib_topdown(big_n)        == expected_big
    assert fib_bottomup(big_n)       == expected_big
    assert fib_matrix_power(big_n)   == expected_big
    print(f"Test passed: fib({big_n}) = {expected_big}")
    print()

    # Demonstrate the cost of the naive approach — calling fib_naive(35) is
    # slow enough to FEEL; naive(40) takes noticeable seconds.
    import time
    t0 = time.time()
    fib_naive(30)
    print(f"fib_naive(30) took {time.time() - t0:.3f} seconds  (this is O(2^n))")

    t0 = time.time()
    fib_bottomup(10_000)
    print(f"fib_bottomup(10_000) took {time.time() - t0:.3f} seconds  (this is O(n))")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Optimization Arc in One Table:
    #
    #   version             time       space      what changed
    #   -------             ----       -----      ------------
    #   naive recursion     O(2^n)     O(n)       —
    #   top-down DP         O(n)       O(n)       stopped recomputing
    #   bottom-up DP        O(n)       O(n)       dropped recursion
    #   space-optimized     O(n)       O(1)       kept only the last 2 values
    #   matrix power        O(log n)   O(log n)   exploited algebraic structure
    #
    # Each row removes some redundant work the previous row was doing.
    # That's the whole point of DP — find the redundancy, remove it.
    # ---------------------------------------------------------------
