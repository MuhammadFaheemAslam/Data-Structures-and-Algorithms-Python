"""
Problem: Fibonacci Number

Difficulty: Introductory (LeetCode #509)

---------------------------------------------------
Problem Statement:

The Fibonacci sequence is defined as:

    F(0) = 0
    F(1) = 1
    F(n) = F(n-1) + F(n-2)   for n ≥ 2

Given n, return F(n).

---------------------------------------------------
Why Fibonacci Is THE Recursion Lesson:

The naive recursion is exponential. The fix (memoization) is O(n).
The next step (iteration) is O(1) space. Each step teaches a core
idea:

    1. Tree recursion without overlap control → EXPONENTIAL TIME
    2. Memoization collapses repeated subproblems → LINEAR TIME
    3. Bottom-up tabulation removes recursion → LINEAR TIME, ITERATIVE
    4. Space-optimized keeps only the last two values → O(1) SPACE

Every DP problem is some variant of this escalation. Fibonacci is
the cleanest introduction.

Also covered (from a different angle) in:
  - Phase 02 / 01 / 04-Dynamic-Programming / problems / fibonacci.py
  - Phase 02 / 02 / 11-Bit-Manipulation (matrix-power version)

We repeat it here as the CANONICAL recursion example, with emphasis
on the recursion-tree intuition.
"""

from functools import lru_cache


# =========================================================================
# 1. Naive Tree Recursion — O(φ^n), Exponential
# =========================================================================

def fib_naive(n):
    """
    The textbook recursive Fibonacci.

    Time:  O(φ^n) ≈ O(1.618^n)   — exponential!
    Space: O(n) stack

    Each call spawns two more. The recursion tree is EXPONENTIAL:

                    fib(5)
                   /      \
               fib(4)      fib(3)
              /    \      /    \
          fib(3)  fib(2) fib(2) fib(1)
           / \    / \   / \
       fib(2) fib(1) ... ...

    fib(30) → ~2.7 million calls. fib(40) → ~300 million.

    Run it up to n ≈ 30; beyond that it becomes unusably slow.
    """
    if n < 2:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


# =========================================================================
# 2. Memoized Tree Recursion — O(n)
# =========================================================================

def fib_memo(n, memo=None):
    """
    Same algorithm, memoized. Each distinct subproblem is computed once.

    Time:  O(n)
    Space: O(n) memo + O(n) stack

    The recursion tree collapses to a straight chain: every fib(k)
    is either a cache HIT (O(1)) or a new computation (one per k).
    """
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n < 2:
        return n
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]


# =========================================================================
# 3. @lru_cache — Memoization for Free
# =========================================================================

@lru_cache(maxsize=None)
def fib_lru(n):
    """
    Memoization via the standard library.

    Time:  O(n)
    Space: O(n) cache + O(n) stack
    """
    if n < 2:
        return n
    return fib_lru(n - 1) + fib_lru(n - 2)


# =========================================================================
# 4. Bottom-Up DP — O(n) Time, O(n) Space, NO Recursion
# =========================================================================

def fib_dp(n):
    """
    Tabulation: fill the DP table from 0 up to n.

    Time:  O(n)
    Space: O(n)

    No recursion, no stack-depth worries, same asymptotic cost.
    """
    if n < 2:
        return n

    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]


# =========================================================================
# 5. Space-Optimized — O(n) Time, O(1) Space
# =========================================================================

def fib_iterative(n):
    """
    Keep only the last two values.

    Time:  O(n)
    Space: O(1)

    This is the version to ship. Correct, simple, fast, no stack or
    cache overhead.
    """
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


# =========================================================================
# 6. Matrix Exponentiation — O(log n)
# =========================================================================

def fib_matrix(n):
    """
    Compute fib(n) in O(log n) via matrix exponentiation.

    The recurrence F(n) = F(n-1) + F(n-2) can be expressed as:

        [F(n+1)]   [1 1] ^ n   [F(1)]
        [F(n)  ] = [1 0]     · [F(0)]

    Compute the matrix power in O(log n) via repeated squaring.

    Time:  O(log n)
    Space: O(log n) recursion

    Only useful for very large n (n > 10^6 or so). For normal
    interview-sized inputs, fib_iterative is simpler and fast enough.
    """
    def matmul(A, B):
        """2x2 matrix multiplication."""
        return [
            [A[0][0] * B[0][0] + A[0][1] * B[1][0],
             A[0][0] * B[0][1] + A[0][1] * B[1][1]],
            [A[1][0] * B[0][0] + A[1][1] * B[1][0],
             A[1][0] * B[0][1] + A[1][1] * B[1][1]],
        ]

    def matpow(M, p):
        """Fast exponentiation: M^p."""
        if p == 1:
            return M
        half = matpow(M, p // 2)
        squared = matmul(half, half)
        return squared if p % 2 == 0 else matmul(squared, M)

    if n == 0:
        return 0

    M = matpow([[1, 1], [1, 0]], n)
    return M[0][1]                                # equivalent to fib(n)


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    known = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]

    # All five agree for small n
    fib_lru.cache_clear()
    for n, expected in enumerate(known):
        assert fib_naive(n) == expected
        assert fib_memo(n) == expected
        assert fib_lru(n) == expected
        assert fib_dp(n) == expected
        assert fib_iterative(n) == expected
        assert fib_matrix(n) == expected
        print(f"   fib({n:2}) = {expected}")
    print()

    # Larger n — naive would be too slow, skip it
    for n in [50, 100, 500]:
        a = fib_iterative(n)
        b = fib_matrix(n)
        c = fib_memo(n)
        assert a == b == c
        print(f"   fib({n}) = {a}")
    print()

    # Timing on n = 30 — the exponential approach starts to hurt
    import time
    n = 30

    t0 = time.time()
    fib_naive(n)
    t_naive = time.time() - t0

    t0 = time.time()
    fib_iterative(n)
    t_iter = time.time() - t0

    print(f"Timing on n = {n}:")
    print(f"   fib_naive:       {t_naive:.4f}s   (~2.7 million calls)")
    print(f"   fib_iterative:   {t_iter:.6f}s   (30 loop iterations)")
    print(f"   speedup:         {t_naive / max(t_iter, 1e-9):.0f}×")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Optimization Arc — The Single Most Important DP Lesson:
    #
    #   fib_naive    → O(2^n)   tree recursion, redundant
    #   fib_memo     → O(n)     memoized — cache lookups collapse the tree
    #   fib_dp       → O(n)     bottom-up tabulation — no recursion
    #   fib_iterative→ O(n)     + O(1) space — keep only last 2
    #   fib_matrix   → O(log n) algebraic shortcut for huge n
    #
    # Every DP problem follows this exact progression. Learn the
    # pattern on Fibonacci; it generalizes to every harder DP.
    # ---------------------------------------------------------------
