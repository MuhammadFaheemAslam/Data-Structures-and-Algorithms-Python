# Python Set – Time & Space Complexity

This document is a deeper companion to [`theory.md`](theory.md). It walks through each
operation, explains **why** it has the complexity it does, and flags the edge cases that
turn a clean O(1) into a surprise O(n).

Throughout the document, `n = len(s)` unless stated otherwise.

---

## Why Sets Are Fast: The 30-Second Version

A Python set is a **hash table**. For any element `x`:

1. `hash(x)` is computed — this is (usually) O(1).
2. The hash picks a slot in the internal array.
3. The element in that slot is compared to `x` with `==`.

If the hash is good, every operation that touches a single element reduces to:
**one hash + one comparison = O(1) average.**

The "average" qualifier matters because:
- Hash collisions force Python to probe neighbouring slots.
- Adversarial or pathological inputs can make every operation degrade to O(n).
- Resizing the underlying table is itself O(n), though it happens rarely enough that
  the **amortized** cost stays O(1).

For normal data, you can treat membership, add, and remove as O(1) with confidence.

---

## Per-Operation Complexity

### Creation

| Expression                  | Time     | Space   | Notes                                        |
|-----------------------------|----------|---------|----------------------------------------------|
| `set()`                     | O(1)     | O(1)    | Empty set.                                   |
| `{1, 2, 3}` (literal)       | O(k)     | O(k)    | k = number of literal elements.              |
| `set(iterable)`             | O(k)     | O(k)    | k = len(iterable). Each element is hashed.   |
| `{x for x in iterable}`     | O(k)     | O(k)    | Set comprehension; same cost as `set(...)`.  |
| `s.copy()` or `set(s)`      | O(n)     | O(n)    | Shallow copy — references, not deep clones.  |

> **Pitfall:** `{}` is an empty **dict**, not a set. Use `set()` for an empty set.

---

### Membership: `x in s`

**Complexity:** O(1) average, O(n) worst case.

This is the whole reason sets exist. Compare:

| Structure     | `x in ?`    |
|---------------|-------------|
| list / tuple  | O(n) scan   |
| **set / dict**| **O(1) avg**|

The worst case kicks in only if many elements collide on the same hash bucket, which
requires either adversarial input or a terrible `__hash__` method. For normal data,
treat it as O(1).

**Pitfall — `hash()` itself isn't always O(1):**
- Hashing an `int` or a short `str` is effectively O(1).
- Hashing a long `str` or a large `tuple` is **O(k)** where k is the element's size,
  because every character / sub-element contributes to the hash.

So for strings of length k, `s in big_set` is O(k), not O(1). For small strings this
never matters; for, say, long DNA sequences it can.

---

### Add / Remove / Discard / Pop

| Operation        | Time (avg) | Time (worst) | Notes                                            |
|------------------|------------|--------------|--------------------------------------------------|
| `s.add(x)`       | O(1)       | O(n)         | Amortized O(1). May trigger resize.             |
| `s.remove(x)`    | O(1)       | O(n)         | Raises `KeyError` if `x` absent.                |
| `s.discard(x)`   | O(1)       | O(n)         | Silently no-op if `x` absent.                   |
| `s.pop()`        | O(1)       | O(n)         | Removes & returns an **arbitrary** element.     |
| `s.clear()`      | O(n)       | O(n)         | Frees all slots.                                |

**Why amortized O(1) on `add`:** when the load factor exceeds ~2/3, the set allocates
a larger table and rehashes every element. That resize is O(n), but it happens on
roughly every doubling of size, so over a long sequence of adds the total work stays
proportional to n → **O(1) per add on average.**

**Pitfall — `pop()` order is arbitrary.** It's not FIFO, not LIFO — it's "whatever the
first non-empty slot is." Don't use `pop()` expecting specific ordering.

---

### Set Algebra

For two sets `a` (size `n`) and `b` (size `m`):

| Operation                       | Time               | Space              | Why                                                              |
|---------------------------------|--------------------|--------------------|------------------------------------------------------------------|
| `a \| b` — union                | O(n + m)           | O(n + m)           | Must visit every element of both sets.                           |
| `a & b` — intersection          | **O(min(n, m))**   | O(min(n, m))       | Iterate the **smaller** set; look up each in the larger.         |
| `a - b` — difference            | O(n)               | O(n)               | Iterate `a`; include elements not found in `b`.                  |
| `a ^ b` — symmetric difference  | O(n + m)           | O(n + m)           | Must consider every element of both.                             |
| `a <= b` — subset               | O(n)               | O(1)               | Iterate `a`; each lookup in `b` is O(1).                         |
| `a >= b` — superset             | O(m)               | O(1)               | Symmetric to subset.                                              |
| `a.isdisjoint(b)`               | O(min(n, m))       | O(1)               | Stops at the first shared element.                               |

