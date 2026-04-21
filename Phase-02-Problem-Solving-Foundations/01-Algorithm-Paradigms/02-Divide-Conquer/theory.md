# Divide & Conquer — Theory

## Introduction

**Divide & Conquer** is the first paradigm that beats brute force by exploiting
*structure*: it notices that some problems can be cut in half, solved on each
half independently, and then stitched back together — and that the stitching
is often dramatically cheaper than solving the whole problem at once.

If brute force says *"try every possibility"*, Divide & Conquer says:

> *"Break the problem into smaller versions of itself, solve those, and
> combine their answers."*

This is the paradigm behind merge sort, quicksort, binary search, the
Fast Fourier Transform, Karatsuba multiplication, and the closest-pair-of-points
algorithm. Any time you see complexity of the form **O(n log n)** or
**T(n) = 2·T(n/2) + O(n)**, Divide & Conquer is almost always the reason.

---

## The Divide & Conquer Recipe

Every D&C algorithm has exactly three steps:

1. **Divide** — Split the input into smaller subproblems of the *same shape*.
2. **Conquer** — Solve each subproblem (usually by recursing).
3. **Combine** — Merge the subproblem solutions into a solution for the whole.

The art of Divide & Conquer is almost entirely in step 3. If the combine step
is trivial, the algorithm is fast. If it's expensive, D&C may not help at all.

```
function divide_and_conquer(problem):
    if problem is small enough:
        return solve_directly(problem)              # base case

    subproblems = divide(problem)                   # step 1
    sub_solutions = [divide_and_conquer(p)          # step 2
                     for p in subproblems]
    return combine(sub_solutions)                   # step 3
```

---

## The Three Parts, In Detail

### 1. Divide

Most D&C algorithms split the problem into **two halves**, but that's a
convention — not a rule. Binary search splits into one half (the other is
thrown away). FFT splits into two halves of the same size. The closest-pair
algorithm splits into left and right point sets.

What matters is that the subproblems are:

- **Smaller** than the original (otherwise you infinite-loop).
- **The same shape** as the original (so you can recurse into them).
- **Independent** of each other (no shared state).

That last property — **independence** — is what separates Divide & Conquer
from Dynamic Programming. In D&C subproblems don't overlap; they're solved
once, used once, and discarded. If they *did* overlap, you'd want DP.

### 2. Conquer

Recurse on each subproblem. The magic is that you don't have to think
about *how* the recursion works — you only have to trust that the same
function, called on a smaller input, returns a correct answer.

When the subproblem is small enough to solve directly (one element, empty
range, known formula), you hit the **base case** and return immediately.

### 3. Combine

This is where all the work happens. The speed of the whole algorithm
depends on how cheap the combine step is:

- **O(n) combine** (merge sort, closest pair): gives T(n) = 2·T(n/2) + O(n) = **O(n log n)**.
- **O(1) combine** (binary search): gives T(n) = T(n/2) + O(1) = **O(log n)**.
- **Expensive combine** (≥ O(n²)): the combine dominates and D&C gives
  no improvement over brute force. Look for a different paradigm.

---

## Complexity: The Master Theorem (Informal)

For a recurrence of the form:

> **T(n) = a · T(n/b) + O(n^d)**

where `a` is the number of subproblems, `b` is the factor by which each
subproblem shrinks the input, and `O(n^d)` is the combine cost:

| Case                        | Total Complexity      | Intuition                                |
|-----------------------------|-----------------------|------------------------------------------|
| `d > log_b(a)`              | **O(n^d)**            | Combine dominates.                       |
| `d == log_b(a)`             | **O(n^d · log n)**    | Work balanced at every level.            |
| `d < log_b(a)`              | **O(n^(log_b a))**    | Leaf work (base cases) dominates.        |

Most classical D&C algorithms fall into the balanced case. For example:

| Algorithm      | a | b | d | Recurrence              | Complexity   |
|----------------|---|---|---|-------------------------|--------------|
| Merge sort     | 2 | 2 | 1 | T(n) = 2T(n/2) + O(n)   | O(n log n)   |
| Binary search  | 1 | 2 | 0 | T(n) = T(n/2) + O(1)    | O(log n)     |
| Karatsuba      | 3 | 2 | 1 | T(n) = 3T(n/2) + O(n)   | O(n^log₂3) ≈ O(n^1.585) |
| Strassen (matrix mult) | 7 | 2 | 2 | T(n) = 7T(n/2) + O(n²) | O(n^log₂7) ≈ O(n^2.807) |

You don't need to memorize the Master Theorem — just recognize the pattern.
Most of the time you can read the complexity straight off the recursion tree.

---

## Recursion Tree Intuition

For merge sort:

```
                    T(n)             ← O(n) work to merge
                   /    \
                T(n/2)  T(n/2)       ← O(n/2) work each → O(n) total
                / \      / \
              T(n/4) ... T(n/4)      ← O(n/4) * 4 = O(n) total
                 ...
                  T(1) ... T(1)      ← O(1) * n = O(n) total
```

