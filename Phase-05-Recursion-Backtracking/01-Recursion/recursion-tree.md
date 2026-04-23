# Recursion Trees — Visualizing Calls and Complexity

The **recursion tree** is the single most useful tool for reasoning
about a recursive algorithm's complexity. It's a picture — each node
is one invocation of the function, each edge is a recursive call.

Once you can draw the tree and count the work at each level, you can
derive the algorithm's Big-O without memorizing any theorems.

---

## The Anatomy of a Recursion Tree

Take the classic linear recursion:

```python
def sum_to(n):
    if n == 0:
        return 0
    return n + sum_to(n - 1)
```

Its recursion tree for `sum_to(4)`:

```
           sum_to(4)
               │
           sum_to(3)
               │
           sum_to(2)
               │
           sum_to(1)
               │
           sum_to(0)     ← base case
```

- **Height (depth):** 5 levels.
- **Nodes (total calls):** 5.
- **Work per node:** O(1) — one addition.
- **Total work:** O(n).

Linear recursion produces a **linear tree** (a chain). Every node has
exactly one child. Total work = depth × work-per-node.

---

## Binary / Tree Recursion

Now consider the classic exponential example:

```python
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
```

Its tree for `fib(5)`:

```
                         fib(5)
                        /      \
                    fib(4)      fib(3)
                   /    \      /    \
               fib(3)  fib(2) fib(2) fib(1)
              /    \    / \   / \
          fib(2) fib(1) …  …  …  …
          / \
      fib(1) fib(0)
```

- **Height:** n (linear in the input).
- **Branching factor:** 2 (two recursive calls per node).
- **Nodes:** ~2ⁿ (exponential).
- **Total work:** O(2ⁿ) — each node does O(1).

Exact count is closer to Fibonacci itself — about **1.618ⁿ** — but
the exponential-in-n bound is what matters.

This is WHY `fib(50)` takes forever: 2⁵⁰ ≈ 10¹⁵ operations.

Memoization collapses this tree: repeat subproblems (`fib(3)`
appears many times) get looked up instead of recomputed. The tree
becomes a straight chain again → O(n).

---

## Divide & Conquer — The Balanced Tree

Merge sort:

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)
```

Its tree for an array of length n:

```
                                 n
                                / \
                              n/2  n/2
                             / \   / \
                           n/4 n/4 n/4 n/4
                          ...
                      1 1 1 1 1 ... 1 1 1 1 1      (leaves)
```

- **Height:** log₂(n) levels (each split halves the input).
- **Nodes:** 1 + 2 + 4 + ... + n ≈ 2n (geometric series).
- **Work per LEVEL (not per node):** O(n) — the merge at each level
  processes every element of the current slice.
- **Total work:** log(n) levels × O(n) per level = **O(n log n)**.

The critical insight: **the work per LEVEL is constant at O(n)**,
and the number of levels is log n. That's how O(n log n) comes out
of a tree whose total node count is O(n).

---

## The Recursion-Tree Method for Complexity

For any recurrence `T(n) = a·T(n/b) + O(f(n))`, the recursion tree
looks like:

```
                             n            ← root: f(n) work
                          / / | \ \       ← a children, each of size n/b
                       ... ... ... ...    ← a² grandchildren of size n/b²
                      ...
                     ... ...              ← O(1) leaves at depth log_b(n)
