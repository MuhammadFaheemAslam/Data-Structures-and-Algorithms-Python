# Dynamic Programming — Fundamentals

DP looks intimidating. It isn't. Almost every DP problem is
**recursion with a memo**: write the naive recursive solution first,
notice that it recomputes, cache the answers.

---

## The canonical example — Fibonacci

```python
def fib(n):
    if n < 2: return n
    return fib(n - 1) + fib(n - 2)
```

This is correct but slow — O(φⁿ) ≈ O(1.618ⁿ). `fib(50)` takes
minutes because `fib(48)` is computed many times (billions of
times by the time you reach `fib(50)`).

**Memoization**: remember each call's result.

```python
from functools import cache

@cache
def fib(n):
    if n < 2: return n
    return fib(n - 1) + fib(n - 2)
```

Now O(n) — each distinct argument is computed ONCE; subsequent calls
hit the cache.

**Tabulation**: iteratively fill a table, bottom-up.

```python
def fib(n):
    if n < 2: return n
    dp = [0, 1]
    for i in range(2, n + 1):
        dp.append(dp[i - 1] + dp[i - 2])
    return dp[n]
```

Also O(n), and explicit — no recursion stack, no cache overhead.

**Space-optimized**: only the last two values matter. Keep them in
variables.

```python
def fib(n):
    if n < 2: return n
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b
```

O(n) time, **O(1) space**. This pattern — "the `dp` array only looks
back a bounded distance, so keep a window instead" — recurs
throughout this phase.

---

## Memoization vs tabulation — which to pick

| Aspect                       | Memoization (top-down)       | Tabulation (bottom-up)   |
|------------------------------|------------------------------|--------------------------|
| How to write                 | Add `@cache` to recursion    | Loops over the dp array  |
| Feels natural when…          | The recursive definition is obvious | The subproblem DAG is clear |
| Skips unreached states?      | ✓ (lazy — only computes what's called) | ✗ (fills the whole table) |
| Easy to apply space opt?     | ✗ (opaque cache)              | ✓ (roll the array)       |
| Stack safety                 | ✗ (recursion depth = state depth) | ✓ (explicit loop)    |
| Interview-friendly           | ✓ (minimal code)              | ✓ (more visible work)    |

Rule of thumb: **write memoization to explore the problem, tabulate
to ship it**. Memoization is great when you're figuring out the
recursion; once it's working, tabulation is usually what you want in
production code because it avoids recursion depth issues and makes
space optimization straightforward.

---

## Top-down to bottom-up — mechanical conversion

Any memoized recursion can be rewritten as tabulation. The steps:

1. Identify the state variables (the arguments to the recursive
   function).
2. Figure out the dependency order — which states must be computed
   before others? For Fibonacci it's obvious (small `n` first);
   for 2D problems it's "top-left to bottom-right" or
   "outer-to-inner".
3. Replace the recursion with nested loops over the state variables
   in dependency order.
4. Look up `dp[smaller]` instead of recursing.
5. Return `dp[full problem]`.

---

## When DP DOESN'T work

Two necessary properties:

1. **Overlapping subproblems**: the same subproblem is solved
   multiple times by naive recursion. If every subproblem is unique
   (like many divide-and-conquer problems), caching buys you nothing.
2. **Optimal substructure**: the optimal solution to the whole is
   built from optimal solutions to the parts. This FAILS for some
   problems — e.g. shortest path with a "no vertex repeated" rule
   (NP-hard), longest simple path (no DP possible).

Greedy algorithms are DP's simpler cousin: they also exploit optimal
substructure, but commit to a local choice without trying
alternatives. They work when the local choice is GLOBALLY OPTIMAL
(Dijkstra on non-negative graphs, MST). When it isn't, you need DP.

---

## What's in 01-Fundamentals

- [memoization-vs-tabulation.py](memoization-vs-tabulation.py) — all four Fibonacci variants side-by-side, with timing.
- [space-optimization.py](space-optimization.py) — rolling-array technique shown on climb-stairs and LCS.
- [state-design.md](state-design.md) — the art of picking a good state, by example.
