# Interval DP — Theory

**Interval DP** is the pattern where the state is a RANGE `[l, r]`
over the input, and the transition is "pick a split point `k` inside
the range". These problems all have the shape:

> To solve the range `[l, r]`, try every split, solve the two halves
> optimally, then combine.

```
    dp[l][r] = best over all k in [l..r-1] of:
        combine(dp[l][k], dp[k+1][r], l, k, r)
```

The `O(n)` inner loop over splits, combined with `O(n²)` ranges,
gives the classic **O(n³)** time complexity. That's the cost of
interval DP — cubic in the problem size.

---

## The telltale shapes

Interval DP is the right tool when the problem involves:

- **Splitting into two halves** at an arbitrary break point.
- **"Last operation" semantics** where the last thing you do in
  range `[l, r]` pairs with a specific `k`.
- **Associativity** of the operation being optimized (can reorder
  the pairings).

Classic examples:

| Problem                                 | Split semantics                    |
|-----------------------------------------|------------------------------------|
| Matrix Chain Multiplication             | `k` = last matrix multiplication position |
| Burst Balloons (LC #312)                | `k` = LAST balloon to burst in range |
| Palindrome Partitioning (LC #132)       | `k` = start of the last palindrome slice |
| Optimal BST construction                | `k` = root choice                  |
| Minimum cost of adding a knot to a rope | `k` = first cut                    |

---

## Filling order

The tricky part: for `dp[l][r]` to know its smaller subproblems, we
need to compute SHORTER ranges first. Iterate by LENGTH:

```python
for length in range(1, n + 1):
    for l in range(n - length + 1):
        r = l + length - 1
        # try every split point k
        dp[l][r] = min(
            dp[l][k] + dp[k+1][r] + cost(l, k, r)
            for k in range(l, r)
        )
```

Outer loop = range length. Inner = starting index. Innermost = split
point. This guarantees every `dp[l][k]` and `dp[k+1][r]` is already
populated before we use them.

---

## Base cases

Length-1 ranges are trivially solvable and need to be seeded. For
Burst Balloons: `dp[l][l] = nums[l - 1] * nums[l] * nums[l + 1]`
(a single balloon's pop cost). For Matrix Chain: `dp[l][l] = 0`
(a single matrix needs zero multiplications).

The "length 0 / 1" initialization is where most bugs live — worth
writing out explicitly before coding the main recurrence.

---

## When interval DP doesn't work

Interval DP assumes a KEY PROPERTY: the choice of split point `k`
leaves the two sides INDEPENDENT. In burst balloons, for example,
once we decide `k` is the last balloon to burst, the left and right
halves become independent sub-problems (because by the time we
reach `k`, the outer boundaries are `l-1` and `r+1`, unchanged).

When the halves AREN'T independent — when choices on the left side
affect choices on the right — interval DP fails. You need extra
state to carry that cross-range information, which explodes the
complexity. Such problems often need bitmask DP instead.

---

## Complexity summary

Most interval-DP problems:

    Time:  O(n³)
    Space: O(n²)

For very specific structures (monotone interval DP with
**Knuth's optimization** or **divide-and-conquer optimization**),
the inner loop over `k` can be reduced to amortized O(log n) or
eliminated, giving O(n² log n) or O(n²). Knuth's condition requires
the cost function to satisfy the "quadrangle inequality". This is
rare in practice but shows up in:

- Optimal binary search tree (Knuth, 1971) — O(n²)
- Matrix-chain with special structure
- Some interval scheduling problems

We don't cover Knuth's optimization in this module. If you see
"interval DP with n ≈ 10⁴ and TLE on n³", that's the hint to look
it up.

---

## What's in this module

- [matrix-chain-multiplication.py](matrix-chain-multiplication.py) — the textbook interval-DP example.
- [burst-balloons.py](burst-balloons.py) — LC #312 with the "reverse the burst order" twist.
- [palindrome-partitioning.py](palindrome-partitioning.py) — LC #132, min cuts to get all palindromes.
