"""
memoization-vs-tabulation.py — Fibonacci, All Four Ways

The same problem, solved four progressively better ways. Timing shows
the dramatic asymptotic and constant-factor differences.

    1. Naive recursion             — O(φⁿ) time, O(n) stack        ← impractical past n=35
    2. Memoized recursion          — O(n) time, O(n) cache + stack ← top-down DP
    3. Tabulation                   — O(n) time, O(n) array         ← bottom-up DP
    4. Space-optimized tabulation  — O(n) time, O(1) memory         ← rolling window

All four return the same value for every n. We stress-test this and
show the runtime gap.
"""

from functools import cache
import time


# -------- 1. Naive (don't try n > 35 — exponential) --------

def fib_naive(n):
    if n < 2:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


# -------- 2. Memoized recursion (top-down DP) --------

@cache
def fib_memo(n):
    if n < 2:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)


# -------- 3. Tabulation (bottom-up DP) --------

def fib_tab(n):
    if n < 2:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]


# -------- 4. Space-optimized — "rolling two variables" --------

def fib_rolling(n):
    if n < 2:
        return n
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Correctness: small cases match
    first_30 = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610,
                987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368,
                75025, 121393, 196418, 317811, 514229]

    for i, expected in enumerate(first_30):
        assert fib_naive(i) == expected
        assert fib_memo(i) == expected
        assert fib_tab(i) == expected
        assert fib_rolling(i) == expected

    # Larger values: naive skipped (too slow); the other three agree
    for n in (100, 500, 1000):
        v_memo = fib_memo(n)
        v_tab = fib_tab(n)
        v_rolling = fib_rolling(n)
        assert v_memo == v_tab == v_rolling

    # Timing demonstration
    print("Fib timing (values identical, only method differs):\n")

    # Naive is only feasible up to ~35
    n_small = 35
    t0 = time.time()
    v = fib_naive(n_small)
    print(f"   fib_naive(n={n_small})       = {v:,}   in {(time.time() - t0) * 1000:8.1f} ms")

    # For n = 1000, naive is astronomical; skip
    n_big = 1000

    t0 = time.time()
    v = fib_memo(n_big)
    print(f"   fib_memo(n={n_big})        — first call  in {(time.time() - t0) * 1000:8.1f} ms")

    t0 = time.time()
    for _ in range(1000):
        fib_tab(n_big)
    print(f"   fib_tab(n={n_big}) × 1000  in {(time.time() - t0) * 1000:8.1f} ms")

    t0 = time.time()
    for _ in range(1000):
        fib_rolling(n_big)
    print(f"   fib_rolling(n={n_big}) × 1000 in {(time.time() - t0) * 1000:8.1f} ms")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Takeaway:
    #
    #   - `fib_naive(50)` would take MINUTES; `fib_memo(50)` is
    #     instant. That's O(φⁿ) vs O(n).
    #
    #   - Memoization and tabulation have the SAME asymptotic but
    #     tabulation has lower constants (no function call overhead,
    #     no cache lookup).
    #
    #   - Rolling variables beat tabulation by O(n) memory — the
    #     "only look back 2 steps" observation. Same asymptotic,
    #     but can matter for enormous n or RAM-constrained contexts.
    #
    #   - For ENORMOUS n (say 10^18), all four are too slow. Matrix
    #     exponentiation computes fib(n) in O(log n) — a different
    #     algorithm family entirely. Not DP anymore.
    # ---------------------------------------------------------------
