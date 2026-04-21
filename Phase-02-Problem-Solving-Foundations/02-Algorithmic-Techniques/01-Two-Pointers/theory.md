# Two Pointers — Theory

## Introduction

**Two Pointers** is the simplest, most reusable technique in the whole
Phase 02 / 02 toolkit. It shows up in more interview problems than any
other single pattern, and most "clever" linear-time solutions on sorted
arrays are a two-pointer walk in disguise.

The core idea:

> *Maintain two indices into the array. Move them toward each other (or
> along the array together) based on what you find. Whenever the pair
> satisfies the constraint, record it; otherwise adjust and continue.*

The technique replaces a **nested loop** with a **single pass** by
using structure in the input (usually "sorted") to decide which pointer
to move. The speedup is typically from **O(n²)** to **O(n)**.

---

## The Three Flavours

Two Pointers comes in three shapes, differing in how the pointers relate:

### 1. Opposite-direction (converging)

Pointers start at the two ends of a sorted array and move toward each other.

```
left  →                            ← right
```

Classic uses:
- **Two Sum on a sorted array** — move `left` up or `right` down based
  on whether the current sum is too small or too large.
- **Valid palindrome** — check characters from both ends inward.
- **Container With Most Water** — shrink from the taller side to
  look for more area.

This is the flavour most people mean by "two pointers".

### 2. Same-direction (fast & slow, or window edges)

Both pointers start at the left and move rightward, possibly at different
speeds or on different conditions.

```
slow     fast →
  →
```

Classic uses:
- **Remove duplicates in place on a sorted array** — `slow` marks the
  write position, `fast` scans ahead.
- **Move zeros to the end** — same pattern.
- **Sliding Window** — `slow` = window start, `fast` = window end.
  (Covered in 02-Sliding-Window as a specialization.)

### 3. Two separate arrays

One pointer per array; advance based on which element is smaller or
which condition matches.

```
ptr_a →                 ptr_b →
array_a:                array_b:
```

Classic uses:
- **Merge two sorted arrays** (the combine step of merge sort).
- **Intersection of two sorted arrays.**
- **Longest common prefix by character.**

---

## The Invariant — Why Two Pointers Works

Two-pointer algorithms are powerful because of an **invariant** you
maintain during the scan. For the converging flavour on a sorted array,
the typical invariant is:

> *At any moment, the search space `arr[left..right]` still contains
> all candidate pairs we haven't yet ruled out.*

Each movement of `left` or `right` **rules out** some pairs forever:

- If `arr[left] + arr[right] < target`: no pair involving `arr[left]`
  and anything `≤ arr[right]` can reach `target`, because `arr[right]`
  is the largest value left. So advance `left` — `arr[left]` is out of
  contention.
- If `arr[left] + arr[right] > target`: symmetrically, advance `right`.

Each step eliminates one element from further consideration, so the total
work is **O(n)** rather than O(n²).

If you can't state an invariant like this, the two-pointer solution is
probably wrong. Always check: *"what am I ruling out when I move this
pointer?"*

---

## When to Reach for Two Pointers

Strong signals:

1. **The input is sorted** (or can be cheaply sorted).
2. **You're looking for a pair, triple, or sub-array** satisfying some
   target / constraint.
3. **A brute-force solution has nested loops** that scan the same data
   repeatedly.
4. **There's a monotonicity:** moving one pointer in some direction
   can only increase (or only decrease) some quantity — meaning the
   other pointer need not look backward.

Weaker (but still useful) signals:

5. You're **partitioning** an array in place (putting all reds before
   blues, all zeros at the end, etc.).
6. You're **merging** two ordered sequences.
7. You need to **find a symmetric property** (palindrome, mirror).

---

## The General Template

