# Exponential Search — Analysis

## The Algorithm in One Paragraph

Exponential search **discovers a range containing the target in
O(log i) probes** by doubling the probe position (1, 2, 4, 8, …)
until it overshoots. Then a standard binary search finishes the
search inside the doubled range. Total: O(log i) — where `i` is the
target's index, not the array's size.

Also known as:
- **Galloping search** (when used as part of Timsort's merge to find
  the insertion point)
- **Struzik search**
- **Doubling search**

---

## Complexity

| Dimension | Bound                                      |
|-----------|--------------------------------------------|
| Time      | O(log i) where i = target's index          |
| Space     | O(1)                                        |
| Adaptive  | Yes — faster when target is near the start |
| Stable    | n/a (search, not sort)                     |

Worst case: the target is at the last index, giving O(log n).
Best case: the target is at index 0 or 1, giving O(1).

Binary search is O(log n) regardless of position. Exponential search
wins when `i << n` — which is common in practice when arrays are long
but interesting data clusters near the front.

---

## Comparison with Binary Search

| Target position        | Binary Search | Exponential Search |
|------------------------|---------------|---------------------|
| arr[0]                 | O(log n)      | **O(1)**            |
| arr[100] in n=10^9     | O(log n) ≈ 30 | **O(log 100) ≈ 7**  |
| arr[n/2]               | O(log n)      | O(log n)            |
| arr[n-1]               | O(log n)      | O(log n) — one more round than binary |

For a uniformly random target, binary search is slightly better in
practice (same Big-O, smaller constants). Exponential search wins
when the target is KNOWN to be near the start, or the array size is
unknown.

---

## The Killer Use Case: Unbounded Arrays

Binary search needs a known `hi`. If the array is a sorted stream
whose length you don't know (common in:
- Files on disk with unknown length,
- Sorted logs or telemetry being ingested,
- Function f(i) that is monotone but opaque (you can only query it),
- LeetCode's "Search in a Sorted Array of Unknown Size" — LC #702),

...you can't start binary search. Exponential search discovers the
upper bound in O(log i) probes by doubling, then hands off to binary
search.

This makes it the **only sub-linear algorithm** for sorted-but-
unknown-size search.

---

## Galloping Search Inside Timsort

Python's built-in `list.sort()` is **Timsort**, which uses **galloping
search** (a form of exponential search) during merges.

When merging two sorted runs, Timsort starts with a standard one-at-
a-time merge. If one run keeps "winning" — its element is always
chosen over the other's — Timsort suspects the other run has a long
prefix that's uniformly smaller. It switches to **galloping mode**:
exponentially probe into the losing run to find how many of its
elements fall below the current winner, then block-copy them in bulk.

This is why Timsort is amazing on partially-sorted or block-sorted
data — merging "long wins" is cheap. The theoretical backbone is
exponential search.

---

## When to Use Exponential Search

- **Unknown array size / streamed sorted data.**
- **Target is likely near the start** of a very long array.
- **Small early region of a sorted function / implicit structure.**
- **Galloping / finding insertion points** in production sort merges.

Otherwise, binary search is simpler and has smaller constants.

---

## Pitfalls

- **Bound overshooting past the end:** once `bound >= n`, use
  `min(bound, n - 1)` for the binary-search hi. Missing this either
  crashes (index out of range) or misses the last chunk of the array.
- **Skipping arr[0] check:** many write-ups assume i ≥ 1 in the
  doubling phase. Explicitly test `arr[0] == target` first to avoid
  bugs on that edge case.
- **Using > instead of >= in the doubling loop:** standard write-ups
  use `arr[bound] < target` to stop; `<=` would skip the bound that
  equals target.
- **Unbounded arrays with a too-small SENTINEL:** the "one past the
  array" sentinel must be larger than any real value to act as
  positive infinity.

---

## Key Takeaways

1. **Exponential search = exponential doubling + binary search.**
2. **O(log i)** — faster than binary search when the target is near
   the start.
3. **The go-to algorithm for unknown-size / streamed sorted data.**
4. **Galloping search inside Timsort** is the most important real-
   world use: merging long runs efficiently.
5. **For random-access arrays of known size with uniformly
   distributed queries, binary search is simpler and equally fast
   asymptotically.** Pick exponential only when one of its niches
   applies.
