# Queue — Theory

## Introduction

A **queue** is a container with one rule:

> *Add at one END, remove at the other.*

This is **First In, First Out (FIFO)** discipline — the mirror image
of the stack's LIFO. Where a stack is a *"last one in wins"* structure
(function calls, undo history), a queue is a *"fairness"* structure
(task schedulers, print queues, BFS traversal, producer-consumer
pipelines).

---

## The Queue ADT — Just Four Operations

| Operation       | Meaning                              | Time |
|-----------------|--------------------------------------|------|
| `enqueue(x)`    | Add `x` at the BACK.                 | O(1) |
| `dequeue()`     | Remove and return the FRONT.         | O(1) |
| `peek()` / `front()` | Return the front without removing. | O(1) |
| `is_empty()` / `len()` | Status queries                     | O(1) |

**Every operation is O(1).** Like stacks, queues are about DISCIPLINE
— you only ever touch one specific element, and that's what makes
them useful.

---

## Three Ways to Implement a Queue

### 1. Array-Backed Queue (NAÏVE Version)

Use a list. Enqueue at the end, dequeue at the front:

```python
enqueue(x):  self._data.append(x)   # O(1) amortized
dequeue():   return self._data.pop(0)   # O(n) — shifts everything left
```

**This is wrong.** `list.pop(0)` is O(n) because all remaining
elements must shift one position left. On n enqueues followed by n
dequeues, you get O(n²) total work — quadratic, not linear.

This naïve version is **the classic Python queue bug**. Don't use
it. Use one of the next two implementations instead.

### 2. Array-Backed Queue (CORRECT — Two Pointers / Circular Buffer)

Use a fixed-capacity array with two pointers: `front` and `rear`.
Enqueue advances `rear`; dequeue advances `front`. When either pointer
reaches the end, it wraps around.

```
Array of capacity 8, with front at index 2, rear at index 5:

     [ _, _, A, B, C, _, _, _ ]
             ↑     ↑
            front  rear

enqueue(D):  data[rear] = D; rear = (rear + 1) % capacity
dequeue():   value = data[front]; front = (front + 1) % capacity
```

All operations O(1). No shifting. This is a **circular buffer** —
covered in `implementation/circular-queue.py`.

### 3. Linked-List-Backed Queue

Use a singly-linked list with both `head` (the front) and `tail`
(the back) pointers. Enqueue at tail, dequeue at head.

```
front → [A] → [B] → [C] ← rear

enqueue(D):  new_tail = Node(D); tail.next = new_tail; tail = new_tail
dequeue():   v = head.value; head = head.next; return v
```

All operations O(1), no resize cost, no capacity limit. Covered in
`implementation/linked-queue.py`.

### 4. In Python — Use `collections.deque`

Python's `collections.deque` is a doubly-linked list of BLOCKS — a
hybrid that gets O(1) operations at both ends with excellent cache
behaviour. It's the right queue for any real Python code:

```python
from collections import deque
q = deque()
q.append(x)        # enqueue — O(1)
q.popleft()        # dequeue — O(1)
q[0]               # peek — O(1)
```

The implementations in this module exist to teach the ADT. For
production: `collections.deque`, always.

---

## Queue vs Stack — The FIFO/LIFO Mirror

| Property         | Stack (LIFO)         | Queue (FIFO)         |
|------------------|----------------------|----------------------|
| Add at...        | Top                  | Back                 |
| Remove from...   | Top                  | Front                |
| Canonical ops    | push, pop, peek      | enqueue, dequeue, peek |
| Use cases        | Function calls, DFS, expression eval | Schedulers, BFS, print queues |
| Python list      | `list.append` / `list.pop()` | **DON'T** use `list.pop(0)` — use `deque` |

Internally, both can be implemented with arrays OR linked structures.
The DISCIPLINE is what distinguishes them.

---

## When to Use a Queue

### ✅ Good fits

- **BFS on graphs and trees.** The frontier of unvisited nodes is a queue.
- **Task scheduling / work queues.** Jobs enter at the back, are
  executed from the front.
- **Producer-consumer patterns.** Multiple threads push items; consumer
  threads pop. (Use `queue.Queue` for thread safety.)
- **Buffering streams.** Audio, video, network packets arrive in
  bursts; a queue smooths them out.
- **Round-robin processing.** Iterate through queued items, moving
  partially-processed items to the back.
- **Level-order traversal of a tree.** Process level k's nodes and
  enqueue level k+1's children.

### ❌ Poor fits

