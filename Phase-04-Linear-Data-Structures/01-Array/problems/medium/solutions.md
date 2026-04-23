# Medium Problems — Solution Walkthroughs

Two problems that reveal the most important array transformations:

1. **Rotate** → the three-reverse trick (composable with any
   sub-array manipulation).
2. **Max Subarray** → Kadane's algorithm (the prototype for streaming DP).

Together they represent two distinct optimization styles:

- Rotate: a "clever manipulation" — multiple simple operations
  combined.
- Kadane: a "DP insight" — recognize that each step's optimum
  depends only on the previous step.

---

## ✅ Problem 01 — Rotate an Array

### The Four Approaches

| Approach            | Time        | Space | In place | When to use                   |
|---------------------|-------------|-------|----------|-------------------------------|
| Slicing             | O(n)        | O(n)  | No       | Quick, one-shot               |
| Naïve (rotate × k)  | **O(n · k)**| O(1)  | Yes      | Never — educational only      |
| **Three-reverse**   | **O(n)**    | O(1)  | Yes      | **The answer**                |
| Cyclic replacements | O(n)        | O(1)  | Yes      | Same complexity, trickier     |

### The Three-Reverse Trick (Memorize This)

To rotate RIGHT by k:

```
1. Reverse the entire array.
2. Reverse the first k elements.
3. Reverse the last n - k elements.
```

Each reverse is O(n) and in place → total O(n) time, O(1) space.

**Why does it work?** Think of the array as two blocks separated at
position `n - k`:

    Original: [ A | B ]    where |A| = n-k, |B| = k
    Goal:     [ B | A ]

- Reverse whole:  [ B_reversed | A_reversed ]
- Reverse first k (= reverse B_reversed): [ B | A_reversed ]
- Reverse last n-k (= reverse A_reversed): [ B | A ]

Each reverse undoes the previous reverse on that section. The
composition lands exactly where we want.

### Don't Forget `k = k % n`

If k > n, you'd go past the end in the three-reverse trick — literal
crash. Always normalize at the top:

```python
k = k % n
```

If n is 0, skip the whole thing.

### Cyclic Replacements — Why It's Tricky

Each element at position `i` should move to position `(i + k) % n`.
So you could walk through ONE cycle, swapping as you go. Problem:
there are actually `gcd(n, k)` cycles, not one. You need an outer loop
that starts each cycle, plus a counter that stops when all elements
have been placed.

It's O(n) with one memory read per element — arguably the most
efficient algorithm for this problem. But the three-reverse trick is
simpler and has better cache behaviour, so it's usually preferred.

### The Lesson

**Composing reverses is a surprisingly powerful toolkit.** It shows
up in:

- Next permutation (LC #31)
- Reorder list (linked list version uses midpoint + reverse + merge)
- Rotate string (LC #796 is solvable in one line because rotations
  are all substrings of `s + s`)
- Any "shift by k with O(1) space" problem

Master `reverse_subarray(arr, left, right)` (from `easy/02-reverse.py`)
and compose it to build these.

---

## ✅ Problem 02 — Maximum Subarray Sum (Kadane's Algorithm)

### The Optimization Arc

| Approach           | Time        | Space  | Key insight                        |
|--------------------|-------------|--------|------------------------------------|
| Brute force        | O(n³)       | O(1)   | Check every (i, j) pair, sum each  |
| Running sum        | O(n²)       | O(1)   | Reuse sum as j grows               |
| **Kadane**         | **O(n)**    | O(1)   | **"Extend or start fresh"**        |
| Divide & conquer   | O(n log n)  | O(log n) | Interesting but suboptimal       |

### Kadane's Core Insight

> *At position i, the best subarray ENDING AT i is either
> `nums[i]` alone, or the best-ending-at-(i-1) extended by `nums[i]`.*

This means we don't need to look at every possible subarray — we just
need to make one decision per position:

```python
current = max(nums[i], current + nums[i])
```

If `current + nums[i]` has become negative (or just worse than `nums[i]`),
we throw away the previous subarray and start fresh at `i`. Otherwise,
extend.

The global `best` tracks the highest `current` we've ever seen:

```python
best = max(best, current)
```

### Why Kadane Is the Streaming DP Prototype

Kadane is DP in disguise. The state `current = best sum ending at i`
depends only on `current_{i-1}`. That's a 1D DP with O(1) memory —
the purest form of streaming DP.

Other streaming DPs that follow the same shape:

- **Best Time to Buy and Sell Stock:** `current = max(current, price - min_so_far)`.
- **Longest Streak of 1s:** `current = current + 1 if x == 1 else 0`.
- **Max Sum of Non-Adjacent Elements:** `current = max(skip + arr[i], take)`.

Each is one line of state evolution plus one global max. Once Kadane
clicks, these all look identical.

### Subarray Bounds — The Bookkeeping Twist

If the interviewer asks "what are the INDICES of the best subarray?"
(not just the sum), add a bit of bookkeeping:

- Track `start` — where the current subarray began (updated when we
  "start fresh").
- Track `best_start, best_end` — snapshot whenever `best` updates.

See `max_subarray_with_bounds` in the solution file.

### Edge Cases

1. **All negatives.** Kadane must return the LEAST-NEGATIVE value
   (the "best single element"), not 0. Seeding with `nums[0]`
   handles this naturally; seeding with `0` does not.

2. **Empty array.** Undefined by the problem; most implementations
   return 0 or raise. Pick one and document it.

3. **Single element.** The loop body never runs; just return the element.

### The Divide & Conquer Version

Splits the array in half. The answer is one of:

- Best subarray entirely in the left half.
- Best subarray entirely in the right half.
- Best subarray CROSSING the midpoint.

The third case is computed by expanding outward from the midpoint in
O(n). Total recurrence: T(n) = 2T(n/2) + O(n) → O(n log n).

Why include it? Because recognizing that DIVIDE & CONQUER also works
(just not as well) is a good interview display of algorithmic
vocabulary. Kadane is the right answer; D&C is the "I can do better
than quadratic if I don't see Kadane" fallback.

### The Lesson

Kadane shows that **sometimes the best algorithm is streaming, not
multi-pass.** If you can identify a DP state that evolves via a
single constant-work transition, you get O(n) time, O(1) space —
the absolute best any algorithm can do on a linear pass.

---

## Self-Check

Before moving to hard problems, you should be able to:

- [ ] Implement the three-reverse rotation from memory.
- [ ] Implement Kadane's in under 30 seconds.
- [ ] Recognize "running state + global best" as a pattern applied
      to stock prices, longest streak, maximum subarray, and friends.
- [ ] Explain why all-negative arrays break "seed with 0" Kadane
      variants.
- [ ] Compose `reverse_subarray` to solve rotate (and see the pattern
      in next-permutation).
