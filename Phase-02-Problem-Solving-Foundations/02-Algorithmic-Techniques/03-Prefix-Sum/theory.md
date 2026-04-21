# Prefix Sum — Theory

## Introduction

**Prefix Sum** is the simplest preprocessing trick in the algorithms
toolbox — and one of the most consistently useful.

The idea:

> *Instead of recomputing a range sum every time it's asked, precompute
> every cumulative sum once. Then any range sum is the difference of
> two precomputed values.*

That's the whole technique. The elegance is in what it unlocks:

- **O(1) range sums** on an immutable array, after O(n) preprocessing.
- **O(n) subarray-sum-equals-K** via prefix sum + hashing.
- **O(1) 2D range sums** on a grid, after O(m·n) preprocessing.
- Generalizes to **any associative operation** — XOR, product, min if
  augmented, etc. — not just sum.

The cost is O(n) extra space, which is almost always acceptable.

---

## The Core Idea

Given an array `arr[0..n-1]`, define:

```
prefix[i] = arr[0] + arr[1] + ... + arr[i-1]     for i in 0..n
```

So `prefix[0] = 0` (empty prefix), `prefix[n]` is the total sum.

Then the sum of any range `arr[L..R]` (inclusive) is:

```
range_sum(L, R) = prefix[R+1] - prefix[L]
```

One subtraction. That's it. No loop, no scan.

### Why the +1 offset?

The convention of `prefix[i] = sum(arr[0..i-1])` (length i) means:

- `prefix[0] = 0` — no ambiguity for the empty prefix.
- `range_sum(L, R) = prefix[R+1] - prefix[L]` — no off-by-one.

Some books define `prefix[i] = sum(arr[0..i])` instead. Either works,
but the **off-by-one offset** form is cleaner for range queries and is
the convention used throughout this repo.

---

## A Quick Example

```
arr     = [3, 1, 4, 1, 5, 9, 2, 6]

prefix  = [0, 3, 4, 8, 9, 14, 23, 25, 31]
           ↑  ↑  ↑  ↑  ↑   ↑   ↑   ↑   ↑
         pref[0..8], one longer than arr

range_sum(2, 5) = arr[2] + arr[3] + arr[4] + arr[5]
                = 4 + 1 + 5 + 9
                = 19

Same as:
range_sum(2, 5) = prefix[6] - prefix[2]
                = 23 - 4
                = 19                ✓
```

---

## When to Reach for Prefix Sum

Strong signals:

1. **Many range-sum queries on the same (immutable) array.** If the
   array never changes and you're asked "sum from L to R" more than
   a handful of times, prefix sum is the default answer.
2. **You need to find subarrays with a specific sum.** Combining prefix
   sum with hashing turns this into an O(n) problem.
3. **2D version — many range sums on a fixed grid.** The 2D prefix sum
   trick handles this in O(m·n) preprocessing + O(1) per query.
4. **You're doing something that factors through "sum from 0 to i"** —
   cumulative counts, running balances, running products.

Weak signals:

5. **The array is mostly immutable but needs occasional updates.** At
   some point a Fenwick / Segment tree is faster (log n per update
   and query). Prefix sum is a good baseline to check before reaching
   for those.

---

## Prefix Sum + Hashing — The Real Unlock

The single most important application of prefix sum beyond plain range
queries is:

> **"Count the number of contiguous subarrays whose sum equals K."**

Given prefix sums, `range_sum(L, R) = prefix[R+1] - prefix[L]`. We want
this to equal K, so:

```
prefix[R+1] - prefix[L] = K
prefix[L]               = prefix[R+1] - K
```

So for each position `R`, we want to count how many previous positions
`L` had `prefix[L] = prefix[R+1] - K`. That's a classic hash-map lookup
— see Phase-02 / 01 / 04-Dynamic-Programming knapsack or 07-Hashing-Technique.

This converts an O(n²) brute-force "sum every subarray" into **O(n)**.
It is one of the most important three-line tricks in algorithmic
programming.

---

## The 2D Prefix Sum

For a grid `A[i][j]` (m × n), define:

```
prefix[i][j] = sum of all cells in the rectangle
               with rows in [0..i-1] and columns in [0..j-1]
```

Built in O(m·n) via inclusion-exclusion:

```
prefix[i][j] = A[i-1][j-1]
             + prefix[i-1][j]
             + prefix[i][j-1]
             - prefix[i-1][j-1]       ← subtract the double-counted overlap
```

Then any sub-rectangle sum `sum(A[r1..r2, c1..c2])` comes out in O(1):

