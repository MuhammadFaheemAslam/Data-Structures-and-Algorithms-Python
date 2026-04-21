# Algorithm Paradigms — Overview

A **paradigm** is a high-level strategy for attacking a problem. Before you
pick a data structure, before you write a single line of code, you pick
a paradigm — it determines the *shape* of your solution.

Every problem you'll ever solve falls into one (or a blend) of six families.

---

## The Six Paradigms at a Glance

| # | Paradigm            | One-line idea                                               | Typical complexity     |
|---|---------------------|-------------------------------------------------------------|------------------------|
| 1 | Brute Force         | Try every possibility; return the one that works.           | Often exponential or polynomial |
| 2 | Divide & Conquer    | Split into independent subproblems, solve, combine.         | Often O(n log n)       |
| 3 | Greedy              | Make the locally best choice at every step.                 | Often O(n log n)       |
| 4 | Dynamic Programming | Split into **overlapping** subproblems, memoize answers.    | Polynomial (O(n·m), O(n²), …) |
| 5 | Backtracking        | Recursive exploration of all solutions with pruning.        | Exponential, reduced by pruning |
| 6 | Branch & Bound      | Backtracking + a bound function that kills bad branches.    | Still exponential, typically much faster in practice |

---

## How They Relate

These paradigms are **not six disjoint boxes**. They form a rough evolution:

```
              [ brute force ]   ← start here; always works
                    │
                    ├── divide? ──→ [ divide & conquer ]
                    │
                    ├── can commit locally? ──→ [ greedy ]
                    │                              (fast if it works)
                    │
                    ├── subproblems overlap? ──→ [ dynamic programming ]
                    │                              (greedy with memory)
                    │
                    ├── need all solutions? ──→ [ backtracking ]
                    │
                    └── optimizing + prunable? ──→ [ branch & bound ]
```

Every "smarter" paradigm is, in some sense, a brute force with extra
structure added to eliminate redundant work.

---

## How to Pick the Right Paradigm

Ask yourself, in order:

1. **Can I describe a brute-force solution?** If not, you don't yet understand
   the problem. Start here *always*. Even if you don't submit it, it reveals
   the search space.

2. **Does the problem split into independent halves?** → Divide & Conquer.
   *(merge sort, quick sort, binary search, closest pair of points)*

3. **Can I prove that picking the locally best option at each step yields the
   global optimum?** → Greedy.
   *(activity selection, Huffman coding, Dijkstra, Kruskal)*

4. **Does my brute force recompute the same subproblem many times?** → DP.
   *(fibonacci, knapsack, edit distance, longest common subsequence)*

5. **Do I need every solution, not just one optimal one, or is the search
   tree too big to enumerate blindly?** → Backtracking.
   *(N-Queens, permutations, subsets, Sudoku)*

6. **Am I optimizing over the backtracking tree and can I cheaply bound
   each branch's best-case value?** → Branch & Bound.
   *(traveling salesman, 0/1 knapsack with bounds, integer programming)*

---

## Paradigm vs Technique

This is the most common source of confusion, so make it crisp:

| Paradigm            | Technique (Phase-02 / 02)              |
|---------------------|----------------------------------------|
| **A strategy.**     | **A move inside a strategy.**          |
| "We will solve this with Divide & Conquer." | "…and inside the merge step we'll use two pointers." |
| Broad, architectural.| Narrow, tactical.                      |

You pick a paradigm first. You execute it using one or more techniques.

---

## Common Pitfalls

- **"I jumped straight to DP."** Sometimes the problem is greedy. Test greedy
  first — it's often shorter, faster, and easier to prove correct when it works.
- **"My greedy gave the wrong answer."** Greedy is dangerous; it requires proof.
  When you can't prove the local choice leads to the global optimum, fall back to DP.
- **"My brute force is too slow but I can't see a pattern."** Look at what the
  brute force *recomputes*. Memoization usually hides in plain sight.
- **"I keep writing the same recursion."** That's a signal to switch from
  backtracking to DP — you're solving the same subproblem from different paths.

---

## Module Order

The folders are numbered in the recommended reading order:

1. **Brute Force** — the baseline every other paradigm improves on.
2. **Divide & Conquer** — the first "smart" structure: independent subproblems.
3. **Greedy** — when local choices suffice.
4. **Dynamic Programming** — when they don't, and subproblems overlap.
5. **Backtracking** — exhaustive search done right.
6. **Branch & Bound** — backtracking's optimization-focused sibling.

Each module has the same shape: `theory.md`, `template.py`, and 1–2
worked problems under `problems/`.
