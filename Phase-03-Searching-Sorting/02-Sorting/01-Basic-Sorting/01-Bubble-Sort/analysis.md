# Bubble Sort — Analysis

## The Algorithm in One Paragraph

Bubble sort repeatedly scans the array and swaps adjacent out-of-order
pairs. After the first pass the maximum element has "bubbled up" to
the last position; after the second pass the second-maximum is in
place; etc. After n − 1 passes the array is sorted.

---

## Complexity

| Dimension                  | Classical      | Optimized (early-exit + bounded) |
|----------------------------|----------------|-----------------------------------|
| Best case (sorted input)   | **O(n²)**      | **O(n)**                          |
| Average case               | O(n²)          | O(n²)                             |
| Worst case (reverse sorted)| O(n²)          | O(n²)                             |
| Space                      | O(1)           | O(1)                              |
| Stable                     | Yes            | Yes                               |
| Adaptive                   | No             | **Yes**                           |
| In place                   | Yes            | Yes                               |

The O(n) best case requires BOTH optimizations (see `optimized-bubble.py`):

- **Early-exit flag:** stop when a full pass makes no swaps.
- **Bounded tail:** track the position of the last swap, so the next
  pass's bound is tighter than `n - 1 - i`.

Without those, bubble sort does the same (n-1) + (n-2) + … + 1 = n(n-1)/2
comparisons regardless of input.

---

## Stability

Bubble sort is stable IF the comparison is STRICT (`>`, not `>=`):

```python
if arr[j] > arr[j + 1]:        # stable
if arr[j] >= arr[j + 1]:       # NOT stable — swaps equal elements
```

With the strict comparison, two equal elements never swap, so their
relative order is preserved. This is important when sorting records
(tuples, objects) by a partial key.

---

## Counting Operations

For an array of `n` distinct elements:

| Quantity       | Best (sorted)  | Average        | Worst (reverse) |
|----------------|----------------|----------------|-----------------|
| Comparisons    | n − 1 (opt.)   | ~n²/4          | n(n−1)/2        |
| Swaps          | 0              | ~n²/4          | n(n−1)/2        |

On random inputs, roughly half of the pairs are out of order → ~n²/4
comparisons and ~n²/4 swaps.

---

## Why Bubble Sort Is Bad

Two reasons:

1. **O(n²) comparisons.** Same as selection sort and insertion sort.
2. **Too many swaps.** Each misplaced element is moved ONE position
   per pass. An element at distance `d` from its sorted position needs
   `d` passes to get there. Worst case: each element moves n − 1 times.

Compare to Insertion Sort: it also does ~n²/4 comparisons on random
input, but **each element is moved only when it makes progress** —
no wasted swaps. In practice, insertion sort is 2–3× faster than
bubble sort on the same data.

And of course, all of these are obliterated by O(n log n) sorts.

---

## Why Bubble Sort Is Still Taught

1. **Simplest sort by a wide margin.** Two lines of pseudocode.
2. **Clean introduction to in-place, stable sorting** — no memory
   allocation, no comparisons between distant elements.
3. **The "early exit" optimization** teaches an important idea:
   algorithms can be *adaptive* to input structure.
4. **Still comes up in interviews** — usually as "implement this"
   rather than "use this".
5. **Pedagogically valuable** for visualizing how sorts work (each
   pass settles one element).

In production code, never use it.

---

## Variants and Relatives

### Cocktail Shaker Sort (Bidirectional Bubble Sort)

Alternate between left-to-right and right-to-left passes. Each
left-to-right pass settles the maximum; each right-to-left pass
settles the minimum. Same O(n²), sometimes a bit faster on specific
inputs. Still impractical.

### Odd-Even Transposition Sort

A parallel-friendly variant: on "odd" passes compare/swap adjacent
pairs at odd indices; on "even" passes the even indices. Runs in
O(n) parallel time with O(n) processors; a curiosity rather than a
workhorse.

### Comb Sort

A real-world improvement on bubble sort: start with a large gap (say,
n / 1.3), shrink it each pass, and do bubble-style compares at that
gap. Approaches O(n log n) in practice. Included in some legacy
embedded systems.

---

## Pitfalls

- **Using `>=` instead of `>`:** breaks stability.
- **Forgetting the early-exit flag:** you're doing O(n²) on every
  sorted input.
- **Off-by-one on the outer loop:** `range(n - 1)`, not `range(n)`.
- **Off-by-one on the inner loop:** `range(n - 1 - i)`, not `range(n)`.
- **Shipping bubble sort to production:** don't.

---

## When to Use Bubble Sort

- **Teaching and interviews** — almost its sole remaining purpose.
- **Extremely small inputs (n ≤ 5)** where the simplicity outweighs
  performance. Even then, insertion sort is strictly better.
- **One-off scripts** where "obviously correct" matters more than
  speed. Even here, `sorted(arr)` is better.

---

## Key Takeaways

1. **Bubble sort is O(n²) classically; O(n) best case with optimizations.**
2. **Stable when implemented with strict `>` comparison.**
3. **The optimizations (early-exit, bounded tail) are the interesting part** —
   they illustrate adaptivity on a simple base.
4. **Never use in production.** Timsort, quicksort, merge sort — any
   O(n log n) algorithm — is orders of magnitude faster.
5. **The right mental model:** "largest elements bubble to the end
   one at a time." After k passes, the last k elements are in place.
