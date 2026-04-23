# Backtracking — Theory

## Introduction

**Backtracking** is recursion with a purpose: *systematically explore
every candidate solution, abandoning any that can't possibly lead to
a valid answer.*

It's the algorithmic form of "trial and error" — but with discipline.
At every step:

1. **Make a choice** among the currently available options.
2. **Recurse** to explore the consequences of that choice.
3. **Undo the choice** on the way back (so the next iteration of
   the caller's loop can try a different option).

This three-step pattern — **choose, explore, un-choose** — is the
whole algorithm. Every backtracking problem is the same skeleton
with different definitions of "choice," "consequence," and "valid."

---

## The Universal Backtracking Template

```python
def backtrack(state):
    if is_solution(state):                  # ← BASE CASE
        record(state)
        return
    for choice in candidates(state):        # ← BRANCH over choices
        if feasible(choice, state):         # ← PRUNE early
            apply(choice, state)            # CHOOSE
            backtrack(state)                # EXPLORE
            revert(choice, state)           # UN-CHOOSE
```

Five blanks to fill for any backtracking problem:

1. `is_solution(state)` — when are we done?
2. `candidates(state)` — what choices are available from here?
3. `feasible(choice, state)` — is this choice valid right now?
4. `apply / revert` — how do we record / undo a choice?
5. `record(state)` — what do we do when we find a solution?

Fill these five for the problem at hand, and the skeleton delivers
the full algorithm. `template.py` in this module walks through the
skeleton on a minimal example.

---

## Why Backtracking Isn't "Brute Force"

Brute force = enumerate every candidate, check each one for validity.

Backtracking = enumerate candidates **incrementally** and
**abandon a partial solution the moment it becomes infeasible**.

The difference: backtracking PRUNES the search tree. Instead of
generating all n! permutations and checking which are valid, you
generate one permutation node at a time, and as soon as it violates
a constraint you *stop exploring* — saving all the downstream
descendants from being generated at all.

On problems with strong constraints (Sudoku, N-Queens), this can
turn an O(n!) search into something manageable. On problems with
weak constraints, backtracking degrades to brute force, which is
fine — you still have to visit every candidate.

---

## The Four Problem Shapes

Every backtracking problem falls into one of four shapes. The
template is the same; only the parameters change.

### 1. Enumeration (Find All Solutions)

Examples: all subsets, all permutations, all combinations that sum
to k.

```python
if is_solution(state):
    record(state)
    return              ← don't stop searching; keep exploring
```

No termination — walk the entire tree.

### 2. Existence (Does ANY Solution Exist?)

Examples: "is there a subset that sums to K?" "can I solve this
Sudoku?" "is there a path in this maze?"

```python
if is_solution(state):
    return True
...
if backtrack(state):    ← propagate success up the call stack
    return True
```

Short-circuit as soon as you find ONE.

### 3. Optimization (Find the BEST Solution)

Examples: "what's the minimum number of moves?", "the best schedule?",
"the fewest queens that still cover?"

```python
if is_solution(state):
    nonlocal best
    best = min(best, score(state))   ← track the best so far
    return
```

Track a global best. This becomes **Branch & Bound** when you add
a bound function to prune branches that can't beat `best` —
covered in Phase 02 / 01 / 06-Branch-Bound.

### 4. Counting (How Many Solutions?)

Examples: "how many ways to place n queens?" "how many paths
through this grid?"

```python
if is_solution(state):
    nonlocal count
    count += 1
    return
```

Same as enumeration but without keeping the solutions — just
increment a counter.

All four shapes use the SAME template. What changes is what
happens at the base case.

---

## The Three Pruning Strategies

Pruning is what separates backtracking from brute force. Three kinds:

### 1. Feasibility Pruning

Reject choices that violate a constraint right now.

```python
if feasible(choice, state):
    apply(choice, state)
    backtrack(state)
    revert(choice, state)
```

Applied as a FILTER inside the loop over candidates. If the choice
would immediately violate a rule (N-Queens: same column; Sudoku:
row already contains this number), skip it.

### 2. Dead-End Pruning

Detect that the current partial state CAN'T be completed into a
valid solution — and stop early.

```python
if is_dead_end(state):
    return              # don't bother continuing
```

Examples:
- N-Queens: placing a queen in a row where the remaining rows
  have no valid positions.
- Sudoku: a cell has zero legal values.
- Word search: the remaining letters don't appear in the grid.

Detecting dead-ends requires problem-specific insight, but pays off
enormously — often the difference between "runs in a second" and
"runs forever."

### 3. Optimality Pruning (Branch & Bound)

For optimization problems: if even the BEST possible completion of
this state can't beat the current best, stop exploring.

```python
if upper_bound(state) < best:
    return              # this branch can't win
```

Requires a cheap, admissible bound function. Covered in Phase 02 /
01 / 06-Branch-Bound; we touch on it in
`optimization-techniques.md`.

---

## Time and Space Complexity

### Time

In the WORST case, backtracking explores the full search tree:

- Subsets of n: **2^n**
- Permutations of n: **n!**
- Grid paths of length k: **4^k** (or less with obstacles)
- Sudoku: **9^(empty cells)** in the worst case

With good pruning, the actual work is typically far less — often
exponential still, but with a much smaller base or a much smaller
exponent.

**Backtracking problems are typically exponential or factorial.**
That's fine up to n = 15–20 or so. Past that, either the problem
needs DP, a specialized algorithm, or clever pruning.

### Space

O(depth of recursion) stack memory. Usually O(n) for the state and
O(n) for the call stack.

The OUTPUT may itself be exponential (all subsets is 2^n outputs,
each of size n, so O(n · 2^n)). That's intrinsic to the problem,
not to the algorithm.

---

## Backtracking vs Related Techniques

| Technique              | When it wins                                      |
|------------------------|--------------------------------------------------|
| **Backtracking**       | Enumerate or search over a constrained decision tree |
| Brute force            | No constraints to prune; just enumerate          |
| Dynamic programming    | Subproblems overlap heavily                      |
| Branch & Bound         | Backtracking + admissible bound for optimization |
| Greedy                 | Locally optimal choice gives globally optimal result |

**Backtracking vs DP** is the most useful comparison:

- **DP**: subproblems overlap. Memoize each unique state.
- **Backtracking**: subproblems are UNIQUE by construction (they
  depend on the full path taken to reach them, not just the state).
  No memoization possible in the same way.

Sometimes you can convert a backtracking problem to DP by
recognizing that the state encodes all the information needed
(not just the current position but also which elements have been
used, etc.). When you can, DP is usually faster. When you can't,
backtracking is the right tool.

---

## Problem Shapes Covered in This Module

1. **01-subsets/** — 2^n subsets
2. **02-permutations/** — n! permutations
3. **03-combinations/** — combinations with sum / count constraints
4. **04-n-queens/** — constraint satisfaction, classic
5. **05-sudoku/** — grid constraint satisfaction
6. **06-word-search/** — grid path search with backtracking
7. **07-graph-backtracking/** — Hamiltonian path, graph colouring

Each shows the SAME TEMPLATE with different "choice" and "feasibility"
definitions. By the end, you should recognize the template on sight.

---

## The Choose–Explore–Un-choose Pattern In Detail

The single most important concept in backtracking is the symmetry
between "apply" and "revert." Whatever you change when making a
choice, you must undo when unmaking it. If you DON'T undo, the state
becomes "stale" — poisoned by a past choice that's no longer
relevant.

```python
def backtrack(state):
    if is_solution(state):
        record(state)
        return

    for choice in candidates(state):
        apply(choice, state)           # ← change state
        backtrack(state)               # ← explore
        revert(choice, state)          # ← MUST undo the exact change
```

Examples of apply/revert pairs:

| Apply                              | Revert                              |
|------------------------------------|-------------------------------------|
| `path.append(x)`                   | `path.pop()`                        |
| `used[i] = True`                   | `used[i] = False`                   |
| `grid[r][c] = digit`               | `grid[r][c] = '.'`                  |
| `board[row] = col; diag.add(...)`  | `board[row] = -1; diag.remove(...)` |

If any of your apply/revert pairs are asymmetric, you have a bug.
This is the #1 source of backtracking errors.

---

## Common Pitfalls

1. **Forgetting to revert.** Your "solutions" all look like the same
   state because partial changes linger. Every apply needs a revert.
2. **Sharing a mutable `path` in results.** `results.append(path)` is
   a bug — every entry in `results` ends up pointing at the same
   (finally empty) list. Always `results.append(path[:])` to snapshot.
3. **Infinite recursion.** If you don't PRUNE or REDUCE the state,
   the recursion won't terminate. Make sure every branch either makes
   progress or hits a base case.
4. **Quadratic validity checks.** If `feasible(choice, state)` is
   O(n), you've made each iteration expensive. Maintain invariants
   incrementally (sets of used columns, running sums, etc.) so
   `feasible` runs in O(1).
5. **Wrong candidates ordering.** On some problems, trying the
   "most constrained" choice first dramatically reduces the search
   space. Sudoku is the classic example.
6. **Not short-circuiting on existence problems.** If you're asked
   "does any solution exist?" and your code keeps searching after
   finding one, you're doing extra work.
7. **Mutable default arguments.** `def backtrack(state, memo={})` —
   the `memo` is shared across invocations. Use `memo=None` and
   initialize inside.

---

## Key Takeaways

1. **Backtracking = recursion with systematic pruning.**
2. **The template is universal:** is_solution → record; otherwise
   for each feasible choice, apply → recurse → revert.
3. **Four problem shapes:** enumeration, existence, optimization,
   counting. The template is the same; the base case differs.
4. **Three pruning strategies:** feasibility, dead-end, optimality
   (Branch & Bound).
5. **Always pair `apply` with `revert`.** The symmetry is what makes
   backtracking correct.
6. **Complexity is usually exponential.** Good pruning is the
   difference between usable and unusable.

For the universal template, see [`template.py`](template.py).
For pruning and other performance strategies, see
[`optimization-techniques.md`](optimization-techniques.md).
For seven concrete problem families, see [`problems/`](problems/).
