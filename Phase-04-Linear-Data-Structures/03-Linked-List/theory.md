# Linked List — Theory

## Introduction

The **linked list** is the quintessential *"pointer-based"* data
structure. Where an array stores its elements in one contiguous
block of memory, a linked list scatters them — each element in its
own **node** — and connects them via **pointers**.

This tradeoff is the first big decision in data structure design:

> **Array vs Linked List** — contiguous memory (fast access) vs
> chained nodes (fast insert/delete). Neither is universally better.

Every other "pointer-heavy" structure you'll meet (trees, graphs,
heaps with pointers, hash-map chaining) is an elaboration of the
linked-list idea.

---

## Anatomy of a Node

A linked-list **node** holds:

1. A **value** (the actual data).
2. One or more **pointers** to OTHER nodes.

```
Node:    ┌─────────┬────────┐
         │  value  │  next  │─────→ next node
         └─────────┴────────┘
```

Which pointers, and in what direction, define the four variants:

| Variant                | Pointers per node         | Can traverse...                       |
|------------------------|---------------------------|----------------------------------------|
| **Singly linked list (SLL)**  | `next`              | Forward only                           |
| **Doubly linked list (DLL)**  | `prev`, `next`      | Both directions                        |
| **Circular linked list**      | `next` forms a loop | Forward, forever (wraps to head)       |
| **Doubly circular**           | Both, both form loops | Both directions, forever             |

---

## Array vs Linked List — The Big Table

| Operation                         | Array (Python `list`) | Linked List            |
|-----------------------------------|-----------------------|------------------------|
| **Access by index** `arr[i]`      | **O(1)**              | O(n)                   |
| **Append (at end)**               | O(1) amortized        | O(1) with a tail pointer; O(n) without |
| **Prepend (at start)**            | O(n)                  | **O(1)**               |
| **Insert at KNOWN node**          | n/a (arrays are indexed) | **O(1)**            |
| **Delete at KNOWN node**          | O(n) (shift)          | **O(1)** (DLL); O(n) find prev (SLL) |
| **Search by value**               | O(n)                  | O(n)                   |
| **Iteration**                     | O(n), cache-friendly  | O(n), cache-unfriendly |
| **Space overhead per element**    | ~1 pointer            | ~2+ pointers per node (+ malloc overhead) |
| **Cache behaviour**               | Excellent             | Poor                   |

**Two key asymmetries:**

1. **Arrays win random access; linked lists win middle-insert.**
   The defining tradeoff of linear data structures.

2. **Arrays win in practice, almost always.** Their cache-friendly
   memory layout often makes them 10× faster than linked lists on
   the same workload, even when both are theoretically O(n).

The linked list's sweet spot is narrow: **you need fast insert/delete
at a KNOWN position**, and you can't maintain an index into the array.
Most modern uses of linked lists are in:
- **LRU caches** (combined with a hash map for O(1) access).
- **Filesystem free lists** and low-level memory allocators.
- **Graph / tree adjacency lists** (where "next child" is a natural edge).

---

## When Should You Use a Linked List?

### ✅ Good fits

- **You need O(1) insert/delete at known positions.** The classic is
  the LRU cache: a hash map maps keys to DLL nodes; when a key is
  accessed, you splice its node to the front in O(1).
- **You rarely need random access.** Sequential traversal is fine.
- **You often append/prepend in any mix.** Python's `collections.deque`
  is a doubly-linked BLOCK list — gets the amortized benefits without
  the per-element pointer overhead.
- **The data fits naturally as "a chain of things with a next-link."**
  Undo history, event logs, chains of custody.

### ❌ Poor fits

- **You need random access.** Use an array.
- **You do lots of searching.** Both are O(n), but array scans are
  10× faster due to cache locality.
- **Memory is tight.** Per-node overhead is significant on small
  values (a node storing a single int can be 32+ bytes; a raw int
  in a C array is 8).
- **Cache behaviour matters.** See above.

### Python-Specific Note

Python doesn't have a built-in singly or doubly linked list in the
way C++, Java, or Rust do. The closest built-in is
`collections.deque`, which is a **doubly-linked list of BLOCKS** —
a hybrid that gets O(1) operations at both ends with much better
cache behaviour than a classical DLL.

When you implement a linked list from scratch in Python, you're
doing it for LEARNING — not because Python's built-ins aren't good
enough. In most real code, `list` or `deque` is the right answer.

---

## The Four Variants at a Glance

### 1. Singly Linked List (SLL)

```
head → [A] → [B] → [C] → [D] → None
```

- Each node has `value` and `next`.
- Traversal: forward only.
- Minimal pointer overhead; simpler to reason about.
- Covered in [`01-SLL/`](01-SLL/).

### 2. Doubly Linked List (DLL)

```
      head       tail
       ↓          ↓
None ← [A] ↔ [B] ↔ [C] ↔ [D] → None
```

