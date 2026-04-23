# Stack — Theory

## Introduction

A **stack** is a container with one rule:

> *Only the TOP element can be accessed, added, or removed.*

That single constraint — **Last In, First Out (LIFO)** — seems
restrictive, but it's exactly what many algorithms need. Function
calls, bracket matching, undo history, DFS traversal, expression
evaluation — all are natural stack operations.

---

## The Stack ADT — Just Three Operations

A stack is defined by what you can DO to it, not how it's stored:

| Operation | Meaning                              | Time |
|-----------|--------------------------------------|------|
| `push(x)` | Add `x` to the top.                  | O(1) |
| `pop()`   | Remove and return the top.           | O(1) |
| `peek()`  | Return the top WITHOUT removing.     | O(1) |

Plus a few bookkeeping ops:

| Operation | Meaning                | Time |
|-----------|------------------------|------|
| `is_empty()` | Is the stack empty?   | O(1) |
| `__len__` | Current size.          | O(1) |

**Every operation is O(1).** This is what makes stacks powerful:
you get constant-time access to *some* element — just a very
specific one — and the discipline of only touching that element is
what enables the algorithms.

---

## Two Ways to Implement a Stack

### 1. Array-Backed Stack

Use a dynamic array. The END of the array is the top of the stack:

```
bottom [ 1, 2, 3, 4, 5 ] top
        ↑               ↑
        arr[0]          arr[-1]

push(6):  arr.append(6)          →  [1, 2, 3, 4, 5, 6]
pop():    return arr.pop()       →  returns 6
peek():   return arr[-1]         →  returns 5
```

**All operations O(1) amortized** (thanks to the dynamic array's
amortized-O(1) append).

**Pros:**
- Minimal overhead per element.
- Cache-friendly memory layout.
- The simplest implementation.

**Cons:**
- Hidden O(n) resize can happen on `push` (amortized away over many
  operations — see Phase-04 / 01-Array / theory.md).

In Python, you can just use a `list` directly — `list.append` and
`list.pop` give you a stack. That's exactly what most production
Python code does.

### 2. Linked-List-Backed Stack

Use a singly-linked list. The HEAD is the top:

```
top →  [5] → [4] → [3] → [2] → [1]  (bottom)

push(6):  new node becomes head     →  [6] → [5] → [4] → [3] → [2] → [1]
pop():    head = head.next          →  returns 6
peek():   return head.value         →  returns 5
```

**All operations O(1)** — no amortization needed, no resize.

**Pros:**
- True O(1) push and pop (no hidden resize).
- Grows without ever allocating a big block.

**Cons:**
- One extra pointer per element (memory overhead).
- Poorer cache behaviour than array version.

In Python, you'd rarely implement this yourself — `list` is almost
always enough. But it's the right mental model for understanding
linked-structure stacks in systems code.

---

## Stack vs Queue vs Deque — The LIFO/FIFO Trinity

Stacks, queues, and deques are the three **discipline-based**
linear data structures:

| Structure | Add at | Remove at | Discipline | Canonical use     |
|-----------|--------|-----------|------------|-------------------|
| Stack     | top    | top       | LIFO       | Function calls    |
| Queue     | back   | front     | FIFO       | Task schedulers   |
| Deque     | either | either    | Mixed      | Sliding windows   |

All three are covered in this phase:
- Stack — this module (04)
- Queue — next module (05)
- Deque — module 06

Internally, any of them can be implemented with an array or a linked
structure. The DISCIPLINE (LIFO / FIFO / both-ended) is what distinguishes
them — not the underlying storage.

---

## When to Use a Stack

### ✅ Good fits

- **Function call stacks.** Every programming language uses a stack
  for call frames. Recursion is literally "let the CPU manage a stack
  for you."
- **Bracket matching.** `()`, `[]`, `{}` — push opens, match closes
  against top. Covered in `applications/parentheses.py`.
- **Expression evaluation.** Postfix evaluation uses one stack;
  infix-to-postfix (Shunting-yard) uses two. Covered in
  `applications/eval-postfix.py` and `applications/infix-postfix.py`.
- **Undo history.** Each action pushes a "reverse me" record onto a stack.
  `Ctrl+Z` pops.
- **DFS traversal.** Pushing neighbours onto a stack implements DFS
  iteratively (avoiding recursion-depth limits).
- **Backtracking.** The implicit recursion stack IS your "state to try."
- **Monotonic stack.** A stack with an invariant that its contents
  are strictly increasing or decreasing — see
  Phase-02 / 02 / 09-Monotonic-Stack. Problems like Next Greater
  Element, Stock Span, and Largest Rectangle in Histogram use this.

### ❌ Poor fits

- You need random access.
- You need FIFO (first in, first out) — use a queue.
- You need to inspect anything other than the top.

---

## Stack Applications — The Canonical Four

### 1. Parenthesis / Bracket Matching

Walk the string. Opens → push onto stack. Closes → pop and verify
match. Valid iff stack ends empty.

```python
stack = []
pairs = {")": "(", "]": "[", "}": "{"}
for ch in s:
    if ch in "([{":
        stack.append(ch)
    else:
        if not stack or stack[-1] != pairs[ch]:
            return False
        stack.pop()
return not stack
```

