# Recursion — Theory

## Introduction

A **recursive function** is a function that calls itself.

That sentence makes recursion sound circular, and for many people
it feels that way at first. The key mental shift:

> *The function doesn't really "call itself." It creates a NEW
> INSTANCE of the same function, with its own parameters and local
> variables, separate from the caller.*

Recursion is about **reducing a problem to a smaller instance of
itself, until the instance is small enough to solve directly.**
Every recursive function has two parts:

1. **Base case** — the smallest instance, which is solved WITHOUT
   any further recursive call.
2. **Recursive case** — the larger instance, which is solved by
   reducing to a smaller one and letting the function handle it.

---

## The Shape of Every Recursive Function

```python
def recursive(input):
    if is_base_case(input):
        return solve_directly(input)            # BASE CASE

    smaller_input = reduce(input)
    smaller_result = recursive(smaller_input)   # RECURSIVE CASE
    return combine(smaller_result, input)
```

That's it. Every correct recursive function has this structure
somewhere — though it may be spread across multiple branches or
interleaved with the recursive call.

Three questions to ask when writing one:

1. **What's the smallest input?** → the base case.
2. **How do I shrink the problem?** → the reduction.
3. **Given the solution to the smaller problem, how do I build
   the solution to the current one?** → the combination.

If all three answers are clear and correct, the function is correct.

---

## Why Recursion Works — Mathematical Induction

Recursion is **the algorithmic form of mathematical induction**.
Proving a recursive function is correct is the same as proving an
inductive statement:

1. **Base:** prove that the function works when `input` is the
   smallest (the base case).
2. **Induction step:** ASSUME the function works for any smaller
   input. Show that, given that assumption, it works for the current
   input.

If both hold, the function works for every input.

This is why recursive code is so often **provably correct** with
little effort, compared to iterative code with its loop invariants.
Write the function so that induction is clean, and correctness
follows.

---

## The Call Stack — What Happens Under the Hood

When a function calls another function (including itself), the
runtime pushes a **stack frame** containing:

- The return address (where to resume in the caller).
- The caller's local variables.
- The new function's parameters.

When the function returns, its frame is popped and the caller resumes.

For recursion, this means:

- Each recursive call pushes a new frame.
- The stack GROWS as we recurse deeper.
- Frames are popped as each call returns.
- The deepest call returns first (LIFO).

### The Recursion-Depth Trap

Python's default recursion limit is **1000 stack frames**. Try to
recurse deeper and you'll hit `RecursionError`.

```python
import sys
sys.setrecursionlimit(100_000)             # raise it if needed
```

But raising the limit doesn't solve the real problem: deep recursion
consumes significant stack memory (O(n) in Python). For anything that
might recurse more than a few thousand levels, **convert to iteration**
— either with a while loop or an explicit stack.

Algorithms where depth is bounded by log n (binary search, balanced-
tree operations) are fine. Algorithms where depth can be O(n)
(linked-list recursion, linear accumulation) are risky.

---

## Tail Recursion — Recursion That Acts Like Iteration

A **tail-recursive** function is one where the recursive call is the
LAST thing it does:

```python
def sum_to(n, acc=0):
    if n == 0:
        return acc
    return sum_to(n - 1, acc + n)           # recursive call is the LAST operation
```

vs non-tail-recursive:

```python
def sum_to(n):
    if n == 0:
        return 0
    return n + sum_to(n - 1)                # still have work after the call (the +)
```

In languages with **tail-call optimization (TCO)** — Scheme, ML,
Haskell, some Scala — tail-recursive functions DON'T grow the stack;
the compiler rewrites them as loops. Python does NOT have TCO —
tail-recursion in Python still blows the stack at depth 1000.

So in Python, the lesson is different: if you recognize a tail-
recursive function, consider **converting it to a while loop by hand**.
You'll get the same answer with no stack-depth risk.

Covered in depth in `patterns/tail-recursion.py`.

---

## Head Recursion — "Process on the Way Up"

**Head-recursive** functions do work AFTER the recursive call
returns — the recursive call is processed first, and the current
frame's work happens on the way back up the stack:

```python
def print_reverse(n):
    if n == 0:
        return
    print_reverse(n - 1)                    # recurse FIRST
    print(n)                                # then do work — prints 1, 2, 3, ..., n
```

Contrast with tail recursion, which does the work BEFORE recursing:

```python
def print_forward(n, current=1):
    if current > n:
        return
    print(current)                          # do work first
    print_forward(n, current + 1)           # then recurse
```

Both are O(n) time. The difference is WHEN the useful work happens
— which determines iteration order. Covered in
`patterns/head-recursion.py`.

---

## Tree Recursion — Multiple Calls per Step

**Tree recursion** happens when a function makes MORE THAN ONE
recursive call per invocation:

```python
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)          # two recursive calls
```

The recursion tree BRANCHES at every level, so the total number of
calls is EXPONENTIAL. For fib(n), it's roughly O(φⁿ) ≈ O(1.618ⁿ).

The fix is **memoization** (DP, see Phase 02 / 01 / 04) — cache the
result of each subproblem so tree recursion collapses to linear.

Tree recursion is also the underlying shape of backtracking, divide
& conquer, and merge/quick sort. Covered in `patterns/tree-recursion.py`.

---

## Indirect Recursion — A Calls B Calls A

When function A calls function B, and B calls A back, they're
**mutually / indirectly recursive**:

