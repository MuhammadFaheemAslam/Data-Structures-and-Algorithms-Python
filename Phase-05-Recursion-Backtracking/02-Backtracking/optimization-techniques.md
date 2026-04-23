# Backtracking — Optimization Techniques

A plain backtracking implementation is *correct* but often far
slower than it needs to be. The gap between "correct" and "fast"
on hard problems (Sudoku, N-Queens at n=14, graph colouring) is
always closed by the same handful of techniques.

This file is a reference for the five most important ones. Each is
illustrated with a specific problem pattern it applies to.

---

## 1. Feasibility Pruning — Reject Immediately

The simplest and most universal. If a choice would immediately
violate a constraint, don't try it at all.

### Example: N-Queens

Instead of placing a queen and THEN checking validity:

```python
# ❌ SLOW
for col in range(n):
    place_queen(row, col)
    if is_valid(board):             # O(n²) validity scan
        backtrack(row + 1)
    unplace_queen(row, col)
```

Maintain invariant data structures that give O(1) validity checks:

```python
# ✅ FAST
used_cols   = set()
used_diag1  = set()   # row - col
used_diag2  = set()   # row + col

for col in range(n):
    if col in used_cols:         continue
    if (row - col) in used_diag1: continue
    if (row + col) in used_diag2: continue

    place(row, col)              # add to all three sets
    backtrack(row + 1)
    unplace(row, col)            # remove from all three sets
```

Before: O(n²) per node. After: O(1). For n = 14, speedup is ~100×.

**Lesson:** whenever you check validity, ask "can I maintain this
as an invariant instead of computing it from scratch?"

---

## 2. Dead-End Detection — Stop Before Going Deep

Feasibility pruning rejects ONE choice. Dead-end detection rejects
the ENTIRE subtree from the current state.

### Example: Sudoku

If the next empty cell has ZERO legal values, no completion of the
current partial grid can succeed. Return immediately.

```python
def solve():
    empty = find_empty_cell()
    if empty is None:
        return True                 # solved

    r, c = empty

    legal = {1, 2, ..., 9} - used_in_row[r] - used_in_col[c] - used_in_box[(r // 3, c // 3)]

    if not legal:                   # ← DEAD-END PRUNE
        return False

    for d in legal:
        assign(r, c, d)
        if solve():
            return True
        unassign(r, c, d)

    return False
```

The `if not legal: return False` line turns a Sudoku solver from
"maybe runs forever" to "solves hardest puzzles in < 1 second."

Generalization: any state-check that determines "this can't succeed"
belongs at the top of the recursion.

---

## 3. Ordering — Most-Constrained First

In most backtracking problems, the ORDER in which you try choices
dramatically affects runtime. The principle:

> *Try the most CONSTRAINED choice first — the one that has the
> fewest available options.*

### Example: Sudoku (MRV — Minimum Remaining Values)

Instead of filling cells left-to-right top-to-bottom, at each step
PICK THE EMPTY CELL with the fewest legal values:

```python
def find_empty():
    best_cell = None
    best_count = 10
    for r in range(9):
        for c in range(9):
            if grid[r][c] == '.':
                legal = count_legal_values(r, c)
                if legal < best_count:
                    best_count = legal
                    best_cell = (r, c)
    return best_cell
```

This "most-constrained-variable" heuristic (MRV) reduces branching.
A cell with only 2 legal values branches 2 ways; one with 9 branches
9 ways. Committing to the 2-way cell first reduces total work
dramatically.

For the hardest Sudoku puzzles, MRV is often the difference between
1 second and 10 minutes.

### Example: Graph Colouring

Colour the most-constrained vertex (the one with the fewest allowed
colours) first. Same principle as Sudoku.

### General Rule

Reorder your `for choice in candidates` loop so the most restrictive
choices come first.

---

## 4. Memoization — When Subproblems Overlap

Backtracking typically has UNIQUE subproblems (each state reflects
a specific path taken to reach it). But sometimes the state can be
summarized in a way that ignores the path.

When you notice that different branches arrive at the same
"essential state," memoize:

```python
@functools.lru_cache(maxsize=None)
def backtrack(hashable_state):
    ...
```

### Example: Word Break (LC #139)

"Can this string be split into dictionary words?" — backtracking
on break positions. Different paths reach the same suffix; memoize
on the suffix:

```python
@lru_cache
def can_break(suffix):
    if suffix == "":
        return True
    for word in words:
        if suffix.startswith(word) and can_break(suffix[len(word):]):
            return True
    return False
```

Once `can_break("some_suffix")` has been computed, don't recompute.

### When Memoization Makes Sense

- The state can be summarized in a small, hashable value.
- Different recursion paths reach the same summary state.
- Subproblems overlap in a meaningful way.

Adding `@lru_cache` to a backtracking function is equivalent to
converting it to DP. When in doubt, try it.

### When It Doesn't

