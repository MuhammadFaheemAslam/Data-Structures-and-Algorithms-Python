# Knapsack — Theory

The **knapsack problem** is the archetypal "pick a subset of items
under a capacity constraint, maximize something" problem. It shows
up disguised dozens of ways on LeetCode, and recognizing that a
problem IS knapsack in disguise is the whole game.

---

## The canonical statement

Given `n` items, each with a **weight** `w[i]` and a **value**
`v[i]`, and a capacity `W`, pick a subset of items such that:

- Total weight ≤ W.
- Total value is maximized.

Two main variants:

| Variant              | Each item...        | Example                          |
|----------------------|---------------------|----------------------------------|
| **0/1 knapsack**     | taken 0 or 1 times  | pack a backpack (unique items)   |
| **Unbounded**        | taken any # times   | coin change (LC #322, LC #518)   |

Together these cover maybe 30% of "hard" DP problems, even when the
word "knapsack" never appears.

---

## 0/1 knapsack

### State

    dp[i][c] = max value using items 0..i-1, with capacity ≤ c.

### Transition

Two choices for item i-1:

    Skip it:   dp[i][c] = dp[i-1][c]
    Take it:   dp[i][c] = dp[i-1][c - w[i-1]] + v[i-1]    (only if c >= w[i-1])

Take the better of the two:

    dp[i][c] = max(skip, take)

### Time / Space

    Time:  O(n · W)
    Space: O(n · W) — then O(W) with the rolling-row optimization.

### Space optimization: iterate c BACKWARDS

When rolling the 2D dp down to a single 1D array indexed by capacity,
iterate `c` from W down to w[i]:

    for i in 0..n-1:
        for c in W..w[i]:                         # BACKWARDS
            dp[c] = max(dp[c], dp[c - w[i]] + v[i])

The reverse order ensures we use `dp[c - w[i]]` from the PREVIOUS
iteration (item not yet taken) — same as `dp[i-1][c - w[i]]`. If we
iterated forward, we'd double-count and land in "unbounded" territory
(see below).

---

## Unbounded knapsack

### State

    dp[c] = max value with capacity ≤ c (items can be reused).

### Transition

    dp[c] = max over all items i: dp[c - w[i]] + v[i]

or equivalently, iterate items outside and capacity FORWARD:

    for each item i:
        for c in w[i]..W:                         # FORWARD
            dp[c] = max(dp[c], dp[c - w[i]] + v[i])

Note: the ONLY difference from 0/1 knapsack with 1D dp is the loop
direction of `c`. Forward → unbounded; backward → 0/1. Minor syntax,
completely different semantics.

### Time / Space

    Time:  O(n · W)
    Space: O(W)

---

## Recognizing knapsack in the wild

Many problems are knapsack in disguise. The tell:

- There's a FIXED BUDGET (total weight, sum, length, count).
- Each item has a COST and a VALUE (value can be "1" for counting).
- You want to MAXIMIZE or MINIMIZE something subject to the budget.

Classic disguises:

| Problem                                   | Items are…               | Budget is…          |
|-------------------------------------------|--------------------------|---------------------|
| LC #416 Partition Equal Subset Sum        | array values             | sum / 2             |
| LC #494 Target Sum                        | array values ± signed    | target              |
| LC #474 Ones and Zeroes                   | strings with (#0s, #1s)  | (m zeros, n ones)   |
| LC #518 Coin Change II (combinations)     | coins                    | amount              |
| LC #322 Coin Change (min coins)           | coins                    | amount              |
| LC #139 Word Break                        | dictionary words         | string length       |
| LC #1049 Last Stone Weight II             | stones                   | sum / 2             |

For each: "max value with budget ≤ B" becomes "can I reach sum B
with these items?", or "count ways to reach B", or "fewest items
summing to B". Same skeleton.

---

## Memoization vs tabulation

Both work. The **interview answer is usually tabulation** because:

1. Space optimization is natural (1D rolling array).
2. No recursion-depth worries.
3. The bottom-up order exposes the structure.

Memoization is often shorter to WRITE — a straight translation of
the recursive definition. If the problem has a sparse state space
(most states never reached), memoization can also be asymptotically
faster.

---

## What's in this module

- [0-1-knapsack.py](0-1-knapsack.py) — the classic, with both 2D and 1D-rolling implementations.
- [unbounded-knapsack.py](unbounded-knapsack.py) — items can be reused.
- [partition-equal-subset-sum.py](partition-equal-subset-sum.py) — LC #416, disguised 0/1.
- [target-sum.py](target-sum.py) — LC #494, convert to 0/1 subset-sum via ±math.
