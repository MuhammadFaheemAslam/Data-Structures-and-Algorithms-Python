# Difference Array — Theory

## Introduction

**Difference Array** is the **dual** of Prefix Sum. Where Prefix Sum
makes range *queries* O(1), Difference Array makes range *updates* O(1).

The idea:

> *Instead of applying a range update by touching every element in the
> range, record the update once at each endpoint. At the end, integrate
> the endpoints back into the array with a single O(n) scan.*

One update on a range of length k becomes O(1) instead of O(k). Over
many updates, this pattern turns an O(n·Q) naive algorithm (Q updates
each touching n elements) into **O(n + Q)**.

It's a simple, one-line trick. It's also the right answer to a
surprising fraction of array-update problems.

---

## The Core Idea

Given an array `arr`, define the **difference array** `diff` where:

```
diff[i] = arr[i] - arr[i-1]        (with diff[0] = arr[0])
```

So `diff[i]` records how `arr` *changes* at position `i`.

The key property:

> *The prefix sum of `diff` equals the original `arr`.*

```
arr[i] = diff[0] + diff[1] + ... + diff[i]
```

(That's immediate from telescoping: summing the differences recovers
the cumulative array.)

### What This Buys Us

Suppose you want to add `x` to every element in `arr[L..R]`:

- **Naive:** loop from L to R, updating each element → O(R - L + 1).
- **Difference array:** `diff[L] += x; diff[R+1] -= x` → O(1).

Why does that work?

- `diff[L] += x` says: *"the array jumps up by x at position L"*.
- `diff[R+1] -= x` says: *"and jumps back down by x at position R+1"*.

When you reconstruct `arr` from `diff` via prefix sum, the `+x`
propagates from position L onward — but the `-x` at position R+1
cancels it out, leaving the effect only on positions L through R.

That is the whole technique.

---

## A Quick Example

```
arr  = [0, 0, 0, 0, 0, 0]
diff = [0, 0, 0, 0, 0, 0]    initially all zero

Update: add 3 to arr[1..3]
    diff[1] += 3  →  diff = [0, 3, 0, 0, 0, 0]
    diff[4] -= 3  →  diff = [0, 3, 0, 0, -3, 0]

Update: add 5 to arr[2..4]
    diff[2] += 5  →  diff = [0, 3, 5, 0, -3, 0]
    diff[5] -= 5  →  diff = [0, 3, 5, 0, -3, -5]

Reconstruct arr as prefix sum of diff:
    arr[0] = 0
    arr[1] = 0 + 3 = 3
    arr[2] = 3 + 5 = 8
    arr[3] = 8 + 0 = 8
    arr[4] = 8 + (-3) = 5
    arr[5] = 5 + (-5) = 0

Final: arr = [0, 3, 8, 8, 5, 0]    ✓
```

Each update was O(1) regardless of range length. The final reconstruction
was one O(n) scan.

---

## When to Reach for Difference Array

Strong signals:

1. **Many range updates** (add x to arr[L..R]) followed by **one final
   query/scan**. This is the canonical shape.
2. **Offline problems** — all updates are known up front, and you just
   need the final array.
3. **Interval / event / flight-booking-style problems** — "n
   reservations, each occupies rows L to R, return seats per row".
4. **Counting overlaps at each point** — "N intervals on a timeline,
   how many overlap at each timestamp?"

Weak signals:

5. The array is **very large**, updates are **very local**, and you
   don't want to instantiate the full array.

---

## When NOT to Use Difference Array

- **You need the current array DURING the updates.** Difference array
  hides the array until reconstruction. If you need `arr[i]` mid-way
  through the update stream, use a Fenwick/segment tree instead.
- **Updates are single-point, queries are range-sum.** That's the
  opposite shape — use prefix sum, not difference array.
- **Mix of updates and queries interleaved.** Same story — Fenwick
  tree (O(log n) per operation) is the right tool.

The dividing line:

| Scenario                          | Use                       |
|-----------------------------------|---------------------------|
| Range UPDATES, then final array   | **Difference Array**      |
| Range QUERIES on fixed array      | **Prefix Sum**            |
| Mixed updates + queries           | Fenwick / Segment tree    |