- The state depends on the entire path (e.g., "which specific queens
  have been placed, in what order?").
- No two recursion branches reach the same state.

In these cases memoization does nothing — no cache hits, just
overhead.

---

## 5. Optimality Pruning — Branch & Bound for Optimization Problems

For problems where you want the BEST solution, not just any
solution, use a BOUND to eliminate branches that can't improve on
the current best.

```python
best = INF

def backtrack(state):
    nonlocal best
    if is_solution(state):
        best = min(best, score(state))
        return

    if optimistic_bound(state) >= best:        # ← OPTIMALITY PRUNE
        return

    for choice in candidates(state):
        apply(choice, state)
        backtrack(state)
        revert(choice, state)
```

`optimistic_bound(state)` is a cheap estimate of the BEST score
achievable from `state`. If even the optimistic case can't beat
`best`, abandon this branch.

### Example: Travelling Salesman (TSP) Branch & Bound

As you extend a partial tour, compute a lower bound on the total
tour length. If it already exceeds the current best, stop.

Covered in detail in Phase 02 / 01 / 06-Branch-Bound.

### The Key to Making This Work

The bound must be:

- **Admissible** — never worse than the true optimum (for min-problems,
  a LOWER bound on completion cost).
- **Cheap to compute** — if it takes O(n²) per node, you've made
  the algorithm slower, not faster.
- **Tight** — a bound that's always "infinity" prunes nothing. The
  tighter the bound, the more you prune.

---

## 6. Symmetry Breaking — Don't Explore Equivalent Branches

Some backtracking problems have SYMMETRIES that cause the search to
explore the same answer multiple times in disguise.

### Example: N-Queens on an Empty Board

The first queen has `n` columns to choose from, but by SYMMETRY, we
only need to try `⌈n/2⌉` of them — the others produce mirror-image
solutions.

Once the first row is placed, symmetry is broken, and you can
proceed normally. The final solution count doubles (to account for
the mirrored half) if n is even; for odd n, middle-column solutions
are their own mirrors.

### Example: Graph Colouring

If you're asked "is this graph k-colourable?" (existence question),
you only need to TRY ASSIGNING color 1 to the first vertex — any
solution with a different first-vertex color can be renamed to one
with color 1 first.

Symmetry breaking can reduce a search by a factor of 2, 6, n!, or
more — problem-specific. Not every problem has exploitable
symmetry, but when it does, the payoff is large.

---

## 7. Iterative Deepening — When Depth Matters

For problems where you care about SHORT solutions (e.g., "solve this
puzzle in the fewest moves"), **iterative deepening DFS** avoids
exploring needlessly deep branches.

```python
for depth_limit in range(1, MAX):
    if search(state, depth_limit):
        return depth_limit
```

Searches depth-first up to `depth_limit`; if no solution, increment
the limit. Like BFS but with O(depth) space instead of O(branching
factor^depth).

Standard in puzzle solvers (Rubik's cube, 15-puzzle, planning).

---

## 8. Constraint Propagation (Advanced)

For very hard constraint-satisfaction problems (hard Sudoku, some
scheduling), constraint propagation goes beyond backtracking:

After each assignment, propagate its consequences to reduce the
legal values of all OTHER affected variables. If any variable's
legal set becomes empty, prune immediately.

Algorithms like AC-3 (Arc Consistency 3) do this systematically.
Production Sudoku solvers combine backtracking + propagation to
solve even "world's hardest" puzzles in microseconds.

Beyond the scope of this module; covered in CSP / AI texts.

---

## Priority Checklist for Speeding Up a Slow Backtrack

When a backtracking solution is too slow, apply the techniques in
this order:

1. ✅ **Feasibility pruning** — make your constraint checks O(1).
2. ✅ **Dead-end pruning** — detect "can't succeed" states early.
3. ✅ **Ordering** — try most-constrained choices first.
4. ✅ **Memoization** — if subproblems overlap.
5. ✅ **Optimality pruning** — if it's an optimization problem.
6. ✅ **Symmetry breaking** — if there are exploitable symmetries.
7. 🚧 **Iterative deepening** — for "shortest solution" problems.
8. 🚧 **Constraint propagation** — for hard CSP problems.

Items 1–4 apply to almost every backtracking problem. Items 5–8
are problem-specific but transformative when they fit.

---

## Key Takeaways

1. **Pruning is the point of backtracking.** Without it, you have
   brute force.
2. **Maintain invariants for O(1) feasibility** — sets, counters,
   bitmasks.
3. **Detect dead-ends early.** A `return False` two levels up is
   worth thousands of deeper calls.
4. **Order your candidates wisely.** MRV / most-constrained-first is
   the universal heuristic.
5. **Memoize when subproblems overlap.** If they don't, skip it.
6. **For optimization, use bounds** (Branch & Bound). See Phase 02 /
   01 / 06.
7. **Break symmetries.** Two mirror-image solutions are ONE solution.

These techniques turn the exponential cost of backtracking into
something usable. The worked problems in
[`problems/`](problems/) apply them concretely.