```
rect_sum = prefix[r2+1][c2+1]
         - prefix[r1][c2+1]
         - prefix[r2+1][c1]
         + prefix[r1][c1]              ← add back the twice-subtracted overlap
```

The inclusion-exclusion principle is the whole algorithm. Draw a picture;
it's very visual.

---

## Generalization — Any Associative Operation

Prefix sum is often called "prefix sum", but really the technique works
for any **associative operation with an identity**:

| Operation | Identity   | "Range query" becomes                     |
|-----------|------------|--------------------------------------------|
| +         | 0          | `prefix[R+1] - prefix[L]` (invertible)    |
| ×         | 1          | `prefix[R+1] / prefix[L]` (if no zeros)   |
| XOR       | 0          | `prefix[R+1] ^ prefix[L]` (self-inverse)  |
| min / max | ±∞         | Must use a sparse table / segment tree; not subtractable |

The key requirement is that the operation is **invertible** in some
sense — so you can "undo" the prefix up to index L. Sum and XOR work
cleanly; min and max don't, which is why they need different data
structures.

---

## Prefix Sum vs Related Techniques

| Technique          | Use case                                     | Cost                    |
|--------------------|----------------------------------------------|-------------------------|
| **Prefix Sum**     | Many **range sum** queries on **immutable** array | O(n) setup, O(1) query |
| Sliding Window     | Running window over contiguous range         | O(n) total              |
| Difference Array   | Many **range updates** on immutable array    | O(n) setup, O(1) update, O(n) materialize |
| Fenwick / Segment  | Mixed **updates + queries**                  | O(log n) per operation  |

Prefix Sum and Difference Array are **duals** of each other:

- Prefix Sum optimizes *queries*.
- Difference Array optimizes *updates*.

If you're doing many queries on a fixed array → prefix sum. If you're
doing many range updates and then one scan → difference array (next
module). If both → Fenwick tree (beyond Phase 02).

---

## Complexity

- **Preprocessing:** O(n) time, O(n) space (the prefix array).
- **Per-query:** O(1) time for a range sum.
- **Total cost for Q queries:** O(n + Q).

Compared to the naive "sum in a loop per query", which is O(n · Q),
the speedup is dramatic when Q is large.

---

## Common Pitfalls

- **Off-by-one on the prefix index.** The most common bug in this
  technique. Remember: with the convention `prefix[0] = 0`,
  `range_sum(L, R) = prefix[R+1] - prefix[L]`. Draw a small example
  if you're unsure.
- **Modifying the original array after building prefix.** The prefix
  becomes stale. If the array changes often, use a Fenwick tree.
- **Confusing L and R conventions.** `arr[L..R]` can mean "inclusive
  on both ends" or "inclusive of L, exclusive of R" depending on the
  source. Pick one convention and stay with it.
- **Using a list instead of an int for prefix_so_far in streaming
  problems.** In the "subarray sum equals K" problem, you only need
  the RUNNING prefix sum — not the whole array. Keep it as a single
  int.
- **Forgetting `prefix_count[0] = 1` for the subarray-sum problem.**
  The initial (empty) prefix has value 0 and must be counted once —
  otherwise subarrays starting at index 0 are missed.

---

## Canonical Examples

### Range Sum Query (Immutable) — LeetCode #303

Build `prefix` once; each `sumRange(L, R)` returns `prefix[R+1] - prefix[L]` in O(1).

### Range Sum Query 2D (Immutable) — LeetCode #304

The 2D prefix-sum construction above; each query is four lookups + two adds + one subtract.

### Subarray Sum Equals K — LeetCode #560

Streaming prefix sum + hash map of prefix-sum frequencies. O(n) time.

### Count of Subarrays Divisible by K — LeetCode #974

Same pattern as #560, but keyed on `prefix_sum % k`.

### Find Pivot Index — LeetCode #724

Find an index where left_sum == right_sum. Both sides in O(1) using the prefix.

These five problems all dissolve into one-or-two liners once you have
the prefix array in hand.

---

## Key Takeaways

1. **Prefix Sum turns O(n) range queries into O(1) after O(n)
   preprocessing.** That's its whole job.
2. **The convention `prefix[0] = 0; prefix[i] = sum(arr[0..i-1])`**
   gives clean off-by-ones: `range_sum(L, R) = prefix[R+1] - prefix[L]`.
3. **Prefix Sum + Hashing** is the O(n) solution to "count subarrays
   with sum K". One of the most important three-line tricks in
   interviews.
4. **2D prefix sum** works by inclusion-exclusion. Draw the rectangles.
5. **The operation must be invertible** — sum, XOR work; min, max don't.

For the template, see [`template.py`](template.py). For the two most
important applications, see [`problems/`](problems/).
