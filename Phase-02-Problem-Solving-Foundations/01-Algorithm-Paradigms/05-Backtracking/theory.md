# Backtracking — Theory

## Introduction

**Backtracking** is brute force done with discipline.

Where plain brute force says *"enumerate every possibility blindly"*,
backtracking says:

> *"Build the solution one decision at a time. At each step, try every
> viable choice. When a choice leads somewhere invalid, undo it and try
> the next."*

Backtracking is the paradigm behind N-Queens, Sudoku solvers,
permutation generators, maze solvers, combination search, and word
search in a grid. Any problem that asks you to *construct* something
under constraints — rather than pick from a pre-existing set — is
probably a backtracking problem.

Its complexity is usually still exponential, but with **pruning** it
becomes practical on inputs that plain brute force couldn't touch in
a million years.

---

## The Core Idea

Imagine every possible solution to a problem as a **decision tree**:

- The root is the empty / starting solution.
- Each edge represents making one decision (placing a queen, picking
  a digit, taking an item).
- Each leaf is a complete solution (possibly invalid).

Brute force walks *every* leaf. Backtracking walks only the leaves
**reachable from valid intermediate states** — the moment a partial
solution is doomed to fail, backtracking abandons it and tries the
next decision at the most recent choice point.

That is the entire paradigm.

---

## The Choose → Explore → Un-choose Pattern

Every backtracking algorithm follows this three-step template:

```
def backtrack(path, choices):
    if is_complete(path):
        record(path)
        return

    for choice in choices:
        if is_valid(choice, path):
            path.append(choice)         # 1. CHOOSE
            backtrack(path, next_choices)   # 2. EXPLORE
            path.pop()                  # 3. UN-CHOOSE (the "backtrack")
```

The last line — "un-choose" — is the defining move. It's what makes
this "backtracking" and not just "recursion."

It's also the single most common place for bugs. Forget to un-choose,
and your "solutions" will have state from previous branches leaking into them.

---

## When to Reach for Backtracking

Good signals:

1. **"Find all ..." or "Find a ...".** Generate every valid combination,
   permutation, subset, placement, or path.
2. **The solution is built up from discrete decisions.** Place a queen
   on a row, pick a digit, choose a cell to extend a path.
3. **Decisions are constrained.** Each choice must satisfy some rule
   relative to choices already made (no two queens attack; no repeated
   numbers in a Sudoku row; path stays within the grid).
4. **Small branching factor OR aggressive pruning.** Backtracking is
   exponential; it only runs in reasonable time when pruning kills
   most branches early.

Examples that are backtracking problems:

| Problem                       | What you construct                         |
|-------------------------------|--------------------------------------------|
| **N-Queens**                  | A board placement (one queen per row)      |
| **Permutations of a list**    | Every ordering                             |
| **Subsets of a set**          | Every combination                          |
| **Sudoku Solver**             | A fully-filled 9×9 grid                    |
| **Word Search (grid)**        | A path of adjacent cells spelling a word   |
| **Combination Sum**           | A list of numbers summing to a target      |
| **Palindrome Partitioning**   | A partition into palindromic substrings    |
| **Generate parentheses**      | Every valid string of n open/close pairs   |

---

## The Three Faces of Backtracking

Backtracking problems come in three broad flavours:

### 1. Find ALL solutions (enumeration)

Generate every valid solution and return them. Typical cost: O(answer-size).

```
def backtrack(path):
    if is_complete(path):
        result.append(path[:])      # snapshot — don't share the mutable `path`!
        return
    for choice in viable_choices():
        path.append(choice); backtrack(path); path.pop()
```

Examples: permutations, subsets, combinations.

### 2. Find ANY valid solution (search)

Stop as soon as you find one valid solution. Used when the existence
question is what matters.

```
def backtrack(state):
    if is_complete(state):
        return state                # return up the recursion chain
    for choice in viable_choices():
        state.apply(choice)
        result = backtrack(state)
        if result is not None:
            return result
        state.unapply(choice)
    return None
```

Examples: Sudoku solver, maze solver.

### 3. Find the BEST solution (optimization)

Track the best valid solution seen so far. This morphs into
**Branch & Bound** when you add a bound function that prunes branches
guaranteed to be worse than the current best — covered in 06-Branch-Bound.

```
def backtrack(state):
    if is_complete(state):
        nonlocal best
        best = better(best, state)
        return
    for choice in viable_choices():
        if bound(choice, state) >= best:   # prune
            state.apply(choice); backtrack(state); state.unapply(choice)
```

---

## Pruning: The Reason Backtracking Works in Practice

Without pruning, backtracking is just brute force with extra steps.
**Pruning** is the move that makes it fast: detecting early that a
partial solution can never lead to a valid complete solution, and
abandoning it.

Two kinds of pruning, both essential:

### 1. Feasibility pruning (correctness-required)

Kill branches that violate a hard constraint. *Must* be present;
without it, the algorithm explores garbage states.

Examples:
- Sudoku: the number you're about to place already exists in this row.
- N-Queens: the column you're about to place a queen in is already
  attacked.
- Word Search: the next letter doesn't match the target character.

### 2. Optimality pruning (performance boost)

