# Branch & Bound — Theory

## Introduction

**Branch & Bound (B&B)** is backtracking for optimization problems.

If backtracking says *"explore every valid possibility and collect them"*,
Branch & Bound says:

> *"Explore every valid possibility — but the moment a branch's
> best-possible outcome is worse than what we've already found,
> abandon it."*

B&B is the paradigm behind practical solutions to the Traveling
Salesman Problem, 0/1 knapsack on large instances, integer programming,
and many CPU-intensive optimizations in compilers, schedulers, and
combinatorial search. In the worst case it remains exponential — but in
practice, a good bound function can eliminate enough branches that
B&B solves problems that brute force couldn't touch in a lifetime.

It is a specialized paradigm: not the first tool you reach for on
every problem, but the one that unlocks certain problems that nothing
else does.

---

## The Core Idea

Start with the backtracking decision tree. At each node:

1. Compute an **optimistic estimate** of the best solution reachable
   from this node (the "bound").
2. Compare that estimate to the best complete solution found so far.
3. If the bound is already **worse** than the current best, prune —
   no descendant of this node can improve on what we have.

The cheaper the bound is to compute, and the tighter it is to the true
optimum, the faster B&B runs.

Everything else is bookkeeping.

---

## The Three Ingredients

Every B&B algorithm has three components:

### 1. A branching strategy

Same as backtracking: how do you split the problem into smaller
subproblems? (Which edge to include/exclude? Which item to take or skip?)

### 2. A bound function

The heart of B&B. For any partial solution, compute an **optimistic
estimate** of the best complete solution reachable from here.

- **For maximization:** the bound must be an **upper bound**
  (*"the best I could possibly do from here is..."*).
- **For minimization:** the bound must be a **lower bound**
  (*"the best I could possibly do from here is AT LEAST..."*).

The bound must be *admissible* — it can't be tighter than the true
optimum, or B&B will prune the actual answer.

### 3. A current-best tracker

A running record of the best *complete* solution found so far. This is
what the bound is compared against.

As better solutions are found, the bound becomes more aggressive and
more branches are pruned. B&B naturally accelerates as it runs.

---

## The Pattern

```
best = INF                              # for minimization; -INF for max

def branch_and_bound(state):
    global best

    if is_complete(state):
        best = min(best, state.cost)    # or max(...) for maximization
        return

    # PRUNE if the bound says this branch can't beat `best`
    if bound(state) >= best:            # flip to <= for maximization
        return

    for choice in candidate_choices(state):
        if is_feasible(choice, state):
            state.apply(choice)
            branch_and_bound(state)
            state.unapply(choice)
```

Compare to the backtracking template — the ONLY addition is the line
`if bound(state) >= best: return`. That's the whole paradigm in one if-statement.

---

## Why the Bound Function Is Everything

A bound function must balance two competing goals:

- **Tight.** Close to the true optimum, so pruning kicks in aggressively.
- **Cheap.** Fast to compute — if the bound takes longer than just
  exploring the subtree, it's not helping.

The quality of your B&B algorithm is essentially the quality of your
bound function. Changing nothing else:

- **A weak bound** (e.g., "the best score is always ≤ infinity") prunes
  nothing. You just have backtracking.
- **A perfect bound** (return the true optimum) prunes everything. But
  computing it is as hard as solving the original problem.
- **A good practical bound** sits between these — usually derived from
  a relaxation of the problem (solving a fractional version,
  ignoring some constraints, or using a greedy estimate).

---

## Examples of Bound Functions

### 0/1 Knapsack → upper bound via fractional knapsack

For 0/1 knapsack, the fractional version is solvable greedily and gives
an upper bound on the best achievable 0/1 value from any partial state.

- Take all remaining items as fractions by value/weight ratio until the
  knapsack is full.
- The value obtained this way is an upper bound for any legal
  completion of the current state.

If that upper bound is already less than the current best, prune.

### Traveling Salesman → lower bound via MST or nearest-neighbour

Any Hamiltonian tour has length at least the weight of a minimum
spanning tree on the unvisited cities (plus the outgoing/incoming edges).

- The MST lower bound is tight but expensive.
- A cheaper alternative: for each unvisited city, add the cheapest
  edge leaving it; sum those halved (each edge is shared between two
  cities).

### Job Scheduling → lower bound via longest-path

For minimizing makespan on a DAG of tasks, a lower bound is the length
of the longest path in the precedence graph. No schedule can be shorter
than that.

### Integer Programming → linear-programming relaxation

Solve the LP (continuous-variable) version of the problem — any integer
solution is at least as bad as the LP solution. Widely used in
industrial solvers.

---

## Branch & Bound vs Backtracking

