# Easy Problems — Solution Walkthroughs

Two problems in this tier, each illustrating a foundational array
technique:

1. **Max/Min** → single-pass state tracking.
2. **Reverse** → two-pointer swap.

Both patterns reappear dozens of times in later modules — every
streaming algorithm, every palindrome problem, every in-place
partition is a variant of one of these two shapes.

---

## ✅ Problem 01 — Maximum and Minimum

### The Three Approaches

| Approach               | Time   | Space | Comparisons on n-element input    |
|------------------------|--------|-------|-----------------------------------|
| Built-ins (max + min)  | O(n)   | O(1)  | 2n (two separate scans)           |
| Single-pass manual     | O(n)   | O(1)  | up to 2n (but one scan)           |
| Pairwise tournament    | O(n)   | O(1)  | **1.5n** (fewer comparisons)      |

### Single-Pass Is The Interview Answer

Most interviewers want you to walk through the array ONCE:

```python
max_val = min_val = arr[0]
max_idx = min_idx = 0
for i in range(1, n):
    if arr[i] > max_val:
        max_val, max_idx = arr[i], i
    elif arr[i] < min_val:
        min_val, min_idx = arr[i], i
```

Two details to get right:

1. **Seed with `arr[0]`**, not `float('inf')` / `-inf`. That way
   you correctly track the INDEX too, and the first iteration isn't
   wasted on a guaranteed update.
2. **`elif`, not two separate `if`s.** An element can't be both
   larger than max AND smaller than min, so skipping the second
   compare saves ~n/2 comparisons on random input. Minor, but
   points in an interview.

### Pairwise Tournament — The 25% Comparison Saver

Process elements in pairs. First compare the two in the pair
(1 comparison) — now you know which is the local max and which
is the local min. Then:

- Compare the local max against running max (1 comparison).
- Compare the local min against running min (1 comparison).

**Total: 3 comparisons per pair of 2 elements = 1.5n comparisons.**

The naive approach is 2n comparisons (one vs max, one vs min, per
element). Pairwise saves ~25%. Rarely matters in Python, but when
comparisons are expensive (long strings, deeply-nested records),
it's a real win.

### The Lesson

"Scan once, track running state" is the single-most-reused pattern
on linear data. Kadane's, Boyer-Moore, best-time-to-buy-stock, max
consecutive ones — all the same shape with different state variables.

---

## ✅ Problem 02 — Reverse an Array

### The Four Approaches

| Approach              | Time | Space | In place? | When to use                  |
|-----------------------|------|-------|-----------|-------------------------------|
| `arr[::-1]` (slice)   | O(n) | O(n)  | No        | Idiomatic, quick one-liner    |
| New-array build       | O(n) | O(n)  | No        | Clear for teaching            |
| Two-pointer swap      | O(n) | **O(1)** | **Yes**   | **Interview standard**        |
| Recursive             | O(n) | O(n)  | Yes (input), O(n) stack | Avoid — stack overhead |

### The Two-Pointer Swap Skeleton

```python
left, right = 0, len(arr) - 1
while left < right:
    arr[left], arr[right] = arr[right], arr[left]
    left += 1
    right -= 1
```

Three things to notice:

1. **`while left < right`**, not `<=`. When `left == right`, they
   point at the same slot — swapping does nothing, so skip it.
2. **Exactly n/2 swaps**, regardless of n. Off-by-one errors here
   will either under- or over-swap.
3. **Simultaneous assignment** (`a, b = b, a`) is the Pythonic swap.
   No temp variable needed.

### Why In-Place Matters

Many "reverse" problems are actually "reverse in place" — the
interviewer wants O(1) space. If you default to `arr[::-1]`,
you've silently used O(n) space. Using two pointers from the start
makes the space constraint non-negotiable.

### Generalizing: `reverse_subarray(arr, left, right)`

The same algorithm, parameterized by start and end indices. This
is the building block for several other problems:

- **Array rotation by k (in place):** reverse the whole array,
  reverse the first k elements, reverse the remaining n-k. See
  `../medium/01-rotate.py`.
- **Next permutation:** reverse the suffix after a pivot position.
- **Reorder list:** reverse the second half of a linked list.

### The Lesson

Two-pointer swap is the first and simplest **O(1)-space in-place
transformation** technique. Every algorithm that converges two
pointers while swapping or comparing is a child of this one pattern.

---

## Self-Check

Before moving to medium problems, you should be able to:

- [ ] Write single-pass max/min from memory in under a minute.
- [ ] Write in-place reverse from memory (two-pointer swap).
- [ ] Explain why `arr[::-1]` is O(n) space but `reverse_in_place(arr)`
      is O(1).
- [ ] Recognize "scan once, track running state" as a pattern applied
      to Kadane's, Boyer-Moore, and best-time-to-buy-stock.
- [ ] Use `reverse_subarray` as a building block (the rotate problem
      in medium will need it).
