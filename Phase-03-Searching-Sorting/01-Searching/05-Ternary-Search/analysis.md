# Ternary Search — Analysis

## Two Distinct Uses

Ternary search is often described as one algorithm; it's really two:

| Use                           | Worth knowing?  | Practical?         |
|-------------------------------|-----------------|--------------------|
| On sorted arrays              | For context only | No — binary search wins |
| On unimodal functions         | **Yes**         | **Yes**            |

This file treats both, but the unimodal-function version is the
interesting one.

---

## Complexity Comparison

### On Sorted Arrays (vs Binary Search)

| Metric                           | Binary Search   | Ternary Search     |
|----------------------------------|-----------------|---------------------|
| Iterations                       | O(log₂ n)       | O(log₃ n)           |
| Comparisons per iteration        | 1               | 2                   |
| Total comparisons                | log₂ n          | **2 log₃ n ≈ 1.26 log₂ n** |
| Range reduction per iteration    | ÷2              | ÷3                  |

Ternary search does FEWER iterations but MORE comparisons per iteration,
and the product favours binary search. It's a counterintuitive but clean
illustration that "more partitions" doesn't always mean "faster search."

### On Unimodal Functions

| Metric                          | Bound                                 |
|---------------------------------|---------------------------------------|
| Time                            | O(log_(3/2) n) ≈ 1.71 log₂ n probes  |
| Space                           | O(1)                                  |

Each iteration shrinks the bracket by a factor of 2/3 (not 1/3 — we
keep two-thirds of the range, discarding only one end third). This
is still sub-linear and the standard choice for unimodal optimization
without derivatives.

---

## The Unimodal Function Use Case

A function f is UNIMODAL on [lo, hi] if it has exactly ONE peak — it
strictly increases then strictly decreases (or vice versa).

Ternary search on such a function:

    mid1 = lo + (hi - lo) / 3
    mid2 = hi - (hi - lo) / 3

    if f(mid1) < f(mid2):
        peak is in (mid1, hi]      →  lo = mid1
    else:
        peak is in [lo, mid2)      →  hi = mid2

Each iteration discards the bottom third if the function is rising at
mid1, else the top third if the function is falling at mid2.

### Why Not Binary Search?

Binary search needs a monotonic decision rule — "which side is the
answer on?" For a unimodal peak, looking at a SINGLE midpoint doesn't
tell you which direction the peak lies in (the function could be
anywhere on either slope). You need TWO probes per iteration to
distinguish "still rising" from "already falling".

Ternary search with two probes per iteration gives you that
information; binary search with one probe can't.

(The peak-element problem LC #162 IS solvable with binary search —
but only because the array's discrete structure lets you compare
ADJACENT values. In continuous unimodal optimization, adjacent
values don't exist.)

---

## When Ternary Search Wins

- **Optimizing a continuous function without derivatives:** ternary
  search with no calculus; gradient descent with derivatives. Pick
  whichever matches what you have.
- **Discrete unimodal arrays where adjacent comparisons are expensive:**
  rare, but ternary converges faster than "scan until peak".
- **Competitive programming:** some problems set up a unimodal
  function in a roundabout way — find the parameter that maximizes
  some outcome. Ternary is the go-to.
- **Physical / simulation optimization:** sweet-spot finding in
  engineering models.

---

## Gotchas

### 1. Floating-Point Termination

With a continuous function, the loop can run forever if it terminates
only on exact equality. Use an epsilon:

    while hi - lo > eps:
        ...

Typical eps is `1e-9` or `1e-6`, depending on your precision needs.

### 2. The Function Must Be *Strictly* Unimodal

If there's a plateau (adjacent values equal), ternary search can get
stuck on the plateau and miss the true peak. Break ties consistently
in one direction or preprocess the input.

### 3. For Discrete Arrays, Use Binary Search Instead (Usually)

Finding the peak of a discrete unimodal array is solvable with
binary search in O(log n) time:

    if arr[mid] < arr[mid + 1]: peak is right
    else: peak is at mid or left

Ternary search works but has no advantage over binary search for
discrete inputs where adjacent comparisons are cheap.

### 4. Two Comparisons vs One

Be aware that ternary search's per-iteration cost is higher. If
function evaluations are EXPENSIVE (e.g., a simulation), the 2×
overhead per iteration can outweigh the reduced iteration count.
Measure before you decide.

---

## Ternary Search vs Golden-Section Search

A close cousin: **Golden-Section Search** probes at the golden-ratio
points rather than thirds. This is slightly more efficient because
ONE of the two probe points can be REUSED from the previous iteration
(instead of recomputing both). The number of function evaluations
per iteration drops from 2 to effectively 1.

If you're doing unimodal optimization with expensive function
evaluations, golden-section search is the production-grade choice.
Ternary search is simpler to explain.

---

## Pitfalls

- **Applying ternary search to a non-unimodal function.** It will
  return wrong answers silently. Verify unimodality.
- **Integer arithmetic on (hi - lo) / 3.** On integer arrays, use
  `// 3` and be careful with `mid1 == mid2` when the range is small.
- **Wrong termination.** For integer ranges, `while lo < hi`; for
  continuous ranges, `while hi - lo > eps`.
- **Binary search is the right tool more often than you think.**
  Before reaching for ternary, ask: is this actually a monotone
  decision, not a unimodal one?

---

## Key Takeaways

1. **Ternary search on sorted arrays is worse than binary search.**
   Included here for completeness only.
2. **Ternary search on unimodal functions is the real use case.**
   O(log n) probes; no calculus needed.
3. **Needs TWO probes per iteration.** Each probe + comparison shrinks
   the bracket by 1/3 (eliminates one third, keeps two).
4. **Use epsilon-based termination for continuous functions** and
   integer-range termination for discrete arrays.
5. **For expensive function evaluations, consider golden-section
   search** — strictly better constant factors.