---

## Difference Array + Prefix Sum = A Pair

They're literally inverses:

- Difference array turns `arr` into `diff`:   `diff[i] = arr[i] - arr[i-1]`.
- Prefix sum turns `diff` back into `arr`:    `arr[i] = diff[0..i]`.

So the technique of "record updates in diff, then prefix-sum to
reconstruct" is:

> *Accumulate edits in the INVERSE representation, apply them cheaply,
> then convert back to the ORIGINAL representation at the end.*

This duality is the same mathematical trick that drives other algorithms
you'll meet — **integrate/differentiate**, **Fourier transforms**,
**matrix multiplication via diagonalization**. The pattern generalizes
far beyond arrays.

---

## 2D Difference Array

For a 2D grid, to add `x` to every cell in the rectangle `(r1, c1)` to
`(r2, c2)` inclusive:

```
diff[r1  ][c1  ] += x
diff[r1  ][c2+1] -= x
diff[r2+1][c1  ] -= x
diff[r2+1][c2+1] += x
```

Four corner updates per rectangle, O(1). Then at the end, take the 2D
prefix sum of `diff` to recover the final grid. O(m·n) reconstruction.

This is exactly the inclusion-exclusion pattern from 2D prefix sum,
running in reverse. The positive corners START the contribution;
the negative corners CANCEL it outside the rectangle.

---

## Complexity

- **Per update:** O(1) — two constant writes (or four in 2D).
- **Reconstruction:** O(n) scan (O(m·n) in 2D).
- **Total for Q updates:** **O(n + Q)** — versus O(n·Q) naive.

For Q much larger than n, the speedup is enormous. For Q similar to n,
it's still a clean constant-factor improvement with no extra memory.

---

## Common Pitfalls

- **Forgetting the `diff[R+1] -= x` cancellation.** Without it, the
  update propagates past R forever. Triple-check the endpoint.
- **Off-by-one at the right endpoint.** If you store `diff` with length
  n, writing to `diff[R+1]` when R = n-1 is out of bounds. Either
  allocate `diff` of length n+1, or conditionally skip the write when
  `R+1 == n` (since nothing comes after it anyway — the decrement has
  nowhere to propagate).
- **Updating the original array by mistake.** The difference-array
  pattern works on `diff`; you reconstruct `arr` only at the end.
  Writing to `arr[L] += x` mid-way defeats the whole purpose.
- **Querying mid-stream.** See above — if you need intermediate values,
  reach for a different structure.

---

## Canonical Examples

### Corporate Flight Bookings — LeetCode #1109

Given `n` flights numbered 1..n, and `bookings[i] = [first, last, seats]`
meaning "seats reserved for every flight from first to last". Return
the total seats booked per flight.

The canonical difference-array problem. See `problems/range-updates.py`.

### Car Pooling — LeetCode #1094

Given trip (passengers, pickup, dropoff) entries, decide if the car
never exceeds capacity. Apply difference-array updates indexed by
location; run the prefix sum; check the max.

### Corporate Flight Bookings II / Range Addition — LeetCode #370

Exactly the template, no narrative.

### Counting Overlapping Intervals

For N intervals, how many cover each point on a timeline? Difference
array gives this in O(N + maxT).

---

## Key Takeaways

1. **Difference Array makes range UPDATES O(1)** at the cost of an
   O(n) final reconstruction.
2. **It is the inverse of Prefix Sum.** Together they form a pair:
   diff is the derivative, prefix-sum is the integral.
3. **The pattern:** `diff[L] += x; diff[R+1] -= x; ... ; reconstruct
   via prefix sum`.
4. **Use it for offline problems** with many range updates and a final
   query. For mixed update/query streams, reach for a Fenwick tree.
5. **2D version works via four corner updates** — same inclusion-exclusion
   logic as 2D prefix sum, running backward.

For the template, see [`template.py`](template.py). For the canonical
worked problem (LeetCode #1109), see
[`problems/range-updates.py`](problems/range-updates.py).