- Each **level** does O(n) total work.
- There are **O(log n) levels** (halving until size 1).
- Total: **O(n · log n)**.

Once you see this picture, most D&C complexities become obvious at a glance.

---

## When Divide & Conquer Wins

D&C is the right paradigm when:

1. **The problem decomposes cleanly.** Sort, search, range queries, geometric
   closest-pair, polynomial multiplication.
2. **Subproblems are independent** (no shared work). If the same subproblem
   appears twice, use DP instead.
3. **The combine step is cheap** — ideally O(n) or less. If combining is
   expensive, D&C might be slower than an iterative approach.
4. **You want good constant factors AND good asymptotics.** Merge sort is
   slower than quicksort *on cache-friendly inputs* despite having the same
   Big-O — but it has guaranteed O(n log n) and is stable.

---

## When Divide & Conquer Loses

D&C is a poor fit when:

1. **Subproblems overlap** → you're doing redundant work. Use DP and
   memoize the results.
2. **The combine step is as expensive as the original problem** → recursion
   gives you nothing. Think carefully about whether "divide" actually made
   progress.
3. **Input is small** → the function-call overhead of recursion can dominate
   the actual work. Many production D&C implementations switch to an
   iterative algorithm (e.g., insertion sort) once the subproblem is
   smaller than ~16 elements.
4. **You need to process the input in order with state** → D&C's subproblems
   are solved in isolation, which is the wrong shape.

---

## Divide & Conquer vs Related Paradigms

| Paradigm         | Subproblems     | Shared answers? | Combine?   | Typical complexity   |
|------------------|-----------------|-----------------|------------|----------------------|
| Brute force      | n/a             | n/a             | n/a        | Often O(n²) or worse |
| **D&C**          | **Independent** | **No**          | **Yes**    | **Often O(n log n)** |
| Dynamic programming | Overlapping  | **Yes** (memoized) | Yes     | Often O(n²) / O(n·m) |
| Greedy           | One subproblem, commit immediately | No | No | Often O(n log n) |

The single most important distinction: **D&C's subproblems don't overlap.
If they did, you'd want DP.** This isn't a performance quibble — it's the
reason those two paradigms exist as separate things.

---

## Canonical Examples

### Merge Sort — O(n log n)

Divide: split the array in half.  
Conquer: recursively sort each half.  
Combine: merge two sorted halves into one sorted array (O(n)).

Guaranteed O(n log n), stable, but needs O(n) extra space for the merge.

### Quick Sort — O(n log n) average, O(n²) worst case

Divide: pick a pivot, partition the array into `< pivot` and `>= pivot`.  
Conquer: recursively sort each partition.  
Combine: **nothing to do** — the partitions are already in order.

Fast in practice (good cache behaviour, in-place), but the worst case
depends on pivot choice. Randomized pivot selection guarantees O(n log n)
*expected*.

### Binary Search — O(log n)

Divide: compare the target with the middle element.  
Conquer: recurse into one half (the other is discarded).  
Combine: nothing — the recursive call's answer is the answer.

Only one subproblem per recursion. `a = 1, b = 2, d = 0` → O(log n).

### Closest Pair of Points — O(n log n)

Divide: split the points by x-coordinate into left and right halves.  
Conquer: recursively find the closest pair in each half.  
Combine: check pairs that straddle the divider — but only pairs close
enough to matter, which turns out to be O(n).

Beats the O(n²) brute force by exploiting the geometric structure.

---

## Pitfalls

- **Forgetting the base case** → infinite recursion → stack overflow.
- **Dividing unevenly** (e.g., "first element vs the rest") → the recursion
  has depth n, not log n → O(n²) instead of O(n log n).
- **Expensive combine step hidden by clean-looking code** → check the
  asymptotic cost of `combine()`, not just its line count.
- **Using D&C when subproblems overlap** → you're reinventing DP without
  the memoization. Add memoization, or just call it DP.
- **Python recursion depth** → Python's default recursion limit is ~1000.
  For very deep recursion, either raise the limit (`sys.setrecursionlimit`)
  or rewrite iteratively.

---

## Pseudocode Skeleton

```
function divide_and_conquer(input):
    if base_case(input):
        return solve_directly(input)

    subproblems = split(input)
    sub_answers = [divide_and_conquer(p) for p in subproblems]
    return combine(sub_answers)
```

For a concrete implementation, see [`template.py`](template.py).
For worked examples, see [`problems/`](problems/) — merge sort and quicksort.

---

## Key Takeaways

1. **D&C is three steps: divide, conquer, combine.** The art is in the combine.
2. **Subproblems must be independent.** Overlap → switch to DP.
3. **The combine cost determines the total cost.** Cheap combine → big speedup.
4. **Most D&C algorithms are O(n log n)** because their recursion tree has
   log n levels of O(n) work each.
5. **The master theorem** is a shortcut for reading off complexity — but
   drawing the recursion tree and counting work-per-level always works.