They share the same decision-tree structure. The differences:

| Dimension           | Backtracking                     | Branch & Bound                               |
|---------------------|----------------------------------|----------------------------------------------|
| Goal                | "Find all" or "find a" valid sol | "Find the **optimal** solution"              |
| Pruning trigger     | Hard feasibility constraint      | Bound says no improvement possible           |
| Running-best state  | n/a                              | `best` — a live watermark that tightens      |
| Speedup             | From cutting invalid branches    | From cutting *unpromising* branches          |
| Worst case          | Exponential                      | Still exponential                            |
| Practical cost      | Exponential with small constants | Often orders of magnitude faster due to bounding |

If you're doing backtracking and you're tracking "best seen so far"
while exploring — you've already reinvented B&B. You just need a
bound function to make the pruning more aggressive.

---

## Search Strategies: DFS vs Best-First

Backtracking is always DFS (depth-first, recursion-based). B&B can use
either:

### DFS Branch & Bound

Same shape as backtracking. Simple, low memory.

### Best-First Branch & Bound

Use a priority queue (min-heap for minimization, max-heap for maximization)
keyed by the bound. Always expand the node with the most promising bound.

```
pq = priority_queue([initial_state])
while pq:
    node = pq.pop()
    if bound(node) >= best:     # stale, already-dominated entry
        continue
    if is_complete(node):
        best = better(best, node)
    else:
        for child in branch(node):
            pq.push(child)
```

Pros: finds good solutions fast, which tightens `best` quickly.  
Cons: priority queue overhead; memory grows with open nodes.

For interview and small-to-medium problems, DFS B&B is usually enough.
Best-first becomes valuable on large industrial problems where finding
*any* good solution quickly is critical.

---

## When to Reach for Branch & Bound

Good signals:

1. **It's an optimization problem** — min or max, not just "find any valid".
2. **Brute force is exponential and not fast enough.**
3. **DP doesn't apply** — subproblems don't overlap meaningfully.
4. **You can compute a good bound cheaply** — this is the critical
   precondition. Without a bound, B&B is just backtracking.

Good fits:
- TSP, assignment problem
- 0/1 knapsack on large instances
- Integer linear programming
- Optimal scheduling, facility location
- Puzzle-solving with cost minimization (e.g., 15-puzzle, Rubik's)

Bad fits:
- Problems where DP works — DP's polynomial time beats B&B's exponential
  worst case.
- Problems without a natural bound function — you'd just have backtracking.

---

## Complexity

Worst case: same as backtracking — exponential. B&B is not an asymptotic
improvement. It's a **practical** improvement: the bound function shaves
off enough branches that real inputs become tractable.

The gap between worst-case and practical performance is where B&B
earns its reputation as a "dark art" — the same algorithm might take
milliseconds or years depending entirely on how tight the bound is.

---

## Pitfalls

- **Non-admissible bound.** If your bound is tighter than the true
  optimum (for minimization: too high; for maximization: too low),
  B&B will prune the actual answer and return a sub-optimal one. Verify
  that your bound is a valid relaxation.
- **Expensive bound.** A perfect bound is useless if it takes longer to
  compute than exploring the subtree. Profile before celebrating.
- **Weak bound.** If the bound almost always exceeds `best`, you've
  built backtracking with extra steps. Tighten the bound.
- **Forgetting to update `best`.** B&B relies on `best` tightening over
  time. If you forget to update it when you find a better complete
  solution, pruning stays weak.
- **Best-first with stale entries.** In priority-queue B&B, a node
  popped from the heap may no longer be promising if `best` has
  tightened since the node was pushed. Always re-check the bound
  after popping.

---

## Pseudocode Skeleton

```
best = +∞                          # minimization problem

function branch_and_bound(state):
    if complete(state):
        best = min(best, cost(state))
        return

    if bound(state) >= best:
        return                      # prune

    for choice in branches(state):
        apply(choice, state)
        branch_and_bound(state)
        unapply(choice, state)
```

For a concrete implementation, see [`template.py`](template.py). For a
worked problem showing dramatic bounding speedups, see
[`problems/tsp.py`](problems/tsp.py).

---

## Key Takeaways

1. **B&B = backtracking + bound-based pruning** for optimization problems.
2. **The bound function is the whole algorithm.** Tight + cheap = fast;
   weak OR expensive = no better than backtracking.
3. **Bounds come from relaxations** — solve a simpler version of the
   problem whose answer is guaranteed to bound the real one.
4. **B&B is worst-case exponential, practically much faster** — its
   value is in real-world performance, not asymptotic complexity.
5. **DP beats B&B when DP applies.** Use B&B when DP doesn't — typically
   on problems with exponential state spaces that don't memoize cleanly.
