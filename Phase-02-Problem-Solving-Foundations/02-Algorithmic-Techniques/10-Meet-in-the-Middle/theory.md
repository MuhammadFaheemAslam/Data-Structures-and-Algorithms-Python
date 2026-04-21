# Meet in the Middle — Theory

## Introduction

**Meet in the Middle** (MITM) is the technique that handles problems
that are *just slightly too big* for brute force.

Brute force on an exponential problem has complexity **O(2^n)** —
unusable past n = 25 or so. DP, when applicable, handles much bigger
inputs. But between the two — roughly **n = 30 to 50** — there's a
gap where brute force is too slow, DP doesn't apply (or has
pseudo-polynomial blowup on massive values), and something more
clever is needed.

MITM is that clever thing. The idea:

> *Split the input into two halves. Brute-force each half separately.
> Each half costs 2^(n/2), a square-root improvement over the full
> problem. Then combine the two halves using sorting + binary search
> (or hashing) to find the target.*

The total cost drops from **O(2^n)** to **O(2^(n/2) · log 2^(n/2)) =
O(n · 2^(n/2))** — for n = 40, that's 40 · 10^6 ≈ 4·10^7 operations
instead of 10^12. The difference between "runs in a second" and
"runs in a year."

---

## The Core Idea

Suppose you want to find all subsets of an array whose sum equals `T`.

Brute force: enumerate all 2^n subsets. For n = 40, that's 10^12 — too
slow.

Meet in the Middle:

1. Split the array into two halves `A` and `B` of size roughly n/2 each.
2. Enumerate all 2^(n/2) subset sums of `A` into a set `S_A`.
3. Enumerate all 2^(n/2) subset sums of `B` into a set `S_B`.
4. For each sum `s` in `S_A`, check whether `T - s` is in `S_B`. If
   yes, some combination of an `A`-subset and a `B`-subset sums to T.

Work per step:
- Steps 1, 2: O(2^(n/2) · (n/2)) — subset enumeration plus summing.
- Step 4: O(2^(n/2)) lookups, each O(1) with a hash set → O(2^(n/2))
  total. Or O(log 2^(n/2)) per lookup with binary search on a sorted
  list → O(2^(n/2) · n/2).

Total: **O(n · 2^(n/2))**. Square-root speedup in n.

That's the whole technique. Everything else is elaboration on how you
combine the halves.

---

## Why the Square-Root Speedup Matters

MITM doesn't magically convert exponential to polynomial. It halves the
exponent:

| n   | 2^n              | 2^(n/2)       | Practical?           |
|-----|------------------|---------------|----------------------|
| 20  | 10^6             | 10^3          | Either works         |
| 30  | 10^9             | 3·10^4        | Brute borderline, MITM instant |
| 40  | 10^12            | 10^6          | Brute impossible, MITM fast |
| 50  | 10^15            | 3·10^7        | Only MITM is feasible |
| 60  | 10^18            | 10^9          | Both infeasible      |

The useful range is roughly **n = 30 to 50**. Smaller, and brute force
works. Larger, and even MITM is too slow — you need DP or an
algorithmic shortcut.

The technique is also widely known under the name **baby-step
giant-step** in number-theoretic settings (like solving discrete logarithms).

---

## When to Reach for Meet in the Middle

Strong signals:

1. **The problem is genuinely exponential.** Subset sums, bitmask
   problems, graph searches with state size ~2^n.
2. **n is between ~30 and ~50.** Brute force is too slow, but 2^(n/2)
   fits in memory.
3. **The search space factors into INDEPENDENT halves.** This is the
   key prerequisite — if the two halves depend on each other, you
   can't enumerate them separately.
4. **A COMBINE step exists** that can stitch the halves in polynomial
   time (sort + binary search, hash lookup).

Indirect signals:

5. **DP would work but has pseudo-polynomial blowup.** Subset Sum has
   DP O(n · T), which explodes when T is large (e.g., T = 10^15).
   MITM handles large values at the cost of limiting n.
6. **A 4Sum / 6Sum problem** where one more-dimensional thinking helps.
   4Sum reduces to "two pairs" — each pair is a two-sum — and MITM
   applies to the pair space.

---

## The Two Combine Strategies

Step 4 above has two common implementations. Both give the same
asymptotic speedup with slightly different constants.

### Combine via Hash Set

```python
seen = {sum_of(subset) for subset in subsets_of_A}
for subset in subsets_of_B:
    if (T - sum_of(subset)) in seen:
        return True
```

- **Time:** O(2^(n/2)) lookups × O(1) avg = O(2^(n/2)) combine.
- **Space:** O(2^(n/2)) for the hash set.
- **Pro:** Fastest constants; cleanest code.
- **Con:** No ordering if you need "closest", "kth largest", etc.

### Combine via Sort + Binary Search

```python
sums_A = sorted(sum_of(s) for s in subsets_of_A)
for subset in subsets_of_B:
    target = T - sum_of(subset)
    if binary_search(sums_A, target):
        return True
```

- **Time:** O(2^(n/2) · n/2) combine (log factor from binary search).
- **Space:** O(2^(n/2)) for the sorted list.
- **Pro:** Supports range queries ("closest", "at most k", etc.).
- **Con:** Slower by a log factor than hashing.

Use hashing for "does a sum equal T?" questions. Use sort + binary
search for "find the closest sum" or "count sums within [L, R]"
questions.

