# Monotonic Stack — Theory

## Introduction

**Monotonic Stack** is the specialized technique for a surprisingly
specific question:

> *"For each element in this array, what's the next (or previous)
> element that is greater (or smaller) than it?"*

That one-liner covers a huge class of interview problems — **Next
Greater Element**, **Daily Temperatures**, **Largest Rectangle in
Histogram**, **Trapping Rain Water**, **Sliding Window Maximum**,
and many more. Each of them has an O(n²) brute force (check every
neighbour) and an O(n) monotonic-stack solution.

The core invariant:

> *Maintain a stack whose elements are always in increasing (or
> decreasing) order. When a new element would violate the ordering,
> POP elements off until it fits — each popped element learns its
> "next" neighbour on the way out.*

That's the technique. Every monotonic-stack problem is a variation
on what gets pushed, what gets popped, and what's recorded on the way.

---

## The Core Idea

Take the most basic problem: **Next Greater Element**. For each index
`i`, find the smallest `j > i` such that `arr[j] > arr[i]`.

Brute force: for each `i`, scan `i+1..n-1`. O(n²).

Monotonic stack (decreasing):

```
Walk arr left to right. Keep a stack of INDICES whose values are
strictly DECREASING from bottom to top.

For each new index i:
    While stack is non-empty and arr[stack.top] < arr[i]:
        j = stack.pop()
        next_greater[j] = arr[i]    # i is j's answer
    stack.push(i)

At the end, any index still on the stack has no "next greater".
```

Each index is pushed once and popped at most once, so the total work
is **amortized O(n)** — even though there's a `while` inside the
`for`.

### Why It Works — The Invariant

At any moment, the stack holds indices whose future is undecided —
i.e., we haven't yet seen a greater value for them. The stack is
monotonically decreasing in VALUE (newer entries are smaller), because:

- If a new element `x` is smaller than or equal to the top of the
  stack, we push it directly (monotonicity preserved).
- If `x` is larger, it's the "next greater" for everything on the
  stack below it that's smaller. We pop them all, record their answer,
  and then push `x`.

This is beautifully tight: elements only leave the stack when we've
resolved their answer. No element is ever re-processed. Hence O(n).

---

## Monotonic Increasing vs Decreasing Stack

Which flavour you need depends on what you're looking for:

| What you're finding                         | Stack to maintain          |
|---------------------------------------------|----------------------------|
| Next **greater** element (to the right)     | **Decreasing** from bottom |
| Next **smaller** element (to the right)     | **Increasing** from bottom |
| Previous **greater** element (to the left)  | **Decreasing** from bottom |
| Previous **smaller** element (to the left)  | **Increasing** from bottom |

The recipe:

- You want GREATER → stack is DECREASING. A new greater element
  "breaks" it and pops elements (their answer).
- You want SMALLER → stack is INCREASING. Same logic, flipped.

Pick the wrong one and the algorithm produces nonsense — so
always write down "I'm looking for the next X → stack holds the
opposite".

---

## The Four Canonical Directions

Combining "greater vs smaller" with "left vs right" gives four
canonical problems. The template is the same; only the comparison
and direction differ:

| Question                              | Comparison | Walk direction |
|---------------------------------------|------------|----------------|
| Next greater to the right             | `<`        | left → right   |
| Next smaller to the right             | `>`        | left → right   |
| Previous greater (= next greater to the left) | `<`  | right → left   |
| Previous smaller (= next smaller to the left) | `>`  | right → left   |

All four share the same five-line skeleton.

---

## When to Reach for Monotonic Stack

Strong signals:

1. **The problem asks about "next/previous greater/smaller" of each
   element.** This is the technique's native habitat.
2. **Brute force has a nested loop over neighbours** looking for a
   monotone comparison. That's the exact shape monotonic stack
   removes.
3. **You need to track something about "the bar / building / rectangle
   to my left/right"** in a histogram / elevation / skyline problem.

Indirect signals:

4. **Counting "how long until something bigger happens"** —
   distances in Daily Temperatures, waiting times, etc.
5. **Span problems** — "stock span", "temperature span", "score
   spread" all reduce to "previous greater/smaller".
6. **Two-sided neighbour queries** — if you need BOTH "next greater"
   and "previous greater" per element, run two passes.

---

## Canonical Problems

### 1. Next Greater Element (LC #496 / #503)

For each element, find the next element greater than it. The textbook
monotonic-stack problem.

### 2. Daily Temperatures (LC #739)

For each day, find how many days until a warmer temperature. Identical
pattern to next-greater, but record the index DIFFERENCE instead of
the value.

