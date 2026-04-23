# Jump Search — Analysis

## The Algorithm in One Paragraph

Jump Search works on **sorted arrays**. It picks a block size `step`,
jumps forward by `step` each iteration until the value at the end of
the current block is ≥ target, then linear-searches within that block.

With `step = √n`, total work is **O(√n)**.

---

## Complexity

| Dimension | Bound                 |
|-----------|-----------------------|
| Time      | O(√n) average/worst   |
| Space     | O(1)                  |
| Stable    | n/a (search, not sort) |
| Adaptive  | No — step size is fixed by n |

### Why √n?

Total work is `O(n/step + step)` — the number of jumps plus the linear
scan inside the final block. Minimizing this expression over `step`:

    d/d(step) [n/step + step] = -n/step² + 1 = 0
    ⇒ step = √n

So `step = √n` is the optimal block size, giving O(√n) total work.

Other block sizes:
- `step = n^(1/3)` → O(n^(2/3) + n^(1/3)) → O(n^(2/3)) — worse.
- `step = n^(2/3)` → O(n^(1/3) + n^(2/3)) → O(n^(2/3)) — worse.

---

## Comparison with Other Searches

| Algorithm      | Time        | When it wins                            |
|----------------|-------------|-----------------------------------------|
| Linear         | O(n)        | Unsorted / tiny arrays                  |
| Jump Search    | **O(√n)**   | Sequential-access media                 |
| Binary Search  | O(log n)    | **Random-access arrays** (almost always) |
| Interpolation  | O(log log n) expected | Uniformly-distributed values   |
| Hashing        | O(1)        | Many repeated queries                   |

For n = 1,000,000:
- Linear:      1,000,000 ops
- Jump:        ~1,000 ops (one per jump + one per linear step in block)
- Binary:      ~20 ops

Binary search dominates in-memory workloads by a wide margin. Jump
search's niche is when "jumping ahead k steps" is much cheaper than
"seeking to an arbitrary position" — e.g., tape drives, some streamed
formats, or running-sum prefix structures.

---

## When Jump Search Is the Right Call

- **Sequential-access storage:** magnetic tape, certain disk layouts.
- **Streamed / paged data:** reading a page at a time is cheap; random
  paging is expensive.
- **Comparison cost is trivial, seek cost is dominant:** minimize
  backtracking.
- **Interview-only pedagogy:** demonstrating that sub-linear doesn't
  require logarithms.

In Python on regular lists, **binary search is always preferable**.
Use `bisect` from the standard library; don't hand-write jump search.

---

## Implementation Notes

1. **Step size as an int:** `step = int(sqrt(n))`. Guard with `max(1, …)`
   to avoid a 0 step on n = 0, 1, 2, 3 (where int(sqrt(n)) = 0 or 1).
2. **Off-by-one on the block boundary:** the block being inspected ends
   at `min(lo + step, n) - 1` (inclusive). Easy to get wrong.
3. **Duplicates:** jump search returns SOME valid index, not necessarily
   the first. If "first occurrence" is required, fall back to binary
   search variants (see ../02-Binary-Search/variations/first-occurrence.py).

---

## Pitfalls

- **Wrong step size.** Using step = n / constant is O(n) in disguise.
  The step must scale with √n.
- **Running linear search past the block.** The linear scan is only
  over the last block's range, not the whole array.
- **Skipping the "≥ target" check.** Some write-ups use `> target`,
  which can overshoot by one block if the target sits exactly at a
  block boundary.
- **Assuming sorted:** jump search requires sorted input. On unsorted
  data it's just a random sampling with linear-scan fallback — which
  is not a useful algorithm.

---

## Key Takeaways

1. **Jump Search is O(√n)** — sub-linear but worse than binary search's O(log n).
2. **The √n step is the minimizer.** Any other block size is strictly worse.
3. **Its niche is sequential-access storage**, not random-access arrays.
4. **On Python lists, use `bisect` instead.**
5. **Still worth knowing** as a stepping stone between linear and
   binary search, and as the right answer in the rare niche where it
   beats alternatives.
