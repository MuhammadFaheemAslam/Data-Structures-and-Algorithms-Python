# Python Set – Theory

## Introduction

The Python `set` is an **unordered** collection of **unique**, **hashable** elements. 
Where a list is "a sequence of things" and a tuple is "a fixed record", a set answers a very different question:

> *"Given a bag of values, which ones are distinct, and does X appear in it?"*

Sets are built on the same hash‑table machinery that powers dictionaries. That gives them **average O(1)** membership 
testing, insertion, and removal — dramatically faster than the O(n) scans you'd need with a list. In exchange, you give 
up two things: **order** (sets don't remember insertion order) and the ability to store **unhashable** elements 
(like lists or other sets).

In this document we'll cover how sets work under the hood, their time complexities, their algebraic operations 
(union, intersection, difference), and when to reach for a set instead of a list or dict.

---

## Underlying Implementation

A Python set is a **hash table** of element slots. When you add an element `x`:

1. Python computes `hash(x)`.
2. The hash selects a slot in the underlying array.
3. If the slot is empty, `x` is stored there.
4. If the slot is full (a **collision**), Python **probes** neighbouring slots using an open‑addressing scheme 
   until it finds an empty one.

Lookups (`x in s`) work the same way: hash, jump to the slot, and compare. On average this is **O(1)**, 
regardless of how many elements the set already holds.

### Why Elements Must Be Hashable

For a set to find an element in O(1), it must be able to compute `hash(element)`. This means:

- Immutable types (`int`, `float`, `str`, `tuple` of hashables, `frozenset`, …) work as set members.
- Mutable types (`list`, `dict`, `set`) are **not** hashable and cannot be stored in a set.

```python
{1, 2, 3}             # OK
{(1, 2), (3, 4)}      # OK – tuples are hashable
{[1, 2], [3, 4]}      # TypeError: unhashable type: 'list'
```

### Dynamic Resizing

Like lists, sets resize as they grow. CPython keeps the **load factor** (fraction of slots filled) below ~2/3 to 
keep probe chains short. When the table fills past that threshold, it is resized to a larger table and all existing 
elements are **rehashed** into the new array.

This resize is O(n), but it happens rarely. The **amortized** cost of `add` / `remove` / `in` stays O(1).

> **Note:** Because items are stored based on their hash, iteration order is **not** the order in which they were 
> inserted (unlike `dict`, which *does* preserve insertion order since Python 3.7). Never write code that depends on 
> set iteration order.

---

## Key Characteristics

| Property                 | Description                                                                  |
|--------------------------|------------------------------------------------------------------------------|
| **Unordered**            | No index, no insertion order guarantee.                                     |
| **Unique elements**      | Duplicates are automatically discarded.                                      |
| **Mutable**              | You can add and remove elements after creation.                              |
| **Elements must be hashable** | Lists, dicts, and other sets cannot be members.                        |
| **Iterable**             | Supports `for`, comprehensions, and set‑algebra operators.                   |
| **Not indexable**        | `s[0]` raises `TypeError`.                                                   |
| **Not hashable itself**  | A set can't be an element of another set. Use `frozenset` for that.         |

---

## Creating Sets

```python
empty = set()                 # NOT {} – that's an empty dict!
numbers = {1, 2, 3, 4}
from_iter = set([1, 2, 2, 3]) # {1, 2, 3} – duplicates dropped
from_string = set("hello")    # {'h', 'e', 'l', 'o'}
comp = {x * x for x in range(5)}  # set comprehension -> {0, 1, 4, 9, 16}
frozen = frozenset([1, 2, 3]) # immutable, hashable variant
```

> **Common pitfall:** `{}` is an **empty dict**, not an empty set. To create an empty set, use `set()`.

---

## Common Operations and Their Complexities

A detailed analysis is available in [`time-complexity.md`](time-complexity.md).

| Operation                      | Time Complexity | Notes                                                 |
|--------------------------------|-----------------|-------------------------------------------------------|
| Membership (`x in s`)          | O(1) average    | Hash + slot check. **This is the set's superpower.**  |
| Add (`s.add(x)`)               | O(1) average    | May trigger a resize (amortized O(1)).                |
| Remove (`s.remove(x)`)         | O(1) average    | Raises `KeyError` if `x` is absent.                   |
| Discard (`s.discard(x)`)       | O(1) average    | Like `remove`, but silently does nothing if absent.   |
| Pop (`s.pop()`)                | O(1) average    | Removes and returns an **arbitrary** element.         |
| Length (`len(s)`)              | O(1)            | Size is stored as an attribute.                       |
| Union (`a \| b`)               | O(len(a) + len(b)) | New set with all elements from both.               |
| Intersection (`a & b`)         | O(min(len(a), len(b))) | Iterates the smaller set.                      |
| Difference (`a - b`)           | O(len(a))       | Elements in `a` not in `b`.                           |
| Symmetric difference (`a ^ b`) | O(len(a) + len(b)) | Elements in exactly one of the two.                |
| Subset / superset (`a <= b`)   | O(len(a))       | Checks every element of `a` against `b`.              |
| Iteration                      | O(n)            | Order is **not** guaranteed.                          |
| Copy (`s.copy()`)              | O(n)            | Shallow copy.                                         |

---

## Set Algebra

One of the most useful things about Python sets is that they support mathematical set operations directly.

| Operator | Method                     | Meaning                                                |
|----------|----------------------------|--------------------------------------------------------|
| `a \| b` | `a.union(b)`               | Everything in `a` or `b` (or both).                    |
| `a & b`  | `a.intersection(b)`        | Elements that appear in BOTH.                          |
| `a - b`  | `a.difference(b)`          | Elements in `a` but NOT in `b`.                        |
| `a ^ b`  | `a.symmetric_difference(b)`| In exactly one of the two (XOR).                       |
| `a <= b` | `a.issubset(b)`            | Every element of `a` is in `b`.                        |
| `a >= b` | `a.issuperset(b)`          | Every element of `b` is in `a`.                        |
| `a.isdisjoint(b)` | —                 | `True` if `a` and `b` share no elements.               |

The operator forms (`|`, `&`, …) require both operands to be sets. The method forms accept any iterable:

```python
{1, 2, 3}.union([3, 4, 5])    # {1, 2, 3, 4, 5} – list is fine
{1, 2, 3} | [3, 4, 5]         # TypeError – both sides must be sets
```

---

## `set` vs `frozenset`

Python has two set types:

| Type        | Mutable? | Hashable? | Can be a set element / dict key? |
|-------------|----------|-----------|----------------------------------|
| `set`       | Yes      | No        | No                               |
| `frozenset` | No       | Yes       | Yes                              |

Use `frozenset` when you need a set that itself needs to be stored in another set or used as a dict key — 
for example, representing a group of users as a single hashable token.

---

## Memory Usage

- A set pre‑allocates a hash table larger than the number of elements (to keep the load factor low).
- Because of that extra headroom, a set uses **more memory per element than a list**.
- The set only holds **references**; the elements themselves live elsewhere in memory.

The tradeoff is explicit: you spend memory to buy O(1) membership testing. For membership‑heavy workloads this 
trade is almost always worth it.

---

## Sets vs Lists vs Dicts

| Aspect                | List                         | Set                          | Dict                          |
|-----------------------|------------------------------|------------------------------|-------------------------------|
| Ordered?              | Yes                          | No                           | Yes (insertion order)         |
| Allows duplicates?    | Yes                          | No                           | Keys unique, values any       |
| Membership cost       | O(n)                         | **O(1) average**             | **O(1) average** (on keys)    |
| Element requirements  | Any                          | Hashable                     | Hashable keys, any values     |
| Typical use           | Ordered sequence             | "Is X present?" / de‑dup     | Key → value lookup            |

Rule of thumb:

> **Use a list when order matters.**  
> **Use a set when only presence/uniqueness matters.**  
> **Use a dict when you need to associate a value with each key.**

---

## When to Use (and Not Use) Sets

✅ **Good use cases:**

- Fast membership testing: "Have I seen this user before?"
- **Deduplicating** a collection: `list(set(items))` (drops order).
- **Set algebra:** shared tags between posts, items in one list but not another, etc.
- Tracking "visited" nodes during graph/BFS/DFS traversal.
- Converting an O(n²) nested‑loop search into an O(n) one by pre‑building a lookup set.

❌ **Avoid when:**

- You need to preserve **insertion order** — use a list (or a dict as an ordered set).
- You need to **index** into the collection — `s[0]` doesn't work.
- Your elements are **unhashable** (lists, dicts, mutable objects) — convert them to tuples / frozensets first.
- You need to store **duplicates** or count occurrences — use `list` or `collections.Counter`.

---

## Code Example (Quick Overview)

```python
# Creating sets
empty = set()
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

# Adding and removing
a.add(5)
a.discard(99)     # no error even if 99 isn't there
a.remove(1)       # KeyError if 1 isn't there

# Membership – the headline feature
if 3 in a:
    print("found")

# Set algebra
print(a | b)      # union
print(a & b)      # intersection
print(a - b)      # difference
print(a ^ b)      # symmetric difference

# Deduplication idiom
items = [1, 2, 2, 3, 3, 3, 4]
unique = list(set(items))   # order not preserved

# Set comprehension
squares = {x * x for x in range(6)}

# Iteration (order NOT guaranteed)
for value in a:
    print(value)

# frozenset – a hashable, immutable set
tags = frozenset({"python", "dsa"})
cache_key = {tags: "result"}   # frozenset can be a dict key
```

For a more thorough demonstration of each operation, see [`operations.py`](operations.py).
