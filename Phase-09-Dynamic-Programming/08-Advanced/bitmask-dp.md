# Bitmask DP — Theory

**Bitmask DP** is the pattern where the state includes a BITMASK
(a single integer interpreted as a set of flags) indicating which
elements of some small universe have been "used", "selected", or
"visited".

Classic shape:

```
dp[mask][...] = optimum, considering the subset `mask` of items
```

Because an n-bit mask has `2^n` values, bitmask DP is only practical
for **small n** — typically n ≤ 20 or so. When the problem statement
says "n ≤ 20" (or "≤ 16" or "≤ 22"), that's the tell.

---

## The canonical example — Traveling Salesman

TSP: given n cities and pairwise distances, find the shortest
Hamiltonian cycle (visit every city exactly once, return to start).

**Brute force**: try every permutation — O(n!). Feasible for n ≤ 10.

**Bitmask DP** (Held-Karp, 1962):

    State:  dp[mask][i] = min cost to visit exactly the cities in `mask`,
                          ending at city `i`
    Base:   dp[{start}][start] = 0
    Trans.: dp[mask | {j}][j] = min over i in mask of (dp[mask][i] + d(i, j))
    Answer: min over i of (dp[full_mask][i] + d(i, start))

    Time: O(n² · 2^n)
    Space: O(n · 2^n)

For n = 20: 2^20 = ~10^6, so ~4 · 10^8 operations — tight but
possible. For n = 25: 2^25 · 25² = ~2 · 10^10, too slow.

This turns an O(n!) brute force into a polynomial-in-2^n algorithm —
still exponential, but TRACTABLE for small n where brute force isn't.

---

## When bitmask DP applies

Two signals:

1. **Small universe** — "n ≤ 16/20/22" constraints.
2. **Set-progression** — the natural state is "which subset have I
   handled?" rather than "how many". If counts alone are enough
   (subset sum, knapsack), you don't need bitmask DP.

Canonical use cases:

- **TSP and variants** — min/max Hamiltonian path, Chinese postman.
- **Assignment problems** — assign n workers to n tasks to minimize
  total cost.
- **Set-cover / partition problems** — cover all items with min number
  of subsets.
- **"Visit every" on a graph** — e.g. LC #847 Shortest Path Visiting
  All Nodes.
- **Exact-cover, graph coloring with small k**.
- **Game theory on small positions** — Nim-like games where game
  state is a small bitmask.

---

## Bitmask mechanics

You'll use these operations constantly. Fluency helps:

| Operation               | Code                          |
|-------------------------|-------------------------------|
| All bits set (size n)   | `(1 << n) - 1`                 |
| Set bit i               | `mask \| (1 << i)`              |
| Clear bit i             | `mask & ~(1 << i)`             |
| Toggle bit i            | `mask ^ (1 << i)`              |
| Test bit i              | `(mask >> i) & 1`              |
| Iterate over set bits   | `while mask: i = (mask & -mask).bit_length() - 1; mask &= mask - 1` |
| Count set bits          | `bin(mask).count('1')` or `mask.bit_count()` (Python 3.10+) |
| Iterate all sub-masks   | `sub = mask; while sub: yield sub; sub = (sub - 1) & mask` |

The sub-mask iteration is a classic — `(sub - 1) & mask` decrements
through every subset of `mask` in descending order. Used in
set-partition DPs.

---

## Time-complexity rule of thumb

With n elements and k extra state dimensions, bitmask DP is typically:

    O(2^n · n^k)

For n = 20, that's ~10^7 states — feasible. For n = 22, 2^22 · 22 ≈
10^8, borderline. For n = 25+, you need either:

- A smaller universe (partition into halves, meet in the middle).
- A different algorithm (approximation for TSP, etc.).
- A domain-specific pruning that drops many masks.

---

## Pitfalls

1. **Off-by-one on the mask**: n items → mask range 0 to (1 << n) - 1.
   The "full mask" is (1 << n) - 1, not (1 << n).

2. **Python int vs C int**: Python handles arbitrary-size ints, so
   n = 30 gives no overflow — but the 2^30 state space is too big.
   The language won't stop you, your runtime will.

3. **Memoization cache explosion**: `@cache` on a function with
   `(mask, other_args)` will happily fill gigabytes of memory if
   the state space is large. Prefer explicit arrays when you can.

4. **Iteration order**: for bottom-up tabulation, process masks in
   increasing popcount. Usually `for mask in range(1 << n)` works
   because a sub-mask `mask' ⊂ mask` has `mask' < mask`.

---

## What's in this module

- [traveling-salesman.py](traveling-salesman.py) — Held-Karp DP for
  the classic TSP problem, tested against brute-force permutations.
- [tree-dp.md](tree-dp.md) — DP on trees (a different kind of state-
  design problem), with LC #337 House Robber III as the worked example.

Bitmask DP appears in a handful of LC "hard" problems:
- LC #847 — shortest path visiting all nodes.
- LC #1125 — smallest sufficient team.
- LC #1349 — max students in a classroom.
- LC #1986 — min sessions to finish tasks.