```python
def two_pointers(arr):
    left, right = 0, len(arr) - 1

    while left < right:
        if condition_satisfied(arr[left], arr[right]):
            record_or_return()
            # advance one or both, depending on whether duplicates matter
            left += 1; right -= 1
        elif current_is_too_small(arr[left], arr[right]):
            left += 1                      # need larger value
        else:
            right -= 1                     # need smaller value
```

For the same-direction flavour:

```python
def two_pointers_same_direction(arr):
    slow = 0
    for fast in range(len(arr)):
        if condition(arr[fast]):
            arr[slow] = arr[fast]
            slow += 1
    return slow                            # new length after the in-place edit
```

---

## Common Pitfalls

- **Forgetting to sort.** Two pointers almost always needs sorted input.
  If the input isn't sorted, sort it first (O(n log n)) or switch to a
  different technique (hashing is usually the alternative).
- **Infinite loops.** If neither pointer moves on a certain branch, you
  loop forever. Every branch of the while loop must advance at least one
  pointer.
- **Off-by-one on the termination condition.** `left < right` vs
  `left <= right` matters — the first is correct for "two distinct
  positions", the second for "range includes equal indices" (rare).
- **Missing duplicate handling.** When the problem says "return unique
  triples", you must explicitly skip equal neighbours after finding a
  match. See `three-sum.py` for the canonical technique.
- **Using two pointers on unsorted data.** The invariant breaks. Sort
  first, or use a different technique.

---

## Two Pointers vs Related Techniques

| Technique           | Shape                                        | When it wins                                  |
|---------------------|----------------------------------------------|-----------------------------------------------|
| **Two Pointers**    | Two indices into sorted / paired input      | Pair/triple search, palindrome, merge         |
| **Sliding Window**  | Two pointers walking same direction as a window | Contiguous subarray / substring problems    |
| **Fast & Slow**     | Two pointers, different speeds               | Cycle detection, find middle                  |
| **Binary Search**   | Two indices collapsing on a single target   | Searching a sorted sequence for one value     |
| **Hashing**         | Dict of seen values                          | Pair-finding on UNSORTED input                |

Two pointers and hashing are often the two best options for the same
problem (e.g., Two Sum). When the input is sorted, two pointers wins:
O(n) time, O(1) space. When it isn't, hashing wins: O(n) time, O(n)
space — no sort needed.

---

## Complexity

- **Time:** O(n) for the single pass, O(n log n) if you must sort first.
- **Space:** O(1) — both pointers are just integers. This is the killer
  feature compared to hashing's O(n).

---

## Canonical Examples

### Two Sum on Sorted Array → O(n)
```
left, right = 0, n-1
while left < right:
    s = a[left] + a[right]
    if s == target: return (left, right)
    if s < target: left += 1
    else: right -= 1
```

### Valid Palindrome → O(n)
```
left, right = 0, n-1
while left < right:
    if s[left] != s[right]: return False
    left += 1; right -= 1
return True
```

### Remove Duplicates from Sorted Array → O(n)
```
slow = 0
for fast in range(len(a)):
    if fast == 0 or a[fast] != a[fast-1]:
        a[slow] = a[fast]
        slow += 1
return slow                                # the new length
```

### Merge Two Sorted Arrays → O(n + m)
```
i = j = 0
while i < n and j < m:
    if a[i] <= b[j]:
        out.append(a[i]); i += 1
    else:
        out.append(b[j]); j += 1
out.extend(a[i:]); out.extend(b[j:])
```

Notice how the same four-line skeleton, slightly tweaked, solves four
different-looking problems. That's the whole value of the technique.

---

## Key Takeaways

1. **Two Pointers replaces nested loops with a single pass** when the
   input has exploitable structure (usually sortedness).
2. **Three flavours** — converging, same-direction, two-array — cover
   most uses.
3. **Every branch must advance at least one pointer.** Otherwise you
   loop forever.
4. **State the invariant.** "What am I ruling out when I move this
   pointer?" If you can't answer, your solution is probably wrong.
5. **Sort first if needed.** Two pointers on unsorted data rarely works.
