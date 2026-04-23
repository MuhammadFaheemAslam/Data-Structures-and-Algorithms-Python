# Deque — Theory

## Introduction

A **deque** (pronounced "deck" — "double-ended queue") is a container
where you can add or remove from **either end** in O(1).

It's the UNION of a stack and a queue. Anything you can do with a
stack OR a queue, you can do with a deque. That makes it the most
flexible of the linear data structures in Phase 04.

---

## The Deque ADT — Six Operations

| Operation        | Meaning                              | Time |
|------------------|--------------------------------------|------|
| `append(x)`      | Add `x` at the BACK.                 | O(1) |
| `appendleft(x)`  | Add `x` at the FRONT.                | O(1) |
| `pop()`          | Remove and return the BACK.          | O(1) |
| `popleft()`      | Remove and return the FRONT.         | O(1) |
| `peek_back()`    | Return the back without removing.    | O(1) |
| `peek_front()`   | Return the front without removing.   | O(1) |

Plus `__len__`, `__iter__`, etc.

**All six are O(1).** That's what makes a deque a deque — full
constant-time access at both ends.

---

## Deque Includes Stack and Queue as Special Cases

    Stack =  deque using only `append` + `pop` (both at the back)
    Queue =  deque using only `append` + `popleft`

So in Python, a single `collections.deque` can serve as a stack, a
queue, a ring buffer (with `maxlen`), or a true deque — depending on
which subset of its methods you use.

This is why `deque` is often the right choice in practice when you're
not sure which discipline you'll need. Replacing `list` with
`deque` costs essentially nothing and eliminates the `list.pop(0)`
performance trap from 05-Queue.

---

## Two Ways to Implement a Deque

### 1. Doubly-Linked List

Each node has `prev` and `next` pointers. All four end operations
splice nodes in/out of the head or tail in O(1). No resize, no cache
hit besides the walk.

This is the implementation in `implementation.py` — essentially the
same as `02-DLL/implementation.py`, specialized to expose only the
deque operations.

### 2. Circular Array of Blocks

The production implementation. Python's `collections.deque` uses a
doubly-linked list of ARRAY BLOCKS (each block holds a handful of
elements). This gets:

- O(1) operations at both ends (like linked list).
- Good cache behaviour (each block is contiguous).
- Lower memory overhead than a node-per-element linked list.

You won't implement this yourself; it's a CPython optimization. But
knowing that `deque` isn't a plain DLL explains why it's ~2× faster
than a hand-rolled Python DLL.

---

## Python's `collections.deque` — The Right Tool in Most Code

```python
from collections import deque

d = deque()
d.append(1)           # back      O(1)
d.appendleft(0)       # front     O(1)
d.pop()               # back      O(1)
d.popleft()           # front     O(1)
d[0]                  # front     O(1)
d[-1]                 # back      O(1)
d[i]                  # middle    O(n)  — random access is slow
len(d)                #           O(1)
```

Key features beyond the basics:

| Feature               | What it does                                     |
|-----------------------|--------------------------------------------------|
| `deque(maxlen=k)`     | Automatic discard when capacity reached (ring buffer) |
| `d.rotate(n)`         | O(k) where k = |n|; rotate elements n positions |
| `d.extend(iterable)`  | Append many elements                             |
| `d.extendleft(iter)`  | Like `extend` but in REVERSE order (each gets prepended) |
| `d.reverse()`         | In-place reverse (O(n))                          |
| `d.copy()`            | Shallow copy                                     |

The `maxlen` feature is particularly useful for sliding-window
problems — the window "auto-shrinks" as you add past the cap.

---

## When to Reach for a Deque

### ✅ Good fits

- **You need O(1) at both ends.** This is the defining case.
- **Sliding-window problems.** Especially the "maximum in a window
  of size k" problem — covered in `problems/sliding-window-max.py`.
  The monotonic-deque pattern is one of the most elegant tricks in
  linear data structures.
- **BFS with bidirectional search.** Some variants of BFS add to the
  front AND the back for lower average cost.
- **Palindrome-like checks.** Pop from both ends, compare —
  `problems/palindrome-check.py`.
