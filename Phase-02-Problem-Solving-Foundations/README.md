# Phase 02 — Problem-Solving Foundations

Phase 01 taught you **what tools exist** (Python's built-in data structures) and
**how to measure their cost** (time and space complexity).

Phase 02 is about something very different. It's about learning to **recognize
patterns** in problems so you know which tool — and which technique — to reach
for before you've written a single line of code.

---

## Two Halves

This phase is split into two complementary parts:

### 01 — Algorithm Paradigms

The **high-level strategies** for attacking a problem. These are the lenses
you use before you worry about any specific data structure.

| # | Paradigm               | The core idea                                              |
|---|------------------------|------------------------------------------------------------|
| 1 | Brute Force            | Try every possibility. Always correct, sometimes too slow. |
| 2 | Divide & Conquer       | Split the problem, solve the halves, combine.              |
| 3 | Greedy                 | Make the locally best choice and never revisit.            |
| 4 | Dynamic Programming    | Remember overlapping subproblem answers.                   |
| 5 | Backtracking           | Search all possibilities with smart pruning.               |
| 6 | Branch & Bound         | Backtracking + a bound function for optimization.          |

When you understand these six, 80% of "unseen" problems start to feel familiar.

### 02 — Algorithmic Techniques

The **reusable micro-patterns** that appear across problems. These are the
specific moves you execute *inside* a paradigm.

| # | Technique                 | When you reach for it                                |
|---|---------------------------|------------------------------------------------------|
| 1  | Two Pointers             | Sorted arrays, pair-finding, in-place partitioning.  |
| 2  | Sliding Window           | Contiguous subarray / substring problems.            |
| 3  | Prefix Sum               | Fast range sums on an immutable array.               |
| 4  | Difference Array         | Fast range updates.                                  |
| 5  | Binary Search on Answer  | Minimize / maximize over a monotonic predicate.      |
| 6  | Fast & Slow Pointers     | Cycle detection and middle-finding on sequences.     |
| 7  | Hashing                  | Turn O(n²) search into O(n) lookup.                  |
| 8  | Frequency Counting       | Count occurrences, find majorities, compare multisets. |
| 9  | Monotonic Stack          | Next-greater / next-smaller element problems.        |
| 10 | Meet in the Middle       | Split an exponential search in half.                 |
| 11 | Bit Manipulation         | Subsets, parity, set operations on small ints.       |
| 12 | Merge Intervals          | Overlap and scheduling problems.                     |

Each technique has a **template file** — a clean, reusable shape you can
adapt to new problems — plus 2–3 worked examples.

---

## How to Work Through This Phase

There are two reasonable orders:

**Paradigms first (top-down).** Read each paradigm's `theory.md`, do its
problems, then move to the techniques. This is the right order if you
learn better from big ideas down to specifics.

**Techniques first (bottom-up).** Learn the templates by doing, then read
the paradigms afterwards to see how the templates fit into broader strategies.
This is the right order if you learn better by pattern-matching on concrete
examples first.

Either way works. What matters is that **by the end you can look at a new
problem and within a minute say "this smells like X"** — whether X is a
paradigm or a specific technique.

---

## Folder Layout

```
Phase-02-Problem-Solving-Foundations/
├── README.md                          ← you are here
├── 01-Algorithm-Paradigms/
│   ├── overview.md                    ← how paradigms compare
│   ├── 01-Brute-Force/
│   ├── 02-Divide-Conquer/
│   ├── 03-Greedy/
│   ├── 04-Dynamic-Programming/
│   ├── 05-Backtracking/
│   └── 06-Branch-Bound/
└── 02-Algorithmic-Techniques/
    ├── README.md
    ├── 01-Two-Pointers/
    ├── 02-Sliding-Window/
    ├── 03-Prefix-Sum/
    ├── 04-Difference-Array/
    ├── 05-Binary-Search-on-Answer/
    ├── 06-Fast-Slow-Pointers/
    ├── 07-Hashing-Technique/
    ├── 08-Frequency-Counting/
    ├── 09-Monotonic-Stack/
    ├── 10-Meet-in-the-Middle/
    ├── 11-Bit-Manipulation/
    └── 12-Merge-Intervals/
```

Each leaf module follows a consistent shape:

- `theory.md` — what the pattern is, when it applies, its complexity
- `template.py` — a clean, reusable reference implementation
- `problems/` — worked problem files, each runnable with assertions

---

## Outcome

By the end of Phase 02 you should be able to:

- Classify a new problem into a known paradigm within a minute.
- Pick the right technique template and adapt it, rather than inventing from scratch.
- Explain **why** a greedy approach fails on a problem that DP solves, and vice versa.
- Recognize when you're about to write O(n²) code and reach for a dict / two-pointer fix first.

That is the difference between "writing code that happens to work" and
**engineering solutions**.