Kill branches that *could* produce a valid solution but can't produce
one BETTER than what we have. Optional from a correctness standpoint;
crucial for speed in optimization problems. This is where backtracking
shades into Branch & Bound.

---

## Complexity

Backtracking is always exponential in the worst case because the
decision tree's size is exponential by construction. Specific bounds:

| Problem               | Decision tree size (worst case)     | Practical cost (pruned) |
|-----------------------|-------------------------------------|-------------------------|
| Permutations of n     | O(n!)                               | O(n!)                   |
| Subsets of n          | O(2^n)                              | O(2^n)                  |
| N-Queens              | O(n!) trivially, O(n^n) bound       | Prunes to ~fast for n ≤ 14 |
| Sudoku 9×9            | 9^81 trivially                      | Prunes to milliseconds   |

The rule of thumb: **without pruning, treat backtracking as O(branching^depth).
With good pruning, treat it as empirically fast up to some problem-specific n.**

---

## Backtracking vs Related Paradigms

| Paradigm          | Structure                        | What it produces            | Typical cost        |
|-------------------|----------------------------------|-----------------------------|---------------------|
| Brute Force       | Try every leaf (no pruning)      | Correct answer               | Exponential         |
| **Backtracking**  | **Try every leaf, prune bad branches** | **Correct answer**     | **Exponential, but smaller in practice** |
| Divide & Conquer  | Split, solve, combine            | Correct answer               | Often polynomial    |
| Dynamic Programming | Explore, memoize overlapping work | Optimal answer              | Polynomial          |
| Branch & Bound    | Backtracking + optimality bound  | **Optimal** answer           | Exponential worst, fast in practice |

**Backtracking vs DP** is the most useful distinction:

- DP is for problems where subproblems **overlap** and you can memoize.
- Backtracking is for problems where subproblems **don't overlap** —
  you're constructing specific objects (permutations, placements, paths)
  and each one is distinct.

If you ever find yourself adding a memoization cache to backtracking
that yields a lot of hits, you probably have a DP problem in disguise.

---

## Implementation Patterns

### Pattern A: Build and Un-build

Mutate a shared `path` list and undo mutations on the way up:

```python
def backtrack(path):
    if is_complete(path):
        result.append(path[:])      # SNAPSHOT — critical
        return
    for choice in choices:
        if valid(choice, path):
            path.append(choice)
            backtrack(path)
            path.pop()
```

Pro: fast, no allocations inside the loop.  
Con: easy to forget the snapshot — `path` is reused across branches.

### Pattern B: Immutable path

Pass a new list to each recursive call:

```python
def backtrack(path):
    if is_complete(path):
        result.append(path)
        return
    for choice in choices:
        if valid(choice, path):
            backtrack(path + [choice])
```

Pro: no un-choose step; no snapshot needed.  
Con: slower — allocates a new list at every decision. For deep
recursion, this matters.

Use Pattern A in production; Pattern B for teaching clarity.

### Pattern C: State-mutating board

For grid / board problems, maintain a shared `board` and constraint sets
(`cols`, `diagonals`), mutating on the way down and reverting on the way up.

See [`problems/n-queens.py`](problems/n-queens.py) for a canonical example.

---

## Pitfalls

- **Forgetting to un-choose.** The defining bug of backtracking.
  Symptom: "solutions" contain leftover state from earlier branches.
- **Sharing a mutable path in results.** `result.append(path)` (without
  `[:]`) appends a *reference* — every entry in `result` ends up pointing
  to the same list, which is empty at the end. Use `result.append(path[:])`
  or `result.append(list(path))`.
- **Weak pruning.** Explored branches you didn't need to = slow code.
  For problems past n ≈ 12, expect to need aggressive constraint checks.
- **No base case / wrong base case.** Infinite recursion or wrong answers.
- **Using backtracking on a DP problem.** If your recursion keeps
  recomputing the same subproblems, you need DP, not backtracking.
  (Symptom: adding a cache gives a big speedup.)
- **Too much work in `is_valid`.** If checking validity is O(n) per
  decision, the algorithm pays that cost every step. Keep constraint
  data structures (sets, arrays of column/diagonal flags) to make
  validity O(1).

---

## Pseudocode Skeleton

```
function backtrack(state):
    if complete(state):
        record_or_return(state)
        return

    for choice in candidate_choices(state):
        if feasible(choice, state):
            state.apply(choice)              # CHOOSE
            backtrack(state)                 # EXPLORE
            state.unapply(choice)            # UN-CHOOSE
```

For a concrete generic implementation, see [`template.py`](template.py).
For worked examples — N-Queens and permutations — see
[`problems/`](problems/).

---

## Key Takeaways

1. **Backtracking is brute force with pruning.** That pruning is what
   makes it practical.
2. **The three-step pattern is: choose → explore → un-choose.** The
   un-choose step is what makes the algorithm *backtracking* rather
   than plain recursion.
3. **Constraint data structures matter.** Keep O(1) validity checks
   by maintaining sets/arrays of what's used/blocked.
4. **Snapshot results before appending them.** Sharing a mutable `path`
   is the classic bug.
5. **Backtracking is for construction problems.** "Find all / any / best
   valid X where each X is built from decisions." If the subproblems
   overlap heavily, you want DP instead.
