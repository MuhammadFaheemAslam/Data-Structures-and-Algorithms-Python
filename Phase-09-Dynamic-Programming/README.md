# Phase 09 — Dynamic Programming

**Dynamic programming (DP)** is an approach to problems with two
properties:

1. **Overlapping subproblems** — the same smaller sub-computation
   appears many times.
2. **Optimal substructure** — an optimal solution is built from
   optimal solutions to subproblems.

When both hold, we can avoid recomputing subproblems by remembering
their answers. Done recursively it's **memoization** (top-down);
done iteratively it's **tabulation** (bottom-up). Both compute the
same thing; both run in the same asymptotic time. The difference is
style — and sometimes memory.

---

## The broad recipe

Almost every DP problem reduces to the same three questions:

1. **State** — what do you need to fully describe a subproblem?
   (e.g. "position `i`", "up to coin `c` with budget `b`", "which
   substring `s[l..r]`".)
2. **Transition** — given solutions to smaller states, how do you
   build this one? Usually `dp[state] = f(dp[smaller-states])`.
3. **Base case** — which states are trivially solvable? Usually the
   empty / 0-size / leaf case.

Once those three are nailed, the code writes itself. The *hard* part
is choosing the state — "how much information do I need to carry?"
is the whole art of DP.

---

## What we cover in this phase

| Module             | Focus                                                      |
|--------------------|------------------------------------------------------------|
| 01-Fundamentals    | Memoization vs tabulation, rolling-array space optimization |
| 02-1D-DP           | State = one index. Fib, stairs, rob, coin-change.          |
| 03-2D-DP           | State = two indices. Grids, LCS, edit distance, regex.     |
| 04-Subsequence     | LIS (O(n²) + patience-sort O(n log n)), palindromic substring |
| 05-Knapsack        | 0/1, unbounded, subset-sum, target-sum.                    |
| 06-Interval-DP     | State = a range [l, r]. Matrix chain, burst balloons.      |
| 07-State-Machine   | State = (index, machine-state). Stock-trading family.      |
| 08-Advanced        | Bitmask DP (TSP), Tree DP.                                  |

## Cross-references

- **Recursion + memoization is the bridge from Phase 05** — many
  "recursion problems" become DP once you add a memo.
- **DP on DAG** — topo-order relaxation in Phase 08 is "DP on a
  graph".
- **Greedy vs DP** — Phase 02's greedy paradigm. Greedy works when
  local choice leads to global optimum; DP is the fallback when it
  doesn't.
- **Backtracking vs DP** — Phase 05's backtracking handles the "count
  solutions" version by raw enumeration. DP speeds it up when
  overlapping subproblems appear.

## The hard part

Most DP problems have ~10 lines of code. The difficulty is in
*identifying* the state — the code is a formality. A few patterns
that recur:

- **Last decision**: "what was the LAST thing I did that produced
  this state?" (coin-change: what was the last coin; LCS: did I
  match the last chars.)
- **Cut at i**: "where do I split the input?" (interval DP,
  matrix-chain, palindrome partitioning.)
- **Include/exclude**: "do I take this item or not?" (knapsack.)
- **Take/not-take with constraints**: (house-robber can't-use-
  adjacent, stock-trading cooldown.)

The more problems you solve, the more quickly you recognize the
shape. There's no substitute for practice.

## Complexity cheat-sheet

Most DP in this phase fits one of:

| Problem family               | State size | Transitions | Time     | Space (optimized) |
|------------------------------|------------|-------------|----------|-------------------|
| 1D DP (climb, rob)           | O(n)       | O(1)        | O(n)     | O(1)              |
| Coin change                  | O(n)       | O(k coins)  | O(nk)    | O(n)              |
| 2D grid DP                   | O(mn)      | O(1)        | O(mn)    | O(min(m, n))      |
| LCS / edit distance          | O(mn)      | O(1)        | O(mn)    | O(min(m, n))      |
| LIS (patience)               | O(n)       | O(log n)    | O(n log n) | O(n)            |
| 0/1 knapsack                 | O(nW)      | O(1)        | O(nW)    | O(W)              |
| Interval DP                  | O(n²)      | O(n)        | O(n³)    | O(n²)             |
| Bitmask DP (e.g. TSP)        | O(n · 2^n) | O(n)        | O(n² · 2^n) | O(n · 2^n)     |

"Space (optimized)" is what you get after the rolling-array trick
from `01-Fundamentals/space-optimization.py`.
