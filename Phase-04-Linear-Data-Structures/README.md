# Phase 04 — Linear Data Structures

Phase 01 introduced Python's **built-in** containers. Phase 03 taught
you the classical **algorithms** that operate on them. Phase 04 is
about the data structures themselves — **how they're built**, what
they cost, and how to implement them from scratch when you need
behaviour Python doesn't provide out of the box.

---

## What This Phase Covers

Six fundamental linear data structures, in the order every
curriculum teaches them:

| # | Structure      | Memory layout       | Access        | Insert/Delete               |
|---|----------------|---------------------|---------------|-----------------------------|
| 1 | **Array**      | contiguous          | O(1)          | O(n) (middle), amortized O(1) at end |
| 2 | **String**     | immutable array of chars (Python) | O(1) | always creates a new string |
| 3 | **Linked List**| scattered nodes     | O(n)          | O(1) at known position      |
| 4 | **Stack**      | LIFO discipline     | top only O(1) | push/pop O(1)                |
| 5 | **Queue**      | FIFO discipline     | front/back O(1) | enqueue/dequeue O(1)      |
| 6 | **Deque**      | double-ended        | both ends O(1)| push/pop at either end O(1) |

All six are **linear** — elements form a sequence with a natural
"next" relationship. None of them need tree structure, heap ordering,
or hash-based access (those come in Phases 06-08).

---

## Why Build These From Scratch?

Python already has `list`, `str`, `collections.deque`, and `queue.Queue`.
Why implement them yourself?

1. **To understand the costs.** Knowing WHY `list.insert(0, x)` is
   O(n) while `deque.appendleft(x)` is O(1) is the difference between
   code that runs in milliseconds and code that times out.

2. **To understand hybrid structures.** LRU cache uses a hash map
   **plus** a doubly-linked list. A BFS queue uses a deque. Every
   subsequent structure is a composition of these primitives.

3. **Because interviews expect it.** "Implement a linked list",
   "implement a stack", "find the middle node" — these show up
   constantly. Writing them once cements the mental model.

4. **Because `list` isn't always the right answer.** When you need
   true O(1) prepend, or a cyclic buffer, or a stack with min-in-O(1),
   you need to build beyond `list`.

---

## The Memory-Layout Dichotomy

The most important division between these six structures is **how
they store their elements in memory**:

### Contiguous (Array, String, Stack-from-array, Queue-from-array)

- Elements live back-to-back in memory.
- **Random access is free** — `arr[i]` is a pointer-arithmetic
  lookup, O(1).
- Resizing / shifting costs O(n) — inserting in the middle means
  moving everything after it.

### Linked (Linked List, Stack-from-linked, Queue-from-linked, Deque)

- Elements are scattered; each "node" has a pointer to the next.
- **Random access is O(n)** — you must walk from the head.
- But insert/delete at a KNOWN position is O(1) — just splice
  pointers.

Everything else flows from this split. Which operations are fast
vs slow on each structure is determined almost entirely by its
memory layout.

---

## Folder Layout

```
Phase-04-Linear-Data-Structures/
├── README.md                            ← you are here
│
├── 01-Array/
│   ├── theory.md
│   ├── implementation.py                ← static array (from scratch)
│   ├── dynamic-array.py                 ← resizable array (Python list semantics)
│   ├── problems/
│   │   ├── easy/
│   │   ├── medium/
│   │   └── hard/
│   └── interview-questions.md
│
├── 02-String/
│   ├── theory.md
│   ├── string-methods.py                ← Python string operations + Big-O
│   ├── string-builder.py                ← efficient string concatenation patterns
│   └── problems/
│       ├── palindrome.py
│       ├── anagram.py
│       └── parentheses.py
│
├── 03-Linked-List/
│   ├── theory.md
│   ├── interview-questions.md
│   ├── 01-SLL/                          ← singly linked
│   ├── 02-DLL/                          ← doubly linked
│   ├── 03-Circular-LL/                  ← head-to-tail loop
│   └── 04-Cycle-Detection/              ← Floyd's, cycle start, variants
│
├── 04-Stack/
│   ├── theory.md
│   ├── implementation/                  ← array-based + linked-based
│   ├── applications/                    ← parentheses, infix-postfix, etc.
│   └── problems/                        ← min-stack, stock span
│
├── 05-Queue/
│   ├── theory.md
│   ├── implementation/                  ← array-based, linked, circular
│   ├── applications/
│   └── problems/                        ← generate-binary, stack-using-queues
│
└── 06-Deque/
    ├── theory.md
    ├── implementation.py
    └── problems/                        ← sliding-window-max, palindrome
```

### New Organizational Patterns in This Phase

1. **Problems tiered by difficulty.** Array (and a few others) have
   `problems/easy/`, `problems/medium/`, `problems/hard/` subfolders
   with a shared `solutions.md` per tier. This mirrors how interview
   prep materials structure problem sets.

2. **`interview-questions.md` per major structure.** Array and
   Linked List get standalone interview cheatsheets covering
   conceptual questions alongside the coding problems.

3. **Nested numbered sub-modules.** Linked List splits into
   singly / doubly / circular / cycle-detection — each a complete
   sub-module with its own `implementation.py` and problems.

---

## Memory of Python's Built-Ins (For Reference)

| Python type           | Backed by               | Head / tail ops                         |
|-----------------------|-------------------------|-----------------------------------------|
| `list`                | dynamic array           | append O(1) amortized; insert(0) O(n)   |
| `str`                 | immutable array         | any operation creates a new string       |
| `collections.deque`   | doubly-linked blocks    | appendleft / popleft / append / pop all O(1) |
| `queue.Queue`         | thread-safe deque       | put / get O(1); blocks if empty/full    |
| `heapq` (module)      | binary heap on a list   | O(log n) push / pop — covered in Phase 07 |

After building these from scratch in Phase 04, you'll understand
exactly when to reach for each of the above in real code.

---

## Outcome

By the end of this phase you should be able to:

1. **Implement any of the six structures from scratch** in ~15 minutes.
2. **Predict the cost of any operation** before running the code.
3. **Compose them into hybrids** — know why an LRU cache uses a
   dict + doubly-linked list, why a BFS uses a deque, why an undo
   stack uses, well, a stack.
4. **Reason about memory layout** — recognize which operations are
   fast vs slow from the layout alone.
5. **Pick the right built-in** for the job in production Python.

Phase 05 (Recursion & Backtracking) will build on this foundation —
most recursive structures (trees, graphs) are elaborations of the
linked-list idea.
