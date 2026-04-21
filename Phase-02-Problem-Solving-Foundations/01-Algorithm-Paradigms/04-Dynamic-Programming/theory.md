# Dynamic Programming — Theory

## Introduction

**Dynamic Programming (DP)** is the paradigm that makes hard problems
tractable. It's the most powerful, most feared, and most rewarding idea
in the entire Phase 02 curriculum.

If Brute Force says *"try everything"* and Greedy says *"commit to the
locally best"*, DP says something subtler:

> *"Try everything — but only ONCE each. Then remember what you learned."*

Dynamic Programming turns exponential brute-force explorations into
polynomial-time algorithms by noticing that most brute forces redo the
same work over and over. DP does that work once, saves the answer, and
reuses it. That's the whole trick.

The cost of learning DP is real: the mental model is less immediate than
greedy or divide-and-conquer, and the recurrences take practice to derive.
But once it clicks, an entire class of problems that previously seemed
impossible becomes routine.

---

## The Core Idea in One Line

> **DP = Recursion + Memoization (OR) build the table from smallest to largest subproblem.**

That's it. Everything else is elaboration on those two operational choices
(**top-down** vs **bottom-up**) and on how to *find* the subproblems in
the first place.

---

## The Two Pillars

For DP to apply, the problem must have BOTH of these properties. Miss
either and DP won't work.

### 1. Optimal Substructure

> *An optimal solution to the full problem contains optimal solutions
> to smaller subproblems.*

Examples:

- **Shortest path:** the shortest path from A to C that passes through B
  is "shortest(A, B) + shortest(B, C)".
- **Fibonacci:** `fib(n) = fib(n-1) + fib(n-2)`.
- **LCS (Longest Common Subsequence):** `LCS(i, j) = 1 + LCS(i-1, j-1)` when
  the characters match, otherwise `max(LCS(i-1, j), LCS(i, j-1))`.

If you can write a recurrence that defines the answer in terms of smaller
versions of the same problem, you have optimal substructure.

### 2. Overlapping Subproblems

> *The recursive solution solves the same subproblems many times.*

Classic example — naive Fibonacci:

```
fib(5) = fib(4) + fib(3)
       = (fib(3) + fib(2)) + (fib(2) + fib(1))
       = ((fib(2) + fib(1)) + (fib(1) + fib(0))) + ...
```

`fib(2)` is computed 3 times, `fib(1)` 5 times, etc. That's exponential
redundant work. DP says: **compute each subproblem once, cache it, reuse it**.

If the subproblems are all unique (i.e., no overlap), you don't need DP —
you have a Divide & Conquer problem. The whole point of DP is that overlap
is what makes memoization worth it.

---

## DP vs Related Paradigms

| Paradigm            | Subproblems      | Shared answers?   | Combine?   | Typical complexity   |
|---------------------|------------------|-------------------|------------|----------------------|
| Brute force         | All candidates   | n/a               | n/a        | Often exponential    |
| Divide & Conquer    | Independent      | No                | Yes        | Often O(n log n)     |
| Greedy              | One, no recursion | n/a              | n/a        | Often O(n log n)     |
| **Dynamic programming** | **Overlapping**| **Yes (memoized)** | **Yes**   | **Polynomial (O(n²), O(n·m), O(n·2ⁿ), …)** |

The single most useful diagnostic:

- If the subproblems **don't overlap** → use Divide & Conquer.
- If they overlap AND a local rule is provably optimal → use Greedy.
- If they overlap AND you must try multiple choices → use DP.

---

## The DP Recipe (Five Steps)

Every DP problem you'll ever solve follows this recipe:

### 1. Define the state

Pick the variables that fully describe a subproblem. For Fibonacci,
the state is `n` (the index you want). For knapsack, it's `(i, remaining_capacity)`.
For LCS, it's `(i, j)` — your positions in each of the two strings.

> The hardest part of DP. Pick the wrong state and nothing else will work.
> When stuck, start by asking: *"What extra information do I need to pass
> down so that a subproblem can be solved independently?"*

### 2. Define the recurrence

Write the answer for a state in terms of answers to smaller states:

```
dp[state] = function of dp[smaller_state_1], dp[smaller_state_2], ...
```

This is where the algorithmic insight lives.

### 3. Base case(s)

The smallest states — the ones the recursion bottoms out at. For Fibonacci:
`dp[0] = 0`, `dp[1] = 1`. For knapsack: `dp[0][w] = 0` (no items → zero value).

### 4. Decide top-down or bottom-up

Same algorithm, two implementations:

- **Top-down (memoization):** write the recursion, cache results.
- **Bottom-up (tabulation):** fill a table from smallest to largest state.

Tradeoffs are in the next section. Pick whichever matches your mental model.

### 5. Space-optimize (optional)

If the recurrence only looks back at the last few states, you can throw
away the rest of the table and keep just those. Fibonacci drops from O(n)
memory to O(1). 2D DP often drops from O(n·m) to O(min(n, m)).

---

## Top-Down vs Bottom-Up

They're the same algorithm, implemented differently. Both are O(number of
unique states × work per state). Their differences are practical:

| Dimension                 | Top-Down (Memoization)                    | Bottom-Up (Tabulation)                       |
|---------------------------|-------------------------------------------|----------------------------------------------|
| Shape                     | Recursive function + cache                | Loop filling a table                         |
| Reads like                | The recurrence                            | The final algorithm                          |
| Only solves what you need | ✓ — lazy                                  | ✗ — fills the whole table                    |
| Python recursion limit    | Can hit it on deep inputs                 | Never hits it                                |
| Function call overhead    | Yes                                       | No                                           |
| Space-optimization        | Harder (cache keys are whatever you want) | Easier (roll the table)                      |
| When to pick              | Recurrence is complex; subset of states needed | You want best constants; deep recursion  |

