# Greedy — Theory

## Introduction

**Greedy** is the fastest, simplest, and most dangerous of all paradigms.

Where Divide & Conquer says *"break it up and recombine"* and Dynamic
Programming says *"remember everything"*, Greedy says:

> *"At every step, make the locally best choice. Never look back."*

When greedy works, the resulting algorithms are beautiful — short, clean,
often O(n log n). When greedy *doesn't* work, it returns wrong answers
that look plausible on small inputs and then quietly fail on the test
cases you didn't think to check.

Greedy is the paradigm where **proving correctness matters more than
writing code**. The code takes ten minutes; the proof takes an hour.
Skip the proof and you ship bugs.

---

## The Greedy Recipe

Every greedy algorithm has the same shape:

1. **Define a greedy choice.** What single move, made now, commits you to
   a locally-best option? ("Pick the item with the largest value-to-weight
   ratio." "Take the job that ends earliest.")
2. **Make that choice.** No recursion, no exploration, no rollback.
3. **Recurse on what remains.** The remaining subproblem must be of the
   same shape, so you can apply the same greedy choice again.
4. **Prove it's correct.** This is non-optional. See below.

```
function greedy(problem):
    solution = empty
    while problem not solved:
        choice = greedy_choice(problem)    # pick locally best
        add choice to solution
        reduce problem (commit to that choice)
    return solution
```

Compare this to Dynamic Programming, which tries many choices at each step
and keeps the best. Greedy tries exactly one.

---

## What Makes a Problem Greedy-Solvable

Two properties must hold. Miss either and greedy produces wrong answers.

### 1. The Greedy Choice Property

> *There is some locally optimal choice that is guaranteed to be part of
> some globally optimal solution.*

This is the claim you must prove. It says: "*I don't have to look at the
other options. The choice I'm making now cannot be wrong.*"

### 2. Optimal Substructure

> *Once you've made the greedy choice, the remaining subproblem — solved
> optimally — combined with the greedy choice, gives an overall optimal
> solution.*

This looks similar to DP's optimal substructure, and it is. The difference:
DP's subproblems **overlap** (which is why DP memoizes them). Greedy's
subproblems don't — after the greedy choice, there's exactly **one**
remaining subproblem to solve.

---

## Proving Greedy: The Exchange Argument

The standard tool for proving greedy correctness is the **exchange argument**.
It has three steps:

1. Assume there's an optimal solution that does *not* make the greedy choice.
2. Show you can swap (exchange) one of its choices for the greedy choice,
   producing a solution that is **no worse**.
3. Conclude there must be an optimal solution that *does* make the greedy choice.

This is beautiful and worth learning. A concrete example:

### Activity Selection — Proof Sketch

> *Given n activities with start and end times, select the largest subset
> of mutually compatible activities (no two overlap).*

**Greedy choice:** sort by end time; always take the activity that ends earliest
among those still compatible.

**Proof (exchange argument):**

- Let `G` be the greedy solution and `O` be an optimal solution.
- Sort both by end time. Let `g₁` be greedy's first pick, `o₁` optimal's.
- By greedy's rule, `g₁` has the earliest end time, so `end(g₁) ≤ end(o₁)`.
- Replace `o₁` in `O` with `g₁`: the remaining activities in `O` are all
  compatible with `o₁`, hence also with `g₁` (which ends at least as early).
- The new `O` has the same size as before — still optimal — and now starts
  with the greedy choice.
- Repeat the argument for the remainder. The greedy solution `G` is optimal.

Skipping proofs like this is how you ship bugs. On a new problem,
**always** sketch the exchange argument before you trust the greedy approach.

---

## When Greedy Works

Common greedy strategies and the problems they solve:

| Greedy Choice                                  | Solves                                        |
|------------------------------------------------|-----------------------------------------------|
| Earliest end time                              | Activity Selection                            |
| Smallest weight/value frequency                | Huffman Coding                                |
| Shortest edge not forming a cycle              | Minimum Spanning Tree (Kruskal)               |
| Closest unvisited node                         | Shortest Path with non-negative edges (Dijkstra) |
| Smallest value at current position             | Some coin-change denomination systems        |
| Longest-reaching jump                          | Jump Game II (LeetCode)                       |
| Lowest current deficit                         | Gas Station (LeetCode)                        |

These work because their proof goes through. Notice the diversity of
greedy criteria — *"smallest"*, *"largest"*, *"earliest"*, *"closest"*.
Picking the right one is the whole game.

---

## When Greedy Fails — The Counter-Example

The canonical example: **Coin Change.**

> *Given coins of denominations D and a target amount T, find the minimum
> number of coins summing to T.*

**Greedy attempt:** always take the largest coin that doesn't exceed the
remaining amount.

For denominations `{1, 5, 10, 25}` (US coins) and any `T`, this works.
The US coin system is **"canonical"** — greedy is provably optimal.

For denominations `{1, 3, 4}` and T = 6:

- Greedy: take 4, then 1, then 1 → **3 coins**.
- Optimal: 3 + 3 → **2 coins**.

Greedy is wrong because committing to the 4 *forces* you into a worse
future — but greedy, by design, can't see the future. This is a problem
for **Dynamic Programming**, not greedy.

> **The lesson:** even a problem that *looks* greedy-friendly can have
> inputs where greedy fails. If you can't prove optimality, you can't
> trust greedy.

---

## Greedy vs Dynamic Programming

These two paradigms solve the same family of problems and are often
confused. The difference:

| Dimension           | Greedy                        | Dynamic Programming              |
|---------------------|-------------------------------|----------------------------------|
| Decisions           | One choice per step, committed| Try all choices, keep best       |
| Speed               | Usually fast (O(n log n))     | Usually polynomial (O(n²) / O(n·m)) |
| Correctness         | Requires proof                | By construction (explores all states) |
| When to use         | When greedy choice can be proven | When greedy fails but structure repeats |
| Code complexity     | Very short                    | Longer — state + transitions     |

**Rule of thumb:** try greedy first. If you can sketch a proof in five
minutes, use it. If not, reach for DP.

---

## Greedy Is Not "Pick the Biggest"

Beginners often think greedy means "always grab the largest thing."
It doesn't. Greedy means **commit to one choice per step using some
well-defined rule, and prove that rule is correct**.

- In activity selection, greedy picks the *smallest* end time.
- In Huffman coding, greedy merges the *two smallest* frequencies.
- In Dijkstra, greedy picks the *closest* unvisited node.

The criterion varies. What's constant is the *shape*: one rule, one pick,
no revisiting.

---

## When to Reach for Greedy

Good signals:

1. The problem asks for **an optimum** (max / min / earliest / fewest).
2. You can describe a single rule that picks "the obvious next move."
3. Making that move reduces the problem to a smaller instance of itself.
4. You can sketch (not just intuit) why the move cannot be wrong.

Bad signals (greedy will probably fail):

1. **Future choices affect the value of a current choice.** (Classic:
   "picking this cell now blocks the best long-term path.")
2. **The problem has "trap" inputs** where committing early loses.
   (The `{1, 3, 4}` counterexample above.)
3. **You need to explore multiple options and compare them.** That's DP.

---

## Pitfalls

- **Assuming greedy works without proof.** The most common greedy bug.
- **Choosing the wrong greedy rule.** Many problems have several plausible
  criteria; only some lead to optimal solutions. (For Activity Selection,
  "earliest start" or "shortest duration" both *sound* good but are wrong.)
- **Confusing "locally best" with "currently best".** The greedy rule
  should commit based on some static property of the available choices,
  not on a runtime tie-breaker that depends on history.
- **Using greedy on a DP problem.** Watch for: "*minimum coins*",
  "*0/1 knapsack*", "*longest increasing subsequence*" — these look
  greedy but aren't.

---

## Pseudocode Skeleton

```
function greedy(problem):
    items = prioritize(problem.items)         # sort / heap by greedy criterion
    solution = []

    for item in items:
        if feasible(item, solution):
            solution.append(item)
            commit(item)

    return solution
```

The `prioritize` step is often just a sort. The `feasible` check enforces
the problem's constraints (e.g., "doesn't overlap any activity already chosen").

For a concrete implementation, see [`template.py`](template.py).
For worked examples — including one where greedy **works** and one where
it **fails** — see [`problems/`](problems/).

---

## Key Takeaways

1. **Greedy: commit to the locally best choice at every step.**
2. **Correctness is not automatic.** You must prove the greedy choice
   is always in some optimal solution — usually via an exchange argument.
3. **Optimal substructure + greedy choice property → greedy works.**
   Miss either, switch to DP.
4. **Greedy produces beautiful, short, fast algorithms when it works.**
   And very convincing wrong answers when it doesn't.
5. **Always test greedy against an adversarial input or a brute force
   solution on small cases before trusting it.**