**Key insight — intersection is O(min(n, m)), not O(n + m):**
Python iterates the smaller set and checks membership in the larger. That's why
intersecting a 10-element set with a 10-million-element set is fast.

**In-place variants are cheaper in space:**
`a |= b` updates `a` in place, avoiding the O(n + m) extra allocation for a new set.
Time complexity is the same; memory is lower.

---

### Iteration

| Operation            | Time | Space | Notes                                             |
|----------------------|------|-------|---------------------------------------------------|
| `for x in s:`        | O(n) | O(1)  | Order is implementation-defined.                  |
| `len(s)`             | O(1) | O(1)  | Stored as an attribute on the set object.         |
| `max(s)` / `min(s)`  | O(n) | O(1)  | Must scan every element.                          |
| `sum(s)`             | O(n) | O(1)  | Same.                                             |
| `sorted(s)`          | O(n log n) | O(n) | Returns a **new list** — sets can't be sorted in place. |

**Pitfall — never rely on iteration order.** Even across two runs of the same script,
small changes to hash seeds or insertion order can produce different output orders.

---

## `frozenset`

`frozenset` has the same read-side complexities as `set`:

| Operation                    | Time    |
|------------------------------|---------|
| `x in fs`                    | O(1) avg|
| `fs1 \| fs2`, `&`, `-`, `^`  | Same as set |
| `hash(fs)`                   | O(n) — combines hashes of every element |

It does not support `add`, `remove`, `update`, or any of the in-place variants.
The tradeoff: **no mutation, but now it's hashable** — so a `frozenset` can live
inside another `set` or act as a `dict` key.

---

## Space Complexity Summary

A set uses **more memory per element than a list** because it pre-allocates its
hash table with headroom (kept below ~2/3 full).

- A list of `n` pointers stores roughly `n` slots plus a small over-allocation buffer.
- A set of `n` elements stores roughly `1.5n` to `2n` slots (empty slots count as used memory).

This is the fundamental trade: you spend memory to buy O(1) membership. For most
workloads, it is a great deal.

---

## Worst-Case Corner Cases

These are rare in practice but worth knowing:

1. **Hash collisions (adversarial data).** If every element hashes to the same bucket,
   every operation degrades to O(n). CPython's string hashing has randomization on by
   default to prevent this attack.

2. **Hashing expensive objects.** A set of long strings or large tuples pays an O(k)
   hashing cost per operation, where k is the size of the element. Still effectively
   O(1) in `n`, but the constant factor is large.

3. **Iterating while mutating.** Adding or removing elements during iteration raises
   `RuntimeError: Set changed size during iteration`. It's not a complexity issue —
   it's an outright bug.

4. **`__hash__` inconsistent with `__eq__`.** Custom classes that override `__eq__`
   but not `__hash__` (or vice versa) will silently misbehave: duplicate-looking
   objects can coexist in a set, or lookups can return `False` for equal objects.

---

## Complexity Decision Table

Use this to pick the right tool:

| Question                                       | Structure              | Cost      |
|------------------------------------------------|------------------------|-----------|
| "Does this collection contain X?"              | **set** / **dict**     | O(1) avg  |
| "What are the unique elements of this list?"   | **set**                | O(n)      |
| "What do these two collections have in common?"| **set intersection**   | O(min(n, m)) |
| "Is collection A fully contained in B?"        | **set subset**         | O(|A|)    |
| "Give me the element at index 5"               | **list** / **tuple**   | O(1)      |
| "Preserve insertion order of unique elements"  | **dict** (as ordered set) | O(n)   |
| "Store a set inside another set"               | **frozenset**          | —         |

---

## Further Reading

- [`operations.py`](operations.py) — runnable examples of every operation listed here.
- [`Problems/`](Problems/) — practice problems where set-based solutions turn O(n²)
  brute-force approaches into O(n).
- Python docs: [Set Types — set, frozenset](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset)
- Python Time Complexity wiki: [wiki.python.org/moin/TimeComplexity](https://wiki.python.org/moin/TimeComplexity)
