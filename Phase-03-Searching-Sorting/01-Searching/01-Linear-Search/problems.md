# Linear Search — Practice Problems

Linear Search looks trivial, but problems based on it are surprisingly
rich. Most of them are variations on "scan once, track something
clever as you go" — which is the mental model you'll keep reusing in
streaming problems for the rest of your career.

The problems here are deliberately grouped into three tiers.

---

## 🟢 Tier 1 — Direct Applications

Straight linear scans. Every solution is some version of:

```
for i, x in enumerate(arr):
    # update some state based on x
return answer
```

### 1. Find First Occurrence

**Problem:** Given an array and a target, return the index of the
first occurrence, or -1.

**Template:** Exactly `linear_search()` from `implementation.py`.

---

### 2. Find All Occurrences

**Problem:** Return a list of every index at which the target appears.

**Template:** `linear_search_all()`. Scan the whole array; never
early-exit.

---

### 3. Find Minimum / Maximum

**Problem:** Return the minimum (or maximum) element's value and
position. Assume the input is non-empty.

**Hint:** `find_min_linear()` / `find_max_linear()`. Scan once; track
the best seen so far. Don't use Python's `min()` — the point is the
single-pass pattern.

---

### 4. Second-Largest Element

**Problem:** Return the second-largest DISTINCT value in an array.
If it doesn't exist (all equal), return None.

**Hint:** Maintain TWO running values: `best` and `second_best`. On
each element:
- If it beats `best`, shift (`second_best = best`, `best = x`).
- Else if it beats `second_best` and differs from `best`, update
  `second_best`.

**Complexity:** O(n), one pass. Don't sort.

---

### 5. Count Occurrences

**Problem:** Count how many times `target` appears in `arr`.

**Hint:** Trivial: a running counter.

**Variant:** Count occurrences of ANY of a list of targets. Still O(n)
if you use a set for the targets (O(1) membership check per element).

---

## 🟡 Tier 2 — Single-Pass State Tracking

Same shape, but the "state" you track is more interesting than a count
or a running max.

### 6. Maximum Difference With Later Element

**Problem:** Given prices `arr`, find `max(arr[j] - arr[i])` for some
`i < j`. Return 0 if the answer would be negative.

**Hint:** As you scan, track `min_so_far`. For each new element, the
best profit *ending here* is `arr[i] - min_so_far`.

**Complexity:** O(n), one pass. This is a STREAMING pattern — it
generalizes to "best stock trade" and "max swing in a window" problems.

---

### 7. Maximum Sum Subarray (Kadane's Algorithm)

**Problem:** Given an array of integers (possibly negative), return
the maximum sum of any contiguous subarray.

**Hint:** Track `current` (best sum ending here) and `best` (global
max). For each element: `current = max(x, current + x)`; `best = max(best, current)`.

**Complexity:** O(n), one pass. The classic DP-by-streaming algorithm.
Covered in depth in Phase-02 / 01 / 01-Brute-Force / problems / max-subarray.py.

---

### 8. First Non-Repeating Character

**Problem:** Given a string, return the first character that appears
exactly once (or None).

**Hint:** One pass to build a Counter; a second pass to find the first
character with count 1. (Technically two passes, but each is linear.)

**Twist:** Can you do it in a single pass? Not quite — without
knowing the full counts, you can't decide "is this character unique?"
until after the scan. But you CAN do the second pass over the Counter
itself if you trust insertion-order iteration (Python 3.7+).

---

### 9. Majority Element (Boyer-Moore)

**Problem:** The majority element appears > n/2 times in the array.
Find it in O(n) time, O(1) space.

**Hint:** Boyer-Moore Voting. Track a `candidate` and a `count`. When
`count` hits 0, pick the next element as the new candidate. Covered
in detail in Phase-02 / 02 / 08-Frequency-Counting / problems / majority-element.py.

---

### 10. Missing Number in `[0..n]`

**Problem:** Given an array of distinct numbers from `[0..n]` with
exactly one missing, find the missing one.

**Hint:** Two clean O(n) solutions:
- **Sum formula:** `n*(n+1)/2 - sum(arr)`.
- **XOR trick:** XOR all `arr[i]` and all indices `0..n`; the
  missing number survives. See Phase-02 / 02 / 11-Bit-Manipulation /
  bit-operations.py.

---

## 🔴 Tier 3 — Linear Scans on Richer Structures

Linear search applied to problems where the data is NOT a flat array
of primitives.

### 11. Find in a 2D Grid

**Problem:** Given a 2D grid and a target, return `(row, col)` where
it first appears (row-major order), or `None`.

**Hint:** Nested loop; break on first match. O(rows · cols). No
cleverness — this is just linear search in two dimensions.

**Twist:** If the grid is ROW-SORTED AND COLUMN-SORTED (LeetCode
#240), there's an O(rows + cols) "staircase" algorithm that beats
linear search. But it's not linear search anymore — it's a tailored
search technique that starts at a corner and moves only right or down.

---

### 12. Search in a Linked List

**Problem:** Given a singly linked list and a target value, return
True iff the target exists in the list.

**Hint:** The linked list's traversal IS linear search. No index
arithmetic; just `node = head; while node: if node.val == target: ...`.

---

### 13. Find an Element in a Stream

**Problem:** You receive integers one at a time and must answer queries
like "has X appeared yet?" while also returning the count so far.

**Hint:** Linear search doesn't scale for this — for repeated queries,
use a hash set / Counter. But if the stream is SHORT-LIVED (say, you
process each element, then forget), linear search inside one pass is
fine. This is the dividing line between streaming and indexed lookup.

---

### 14. Consecutive Sequence Detection

**Problem:** Given an array, find the longest sequence of consecutive
numbers present (not necessarily contiguous in the array).

**Hint:** This ISN'T a linear search — it's a set-based scan. Build a
set; for each `x` that is the START of a sequence (i.e., `x - 1` not
in the set), walk forward counting. O(n) total.

Included here as a "linear search is not always the answer" warning:
when the question is about membership rather than order, hashing wins.

---

## 🎯 Self-Check

You're done with linear search when you can:

- [ ] Write `linear_search` from memory in under 30 seconds.
- [ ] Explain why `list.index()` is a better default than a manual
      loop in real Python code.
- [ ] Recognize which of the above problems are "linear search
      variants" vs "use a different technique" problems.
- [ ] Implement Boyer-Moore voting and Kadane's algorithm from memory
      — both are "linear search with richer state".

---

## Next Up

Once linear search clicks, move to **02-Binary-Search** — the first
algorithm that exploits STRUCTURE (sortedness) to beat linear's O(n)
bound. Binary search has enough depth that it gets its own `variations/`
subfolder and multiple `problems/` files.
