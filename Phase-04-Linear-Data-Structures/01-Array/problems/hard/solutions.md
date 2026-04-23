# Hard Problems — Solution Walkthroughs

One problem in this tier, but it's a big one:

1. **Median of Two Sorted Arrays** — the canonical hard array problem,
   the one most interviewers use to separate "knows algorithms" from
   "*understands* algorithms."

---

## ✅ Problem 01 — Median of Two Sorted Arrays

### The Three Approaches

| Approach               | Time              | Space  | Difficulty    |
|------------------------|-------------------|--------|----------------|
| Merge then find middle | O((m+n) log(m+n)) | O(m+n) | Easy          |
| Two-pointer walk       | O(m+n)            | O(1)   | Medium         |
| **Binary search on partitions** | **O(log(min(m, n)))** | O(1) | **Hard** |

The O(log) solution is what makes this problem LeetCode Hard. Everyone
can produce O(m+n) in two minutes. The log version requires seeing the
problem through an entirely different lens.

### The Partition Insight

Forget merging. Instead, imagine picking a SPLIT POINT in each array:

```
nums1: [ L1 | R1 ]    i elements on left
nums2: [ L2 | R2 ]    j elements on left
```

If `i + j = (m + n + 1) / 2` and:

- Every element in L1 is ≤ every element in R2, AND
- Every element in L2 is ≤ every element in R1,

then the MEDIAN is sitting right at the partition boundary:

- Odd total: `max(L1_max, L2_max)` — the largest element in the left half.
- Even total: `(max(L1_max, L2_max) + min(R1_min, R2_min)) / 2`.

So the problem reduces to: find the right `i` in nums1 (from 0 to m).
That's a binary search over `i`, hence O(log m).

### The Algorithm in Pseudocode

```
Ensure m ≤ n (binary-search the SHORTER array).
half = (m + n + 1) / 2

lo, hi = 0, m
loop:
    i = (lo + hi) / 2
    j = half - i

    L1 = nums1[i-1] if i > 0 else -∞
    R1 = nums1[i]   if i < m else +∞
    L2 = nums2[j-1] if j > 0 else -∞
    R2 = nums2[j]   if j < n else +∞

    if L1 ≤ R2 and L2 ≤ R1:
        return median from max(L1, L2), min(R1, R2)
    elif L1 > R2:
        hi = i - 1    # take FEWER from nums1
    else:
        lo = i + 1    # take MORE from nums1
```

### Three Subtle Details

#### 1. Binary-search the SHORTER array

If you binary-search the longer array, you might pick `i` values that
force `j < 0` or `j > n`, crashing your partition check. By always
picking the shorter array, `i ∈ [0, m]` implies `j ∈ [half - m, half]`,
which stays in [0, n].

#### 2. Use ±∞ for out-of-range boundaries

When `i == 0`, there's nothing to the left of nums1 — so `L1` is
effectively `-∞` (any element of nums2 is ≥ it, so the "L1 ≤ R2"
check trivially passes). Similarly when `i == m`, `R1 = +∞`.

Without the ±∞ trick you need a tangle of `if i == 0 else` conditions;
with it, the partition check is a clean four-line expression.

#### 3. The `half = (m + n + 1) / 2` trick

This gives you the size of the LEFT HALF (including the median if
total is odd). It works uniformly for both odd and even totals:

- Odd total (e.g., 5):  (5+1)/2 = 3  → left half has the median.
- Even total (e.g., 6): (6+1)/2 = 3  → left half has the lower middle.

With this split, the median extraction formula handles both cases
elegantly.

### Why the Three-Approach Progression Matters

Most interviewers DON'T expect you to produce the O(log) solution
on the first attempt. They expect you to:

1. **Start with O(m+n) merge.** "Okay, easy — just merge and take
   the middle."
2. **Notice the O(m+n) space.** "Can I do it in O(1) space?" → Two
   pointers walking to the midpoint.
3. **Ask about better time.** "Is there a way to exploit that both
   arrays are SORTED?" → Binary search.

Each step reveals more algorithmic sophistication. The binary-search
version is the "senior engineer answer"; the two-pointer walk is a
strong "mid-level answer"; the merge is the fallback.

### Related Problems

- **Kth Smallest Element in Two Sorted Arrays:** same binary-search
  technique; find the kth element instead of the middle one.
- **Median of a Stream:** different problem — use two heaps.
- **Kth Smallest Element in Sorted Matrix (LC #378):** binary search
  on the answer space.

### The Lesson

**"Search the answer space, not the input"** is the Phase-02 / 02 /
05-Binary-Search-on-Answer mantra. This problem is its most beautiful
expression: we don't search for a VALUE in the arrays, we search for
the PARTITION POINT that satisfies the median property.

Once you internalize this — "what am I actually binary-searching
over?" — a whole class of "sorted input, seemingly unrelated question"
problems opens up.

---

## Self-Check

- [ ] Write the O(m+n) merge in under 60 seconds.
- [ ] Write the O(m+n) two-pointer walk without the full merge.
- [ ] Derive the partition-point invariant on a whiteboard.
- [ ] Implement the O(log) binary-search version from scratch.
- [ ] Explain why we binary-search the shorter array, not the longer.
- [ ] Explain why the ±∞ boundary trick simplifies the code.

If you can do all six, this problem — and the broader "binary search
on the answer space" pattern — is yours.