**Rule of thumb:** start top-down (closer to the recurrence — easier to
reason about), then rewrite bottom-up if you need performance or
space-optimization.

See [`template-topdown.py`](template-topdown.py) and
[`template-bottomup.py`](template-bottomup.py) for concrete implementations
of both styles.

---

## Common DP Patterns (Quick Survey)

A handful of recurrence shapes cover most DP problems. Covered in detail
in [`patterns.md`](patterns.md); here's the map:

| Pattern               | Shape                                        | Example problems                             |
|-----------------------|----------------------------------------------|----------------------------------------------|
| **1D DP**             | `dp[i]` depends on `dp[i-1], dp[i-2], …`     | Fibonacci, climbing stairs, house robber     |
| **2D DP (grid)**      | `dp[i][j]` from grid neighbours              | Unique paths, min path sum                   |
| **2D DP (two sequences)** | `dp[i][j]` from two input indices        | LCS, edit distance, regex matching           |
| **Knapsack**          | `dp[i][w]` over items and remaining capacity | 0/1 knapsack, coin change, subset sum        |
| **Interval DP**       | `dp[i][j]` over a range `[i, j]`             | Matrix chain multiplication, burst balloons  |
| **State machine DP**  | `dp[i][state]` — finite states per step      | Stock problems (hold / cash / cooldown)      |
| **Bitmask DP**        | `dp[mask]` — subset encoded as an integer    | TSP, assignment problem                      |
| **Tree DP**           | `dp[node]` via post-order                    | Diameter of tree, house robber III           |

When you encounter a new problem, ask yourself: *"which of these shapes
is this a special case of?"* It's faster than re-deriving DP from scratch
every time.

---

## Complexity

For a DP algorithm:

- **Time** = (number of unique states) × (work per state)
- **Space** = (size of the DP table) — often reducible via the
  space-optimization step

Examples:

| Algorithm              | States              | Work per state | Time        | Space (naive) | Space (optimized) |
|------------------------|---------------------|----------------|-------------|---------------|-------------------|
| Fibonacci              | n                   | O(1)           | O(n)        | O(n)          | O(1)              |
| 0/1 Knapsack           | n × W               | O(1)           | O(n·W)      | O(n·W)        | O(W)              |
| LCS                    | n × m               | O(1)           | O(n·m)      | O(n·m)        | O(min(n, m))      |
| TSP (bitmask)          | n × 2ⁿ              | O(n)           | O(n²·2ⁿ)    | O(n·2ⁿ)       | (same)            |
| Edit distance          | n × m               | O(1)           | O(n·m)      | O(n·m)        | O(min(n, m))      |

DP's job is to replace an exponential brute force with a polynomial
algorithm. If your DP is still exponential, either you have a hard
problem (TSP) or your state is over-specified — pare it down.

---

## Common Pitfalls

- **Picking the wrong state.** You can't DP your way out of a state that
  doesn't capture enough information to make the subproblem independent.
  When stuck, ask: *"if I told someone the state, could they solve the
  rest without knowing any prior history?"*
- **Confusing DP with greedy.** Greedy commits to one choice per step;
  DP tries all of them. A problem that breaks greedy (see the coin-change
  counter-example in 03-Greedy) is almost always a DP problem.
- **Overlapping subproblems but you didn't memoize.** Welcome to
  exponential time. Add the cache.
- **Non-overlapping subproblems but you DP'd anyway.** You'd be better
  off with plain recursion (Divide & Conquer). DP's bookkeeping has
  non-trivial constant factors.
- **Missing the base case.** Infinite recursion in top-down, or
  `KeyError`/wrong values in bottom-up.
- **Direction of the bottom-up fill.** You must fill smaller states
  before the larger states that depend on them. Loop order matters.
- **Python recursion limit on deep inputs.** For top-down on n > 1000,
  either bump the limit (`sys.setrecursionlimit`) or switch to bottom-up.

---

## A Worked Example — Fibonacci Through Four Implementations

This is the clearest "why DP" story in existence.

```python
# 1) Naive recursion — O(2^n), unusable past n ≈ 35
def fib(n):
    if n < 2: return n
    return fib(n - 1) + fib(n - 2)

# 2) Top-down memoization — O(n) time, O(n) space
def fib(n, memo={}):
    if n < 2: return n
    if n in memo: return memo[n]
    memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]

# 3) Bottom-up tabulation — O(n) time, O(n) space
def fib(n):
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]

# 4) Space-optimized — O(n) time, O(1) space
def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
```

Each step removes some redundant work the previous step was doing.

- Step 1 → 2: stop recomputing the same subproblem.
- Step 2 → 3: drop the recursion overhead by filling explicitly.
- Step 3 → 4: notice we only ever need the last two values, drop the table.

This is the full DP optimization arc in miniature. Every DP problem
follows some variant of it. See [`problems/fibonacci.py`](problems/fibonacci.py)
for the full runnable version.

---

## Key Takeaways

1. **DP = recursion + memoization, or tabulation from the base up.**
2. **Two pillars:** optimal substructure + overlapping subproblems.
   Both required.
3. **The hardest part of DP is picking the state.** Once the state is
   right, the recurrence usually writes itself.
4. **Top-down and bottom-up are the same algorithm.** Pick whichever
   matches how you think. Rewrite later if needed.
5. **Always ask whether you can space-optimize** by rolling the table.
   Most DP problems have an easy win here.
6. **Patterns matter more than individual problems.** Master the eight
   common shapes in [`patterns.md`](patterns.md) and you'll recognize
   most DP problems on sight.