### 3. Largest Rectangle in Histogram (LC #84)

For each bar, find the first shorter bar to its left AND to its right;
the max rectangle is bounded by those. Uses two monotonic-stack passes
(or one clever single pass with sentinels).

### 4. Trapping Rain Water (LC #42)

For each column, the water trapped is `min(max_left, max_right) -
height[i]`. Solvable either with prefix-max/suffix-max or a monotonic-
stack "layer" accumulation.

### 5. Stock Span Problem

For each day's stock price, count how many consecutive prior days had
price ≤ today's. "Previous greater" pattern.

### 6. Sliding Window Maximum (LC #239)

Use a monotonic DEQUE (double-ended) — same idea but you also drop
indices that have fallen out of the window from the front.

All six of these are four-variation apart from each other. Learn the
template; each problem is a small tweak.

---

## The Stack: What Do You Push?

A surprisingly important detail: should the stack hold **values** or
**indices**?

- **Values** are simpler if you only need the answer's VALUE.
- **Indices** are necessary if you need DISTANCES or to look up
  values again later.

Default to indices — you can always get the value via `arr[idx]`,
but you can't get the index back from a value.

---

## Monotonic Stack vs Related Techniques

| Technique            | Shape                                       |
|----------------------|---------------------------------------------|
| **Monotonic Stack**  | Stack of waiting elements; pop when violated |
| **Monotonic Deque**  | Same, but also removes stale entries from front (sliding window) |
| **Sliding Window**   | Two indices, variable gap; often uses a monotonic deque inside |
| **Two Pointers**     | Two indices, simpler state than a stack      |
| **Prefix Max/Min**   | Alternative for some problems (like Trapping Rain Water) |

Monotonic stack is the right answer whenever the per-element question
is about **neighbours satisfying a monotone comparison**. Sliding
window is the right answer when the question is about **contiguous
subarrays**. They overlap on problems like Sliding Window Maximum
(deque-based monotonic within a window).

---

## Complexity

- **Time:** O(n) — each index is pushed once and popped at most once.
- **Space:** O(n) in the worst case (stack can hold all n indices).

The amortized analysis is the reason this technique exists: a naive
implementation looks O(n²) because of the `while` loop, but the total
work across all iterations is O(n) because pops are bounded by pushes.

---

## Pitfalls

- **Wrong monotonicity direction.** Looking for "next greater" with
  an INCREASING stack silently returns wrong answers. Always pause
  to reason through the direction.
- **Comparing `<` vs `<=`.** "Next STRICTLY greater" (`<`) vs "next
  GREATER OR EQUAL" (`<=`) matter for tie-breaking. The problem
  statement decides which.
- **Pushing values when you need indices.** Causes problems for
  distance-based questions. Push indices by default.
- **Forgetting to handle leftover stack.** Indices still on the stack
  at the end have no answer — initialize the result array with a
  sentinel (-1, None, or n) beforehand.
- **Off-by-one on the walk direction for "previous" queries.** Often
  easier to walk the array in REVERSE and reuse the "next" template
  than to write a separate "previous" logic.
- **Using a list as a stack (Python).** Works fine — `.append()` and
  `.pop()` from the end are both O(1). Just don't use `list.pop(0)`,
  which is O(n).

---

## Pseudocode Skeleton

### Next greater to the right

```
result = [-1] * n
stack = []          # holds INDICES; arr-values are decreasing from bottom to top
for i in range(n):
    while stack and arr[stack[-1]] < arr[i]:
        j = stack.pop()
        result[j] = arr[i]   # or (i - j) for "distance" variants
    stack.append(i)
return result
```

### Next smaller to the right

Same template with the comparison flipped: `arr[stack[-1]] > arr[i]`.

### Previous greater / smaller (to the left)

Walk the array in reverse and apply the "next greater/smaller"
template from the right side.

For a concrete implementation, see [`template.py`](template.py). For
worked problems — one easy and one hard — see [`problems/`](problems/).

---

## Key Takeaways

1. **Monotonic Stack solves "next/previous greater/smaller" in O(n).**
2. **Direction of monotonicity follows the question:** want greater
   → stack DECREASING; want smaller → stack INCREASING.
3. **Push indices, not values, by default.** You can always derive the
   value; distance problems need the index.
4. **Amortized O(n):** each element is pushed once, popped at most
   once. The inner `while` doesn't break the bound.
5. **The same five-line skeleton** covers four problem variants and
   solves most histogram / skyline / bar problems.

For concrete templates and problems, see [`template.py`](template.py),
[`problems/next-greater.py`](problems/next-greater.py) and
[`problems/histogram.py`](problems/histogram.py).
