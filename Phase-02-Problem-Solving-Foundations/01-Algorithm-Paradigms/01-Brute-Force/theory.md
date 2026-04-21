# Brute Force — Theory

## Introduction

**Brute force** is the most honest paradigm: *"I don't know a clever trick,
so I'll just try every possibility and check which one works."*

It's often dismissed as "the dumb approach," but that reputation is unearned.
Brute force is:

- **Always applicable.** If a problem has a finite search space, brute force
  works. No cleverness required.
- **Always correct.** By construction, it checks every candidate — so it
  cannot miss the right answer.
- **The foundation every other paradigm improves on.** Divide & Conquer,
  Greedy, and DP are all just brute force with redundant work cut out.

The only thing wrong with brute force is usually speed. That's a problem
you solve *after* you have a correct brute-force solution — not before.

> **Golden rule:** always describe the brute force first. Even if you never
> run it, the act of writing it down tells you what the search space is and
> where the slow parts live — which is exactly what you need to optimize.

---

## The Brute Force Recipe

Every brute-force algorithm follows the same three-step shape:

1. **Define the search space.** What is the set of *all possible answers*
   to this problem? (All pairs? All subsets? All orderings?)
2. **Enumerate it.** Generate every candidate in that space.
3. **Validate each candidate.** Check whether it satisfies the problem's
   constraints; track the best one seen so far.

That's it. The paradigm has no other rules.

---

## Common Search Spaces

The "shape" of the search space determines the brute-force complexity:

| Search space                            | Size       | Typical complexity |
|-----------------------------------------|------------|--------------------|
| All single elements of an array of n    | n          | O(n)               |
| All pairs `(i, j)` with `i < j`         | n(n-1)/2   | O(n²)              |
| All triples                             | n³ / 6     | O(n³)              |
| All contiguous subarrays                | n(n+1)/2   | O(n²) to enumerate, often O(n³) to evaluate |
| All subsets of a set of n elements      | 2^n        | O(2^n)             |
| All permutations of n elements          | n!         | O(n!)              |

Recognizing the shape of the search space is the first skill to develop.
Once you see that a problem asks for "the best pair" or "the best subset,"
you already know the brute-force complexity before writing any code.

---

## When Brute Force Is the Right Answer

Brute force is the **correct final answer** more often than people admit:

- **n is tiny.** For n ≤ 20 or so, even O(2^n) or O(n!) runs in milliseconds.
  If your input is small and bounded, stop optimizing.
- **The problem is stated as "find all …".** You need every valid solution,
  so you have to enumerate them regardless — you can't do better than the
  output size.
- **You can't prove a clever approach correct.** A slow-but-correct solution
  is better than a fast-but-wrong one. Always.
- **You're writing a reference to test a faster version against.** Brute
  force is the "ground truth" you compare your optimized code to.

When you're not sure whether to optimize, ask: *"what's the largest n this
code will ever see in practice?"* If the answer is "a few thousand" and
your brute force runs in milliseconds on that input, you are done.

---

## When to Move On From Brute Force

Brute force is too slow when:

1. **The input n is large** relative to your search space:
   - n = 10⁵ and your algorithm is O(n²) → 10¹⁰ operations → too slow.
   - n = 30 and your algorithm is O(2^n) → 10⁹ operations → too slow.
2. **The brute force passes small tests but times out on hidden large cases.**
   (This is the most common real-world signal.)

When that happens, ask these three questions in order:

1. **Is there structure I'm not exploiting?** Sorted input, nested loops
   that recompute the same value, a monotonic condition — these are signals
   to use **two pointers**, **binary search**, or **prefix sums**.
2. **Do my nested loops recompute the same subproblem?** That's **DP** or
   **memoization**.
3. **Can I make a locally-best choice without backtracking?** That's **greedy**.

Every optimization after brute force is an answer to "*what work am I
doing that I don't need to do?*"

---

## Brute Force vs "Naive"

These terms get used interchangeably, but there's a useful distinction:

- **Naive**: the first solution you thought of, possibly correct, possibly not.
- **Brute force**: a *systematic, complete* enumeration of the search space.
  Guaranteed correct.

A naive solution might accidentally skip cases or miscount; a brute-force
solution cannot, because it enumerates by construction. When you can't
prove a clever algorithm correct, compare it against the brute force on
small inputs — any disagreement means your clever algorithm is wrong.

---

## The Canonical Examples

These are the problems you'll see over and over as brute-force starting points:

| Problem                       | Brute-force shape                       | Faster paradigm                 |
|-------------------------------|-----------------------------------------|---------------------------------|
| **Two Sum**                   | Check every pair — O(n²)                | Hashing — O(n)                  |
| **Maximum Subarray**          | Every subarray — O(n²) or O(n³)         | Kadane's DP — O(n)              |
| **Longest Substring**         | Every substring — O(n²) or O(n³)        | Sliding window — O(n)           |
| **Closest Pair of Points**    | Every pair — O(n²)                      | Divide & Conquer — O(n log n)   |
| **Knapsack**                  | Every subset — O(2^n)                   | DP — O(n · W)                   |
| **Traveling Salesman**        | Every permutation — O(n!)               | DP with bitmask — O(n² · 2^n)   |

The brute-force columns teach you to *see the search space*. The
"faster paradigm" columns are what the rest of this phase is about.

---

## Complexity Template

For a typical brute force with inputs of size n:

- **Time:** whatever the size of your search space is, times the cost of
  validating each candidate. So checking every pair and verifying each
  in O(1) is O(n²); checking every subset and scoring each in O(n) is O(n · 2^n).
- **Space:** usually O(1) extra beyond the input — you're not building
  lookup tables, just scanning. When brute force does need memory (e.g., to
  store all solutions), the space is proportional to the output size.

---

## Pseudocode Skeleton

```
function brute_force(input):
    best = None

    for candidate in enumerate_search_space(input):
        if is_valid(candidate, input):
            best = better_of(best, candidate)

    return best
```

The whole paradigm fits in five lines. Everything else is a smarter
`enumerate_search_space` or a smarter `is_valid`.

For a concrete implementation of this shape, see [`template.py`](template.py).
For worked problems, see [`problems/`](problems/).

---

## Key Takeaways

1. **Always start with brute force.** Even if you throw it away. It tells
   you the search space.
2. **Brute force is correct by construction** — no cleverness, no edge cases.
3. **Brute force is usually slow, not usually wrong.** Those are very
   different problems. Optimize after correctness.
4. **"Can I do better?" is the only interesting question once the brute
   force works.** Every technique in Phase 02 / 02 is an answer to it.