- You need to remove from the BACK — that's a stack.
- You need random access — use a list.
- You need priority ordering — use a heap (Phase 07).
- You need bidirectional removal — use a deque.

---

## Queue Variants

### 1. Plain FIFO Queue

The one described above. Covered in this module.

### 2. Circular / Ring Buffer

Fixed-capacity queue that overwrites old entries (or rejects new ones)
when full. Covered in `implementation/circular-queue.py`.

Used for:
- Audio buffers (phone calls, streaming).
- Log retention ("keep the last N log lines").
- Networking packet buffers.

### 3. Priority Queue

A queue where `dequeue()` returns the MINIMUM (or maximum) element,
not the oldest. Internally implemented with a binary heap (O(log n)
enqueue / dequeue). Covered in Phase 07.

### 4. Deque ("double-ended queue")

Supports push / pop at BOTH ends. Covered in Phase-04 / 06-Deque.

### 5. Concurrent Queue

Thread-safe for multi-producer / multi-consumer scenarios. Python's
`queue.Queue`, Java's `BlockingQueue`, Go's channels.

---

## The Two-Stacks-as-a-Queue Trick

An elegant classic: **implement a queue using only stacks.**

```
stack_in:  push goes here
stack_out: pop comes from here

enqueue(x):  stack_in.push(x)       # O(1)

dequeue():
    if stack_out is empty:
        while stack_in is non-empty:   # TRANSFER
            stack_out.push(stack_in.pop())
    return stack_out.pop()          # O(1) amortized
```

Each element is pushed twice and popped twice (once on each stack),
so **amortized O(1)** per operation. See `problems/stack-using-queues.py`
for the symmetric problem (stack using queues, trickier — needs only
one or two queues but every push or pop is O(n)).

---

## BFS — The Canonical Queue Use Case

Breadth-first search uses a queue to process nodes in the order they
were discovered. Skeleton:

```python
from collections import deque

def bfs(start):
    visited = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        process(node)
        for neighbour in neighbours(node):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
```

The queue guarantees that nodes at distance k from the start are
processed BEFORE nodes at distance k+1. That's why BFS finds
SHORTEST paths (in unweighted graphs).

We see a small application in `problems/generate-binary.py` — using
a queue to generate binary numbers 1..n in lexicographic order,
essentially a BFS over a binary tree.

---

## Pitfalls

### 1. Never Use `list.pop(0)` as a Queue

```python
# ❌ NEVER
q = []
q.append(x)
q.pop(0)   # O(n)!  On 10_000 dequeues, that's 10^8 operations.

# ✅ ALWAYS
from collections import deque
q = deque()
q.append(x)
q.popleft()   # O(1)
```

This is the **single most common data-structure performance bug in
Python.** `pop(0)` looks innocent — it's not. Replace with `deque`.

### 2. Confusing Enqueue/Dequeue Direction

Python's `deque.append()` adds at the RIGHT (= back), and
`deque.popleft()` removes from the LEFT (= front). Mix them up and
you've built a stack instead of a queue.

### 3. Forgetting to Check for Empty

`deque.popleft()` on an empty deque raises `IndexError`. Always guard
with `while queue:` or catch the exception.

### 4. Thread Safety

`collections.deque` is NOT fully thread-safe — its pop/append are
atomic, but multi-step operations ("check then pop") are not. For
concurrent producers/consumers, use `queue.Queue`.

---

## Key Takeaways

1. **Queue = FIFO discipline.** Enqueue at the back, dequeue at the
   front, both O(1).
2. **In Python, use `collections.deque`** — never `list` with `pop(0)`.
3. **Three implementations** — array with two pointers (circular),
   linked list, or (in real Python) deque.
4. **BFS is the canonical queue use case** — any "process in discovery
   order" algorithm needs a queue.
5. **Two-stacks-as-a-queue** is the classic "build a queue from
   stacks" puzzle — amortized O(1) via lazy transfer.

For concrete implementations, see:
- [`implementation/array-queue.py`](implementation/array-queue.py) —
  correct array-backed queue with wraparound.
- [`implementation/linked-queue.py`](implementation/linked-queue.py) —
  linked-list-backed queue.
- [`implementation/circular-queue.py`](implementation/circular-queue.py) —
  fixed-capacity ring buffer.

For problems, see:
- [`problems/generate-binary.py`](problems/generate-binary.py) —
  BFS-style generation using a queue.
- [`problems/stack-using-queues.py`](problems/stack-using-queues.py) —
  LC #225, the "implement stack using queues" puzzle.
