# DP Patterns — Field Guide

Most DP problems are not new. They're variations on about eight recurring
*shapes* — the patterns in this document. Once you can name the pattern a
problem belongs to, the recurrence almost writes itself.

> This is a **reference**, not a tutorial. Work through the problems in
> [`problems/`](problems/) first, then come back here to see how the
> individual problems fit into the broader families.

---

## Quick Map

| # | Pattern                 | Shape of `dp`                 | Work per state | Canonical problems                                 |
|---|-------------------------|-------------------------------|----------------|----------------------------------------------------|
| 1 | **1D sequence DP**      | `dp[i]` over an array/number  | O(1)           | Fibonacci, climbing stairs, house robber           |
| 2 | **Grid DP**             | `dp[i][j]` over a 2D grid     | O(1)           | Unique paths, min path sum                         |
| 3 | **Two-sequence DP**     | `dp[i][j]` — indices in two strings | O(1)     | LCS, edit distance, regex matching                 |
| 4 | **Knapsack DP**         | `dp[i][w]` over items × capacity | O(1)         | 0/1 knapsack, coin change, subset sum              |
| 5 | **Interval DP**         | `dp[i][j]` over a range       | O(j - i)       | Matrix-chain multiplication, burst balloons        |
| 6 | **State-machine DP**    | `dp[i][state]` — states per step | O(#states)  | Stock problems, paint-fence variants                |
| 7 | **Bitmask DP**          | `dp[mask]` or `dp[i][mask]`   | O(n)           | TSP, assignment, "smallest subset covering …"      |
| 8 | **Tree DP**             | `dp[node]` via post-order     | O(children)    | Diameter of tree, house robber III                 |

---

## 1. 1D Sequence DP

**Shape:** you're walking a sequence and the answer at position `i` depends
only on a small window of earlier positions.

```
dp[i] = f(dp[i-1], dp[i-2], …, input[i])
```

**Space-optimization:** almost always possible — keep only as many previous
values as the recurrence reads.

### Fibonacci
```
dp[i] = dp[i-1] + dp[i-2]
```

### Climbing Stairs (reach step n taking 1 or 2 at a time)
```
dp[i] = dp[i-1] + dp[i-2]       # same recurrence as Fibonacci, different base
```

### House Robber (max money, no two adjacent houses)
```
dp[i] = max(dp[i-1],             # skip house i
            dp[i-2] + nums[i])   # take house i
```

### Longest Increasing Subsequence (LIS) — O(n²) version
```
dp[i] = 1 + max(dp[j] for j < i if nums[j] < nums[i])
```

All of these share a skeleton: scan the array, update `dp[i]` from a small
number of prior entries, return `dp[n-1]`.

---

## 2. Grid DP

**Shape:** a 2D grid where each cell's answer depends on its neighbours
(usually top + left, sometimes all four).

```
dp[i][j] = f(dp[i-1][j], dp[i][j-1], grid[i][j])
```

**Space-optimization:** often reducible from O(m·n) to O(n) by keeping
only the previous row.

### Unique Paths (count lattice paths from top-left to bottom-right)
```
dp[i][j] = dp[i-1][j] + dp[i][j-1]
```

### Minimum Path Sum
```
dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])
```

### Maximum Square of 1's in a binary matrix
```
if grid[i][j] == 1:
    dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
else:
    dp[i][j] = 0
```

---

## 3. Two-Sequence DP

**Shape:** you're comparing two sequences (strings, arrays). State indexes
into both.

```
dp[i][j] = f(characters s1[i], s2[j])  and neighbours dp[i-1][j], dp[i][j-1], dp[i-1][j-1]
```

**Space-optimization:** reducible to O(min(n, m)) by keeping two rows.

### Longest Common Subsequence (LCS)
```
if s1[i-1] == s2[j-1]:
    dp[i][j] = 1 + dp[i-1][j-1]
else:
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```

### Edit Distance (min inserts/deletes/replaces to transform s1 → s2)
```
if s1[i-1] == s2[j-1]:
    dp[i][j] = dp[i-1][j-1]
else:
    dp[i][j] = 1 + min(dp[i-1][j],      # delete
                       dp[i][j-1],      # insert
                       dp[i-1][j-1])    # replace
```

### Regular Expression Matching (with `.` and `*`)

Same 2D shape; transitions are conditioned on `pattern[j-1]`.

---

## 4. Knapsack DP

**Shape:** a set of items, each with some cost; you're choosing a subset
to optimize value under a capacity constraint.

```
dp[i][w] = max(dp[i-1][w],                            # don't take item i
               dp[i-1][w - weight[i]] + value[i])     # take it (0/1 knapsack)
```

**Space-optimization:** almost always possible. For 0/1 knapsack, a 1D
array iterated right-to-left. For unbounded (coin change), left-to-right.

### 0/1 Knapsack (each item 0 or 1 time)
Above recurrence directly.

### Unbounded Knapsack (use each item any number of times)
```
dp[w] = max(dp[w - weight[i]] + value[i] for every i if weight[i] <= w)
```

### Coin Change (minimum coins summing to amount)
```
dp[x] = min(dp[x - coin] + 1 for coin in coins if coin <= x)
dp[0] = 0
```

### Subset Sum (can we make some exact target?)
```
dp[i][s] = dp[i-1][s] or dp[i-1][s - nums[i]]
```

This family is the most common DP pattern in interviews. Master it and
you've taken out a big chunk of the territory.

---

## 5. Interval DP

**Shape:** you're choosing how to split a range `[i, j]` into smaller
ranges. The state is the range itself.

```
dp[i][j] = best over all split points k:
              combine(dp[i][k], dp[k+1][j]) + cost(i, k, j)
```

**Loop order:** fill by *length* of interval — shortest first, then longer.

### Matrix-Chain Multiplication
Minimize the number of scalar multiplications to multiply A₁ × A₂ × … × Aₙ.
```
dp[i][j] = min over k in (i..j-1):
              dp[i][k] + dp[k+1][j] + p[i-1] * p[k] * p[j]
```

### Burst Balloons (LeetCode #312)
Think of bursting *last*, not first.
```
dp[i][j] = max over k in (i+1..j-1):
              dp[i][k] + dp[k][j] + nums[i]*nums[k]*nums[j]
```

Interval DP is harder than most patterns because the "choose a split point"
step enumerates O(n) options per state, giving O(n³) total — that's the
price of considering all possible partitions.

---

## 6. State-Machine DP

**Shape:** at each step you're in one of a finite number of *states*
(e.g., holding a stock, not holding it, in cooldown). Transitions between
states have well-defined costs.

```
dp[i][state] = best over transitions:
                 dp[i-1][prev_state] + transition_cost
```

**Space-optimization:** roll by step, keeping only the previous step's
states.

### Best Time to Buy and Sell Stock (with cooldown)
States: `held`, `not_held_in_cooldown`, `not_held_free`.
```
held[i]     = max(held[i-1], free[i-1] - prices[i])
cooldown[i] = held[i-1] + prices[i]
free[i]     = max(free[i-1], cooldown[i-1])
```

### Paint Fence / Paint House

Finite colour choices per step with "no two adjacent" constraints are
textbook state-machine DP.

---

## 7. Bitmask DP

**Shape:** the state includes a *subset* of something, encoded as an
integer's bits. Each bit = "element k is included/visited".

```
dp[mask] = best over all elements k in mask:
             dp[mask \ {k}] + cost(k, mask)
```

**Use when:** `n` is small (≤ ~22) and the problem seems to demand
considering every subset.

### Traveling Salesman Problem (TSP)
```
dp[mask][i] = min cost path that visits exactly the cities in `mask`
              and ends at city i

dp[mask][i] = min over j in mask \ {i}:
                 dp[mask \ {i}][j] + distance(j, i)
```

Complexity: O(n² · 2ⁿ). Dramatically better than the O(n!) brute force,
but still exponential. Useful up to n ≈ 20.

### Smallest Set Cover via Bitmask

Same idea: mask represents which sets have been picked / elements covered.

---

## 8. Tree DP

**Shape:** the state is a node; the answer at each node is computed from
the answers of its children (post-order).

```
def dfs(node):
    child_answers = [dfs(c) for c in node.children]
    return combine(child_answers, node.value)
```

**Space-optimization:** usually not needed — the tree has O(n) nodes and
each is visited once.

### Diameter of a Binary Tree
For each node, compute `left_depth + right_depth + 1`; track the maximum.

### House Robber III (tree variant)
For each node, return two values:
- Max money if we rob this node (children must be skipped).
- Max money if we skip this node (children can freely rob or skip).

### Longest Path in a Tree / Max Path Sum
Same shape: two returns per node — "best path ending at me" and "best
path passing through me".

---

## How to Recognize the Pattern

Ask yourself these questions in order:

1. **One sequence or two?** One → pattern 1 or 4. Two → pattern 3.
2. **Grid?** → pattern 2.
3. **Choosing items with a constraint?** → knapsack (4).
4. **"Pick a split point / order"?** → interval DP (5).
5. **Finite states at each step?** → state-machine DP (6).
6. **Small `n` and "try every subset"?** → bitmask DP (7).
7. **Input is a tree?** → tree DP (8).

Most problems will match more than one of these — the easiest match is
usually the right one.

---

## Tips That Apply Across All Patterns

- **Start top-down.** Write the recurrence as a recursive function with a
  cache. Rewrite bottom-up later if you need the performance or space
  optimization.
- **Draw the DP table.** For 2D problems, literally draw a small table
  and fill in three or four cells by hand. The pattern of dependencies
  tells you the correct loop order.
- **Validate on small inputs against brute force.** If your DP disagrees
  with brute force on n = 5, your recurrence is wrong. Fix it before
  writing more tests.
- **Look for redundancy in a slow solution first.** DP doesn't appear
  from nowhere — it appears when you notice "I'm computing the same thing
  over and over". That observation IS the recurrence.
- **Name your state carefully.** `dp[i][j]` is less helpful than
  `min_cost_using_first_i_items_with_capacity_j`. Use long names during
  derivation; shorten for the final code.

---

## When to Stop

DP has diminishing returns. At some point you should read real problems
and let the patterns emerge, rather than memorizing theory. Good next
steps:

- Do the two problems in [`problems/`](problems/): fibonacci (1D) and
  0/1 knapsack (2D). These cover the two most common shapes.
- Then graduate to a DP list (LeetCode's "top 100 dynamic programming
  problems", or a DP-focused text). Most "new" DP problems are variants
  of patterns 1–4.
- Come back to patterns 5–8 only after the first four feel routine.
