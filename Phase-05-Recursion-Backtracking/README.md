# Phase 05 — Recursion & Backtracking

Phase 02 introduced recursion as part of Divide & Conquer and
Backtracking as a paradigm. **Phase 05 is where they become
first-class subjects** — treated with the depth they deserve as
a category of problem-solving in their own right.

Two halves:

1. **Recursion** (`01-Recursion/`) — the raw mechanic of "a function
   that calls itself." How to write it, how to visualize its call
   tree, how to reason about its correctness and complexity.

2. **Backtracking** (`02-Backtracking/`) — the disciplined application
   of recursion to **search problems**: subsets, permutations,
   combinations, N-Queens, Sudoku, word search, graph colouring.
   The pattern of *choose → explore → un-choose*.

Together they're the first algorithmic tools that deal fluently
with **exponential search spaces** — the 2ⁿ or n! possibilities that
fill the space between "tiny and trivial" and "too big, need DP."

---

## Why This Phase Deserves Its Own Module

Recursion and backtracking show up everywhere in the curriculum:

- **Phase 02 / 01 / 02-Divide-Conquer** — recursion as the shape of
  divide-and-conquer algorithms.
- **Phase 02 / 01 / 04-Dynamic-Programming** — recursion + memoization.
- **Phase 02 / 01 / 05-Backtracking** — backtracking as a paradigm.
- **Phase 03 / 02 / 02-Efficient-Sorting** — merge sort and quicksort
  are recursive.
- **Phase 04 / 03-Linked-List** — recursive reverse, recursive traversal.
- **Future phases** — trees (Phase 07) are *all* recursion. Graphs
  (Phase 08) use DFS, which is recursion.

So why a dedicated module here? Two reasons:

1. **The earlier treatments are paradigm- or problem-specific.** They
   assume you already think fluently in recursion. This phase builds
   that fluency from the ground up.

2. **Backtracking deserves a deep, systematic treatment** with dozens
   of worked examples — subsets, permutations, combinations,
   constraint satisfaction. One problem per idea isn't enough; you
   need to see the PATTERN 20 different ways to internalize it.

Phase 05 is the place for that.

---

## What This Phase Covers

### 01 — Recursion

| Topic                             | What it covers                                   |
|-----------------------------------|--------------------------------------------------|
| `theory.md`                       | What recursion is, the call stack, base cases, correctness |
| `recursion-tree.md`               | Visualizing recursive calls as trees; complexity derivation |
| `patterns/`                       | Four classic patterns: tail, head, tree, indirect |
| `problems/`                       | Five classic problems: factorial, Fibonacci, Tower of Hanoi, print numbers, Josephus |

The goal: you should be able to **write any correct recursive
function in two minutes**, given only its base case and recursive
step. Then you should be able to **predict its complexity by
drawing the recursion tree**.

### 02 — Backtracking

| Topic                             | What it covers                                   |
|-----------------------------------|--------------------------------------------------|
| `theory.md`                       | The choose/explore/un-choose pattern, pruning    |
| `template.py`                     | The universal backtracking template              |
| `optimization-techniques.md`      | Pruning, memoization, ordering, early exit       |
| `problems/01-subsets/`            | Subsets, with duplicates, subset sum             |
| `problems/02-permutations/`       | Permutations, with duplicates, next permutation  |
| `problems/03-combinations/`       | Combination Sum I / II / III                     |
| `problems/04-n-queens/`           | N-Queens: first solution, all solutions, count   |
| `problems/05-sudoku/`             | Sudoku solver — the canonical constraint problem |
| `problems/06-word-search/`        | Word Search I / II — backtracking on a grid      |
| `problems/07-graph-backtracking/` | Hamiltonian path, graph colouring                |

Each sub-module shows the SAME PATTERN applied to a different
problem structure. By the end, you'll recognize backtracking on
sight — "this is just N-Queens with different constraints" — and
adapt the template in under five minutes.

---

## The Core Mental Shift

Recursion feels strange at first. You write a function, and that
function calls *itself*, and you believe it works by faith. That
discomfort fades once you see two things:

