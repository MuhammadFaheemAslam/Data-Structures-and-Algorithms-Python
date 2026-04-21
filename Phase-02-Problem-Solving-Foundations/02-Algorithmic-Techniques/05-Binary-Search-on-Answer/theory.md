# Binary Search on Answer — Theory

## Introduction

**Binary Search on Answer** (BSOA) is a technique that extends binary
search beyond sorted arrays. Instead of searching for a target value
inside the input, you search for the **answer itself** — the optimal
value the problem is asking for.

The idea:

> *If "is X a feasible answer?" is a **monotone** question — i.e., if
> X works, every X' better than X also works — then you can binary
> search over all candidate answers to find the boundary.*

This unlocks a whole class of problems that look like optimization
challenges but are actually searches in disguise:

- **"Minimum capacity such that …"** (ship, jar, bathroom)
- **"Minimum speed such that …"** (Koko's bananas, running a marathon)
- **"Largest value such that …"** (split arrays, distribute items)
- **"Smallest threshold such that …"** (stream problems)

The trick is recognising the monotone predicate. Once you see it, the
problem collapses into a standard binary search with a `check(X)`
function — usually the easy part.

---

## The Core Idea

A standard binary search on a sorted array `arr` looks like:

```
find X in arr where arr[mid] == X, narrowing [lo, hi]
```

Binary search on answer replaces the array with a **range of candidate
answers**, and the comparison with a **predicate**:

```
find the smallest X in [lo, hi] such that check(X) is True
```

The range `[lo, hi]` might be `[1, maxValue]`, `[minSum, totalSum]`,
or anything else problem-dependent. What matters is that:

1. **`check(X)` is monotone** — once `check(X)` becomes True, it stays
   True for all X' > X (for "minimize" problems) or all X' < X (for
   "maximize" problems).
2. **`check(X)` runs in reasonable time** — typically O(n) or O(n log n).
3. **The search range `[lo, hi]` has a known upper bound.**

Under those conditions, the binary search itself has log(range) iterations,
each costing one `check` call. Total cost: **O(n · log(range))**.

---

## The Two Templates

### Template A — Minimum X such that check(X) is True

Used when you want the **smallest** value that satisfies a constraint.
The predicate must be monotone: "False for small X, becomes True at
some point, True forever after."

```python
def min_feasible(lo, hi):
    while lo < hi:
        mid = (lo + hi) // 2
        if check(mid):
            hi = mid                     # mid works — try smaller
        else:
            lo = mid + 1                 # mid doesn't — must be bigger
    return lo                             # lo == hi == smallest feasible
```

Pattern: **True on the right, False on the left**. The answer is the
left edge of the True region.

### Template B — Maximum X such that check(X) is True

Used when you want the **largest** value. Predicate: "True for small X,
then becomes False."

```python
def max_feasible(lo, hi):
    while lo < hi:
        mid = (lo + hi + 1) // 2         # CEIL — avoid infinite loop when lo + 1 == hi
        if check(mid):
            lo = mid                     # mid works — try bigger
        else:
            hi = mid - 1                 # mid doesn't — must be smaller
    return lo
```

Pattern: **True on the left, False on the right**. The answer is the
right edge of the True region.

> **Watch for:** Template B uses `(lo + hi + 1) // 2` (a ceiling) to avoid
> a subtle infinite loop when `hi = lo + 1`. Template A's floor is fine.

---

## Why This Is Binary Search

Both templates have the same shape as binary search on a sorted array
— because they ARE binary searches, just over a different collection.

Think of the range `[lo..hi]` as an imaginary array where each index
`X` holds `check(X)`. Since the predicate is monotone, this imaginary
array is **sorted** (all Falses, then all Trues, or vice versa). We're
doing standard binary search for the boundary between the two regions.

This reframing makes two things clear:

- **You don't need an actual sorted input.** The sortedness is in the
  answer space, not the input.
- **The number of iterations is O(log(hi - lo))**, not O(log n). The
  bound is logarithmic in the *range of possible answers*, which can
  matter for problems with large value ranges.

---

## When to Reach for Binary Search on Answer

Strong signals:

1. The problem says **"minimum X such that …"** or **"maximum X such
   that …"**. The X you're finding is a number, not an index.
2. Given a specific X, it's **easy** to check whether X is feasible —
   usually a simulation, a greedy pass, or a single scan.
3. There's a **monotonic relationship** between X and feasibility. If
   X = 100 works, X = 200 obviously works too (or vice versa).
4. The search space is bounded — usually `[1, some_max]` or `[total,
   0]`, not unbounded.

Weak signals:

5. The problem *looks* like optimization (might be DP), but the DP
   would be exponential. Often a binary-search-on-answer shortcut works.
6. The problem has parameters like "capacity", "speed", "threshold" —
   all of which are numbers whose feasibility is monotone.

Red flags that indicate NOT BSOA:

- The problem needs a specific *structure* as output (permutation,
  path, selection). Binary search only finds a scalar.
- No monotonicity — some X work, smaller Xes don't, but SMALLER still
  don't. This isn't a monotone predicate; binary search won't converge.

---

## Common Search Ranges

Picking the right `[lo, hi]` is often half the problem. Common choices:

| Problem type                              | Natural `lo`         | Natural `hi`             |
|-------------------------------------------|----------------------|--------------------------|
| "Min speed to finish in H hours"          | 1                    | max(piles)               |
| "Min capacity to ship packages in days"   | max(weights)         | sum(weights)             |
| "Split array, min largest sum"            | max(arr)             | sum(arr)                 |
| "Max min distance between points"         | 0                    | (max - min) / (k - 1)    |
| "Smallest threshold > some divisor"       | 1                    | max(arr)                 |

Getting `lo` and `hi` right is a correctness concern — too small a
range will miss the answer; too large wastes iterations (trivially).

The lower bound is usually the smallest value that *could* be the
answer given the problem's constraints (often 1, `max(arr)`, or 0).
The upper bound is usually either `sum(arr)`, `max(arr)`, or some
problem-specific ceiling.

---

## Anatomy of `check(X)`

The `check(X)` function is usually the meat of the problem. Typical
shapes:

### Shape 1: Greedy simulation

"Given capacity/speed/threshold X, can we do it?"

```python
def check(x):
    # walk the input, simulate with parameter X
    used = 0
    for item in arr:
        # ... something using x ...
    return used <= limit
```

Cost: usually O(n) per call.

### Shape 2: Greedy grouping

"Given cap X, how many groups/pieces do we need?"

```python
def check(x):
    groups = 1
    running = 0
    for v in arr:
        if running + v > x:
            groups += 1
            running = v
        else:
            running += v
    return groups <= max_groups
```

Cost: O(n) per call.

### Shape 3: Counting

"For parameter X, how many items fit / cross threshold / fall below?"

```python
def check(x):
    count = sum(1 for v in arr if v <= x)       # or some variant
    return count >= k
```

Cost: O(n) per call (O(log n) if the input is sorted and you use bisect).

In all three shapes, the predicate is simple once you can compute
`check(X)` in O(n). The BSOA wrapping contributes one more `log`
factor, giving a total of O(n log V) where V is the search range.

---

## Binary Search on Answer vs Related Techniques

| Technique                     | What it does                              |
|-------------------------------|-------------------------------------------|
| **Standard Binary Search**    | Find target in sorted array.              |
| **Binary Search on Answer**   | Find optimal value via monotone predicate. |
| **Greedy**                    | Commit locally-best choice; no search.    |
| **Dynamic Programming**       | Explore every state with memoization.     |
| **Parametric Search**         | Generalization of BSOA to continuous spaces. |

The most useful comparison is against DP. Many BSOA problems *look*
like DP problems (optimization over choices), but BSOA short-circuits
the state space by searching the answer directly. When applicable it
is usually much faster than DP.

---

## Complexity

- **Time:** O(log(hi - lo)) × O(check). The `check` function dominates.
- **Space:** O(1) for the search itself; whatever `check` uses internally.

For Koko Bananas: O(n log(max_pile)). For Split Array Largest Sum:
O(n log(sum(arr))). Both are ~O(n · 30) ≈ O(n) in practice — unbeatable.

---

## Pitfalls

- **Checking the wrong direction of monotonicity.** If you confuse "min
  feasible X" with "max feasible X", your pointers update in opposite
  directions and you converge to the wrong boundary. Always write
  a one-line sanity check: "if `check(lo) == True`, my answer is `lo`".
- **Off-by-one on `mid`.** Template A uses floor; Template B needs ceil.
  Getting this wrong can cause an infinite loop or a ±1 error.
- **Tight `lo` and `hi`.** Too tight a range misses the answer. When
  unsure, err wider — the log factor is cheap.
- **Non-monotonic predicate.** Double-check monotonicity before coding.
  If the predicate flips multiple times over the range, binary search
  won't work — you'd need a different technique (ternary search for
  unimodal functions, or full DP).
- **Expensive `check`.** Each call is inside the binary-search loop.
  An O(n²) check makes the whole algorithm O(n² log V), often
  unnecessary — see if you can do it in O(n).
- **Integer vs floating-point search.** Integer BSOA uses `//` and
  converges exactly. Floating-point BSOA needs an epsilon termination
  condition (`while hi - lo > 1e-9`).

---

## Canonical Examples

### Koko Eating Bananas — LeetCode #875

Find the minimum integer speed k such that eating piles at k/hour
finishes within H hours.

### Split Array Largest Sum — LeetCode #410

Partition an array into m contiguous subarrays to minimize the largest
subarray sum.

### Capacity to Ship Packages Within D Days — LeetCode #1011

Minimum ship capacity to deliver packages in order within D days.

### Find the Smallest Divisor Given a Threshold — LeetCode #1283

Smallest integer divisor such that the sum of ceil(arr[i]/divisor)
is ≤ threshold.

### Aggressive Cows (SPOJ classic)

Given n stalls and k cows, maximize the minimum distance between any
two cows.

All of these have the same skeleton: define `check(X)`, binary search
the answer range. Learn the template once; each problem differs only
in the one-paragraph `check` function.

---

## Key Takeaways

1. **BSOA transforms an optimization problem into a search problem.**
   You stop thinking "how do I build the best answer?" and start
   thinking "given a candidate answer, does it work?"
2. **Two templates:** minimum feasible (floor mid) and maximum feasible
   (ceil mid). Pick based on "True-on-right" or "True-on-left".
3. **The monotonicity of `check(X)` is the precondition.** Verify it
   before reaching for binary search.
4. **Time is O(n log V)** — the log is over the value range, not n.
   For most problems this is the fastest possible algorithm.
5. **Recognizing the pattern is half the game.** Once you see
   "min/max X such that predicate holds" and realise the predicate
   is monotone, the rest is a fill-in-the-blank exercise.

For the template, see [`template.py`](template.py). For two worked
problems covering both directions of monotonicity, see
[`problems/koko-bananas.py`](problems/koko-bananas.py) (min feasible)
and [`problems/split-array.py`](problems/split-array.py) (min feasible
of a harder predicate).
