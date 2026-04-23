# Linked List — Interview Questions

A cheatsheet of the conceptual questions that come up alongside the
coding problems in this module. If you can answer each fluently, you're
prepared for any linked-list interview.

---

## 🧠 Conceptual Questions

### 1. What's the fundamental tradeoff between arrays and linked lists?

- **Array**: contiguous memory → O(1) random access, O(n) middle insert.
- **Linked list**: chained nodes → O(1) middle insert given a node
  reference, O(n) random access.

In practice, arrays win almost always due to **cache locality**.
Linked lists win narrowly — specifically when:
- You need O(1) insert/delete at known positions AND
- Sequential traversal is fine (no random access needed).

### 2. When does a linked list beat an array in real code?

Four main places:
1. **LRU caches** — hash map + DLL combo gives O(1) get, put, evict.
2. **Allocators / free lists** — free blocks chained without moving them.
3. **Adjacency lists in graphs** — edges chained naturally as "next."
4. **Undo/redo histories** — cheap to insert/remove at either end.

### 3. Singly vs doubly — when do you need DLL?

Use DLL when:
- You need to **delete a node given only a reference to it** in O(1).
  (On SLL, you'd need to walk to find the predecessor.)
- You need **bidirectional traversal**.
- You're building an LRU cache or similar where "move to front"
  must be O(1).

Otherwise, SLL saves one pointer per node.

### 4. Why do linked lists have poor cache behaviour?

Array elements sit contiguously in memory — when you access `arr[i]`,
the CPU typically loads a cache line that includes `arr[i+1]`, `arr[i+2]`,
etc. **Next access is free.**

Linked list nodes are scattered across the heap — each `.next` pointer
hop is a fresh memory lookup, likely missing the cache. So even though
both structures are O(n) for a full traversal, the array is often
**10× faster** in practice.

### 5. How do you reverse a singly-linked list in O(1) space?

Three pointers: `prev`, `curr`, `next`. Walk the list, flipping each
link:

```python
prev = None
curr = head
while curr:
    nxt = curr.next
    curr.next = prev
    prev = curr
    curr = nxt
return prev
```

This is the canonical linked-list primitive. You should be able to
write it from memory in under a minute.

### 6. What's the dummy-head pattern and why is it useful?

A sentinel node placed before the real head:

```
dummy → head → node1 → node2 → ...
```

Benefits:
- **No special case for empty list** — `dummy.next = head` works even
  when head is None.
- **No special case for deleting the first node** — every real node
  has a predecessor (dummy).
- **Uniform insertion logic** — "insert after predecessor" works at
  index 0 (dummy is the predecessor).

Heavily used in reverse, merge, remove-nth-from-end, and any other
problem that might modify the head.

### 7. Explain Floyd's cycle-detection algorithm.

Two pointers starting at the head:
- **slow**: advances 1 step at a time.
- **fast**: advances 2 steps at a time.

If there's a cycle, fast eventually "laps" slow and they meet inside
the cycle. If no cycle, fast reaches None first.

To find the cycle's **start**, reset one pointer to head after the
meeting. Advance both at speed 1 — they meet at the cycle entrance.
(Why? Math — see `04-Cycle-Detection/floyd-algorithm.py`.)

### 8. How do you find the middle of a linked list in one pass?

Fast-slow pointers at speeds 2 and 1. When fast reaches the end,
slow is at the middle.

```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
return slow
```

Same trick as Floyd's, different goal.

### 9. How do you find the nth-from-end node in one pass?

**Two-pointer gap trick**: advance `fast` n steps ahead, then move
both pointers together. When fast reaches the end, slow is n steps
behind = the nth-from-end node.

```python
fast = head
for _ in range(n):
    fast = fast.next
slow = head
while fast:
    slow = slow.next
    fast = fast.next
return slow.val
```

### 10. How do you implement an LRU cache with O(1) operations?

**Hash map + doubly-linked list**:
- **Hash map**: `key → DLL node` for O(1) lookup.
- **DLL**: head is most-recent, tail is least-recent.
- On `get(key)`: if present, move the node to head. O(1).
- On `put(key, val)`: if at capacity, evict the tail. Insert new node at head. O(1).

The DLL's "remove a node given a reference in O(1)" is what makes
this work. See `02-DLL/problems/lru-cache.py`.

---

## 💼 Common Coding Questions

### SLL Basics

- **Reverse a linked list** (LC #206) — `01-SLL/problems/reverse.py`
- **Merge two sorted lists** (LC #21) — `01-SLL/operations.py` (`merge_sorted`)
- **Remove nth from end** (LC #19) — `01-SLL/problems/nth-from-end.py`
- **Middle of the linked list** (LC #876) — `01-SLL/operations.py` (`middle_node`)
- **Remove duplicates from sorted list** (LC #83) — `01-SLL/operations.py`

### Two-Pointer Tricks

- **Linked List Cycle** (LC #141) — `04-Cycle-Detection/has-cycle.py`
- **Linked List Cycle II** (LC #142) — `04-Cycle-Detection/cycle-start.py`
- **Happy Number** (LC #202) — Floyd's on a function iteration (Phase-02 / 02 / 06)
- **Find the Duplicate Number** (LC #287) — `04-Cycle-Detection/problems/duplicate-number.py`
- **Palindrome Linked List** (LC #234) — find middle, reverse second half, compare

### Advanced

- **Reverse Nodes in K-Group** (LC #25) — `01-SLL/problems/reverse.py`
- **Reverse Linked List II** (LC #92) — `01-SLL/problems/reverse.py` (`reverse_between`)
- **LRU Cache** (LC #146) — `02-DLL/problems/lru-cache.py`
- **Sort List** (LC #148) — Phase-03 / 02 / 02 / 01-Merge-Sort / problems / sort-linkedlist.py
- **Copy List with Random Pointer** (LC #138) — hash map or interleave trick

### Cyclic / Circular Structures

- **Josephus Problem** — `03-Circular-LL/implementation.py`
- **Rotate List** (LC #61) — connect tail to head, find new tail, break

---

## 🎯 Things to Ask Before Answering

1. **Singly or doubly linked?** Changes what's O(1) vs O(n).
2. **Is there a cycle?** If possible, you need Floyd's or a hash set.
3. **Can I modify the list in place?** Some problems forbid it.
4. **Does the list have a tail pointer / size counter?** Changes complexity.
5. **Is the list sorted?** Enables merge techniques.
6. **Are there duplicates / negative values?** Affects some traversals.
7. **Can nodes be None (empty list)?** Always handle this first.

---

## 🧠 Mental Models Worth Keeping

### "Dummy head for anything that touches the head"

If your solution might remove, reverse, or replace the head node,
add a dummy head. Your code gets shorter and more uniform.

### "Two pointers at different speeds"

Fast/slow at 2:1 speed ratio detects cycles and finds middles.
Fixed gap of n steps finds the nth-from-end node.

### "The array-as-linked-list trick"

Any array of integers in range [1, n] can be treated as a function
graph, which turns cycle-related algorithms into array-only problems
(LC #287, LC #202).

### "Always save a reference before you might lose it"

Before `curr.next = something`, ask: do I still need `curr.next` as
it was? If yes, save it first.

### "Reverse → do stuff → reverse back"

For problems that need backward processing on an SLL, sometimes it's
cheaper to reverse the list, process forward, and reverse back —
three O(n) passes total. Especially useful when you can't afford
the O(n) space of a stack.

---

## ⚡ Speed Round

- **Reverse?** → three-pointer walk (prev, curr, next).
- **Middle?** → fast-slow at 2:1.
- **Cycle?** → Floyd's (2:1 speed).
- **Cycle start?** → Floyd's + reset slow to head.
- **Nth from end?** → fast pointer n steps ahead, then walk together.
- **LRU cache?** → hash map + DLL.
- **Merge two sorted?** → dummy head + two-pointer merge.
- **Palindrome?** → find middle, reverse second half, compare.
- **Delete a node given only that node?** → copy next's value, skip next.

---

## Next Up

With linked lists done, the next module is **04-Stack**. Stacks build
naturally on top of lists (or linked lists) — push/pop at one end,
LIFO semantics. You'll revisit the parentheses-matching stack you saw
in `02-String/problems/parentheses.py` and meet more stack classics
(min-stack, stock span, infix/postfix conversion).
