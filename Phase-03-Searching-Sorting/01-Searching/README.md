# 01 — Searching

Searching is *"finding a value or a position in a collection"* — the
most frequent operation in all of software. This section covers the
five classical search algorithms, in increasing order of structure
they exploit.

| # | Algorithm              | Core idea                                        | Requires sorted? |
|---|------------------------|--------------------------------------------------|------------------|
| 1 | **Linear Search**      | Scan left to right. The baseline.                | No               |
| 2 | **Binary Search**      | Halve the search range every step.               | **Yes**          |
| 3 | **Jump Search**        | Jump √n at a time, then linear within the block. | **Yes**          |
| 4 | **Exponential Search** | Double the range until overshoot, then binary.   | **Yes**          |
| 5 | **Ternary Search**     | Divide by three; for **unimodal** functions.     | Yes / unimodal   |

The progression is a clean "what structure can I exploit?" story:

- **No structure?** → Linear (O(n)).
- **Sorted + random access?** → Binary (O(log n)).
- **Sorted + sequential-access media?** → Jump (O(√n)).
- **Sorted + unknown size?** → Exponential (O(log i)).
- **Unimodal function?** → Ternary (O(log n) probes of two each).

---

## The Searching Decision Flowchart

```
Is the data SORTED?
    No  → Linear Search (or hash set if many queries)
    Yes:
        Is the size KNOWN?
            No  → Exponential Search (discovers range first)
            Yes:
                Is RANDOM ACCESS cheap?
                    Yes → Binary Search
                    No  → Jump Search (tape/stream)

Is the data UNIMODAL (single peak/valley)?
    → Ternary Search

Is the TARGET likely near the start of a huge array?
    → Exponential Search (O(log i) when i << n)
```

---

## Complexity at a Glance

| Algorithm            | Best    | Average  | Worst    | Space  | Sorted?  |
|----------------------|---------|----------|----------|--------|----------|
| Linear Search        | O(1)    | O(n)     | O(n)     | O(1)   | No       |
| Binary Search        | O(1)    | O(log n) | O(log n) | O(1)   | **Yes**  |
| Jump Search          | O(1)    | O(√n)    | O(√n)    | O(1)   | **Yes**  |
| Exponential Search   | O(1)    | O(log i) | O(log n) | O(1)   | **Yes**  |
| Ternary Search       | O(1)    | O(log n) | O(log n) | O(1)   | Yes / unimodal |

Where `i` = index of the target. Exponential wins when the target is
near the start of a huge array.

All five are O(1) space and deterministic. Binary Search is the
default for most interview and production scenarios.

---

## Why Binary Search Gets Special Treatment

Of the five, **Binary Search is deep enough to be its own sub-module**.
Its `02-Binary-Search/` folder contains:

- `iterative.py` — the textbook version.
- `recursive.py` — the same algorithm as divide & conquer.
- `variations/` — four canonical variants:
    - `first-occurrence.py`
    - `last-occurrence.py`
    - `lower-bound.py` (Python's `bisect_left`)
    - `upper-bound.py` (Python's `bisect_right`)
- `problems/` — three classic problems:
    - `rotated-array.py` (LC #33)
    - `peak-element.py` (LC #162)
    - `sqrt.py` (LC #69)

Lower-bound and upper-bound in particular are the two most reusable
binary-search primitives — almost every "binary search with a twist"
problem reduces to one or two calls to these two functions.

---

## Folder Layout

```
01-Searching/
├── README.md                           ← you are here
├── 01-Linear-Search/
│   ├── implementation.py               ← 5 variants (first, all, recursive, with-key, min/max)
│   ├── sentinel-search.py              ← the classical optimization
│   └── problems.md                     ← 14 practice problems in 3 tiers
│
├── 02-Binary-Search/                   ← the deep module
│   ├── iterative.py
│   ├── recursive.py
│   ├── variations/
│   │   ├── first-occurrence.py
│   │   ├── last-occurrence.py
│   │   ├── lower-bound.py
│   │   └── upper-bound.py
│   └── problems/
│       ├── rotated-array.py
│       ├── peak-element.py
│       └── sqrt.py
│
├── 03-Jump-Search/
│   ├── implementation.py               ← √n-step block search
│   └── analysis.md                     ← why √n is the minimizer
│
├── 04-Exponential-Search/
│   ├── implementation.py               ← includes UnknownSizeArray variant
│   └── analysis.md                     ← + Timsort's galloping search
│
└── 05-Ternary-Search/
    ├── implementation.py               ← sorted + unimodal-array + continuous variants
    └── analysis.md                     ← + golden-section search
```

Each module either has an `analysis.md` companion (the shorter ones)
or an embedded "when to use" section in the `.py` file itself (Linear
Search, Binary Search).

---

## The Big Lesson — Structure Beats Brute Force

All four sub-linear algorithms (binary / jump / exponential / ternary)
get their speedup from the same place: **they exploit a structural
property of the input**.

- Binary / Jump / Exponential: the input is **sorted** — so a single
  comparison can rule out half (or more) of the remaining candidates.
- Ternary on unimodal functions: the **peak-then-valley structure**
  lets two probes decide which third of the range to discard.

Without that structure, the best you can do is Linear — **look at
every element**. That's the lower bound for an unsorted search.

This is the same pattern that appears in:
- Phase-02 / 02 / 05-Binary-Search-on-Answer — binary searching the
  SOLUTION SPACE instead of the input.
- Phase-03 / 02 / 03 — non-comparison sorts that exploit key structure
  to break the O(n log n) comparison lower bound.

**Structure-aware algorithms are the difference between O(n) and
O(log n) — and sometimes between "runs in milliseconds" and "runs in
hours."** Recognizing when structure exists is half the skill.

---

## Outcome

By the end of this section you should be able to:

1. **Pick correctly.** Given the input's shape, reach for the right
   search algorithm without hesitation.
2. **Implement Binary Search fluently** — including the four common
   boundary variants. This alone covers ~30% of search-style
   interview questions.
3. **Recognize hidden search problems.** Koko Eating Bananas,
   Split Array Largest Sum, and many "minimize / maximize under
   constraints" problems are binary searches over an ANSWER space —
   covered in Phase-02 / 02 / 05.
4. **Know when NOT to search.** If you have many queries on the
   same data, hashing (O(1) per query) beats any binary search.