1. **The function doesn't "call itself" in the sense you're thinking.**
   It builds a new call frame on the stack — a separate invocation
   with its own local variables. The caller is the OLD instance; the
   callee is a NEW instance. They're just two different runs of the
   same code.

2. **Correctness = base case + induction.** If your base case is
   correct, AND your recursive case correctly reduces to a smaller
   problem that the function (by induction) solves correctly, then
   the whole thing is correct. No loop invariants. No mutation to
   track. Just "does it work at the base, and does the reduction
   shrink?"

These two realizations make recursion click.

---

## The Recursion-Backtracking Connection

Backtracking is recursion with a specific pattern:

```python
def backtrack(state):
    if is_solution(state):
        record(state)
        return
    for choice in candidates(state):
        make(choice)          # CHOOSE
        backtrack(state)      # EXPLORE
        unmake(choice)        # UN-CHOOSE
```

Every backtracking algorithm is THIS shape, with different definitions
of `is_solution`, `candidates`, `make`, and `unmake`. Once you
understand the recursion side (stacks, base cases, induction), the
backtracking side is just a specific recursion pattern applied to
search.

---

## Folder Layout

```
Phase-05-Recursion-Backtracking/
├── README.md                             ← you are here
├── 01-Recursion/
│   ├── theory.md
│   ├── recursion-tree.md                 ← visualizing calls + complexity
│   ├── patterns/
│   │   ├── tail-recursion.py             ← recursion that acts like iteration
│   │   ├── head-recursion.py             ← "process on the way up"
│   │   ├── tree-recursion.py             ← multiple recursive calls per step
│   │   └── indirect-recursion.py         ← A → B → A mutual recursion
│   └── problems/
│       ├── factorial.py
│       ├── fibonacci.py
│       ├── tower-of-hanoi.py
│       ├── print-numbers.py              ← print 1..n and n..1 recursively
│       └── josephus.py
│
└── 02-Backtracking/
    ├── theory.md
    ├── template.py                       ← the universal backtracking skeleton
    ├── optimization-techniques.md        ← pruning, memoization, ordering
    └── problems/
        ├── 01-subsets/
        │   ├── subsets.py                ← LC #78
        │   ├── subsets-dup.py            ← LC #90
        │   └── subset-sum.py             ← decision variant
        ├── 02-permutations/
        │   ├── permutations.py           ← LC #46
        │   ├── permutations-dup.py       ← LC #47
        │   └── next-permutation.py       ← LC #31
        ├── 03-combinations/
        │   ├── combination-sum.py        ← LC #39
        │   ├── combination-sum-ii.py     ← LC #40
        │   └── combination-sum-iii.py    ← LC #216
        ├── 04-n-queens/
        │   ├── n-queens.py               ← LC #51 (return one or all)
        │   ├── n-queens-all.py           ← find EVERY solution
        │   └── n-queens-count.py         ← LC #52 (count only)
        ├── 05-sudoku/
        │   └── sudoku-solver.py          ← LC #37
        ├── 06-word-search/
        │   ├── word-search.py            ← LC #79
        │   └── word-search-ii.py         ← LC #212 (with Trie)
        └── 07-graph-backtracking/
            ├── hamiltonian-path.py
            └── graph-coloring.py
```

---

## Outcome

By the end of this phase you should be able to:

1. **Write any recursive function fluently.** Base case first, then
   the induction step.
2. **Draw recursion trees** to compute complexity without memorizing
   master theorems.
3. **Convert recursion ↔ iteration** when needed — and know when each
   is a better fit.
4. **Recognize backtracking problems** within 30 seconds by shape:
   subsets? permutations? constraint satisfaction?
5. **Apply the universal backtracking template** to any of them,
   adjusting only the choice, feasibility, and solution checks.
6. **Prune effectively** — the difference between "runs forever" and
   "runs in milliseconds" on exponential problems.

Phase 06 (Hashing) will return to flat data. Phase 07 (Trees & Heaps)
and Phase 08 (Graphs) will rely heavily on everything you build here
— trees are recursion structurally, DFS is recursion on a graph.
