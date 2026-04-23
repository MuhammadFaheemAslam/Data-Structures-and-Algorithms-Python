# Selection Sort — Analysis

## The Algorithm in One Paragraph

Selection sort repeatedly SELECTS the minimum of the unsorted tail
and places it at the front of that tail. After the i-th pass, the
first `i` positions are in final sorted order.

It's the *mechanical mirror* of bubble sort: bubble sort "pushes" the
largest element to the end; selection sort "pulls" the smallest to
the front. Both are O(n²), but they differ on stability and swap count.

---

## Complexity

| Dimension                       | Selection Sort  |
|---------------------------------|-----------------|
| Best case                       | **O(n²)**       |
| Average case                    | O(n²)           |
| Worst case                      | O(n²)           |
| Space                           | O(1)            |
| Stable                          | **No**          |
| Adaptive                        | No              |
| Swaps                           | **Exactly n − 1** — best of any O(n²) sort |

The O(n²) bound is unconditional — selection sort performs the same
n(n-1)/2 comparisons on every input, including already-sorted ones.
Unlike bubble / insertion sort, there is no adaptive optimization
that makes it O(n) on sorted input.

---

## The One Real Advantage: Swap Count

Selection sort does **exactly n − 1 swaps**. No other O(n²) sort
guarantees that:

| Sort           | Swaps in worst case | Swaps on random input |
|----------------|---------------------|------------------------|
| Bubble Sort    | n(n-1)/2 ≈ n²/2    | ~n²/4                  |
| Insertion Sort | n(n-1)/2 ≈ n²/2    | ~n²/4                  |
| **Selection**  | **n − 1**          | **n − 1**              |

This matters when a SWAP is much more expensive than a COMPARE — for
example:

- Writing to flash memory or EEPROM (comparisons are free; writes wear
  out the cells).
- Physical sorting (moving large objects in a warehouse).
- Sorting records stored on slow media.

In pure-RAM settings, the advantage disappears — comparisons and
swaps cost about the same, and the O(n²) comparisons dominate.

---

## Why Selection Sort Is NOT Stable

The swap operation puts the selected minimum at position i — but
that destination might be occupied by an element equal to some
element later in the array. The swap can jump that equal element
past another equal element, breaking relative order.

Example:

    arr = [(2, 'a'), (1, 'b'), (2, 'c'), (2, 'd')]
    sort by first:
        pass i=0: min is (1,'b') at index 1. swap with arr[0].
        arr: [(1,'b'), (2,'a'), (2,'c'), (2,'d')]
             ^ the ORIGINAL (2,'a') has now moved past the later (2,'c') and (2,'d').
    pass i=1: min among (2,'a'), (2,'c'), (2,'d') is (2,'a'). no swap.
        ...

The final order of the three `2`s is a,c,d — but if it had been
rightly stable, we'd want the original order (which was a,c,d
too, in this specific case). The point is that SOMETIMES the swap
rearranges equal keys, which is the definition of instability.

To get a stable version, replace the swap with a shift (see
`selection-sort.py / selection_sort_stable`). This costs O(n²)
writes, forfeiting the one advantage.

---

## Counting Operations

For an array of `n` distinct elements:

| Quantity       | Exact count           |
|----------------|-----------------------|
| Comparisons    | n(n-1)/2              |
| Swaps          | n − 1 (at most)       |
| Reads          | n²                    |
| Writes         | O(n)                  |

---

## Selection Sort vs Bubble Sort vs Insertion Sort

| Property             | Bubble       | Selection    | Insertion    |
|----------------------|--------------|--------------|--------------|
| Worst case           | O(n²)        | O(n²)        | O(n²)        |
| Best case            | O(n) with opt| O(n²)        | O(n)         |
| Stable               | Yes          | No           | Yes          |
| In place             | Yes          | Yes          | Yes          |
| Adaptive             | With opt     | No           | Yes          |
| Comparisons (avg)    | ~n²/2        | n(n-1)/2     | ~n²/4        |
| Swaps / moves (avg)  | ~n²/4        | **n − 1**    | ~n²/4 moves  |

**Selection sort wins on SWAPS.** It loses on stability and
adaptivity. It ties on O(n²) comparisons.

Insertion sort is usually the right O(n²) choice — it's adaptive,
stable, and on average does fewer comparisons. Selection sort is
preferred only when writes are very expensive.

---

## Pitfalls

- **Off-by-one on the outer loop:** `range(n - 1)` — the last element
  is automatically in place once n − 1 others are settled.
- **Not tracking the min's index:** some write-ups compare and swap
  immediately; that's bubble sort, not selection sort.
- **Assuming it's stable:** it's not, unless you rewrite to insert
  instead of swap.
- **Using it when insertion sort would serve:** insertion sort has
  the same O(n²) worst case but O(n) best case, stability, and
  adaptivity. Selection sort's only niche is expensive-swap contexts.

---

## When to Use Selection Sort

Very rarely. Specifically:

- **EEPROM / flash-cell wear minimization.** Each cell has a limited
  write budget; minimizing writes matters more than comparisons.
- **Physical sorting where picks are expensive.**
- **Teaching:** it's a clean contrast to bubble and insertion sort.

For pure software: use insertion sort (for tiny n), or Timsort
(for anything else).

---

## Key Takeaways

1. **Selection sort is O(n²) unconditionally.** No adaptive best case.
2. **Its unique feature: O(n) swaps.** Lowest of any comparison-based sort.
3. **It is NOT stable** — the swap can reorder equal keys.
4. **It's almost always beaten by insertion sort**, except when writes
   are the binding cost.
5. **Useful pedagogically as the "pick the smallest" mirror of
   bubble sort's "push the largest".**