- **Undo/redo with bounded history.** `deque(maxlen=N)` gives an
  auto-trimming history.
- **Default replacement for `list`-as-queue.** If there's any chance
  you might `pop(0)`, use `deque` to avoid the O(n²) trap.

### ❌ Poor fits

- **Random access.** `deque[i]` for a middle `i` is O(i) — not O(1).
  Use a `list` if you need index-based access in the middle.
- **Finding things by value.** `x in deque` is O(n). Use a `set` /
  `dict`.

---

## The Monotonic Deque — A Power Move

One of the most beautiful applications of a deque is the **monotonic
deque**: a deque where the elements are kept in strictly increasing
(or decreasing) order. It's the deque version of the monotonic stack
from Phase-02 / 02 / 09, but it also supports REMOVING elements from
the FRONT — which is essential for sliding-window problems.

Classic use: "maximum of every window of size k."

```
Invariant: the deque holds INDICES of elements in decreasing value order
(the largest value's index is always at the front).

For each new index i:
    - Pop from the BACK any index whose value is ≤ nums[i]
      (they can never be the max while nums[i] is in the window).
    - Append i to the back.
    - Pop from the FRONT any index that has fallen out of the window
      (index < i - k + 1).
    - The FRONT of the deque is the window's maximum.
```

Each index is added once and removed once, so total work is O(n) —
amortized O(1) per window. Covered in
`problems/sliding-window-max.py`.

This same pattern solves:
- LC #239 Sliding Window Maximum
- LC #1425 Constrained Subsequence Sum
- LC #862 Shortest Subarray with Sum at Least K
- LC #1696 Jump Game VI

---

## Deque vs Its Relatives

| Structure | Add front | Add back | Remove front | Remove back | Random access |
|-----------|-----------|----------|--------------|-------------|----------------|
| `list`    | O(n)      | O(1)     | O(n)         | O(1)        | O(1)           |
| `deque`   | **O(1)**  | **O(1)** | **O(1)**     | **O(1)**    | O(n) middle    |
| Linked list (SLL) | O(1) | O(n)  | O(1)         | O(n)        | O(n)           |
| Linked list (DLL) | O(1) | O(1)  | O(1)         | O(1)        | O(n)           |

`deque` dominates `list` when you need ANY end operation besides
"append + pop back". It loses only on middle-random-access.

A DLL has the same Big-O as a deque but worse constants (higher
per-element memory overhead, worse cache behaviour). Deques win in
practice.

---

## Pitfalls

### 1. Random Access Is O(n)

```python
d = deque(range(1_000_000))
d[500_000]           # walks 500k nodes → slow
```

If you need random access, don't use `deque`. Use `list`.

### 2. `deque[i] = x` Is O(i)

Same reason. Random assignment requires a walk to position i.

### 3. Don't Confuse the Directions

- `append` / `pop` both operate on the RIGHT.
- `appendleft` / `popleft` both operate on the LEFT.

Mismatched pairs (e.g., `append` + `popleft`) make a queue; matched
pairs (`append` + `pop`) make a stack. This is exactly why deque
generalizes both.

### 4. `extendleft` Reverses

```python
d = deque([1, 2])
d.extendleft([3, 4, 5])
# d is now deque([5, 4, 3, 1, 2])
```

Each element of the argument gets prepended in turn, so the final
order is the argument REVERSED. Usually the right thing, occasionally
surprising.

---

## Key Takeaways

1. **Deque = stack + queue.** O(1) at both ends, lets you pick any
   subset of operations.
2. **In Python, use `collections.deque`** — it's the right default
   for any "might need operations on both ends" scenario.
3. **Monotonic deque** solves sliding-window-max and siblings in O(n).
4. **Don't use `deque` for middle access.** It's O(n). That's `list`'s job.
5. **`maxlen` is a built-in ring buffer.** Useful for bounded history,
   streaming, log retention.

For the implementation see [`implementation.py`](implementation.py).
For problems see [`problems/sliding-window-max.py`](problems/sliding-window-max.py)
(the monotonic-deque classic) and
[`problems/palindrome-check.py`](problems/palindrome-check.py)
(compare from both ends).