```

- **Depth:** log_b(n)
- **Number of nodes at depth d:** aᵈ
- **Work per node at depth d:** f(n / bᵈ)
- **Work per level:** aᵈ · f(n / bᵈ)
- **Total work:** Σ_{d=0}^{log_b n} aᵈ · f(n / bᵈ)

Three cases, depending on which term dominates:

| Case                                       | Total complexity |
|--------------------------------------------|------------------|
| Work grows down the tree (leaves dominate) | O(n^(log_b a))   |
| Work is equal at every level (balanced)    | O(n^(log_b a) · log n) |
| Work shrinks down (root dominates)         | O(f(n))          |

This is the **Master Theorem**. It's much easier to derive by drawing
the tree than to memorize the three cases.

Example — merge sort's `T(n) = 2·T(n/2) + O(n)`:
- a = 2, b = 2, f(n) = n
- Work per level = 2ᵈ · (n / 2ᵈ) = n — CONSTANT per level.
- Case 2 applies → O(n log n).

---

## Common Recurrence Shapes

| Recurrence                        | Complexity      | Example                         |
|-----------------------------------|-----------------|---------------------------------|
| T(n) = T(n-1) + O(1)              | O(n)            | Linear recursion (sum, length)  |
| T(n) = T(n-1) + O(n)              | O(n²)           | Selection sort recursion        |
| T(n) = 2·T(n-1) + O(1)            | O(2ⁿ)           | Tower of Hanoi, naive subsets   |
| T(n) = 2·T(n/2) + O(1)            | O(n)            | Max element via D&C             |
| T(n) = 2·T(n/2) + O(n)            | O(n log n)      | Merge sort                      |
| T(n) = T(n/2) + O(1)              | O(log n)        | Binary search                   |
| T(n) = T(n/2) + O(n)              | O(n)            | Median of medians preprocessing |
| T(n) = T(n-1) + T(n-2) + O(1)     | O(φⁿ) ≈ O(1.618ⁿ) | Naive Fibonacci               |

Every recursive algorithm you'll write fits into (or combines) one
of these shapes.

---

## How to Draw a Recursion Tree Quickly

Three steps:

1. **Identify the recurrence.** Write down T(n) in terms of smaller T's.
2. **Draw the root and its children.** One child per recursive call,
   each labeled with its reduced input.
3. **Count work per level.** Multiply work-per-node × nodes-per-level.

Stop drawing once the pattern is clear (usually by level 3). The
total is the sum of the work across all levels.

For quick sanity checks, run the recursion on small n and COUNT the
calls. If the call count grows as 2ⁿ, the algorithm is exponential.
If it grows as n log n, it's divide-and-conquer.

---

## Why This Matters

When you see a recursive function, the question "is this fast?" is
usually answered by drawing the recursion tree for small n and
checking:

1. **How many leaves are there?** (Is growth linear? polynomial?
   exponential?)
2. **Are subproblems repeated?** (If yes, memoize.)
3. **Is the tree balanced or skewed?** (Balanced → log-factor;
   skewed → no log factor, just linear depth.)

Those three observations cover most analysis. The formal Master
Theorem is a shortcut to write down the answer once you've seen the
tree.

---

## Worked Example — Why `fib(n)` Without Memoization Is Unusable

`fib(30)` makes roughly **2.7 million** calls. `fib(40)` makes
**300 million**. `fib(50)` — about **40 billion**.

Draw just the top three levels of `fib(5)`:

```
                    fib(5)
                   /      \
               fib(4)      fib(3)
              /    \      /    \
          fib(3)  fib(2) fib(2) fib(1)
```

Notice `fib(3)` appears twice at depth 2, and `fib(2)` appears three
times. Each of these duplicated subtrees is being recomputed from
scratch. That's the signature of an algorithm that needs
memoization.

Add memoization → the redundant subtrees collapse to O(1) lookups →
total work drops to O(n).

This is the "why" behind dynamic programming, covered in Phase 02 /
01 / 04.

---

## Key Takeaways

1. **The recursion tree IS the algorithm's complexity.** Draw the
   tree; count the work.
2. **Linear recursion** = chain = O(depth) × O(work per node).
3. **Binary / tree recursion** = exponential unless subproblems
   overlap and we memoize.
4. **Divide & conquer** = balanced tree = log(n) levels of O(f(n))
   work each.
5. **Memoization collapses exponential trees to linear**, turning
   backtracking into DP.
6. **The Master Theorem is a shortcut; the recursion-tree method
   always works.**

Now that we can VISUALIZE recursion, see [`patterns/`](patterns/)
for the four archetypal recursion shapes, each with runnable
examples.