---

## MITM vs Related Techniques

| Technique                  | Typical regime       | When it beats MITM       |
|----------------------------|----------------------|--------------------------|
| Brute force                | n ≤ 25               | Simpler, just as fast    |
| **Meet in the Middle**     | n = 30–50            | the regime it was made for |
| Dynamic Programming        | n large, state small | When DP state is polynomial |
| Pseudo-polynomial DP       | small values         | DP O(n·T) beats MITM when T is small |
| Branch & Bound             | Optimization with good bounds | If the bound is cheap/tight |

**MITM vs DP** is the most interesting comparison. For Subset Sum:

- **DP:** O(n · T) time, O(T) space. Good when T is small (say, T ≤ 10^5).
- **MITM:** O(n · 2^(n/2)) time, O(2^(n/2)) space. Good when n is
  small but T is huge.

They're complementary — pick based on which input size is the binding
constraint.

---

## The General Recipe

```
1. Split the input into two halves A and B.
2. Enumerate every "partial answer" over A.
    - Store them in a sorted list / hash set / indexed structure.
3. For each partial answer over B:
    - Compute the "missing complement" needed from A.
    - Look up the complement using the structure from step 2.
    - Record or return a match.
```

The ingredients are:

- **An enumerable search space** (subsets, bitmasks, permutations of
  small subsets).
- **A split point** where the two halves are independent.
- **A complement / combine operation** you can compute quickly.
- **A compatible data structure** (set, sorted list, balanced tree)
  to make the lookup fast.

---

## Canonical Applications

### Subset Sum with Large Target

Given `nums` (n ≤ 40) and a target `T` (possibly 10^15), is there a
subset summing to exactly T? See [`problems/subset-sum.py`](problems/subset-sum.py).

### 4Sum — LeetCode #18

Find all unique quadruples summing to a target. Brute is O(n^4). MITM
treats pairs as atoms: enumerate all O(n^2) pair-sums from the two
halves, then use hashing to find pair-pair matches.

### Count Pairs with a Given Sum in Two Large Arrays

When each array alone has n = 10^5 but you can't afford to sort them
together, MITM-style hashing + lookup is natural.

### Closest Subset Sum to Target

Enumerate both halves, sort one, binary-search from the other for the
closest complement. MITM + two-pointer walk over the sorted half also
works in O(2^(n/2)).

### Number of Subsets with Sum ≤ T

Count rather than find. Same enumeration structure; combine step
counts "how many sums in A are ≤ T - sum(B_subset)" via binary search.

---

## Complexity

For a problem of size n:

- **Time:** O(2^(n/2) · poly(n)) — the poly factor absorbs sum
  computation and binary-search log factors.
- **Space:** O(2^(n/2)) — the crucial cost. For n = 50 that's ~3·10^7
  entries; manageable but not trivial.

The technique's value is entirely about **n**, not about the cost per
operation. Use it when you need to push n from 25 up to 40 or 50; don't
use it when a polynomial algorithm would work.

---

## Pitfalls

- **Applying MITM when DP is better.** If T is small, DP is O(n·T) —
  usually a better call than MITM's O(2^(n/2)).
- **Enumerating subsets naively in a list.** Building all subsets by
  appending to a list is O(2^n · n) TOTAL, which is fine, but it also
  uses O(2^n · n) memory. Stream the subset-sums as ints instead of
  storing the actual subsets.
- **Not splitting evenly.** Split the input in HALF — a 60/40 split
  has cost O(2^0.6n) on the larger half, which is worse than O(2^0.5n).
- **Double-counting or missing edge cases.** The "empty subset" sum is
  0; make sure your enumeration includes it (the all-false bitmask).
- **Hash collisions on floating-point sums.** If your sum is a float,
  hashing is fragile (two float values that SHOULD be equal may differ
  by ULPs). Stick to ints or use rounded representations.
- **Using MITM when two halves aren't independent.** If the problem's
  halves interact — e.g., "pick exactly one element per pair" across
  the split — MITM doesn't apply.

---

## Pseudocode Skeleton

```
def meet_in_the_middle(nums, target):
    n = len(nums)
    A = nums[:n//2]
    B = nums[n//2:]

    sums_A = {0}
    for x in A:
        sums_A |= {s + x for s in sums_A}      # enumerate via doubling

    sums_B = {0}
    for x in B:
        sums_B |= {s + x for s in sums_B}

    # combine: is there sa + sb == target?
    for sb in sums_B:
        if (target - sb) in sums_A:
            return True
    return False
```

For a concrete implementation with the subset actually reconstructed
rather than only detected, see [`template.py`](template.py). For the
worked subset-sum problem, see
[`problems/subset-sum.py`](problems/subset-sum.py).

---

## Key Takeaways

1. **MITM splits an exponential problem in half**, reducing O(2^n) to
   O(2^(n/2) · poly(n)).
2. **Useful regime:** n ≈ 30–50. Below that, brute force is easier.
   Above, even MITM fails.
3. **Two combine strategies:** hash set (O(1) lookup) or sort + binary
   search (ordered queries). Pick based on the question.
4. **Prerequisite:** the two halves must be INDEPENDENT — each can be
   enumerated without knowing the other's choices.
5. **MITM and DP are complementary.** Use DP when the VALUES are
   small; use MITM when n is small but values are huge.