```python
def is_even(n):
    if n == 0: return True
    return is_odd(n - 1)

def is_odd(n):
    if n == 0: return False
    return is_even(n - 1)
```

Each call reduces `n` by 1, and eventually bottoms out at the base
case. From a correctness standpoint, induction still works — the
inductive hypothesis covers BOTH functions at once.

Rare in practice (direct recursion usually works), but useful for
modelling state machines or toggling between two modes. Covered in
`patterns/indirect-recursion.py`.

---

## Recursion vs Iteration — When to Pick Which

Recursive code is often **shorter and more elegant** — but not
always the right choice in practice.

| Criterion                      | Recursion               | Iteration               |
|--------------------------------|-------------------------|-------------------------|
| Natural for tree / graph problems | **Yes** (DFS is recursion) | Requires explicit stack |
| Easy inductive correctness     | **Yes**                 | Needs loop invariants   |
| Readable for divide-and-conquer | **Yes**                | Clumsier to express     |
| Stack-safe on large inputs     | No (Python O(n) stack)  | **Yes**                 |
| Constant-factor speed          | Slower (call overhead)  | **Faster**              |
| Memory efficiency              | O(depth) stack          | **O(1) typical**        |

**Rule of thumb:**

- **Recurse** when the problem has a natural self-similar structure
  (trees, divide-and-conquer, backtracking).
- **Iterate** when the problem is linear accumulation or iteration
  (summing, transforming, filtering).
- **Convert recursion to iteration** when recursion depth might
  exceed a few thousand.

---

## Converting Recursion to Iteration

Any recursive algorithm can be rewritten iteratively. The standard
technique: **maintain an explicit stack** of work that would have
been done by recursive calls.

Tail-recursive functions are the easiest — they become simple
`while` loops. Tree-recursive functions often become stack-based
DFS with an explicit `list` or `deque`.

Example:

```python
# Recursive
def depth(node):
    if node is None:
        return 0
    return 1 + max(depth(node.left), depth(node.right))

# Iterative, explicit stack
def depth(node):
    if node is None:
        return 0
    stack = [(node, 1)]
    best = 0
    while stack:
        n, d = stack.pop()
        best = max(best, d)
        if n.left:  stack.append((n.left, d + 1))
        if n.right: stack.append((n.right, d + 1))
    return best
```

Same algorithm, no recursion-limit risk, no call-stack overhead —
but much more code. Pick the form that fits your input size.

---

## Complexity of Recursive Algorithms

The complexity of a recursive function is determined by its
**recursion tree**: the tree of all invocations it makes.

- **Linear recursion** (one call per step): n levels × O(1) work = O(n).
- **Binary recursion** (two calls per step): O(2ⁿ) nodes in the tree
  = **exponential** unless memoized.
- **Divide & Conquer** (two calls on halves): log n levels × O(n)
  combine work per level = **O(n log n)**.
- **Tail recursion** (O(1) work at base, no combine): O(n) time,
  O(n) stack (or O(1) with TCO).

Full analysis — including the Master Theorem for divide-and-conquer
and the recursion-tree method for irregular recurrences — is in
[`recursion-tree.md`](recursion-tree.md).

---

## Common Pitfalls

### 1. Missing or Wrong Base Case

```python
def bad(n):
    return n + bad(n - 1)        # no base case → infinite recursion → crash
```

Always write the base case FIRST. It's the foundation.

### 2. Base Case Not Actually Reached

```python
def bad(n):
    if n == 0: return 0
    return bad(n - 2)            # on odd n, never hits 0 — recurses forever
```

Make sure the reduction MONOTONICALLY approaches the base case.

### 3. Infinite Tree

A tree-recursive function where a subproblem's subproblem is
equal to (or bigger than) the original:

```python
def bad(n):
    return bad(n - 1) + bad(n)   # bad(n) calls bad(n)!
```

Double-check that every recursive call uses a STRICTLY SMALLER input.

### 4. Recomputing the Same Subproblem

```python
def fib(n):
    if n < 2: return n
    return fib(n - 1) + fib(n - 2)   # overlapping subproblems
```

For n = 40, this makes ~10⁸ calls. Fix with memoization (see
Phase 02 / 01 / 04-Dynamic-Programming).

### 5. Mutable Default Arguments

```python
def f(x, memo={}):               # memo is SHARED ACROSS CALLS — classic Python bug
    ...
```

Use `memo=None` and initialize inside, or pass the memo explicitly.

### 6. Recursion Depth Blown

Python's default limit is 1000. Any algorithm with recursion depth
> that will crash. Raise the limit with `sys.setrecursionlimit` or
convert to iteration.

---

## Key Takeaways

1. **Recursion = base case + reduction to a smaller instance.**
   Correctness follows by induction.
2. **Each recursive call is a new stack frame.** Depth costs O(n)
   memory; Python's default limit is 1000.
3. **Tail recursion** has the recursive call as the LAST operation.
   Convertible to iteration for free (though Python doesn't do it
   automatically).
4. **Tree recursion** (multiple calls per step) can be exponential
   — memoize it if subproblems overlap.
5. **Mental model:** base case, inductive step, recursion tree.
   If those three are clear, the function is correct.

For visualization of recursion trees and complexity analysis, see
[`recursion-tree.md`](recursion-tree.md). For the four common
patterns, see [`patterns/`](patterns/). For worked problems, see
[`problems/`](problems/).
