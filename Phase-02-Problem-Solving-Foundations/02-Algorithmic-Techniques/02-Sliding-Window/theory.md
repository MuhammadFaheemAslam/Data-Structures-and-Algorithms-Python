# Sliding Window — Theory

## Introduction

**Sliding Window** is the technique that turns O(n²) scans over
contiguous ranges into O(n) single-pass algorithms. It's one of the
most important optimizations you'll ever learn.

The core observation:

> *When you're iterating over all "contiguous subarrays" or "substrings"
> of an input, most of the work for position `i+1` overlaps with the
> work you already did for position `i`. Don't recompute — slide.*

A sliding window is literally what it sounds like: a range `[left, right]`
over the input that moves rightward one element at a time, with `left`
occasionally catching up to maintain some constraint. At each step you
add the entering element, drop the leaving element, and keep a running
summary — never re-summing the window from scratch.

This sounds obvious once stated. It is. The skill is *recognizing*
that a problem fits this shape in the first place.

---

## The Two Flavours

Sliding-window problems split cleanly into two categories that require
slightly different templates.

### 1. Fixed-Size Window

The window has a known, constant size `k`. Both pointers advance by 1
at every step.

```
window of size 3:
    [ a b c ] d e f g h
      a [ b c d ] e f g h
        a b [ c d e ] f g h
          ...
```

Use when the problem says *"subarray of size k"* or *"every window of
size k"*.

