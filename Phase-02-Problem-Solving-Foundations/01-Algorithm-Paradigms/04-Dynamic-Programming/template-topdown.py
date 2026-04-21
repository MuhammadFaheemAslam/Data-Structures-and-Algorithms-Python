"""
template-topdown.py – Top-Down Dynamic Programming Template (Memoization)

Top-down DP = a recursive function that caches its own results.

The shape:

    1. Write a recursion that expresses the answer in terms of smaller subproblems.
    2. Add a cache (dict, @functools.lru_cache, or @functools.cache).
    3. Define the base case(s).
    4. Return the cached result on repeat calls instead of recomputing.

This file shows the pattern three ways:

    1. Fibonacci        — 1D, the canonical DP.
    2. Climbing Stairs  — 1D with a constraint (step 1 or 2 at a time).
    3. Unique Paths     — 2D grid DP.

Every top-down DP solution you'll ever write is a variation on one of these.

Run this file to see each template's output.
"""

from functools import cache, lru_cache


# =========================================================================
# Template 1: Fibonacci (1D, Canonical)
# State: n                    — the index of the Fibonacci number
# Recurrence: fib(n) = fib(n-1) + fib(n-2)
# Base: fib(0) = 0, fib(1) = 1
# =========================================================================

@cache                                          # Python 3.9+ unbounded cache
def fib(n):
    """
    fib(n) using top-down DP with @functools.cache.

    Without @cache, this is O(2^n) — unusable past n ≈ 35.
    With @cache, each of the n distinct subproblems is solved exactly once:

    Time Complexity:  O(n)
    Space Complexity: O(n)   — cache + recursion stack

    @cache is just a dict lookup in disguise. Manual version below for
    illustration.
    """
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def fib_manual_cache(n, memo=None):
    """
    The same algorithm with an explicit dict — useful when you want
    control over the cache (e.g., to reset between calls, or key on
    something @cache can't hash).
    """
    if memo is None:
        memo = {}
    if n < 2:
        return n
    if n in memo:
        return memo[n]
    memo[n] = fib_manual_cache(n - 1, memo) + fib_manual_cache(n - 2, memo)
    return memo[n]


# =========================================================================
# Template 2: Climbing Stairs (1D, Constrained)
# State: i                    — current step
# Recurrence: ways(i) = ways(i-1) + ways(i-2)
#             (take a 1-step to i from i-1, or a 2-step from i-2)
# Base: ways(0) = 1 (empty path), ways(1) = 1
# =========================================================================

@lru_cache(maxsize=None)
def climb_stairs(n):
    """
    Number of distinct ways to climb `n` stairs taking 1 or 2 steps at a time.

    Note: mathematically the same recurrence as Fibonacci, shifted by one.
    This is a great example of "different problem, same pattern."

    Time Complexity:  O(n)
    Space Complexity: O(n)
    """
    if n <= 1:
        return 1
    return climb_stairs(n - 1) + climb_stairs(n - 2)


# =========================================================================
# Template 3: Unique Paths (2D Grid DP)
# State: (i, j)               — current cell
# Recurrence: paths(i, j) = paths(i-1, j) + paths(i, j-1)
# Base: paths(0, j) = paths(i, 0) = 1  (one way along top row or left column)
# =========================================================================

def unique_paths(m, n):
    """
    Number of distinct lattice paths from top-left (0, 0) to
    bottom-right (m-1, n-1), moving only right or down.

    Time Complexity:  O(m * n)    — one subproblem per cell
    Space Complexity: O(m * n)    — cache

    We use a local cache so the function is re-entrant across different
    (m, n) calls without bleed-over.
    """
    @cache
    def paths(i, j):
        if i == 0 or j == 0:
            return 1                            # single path along edges
        return paths(i - 1, j) + paths(i, j - 1)

    return paths(m - 1, n - 1)


# =========================================================================
# Generic Top-Down Skeleton (The Pattern)
# =========================================================================
#
# def dp(state):
#     if is_base_case(state):
#         return base_value(state)
#
#     if state in memo:
#         return memo[state]
#
#     answer = combine(
#         dp(smaller_state_1),
#         dp(smaller_state_2),
#         ...
#     )
#     memo[state] = answer
#     return answer
#
# Replace the state, the base case, and the recurrence — the shape is always
# this. `memo` can be a dict, a 2D array, or @functools.cache.


# =========================================================================
# Demonstration
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Template 1 — Fibonacci (Top-Down)")
    print("=" * 60)
    # Clear the cache between runs so timings are comparable
    fib.cache_clear()
    for n in [0, 1, 2, 5, 10, 20, 50, 100]:
        print(f"   fib({n:3}) = {fib(n)}")
    print()

    print("=" * 60)
    print("Template 2 — Climbing Stairs (Top-Down)")
    print("=" * 60)
    for n in [0, 1, 2, 3, 4, 5, 10, 20]:
        print(f"   climb_stairs({n:3}) = {climb_stairs(n)}")
    print()

    print("=" * 60)
    print("Template 3 — Unique Paths (2D Top-Down)")
    print("=" * 60)
    for m, n in [(1, 1), (2, 2), (3, 3), (3, 7), (10, 10)]:
        print(f"   unique_paths({m:2}, {n:2}) = {unique_paths(m, n)}")