- Each node has `value`, `prev`, and `next`.
- Traversal: both directions.
- O(1) insert/delete given just a node reference.
- More space per node; more pointers to maintain on edits.
- Covered in [`02-DLL/`](02-DLL/).

### 3. Circular Linked List

```
head → [A] → [B] → [C] → [D] ─┐
 ↑                             │
 └─────────────────────────────┘
```

- The last node's `next` points back to `head` (instead of None).
- Useful for round-robin structures, cyclic buffers, game turn
  ordering.
- Covered in [`03-Circular-LL/`](03-Circular-LL/).

### 4. Cycle Detection (Floyd's Algorithm)

A **cycle** is what happens when a non-circular list accidentally
develops a loop (usually due to a bug, sometimes by design). Floyd's
algorithm uses **fast and slow pointers** to detect and locate cycles
in O(n) time, O(1) space.

Covered in [`04-Cycle-Detection/`](04-Cycle-Detection/) — see also
the Fast-Slow-Pointers technique in Phase-02 / 02 / 06.

---

## Common Linked-List Operations

All assume a singly-linked list; doubly- and circular-variants have
minor tweaks.

### Insert at head

```python
new_node = Node(value)
new_node.next = head
head = new_node
# Time: O(1)
```

### Insert at tail (if tail pointer maintained)

```python
new_node = Node(value)
tail.next = new_node
tail = new_node
# Time: O(1)
```

Without a tail pointer, appending is O(n) — must walk to the end.

### Delete a node (SLL)

Deleting a node requires access to its PREDECESSOR (to update
prev.next). Given only a reference to the node itself, you can't
delete it in O(1) on an SLL — you'd need to copy the next node's
value into this one and delete the NEXT node instead.

### Reverse

Two pointers: `prev` and `current`. Walk the list, flipping each
link. See [`01-SLL/problems/reverse.py`](01-SLL/problems/reverse.py).

### Detect a cycle

Two pointers at DIFFERENT speeds — the fast-slow / tortoise-and-hare
trick. Covered in [`04-Cycle-Detection/floyd-algorithm.py`](04-Cycle-Detection/floyd-algorithm.py).

---

## The Dummy-Head Pattern

A common simplification when writing linked-list code: introduce a
**sentinel / dummy head node** that sits before the real first node:

```
dummy → head → [A] → [B] → None
```

Benefits:

- **No special case for an empty list.** Deletion / insertion
  always has a predecessor (dummy).
- **Head-deletion becomes uniform.** No need to track "did I just
  delete the head?" — just update dummy.next.
- **Reduces bug surface** — arguably the best linked-list trick
  to keep your code short.

Used extensively in the problems: `reverse.py`, `nth-from-end.py`,
and merge-sort on linked lists (Phase-03 / 02 / 02 / 01-Merge-Sort /
problems / sort-linkedlist.py).

---

## Pitfalls

- **Losing the head pointer.** In Python, once there's no reference
  to the head, the whole list becomes garbage-collected. Save the
  head before any loop that advances through the list.
- **Dangling `next` pointers.** After delete, always set the removed
  node's `next = None` (or let the GC handle it). Otherwise your
  "removed" node can still be reached through its own next pointer.
- **Off-by-one in the dummy-head pattern.** The dummy counts as
  index −1; the "real" head is the node dummy.next points to.
- **Iterating without a null check.** Always check `while node:`, not
  `while node.next:` — the latter skips the last node.
- **Circular lists and infinite loops.** A bug that turns an SLL into
  a circular LL will cause `print(list)` (or any iteration) to hang
  forever. Always cap your traversal length during debugging.

---

## Key Takeaways

1. **Linked lists trade random access for fast insert/delete at
   known positions.** That's the defining tradeoff.
2. **Arrays win in practice** due to cache locality — so pick
   linked lists ONLY when their specific strengths matter.
3. **Four variants:** SLL, DLL, circular, + their combination. Each
   adds functionality at the cost of more pointers per node.
4. **The dummy-head pattern** simplifies edge cases dramatically.
5. **Floyd's cycle-detection algorithm** is the canonical "fast-slow
   pointer" trick — covered in depth in
   [`04-Cycle-Detection/`](04-Cycle-Detection/).

---

## What's Next

This module covers linked lists in four sub-modules:

1. [`01-SLL/`](01-SLL/) — singly linked list: implementation, operations,
   plus reverse and nth-from-end problems.
2. [`02-DLL/`](02-DLL/) — doubly linked list, and the canonical DLL
   use case: the LRU cache (LC #146).
3. [`03-Circular-LL/`](03-Circular-LL/) — circular variants.
4. [`04-Cycle-Detection/`](04-Cycle-Detection/) — Floyd's algorithm and
   the Find Duplicate Number problem (LC #287).

See [`interview-questions.md`](interview-questions.md) for a
cheatsheet of the conceptual questions that come up in interviews.