Classic problems:
- **Maximum sum subarray of size k** (the canonical fixed-window problem).
- **Average of every k-sized subarray** (LeetCode #643).
- **First negative number in every window of size k.**

Template shape:

```python
# 1) Prime the first window
window = sum(arr[:k])
best = window

# 2) Slide: add the entering element, remove the leaving one
for i in range(k, n):
    window += arr[i] - arr[i - k]
    best = max(best, window)

return best
```

One O(k) pre-computation, then n − k steps of O(1) work each.

### 2. Variable-Size Window

The window's size changes based on a **predicate** about its contents
(e.g., "sum ≤ target", "no repeated characters", "contains all
required letters"). Typical shape: expand on the right, shrink from
the left whenever the predicate breaks.

```
grow right:    [ a ]
               [ a b ]
               [ a b c ]           ← predicate breaks
shrink left:      [ b c ]
grow right:       [ b c d ]
               ...
```

Use when the problem says *"longest/shortest/smallest/largest subarray
such that …"* — a superlative paired with a constraint.

Classic problems:
- **Longest substring without repeating characters** (LeetCode #3).
- **Minimum window substring** (LeetCode #76).
- **Smallest subarray with sum ≥ target** (LeetCode #209).

Template shape (looking for the LONGEST):

```python
left = 0
best = 0
window_state = initial_state()

for right in range(n):
    window_state.add(arr[right])                  # include new right

    while not predicate(window_state):            # shrink while invalid
        window_state.remove(arr[left])
        left += 1

    best = max(best, right - left + 1)            # update answer

return best
```

For the SHORTEST variant, swap the two inner operations: expand until
the predicate IS satisfied, then record and try shrinking further.

---

## Why Sliding Window Works — The Invariant

Sliding window relies on an **amortization** argument:

- Each element is added to the window exactly once (when `right` advances).
- Each element is removed from the window exactly once (when `left` advances).
- Therefore `left` and `right` each take at most n steps total.
- Total work is **O(n)** — even though the inner `while` loop looks like
  it could make the algorithm quadratic.

This is one of the classic "looks O(n·n), actually O(n)" patterns. The
key is that `left` never moves backward. If your problem requires `left`
to move backward, sliding window doesn't apply — you need a different
technique.

---

## When to Reach for Sliding Window

Strong signals:

1. The problem concerns **contiguous** subarrays / substrings
   (non-contiguous usually means DP or sorting).
2. You're looking for a **min/max/count** over these subarrays.
3. The answer involves a **constraint** that can be maintained
   incrementally as the window slides.
4. A brute-force solution has two nested loops over start/end indices.

Weak signals:

5. The input is a **stream** and you want running statistics over the
   last k elements.
6. You're asked for something "**at most k**" or "**at least k**".

---

## Sliding Window vs Related Techniques

| Technique           | What it does                                          |
|---------------------|-------------------------------------------------------|
| **Two Pointers**    | General two-index scan; window shape varies.          |
| **Sliding Window**  | Specialization: `left` and `right` same direction, amortized O(n). |
| **Fast & Slow**     | Two pointers at DIFFERENT speeds; cycle detection.    |
| **Prefix Sum**      | When you need O(1) range sums on an IMMUTABLE array.  |
| **Hashing**         | Often USED inside a sliding window to track window state. |

Sliding window is essentially a specialization of two pointers where
both pointers advance in the same direction. The predicate-driven
shrinking is what makes it distinct.

A large number of sliding-window problems **also use a dict or set**
to represent window state — "how many of each character are in the
window right now?" is the classic pairing.

---

## The Canonical Problem Shapes

Most sliding-window problems fall into one of these four patterns.
Learn them and you'll recognize 90% of the variants:

### 1. Longest ___ such that predicate holds

Expand right always; when predicate breaks, shrink left. Track
`right - left + 1` at each step.

```
Longest Substring Without Repeating Characters
Longest Substring With At Most K Distinct Characters
Longest Subarray With Sum ≤ K
```

### 2. Shortest ___ such that predicate holds

Expand right until predicate holds; THEN try shrinking left as much as
possible while the predicate still holds.

```
Minimum Window Substring
Smallest Subarray With Sum ≥ K
```

### 3. Every window of size K

Fixed window. One O(k) pre-computation, then n − k slides.

```
Maximum Sum Subarray of Size K
Average of All Subarrays of Size K
Sliding Window Maximum (LeetCode #239)  ← uses a monotonic deque
```

### 4. Count of ___ windows / subarrays

The same shape, but accumulate a count instead of tracking min/max.
Often uses the trick:

    #(subarrays with predicate = P)  =  #(with P ≤ k)  −  #(with P ≤ k-1)

```
Subarrays With K Different Integers        (LeetCode #992)
Count Number of Nice Subarrays             (LeetCode #1248)
```

---

## Window-State Data Structures

The "window state" is whatever summary you keep incrementally. Common
choices:

| State                               | Typical use                         |
|-------------------------------------|-------------------------------------|
| **Running sum** (int)               | Fixed/variable sum problems         |
| **Running count of distinct chars** | "At most k distinct" problems       |
| **Dict: char → frequency**          | Anagram windows, minimum window     |
| **Set of chars**                    | "No repeating characters"           |
| **Monotonic deque**                 | Sliding window max/min              |
| **Counter of "need" vs "have"**     | Minimum window substring            |

Pick whatever supports O(1) per add/remove. If your window update is
itself O(n), you've lost the whole point of sliding window.

---

## Pitfalls

- **Using sliding window on a non-contiguous problem.** The technique
  requires that the answer lies in a single contiguous range. If the
  answer is a subset or arbitrary positions, reach for DP or hashing.
- **Shrinking from the wrong side.** The pointers must only advance —
  never backtrack. If your logic needs `left` to decrease, the problem
  is not a sliding window.
- **Recomputing window state in O(n).** The whole point of sliding
  window is incremental O(1) updates. If adding/removing an element
  requires scanning the window, you need a better state representation.
- **Off-by-one on window size.** `right - left + 1` is the inclusive
  window length. Writing `right - left` silently returns one less than
  the true size.
- **Forgetting to update `best` for the SHRINK-first pattern.** In the
  "shortest ___" template, you update the answer inside the shrink
  loop, not outside. Different from the "longest ___" template.
- **Using Sliding Window Maximum's naive version.** Tracking max over
  a window naively is O(k) per slide = O(n·k) total. The correct tool
  is a monotonic deque — covered in 09-Monotonic-Stack.

---

## Complexity

- **Time:** O(n) for the entire scan. Amortized because each element
  is added and removed at most once.
- **Space:** O(1) for numeric windows (running sums), O(k) for windows
  tracking distinct elements or character counts.

The combination "O(n) time, O(k) space" is what makes sliding window
unbeatable on the problems it fits.

---

## Key Takeaways

1. **Sliding window turns nested loops over contiguous ranges into a
   single pass.** The speedup is usually O(n²) → O(n).
2. **Two flavours.** Fixed-size: both pointers step together.
   Variable-size: shrink/grow based on a predicate.
3. **Amortized O(n).** Each element enters and leaves the window at
   most once, so the inner while loop doesn't re-inflate complexity.
4. **The window state must update in O(1).** Pick the right data
   structure (counter, deque, set) so add and remove are cheap.
5. **Sliding window composes with hashing.** The window itself is just
   two indices; the state is almost always a dict or counter.

For the two templates, see [`fixed-window.py`](fixed-window.py) and
[`variable-window.py`](variable-window.py). For worked problems, see
[`problems/`](problems/).