Covered in `applications/parentheses.py`. First seen in
`02-String/problems/parentheses.py`; the stack view makes it cleaner.

### 2. Postfix Expression Evaluation

Postfix (Reverse Polish Notation) writes operators AFTER their operands:

    "2 3 +"       = 2 + 3             = 5
    "2 3 4 * +"   = 2 + (3 * 4)        = 14
    "2 3 + 4 *"   = (2 + 3) * 4        = 20

Evaluation uses ONE stack:

```python
stack = []
for token in tokens:
    if token.isnumeric():
        stack.append(int(token))
    else:  # operator
        b = stack.pop()
        a = stack.pop()
        stack.append(apply(op, a, b))
return stack.pop()
```

Covered in `applications/eval-postfix.py`.

### 3. Infix → Postfix Conversion (Shunting-Yard)

Convert standard math notation ("2 + 3 * 4") to postfix ("2 3 4 * +")
so it can be evaluated without parentheses.

Uses TWO stacks / queues:
- An **operator stack** (stack of pending operators).
- An **output queue** (the postfix result).

Dijkstra's Shunting-Yard algorithm, covered in
`applications/infix-postfix.py`.

### 4. Monotonic Stack — Next-Greater / Previous-Smaller Queries

A stack whose contents are kept strictly increasing (or decreasing).
When the invariant would be broken by a new element, pop until it fits.

The canonical pattern for "find the next element greater/smaller
than each index's value" problems. Covered in depth in Phase-02 / 02 /
09-Monotonic-Stack; we see a specific instance in `problems/stock-span.py`.

---

## Min-Stack — A Special Case Worth Its Own Treatment

**Problem:** implement a stack supporting `push`, `pop`, `peek`, AND
`get_min` — all in O(1).

The naive solution would scan the stack for the min on every query,
giving O(n) per call. The trick: maintain a **second stack** of
minima. Every push also pushes the new min (= min of old min and
new value). Every pop also pops from the min stack. `get_min` is
just `min_stack[-1]`.

Covered in `problems/min-stack.py` (LeetCode #155).

---

## Two-Stacks-as-a-Queue / Queue-as-Two-Stacks

A classic "impossible-looking" interview problem: **implement a
queue using only stacks.** Solvable elegantly with TWO stacks:

    stack_in:  push goes here
    stack_out: pop comes from here

When you need to pop and `stack_out` is empty, TRANSFER everything
from `stack_in` to `stack_out` (reverses the order). Pop from top
of `stack_out`.

Amortized O(1) for all operations. Covered in 05-Queue.

The symmetric problem (**stack using queues**) is also a classic —
also covered in 05.

---

## Python Gotchas

### `list` IS a stack in Python

Python's `list.append()` and `list.pop()` (no argument) both
operate on the END — exactly the stack interface. For 99% of
real Python code, this is the stack you want:

```python
stack = []
stack.append(1)        # push
stack.append(2)
stack[-1]              # peek → 2
stack.pop()            # pop → 2
```

Don't use `list.insert(0, x)` and `list.pop(0)` to "stack from the
front" — those are O(n).

### Don't Use `Queue.LifoQueue` Unless You Need Thread Safety

`queue.LifoQueue` is a thread-safe LIFO queue from the `queue` module.
It has the same interface as a stack but with locking overhead.
Use `list` unless you genuinely need concurrent access.

### `collections.deque` Also Works

`deque.append()` and `deque.pop()` work the same as `list`'s and
are also O(1). Slightly different memory characteristics (no resize
hiccup ever), but rarely a practical difference.

---

## Pitfalls

- **Popping from an empty stack.** Always `if stack:` or catch the
  exception. `list.pop()` raises `IndexError` on empty.
- **Confusing push/pop direction.** Python's `list.pop()` takes from
  the END, which is the top. `list.pop(0)` is a QUEUE dequeue — and
  it's O(n). Don't mix them.
- **Wrong LIFO order in traversal.** DFS iteratively with a stack gives
  DIFFERENT visit order than DFS recursively — the stack version visits
  the LAST-PUSHED neighbour first. Push neighbours in REVERSE order to
  match recursive behaviour.
- **Forgetting the "stack ends empty" check.** Bracket-matching is
  correct only if the stack is empty at the end. An unmatched open
  leaves residue.

---

## Key Takeaways

1. **Stack = LIFO discipline.** Push / pop / peek on one end only,
   all O(1).
2. **In Python, use `list`** unless you have a specific reason not to.
3. **Four canonical applications:** bracket matching, postfix eval,
   infix→postfix conversion, monotonic stack.
4. **Two implementations** (array-backed, linked-list-backed) give
   the same O(1) ops with different cache / resize tradeoffs.
5. **Min-stack and two-stacks-as-queue** are the two "stacks +
   clever trick" problems that show up in interviews constantly.

For concrete implementations, see
[`implementation/array-stack.py`](implementation/array-stack.py) and
[`implementation/linked-stack.py`](implementation/linked-stack.py).
For worked applications and problems, see
[`applications/`](applications/) and [`problems/`](problems/).
