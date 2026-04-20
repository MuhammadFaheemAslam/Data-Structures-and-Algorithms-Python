# Python Tuple – Theory

## Introduction

The Python `tuple` is an ordered, **immutable** collection of elements. It looks and behaves a lot like a list at first glance — 
you can index, slice, and iterate through it — but once created, its contents cannot be changed. This single property 
(immutability) unlocks a number of important guarantees: tuples are **hashable** (when their elements are), they can 
serve as **dictionary keys** or **set members**, and the interpreter can optimise them more aggressively than lists.

In this document, we’ll explore how tuples work, how they differ from lists, their time complexities, memory behaviour, 
and when you should reach for a tuple instead of a list.

---

## Underlying Implementation

Like lists, Python tuples are internally **contiguous arrays of pointers** to Python objects. The key difference is that 
a tuple’s size is **fixed at creation time** — there is no capacity/size distinction and no dynamic resizing logic. 
This makes tuples slightly smaller and faster to construct than equivalent lists.

### No Resizing, No Mutation

Because tuples cannot grow, shrink, or have their elements replaced, CPython can:

1. Allocate exactly as much memory as needed — no over‑allocation buffer.
2. Skip the bookkeeping required for mutation (no `insert`, `append`, `pop`, `__setitem__`, etc.).
3. **Cache and reuse** small tuples internally (CPython keeps a free list of short tuples to speed up allocation).
4. Treat tuple literals of constant values as **compile‑time constants** (peephole optimisation / constant folding).

> **Note:** “Immutable” means the tuple object itself cannot be modified. If a tuple contains a **mutable** object 
> (like a list), that inner object can still be mutated. The tuple’s identity and structure don’t change — only the 
> contents of the nested object do. This is also why a tuple containing a list is **not hashable**.

---

## Key Characteristics

| Property           | Description                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| **Ordered**        | Elements maintain insertion order.                                          |
| **Immutable**      | Cannot be changed after creation — no add, remove, or reassign.             |
| **Heterogeneous**  | Can contain elements of different types (including other tuples/lists).     |
| **Allows duplicates** | Same value can appear multiple times.                                    |
| **Indexable**      | Access any element in O(1) time via `tup[i]`.                               |
| **Iterable**       | Supports iteration, comprehension (via generators), and unpacking.          |
| **Hashable**       | If all elements are hashable, the tuple itself is hashable.                 |

---

## Creating Tuples

```python
empty = ()
single = (42,)              # note the trailing comma – without it, this is just an int in parens
pair = (1, 2)
mixed = (1, "hello", 3.14)
from_iter = tuple([1, 2, 3])
packed = 1, 2, 3            # parentheses are optional – the comma makes the tuple
```

> **Common pitfall:** `(42)` is **not** a tuple — it is just the integer `42` wrapped in parentheses. 
> For a single‑element tuple you must write `(42,)`.

---

## Common Operations and Their Complexities

Tuples support the same **read‑only** operations as lists. A detailed analysis is available in 
[`time-complexity.md`](time-complexity.md).

| Operation                     | Time Complexity | Notes                                                         |
|-------------------------------|-----------------|---------------------------------------------------------------|
| Indexing (`tup[i]`)           | O(1)            | Direct access to the underlying array.                        |
| Slice (`tup[i:j]`)            | O(k)            | Creates a new tuple with k = j‑i elements.                    |
| Length (`len(tup)`)           | O(1)            | Size is stored as an attribute.                               |
| Contains (`x in tup`)         | O(n)            | Linear scan until element found.                              |
| Count (`tup.count(x)`)        | O(n)            | Counts occurrences of `x`.                                    |
| Index of (`tup.index(x)`)     | O(n)            | Returns the first position of `x`; raises `ValueError` if absent. |
| Concatenation (`t1 + t2`)     | O(n + m)        | Creates a **new** tuple; inputs are untouched.                |
| Repetition (`tup * k`)        | O(n · k)        | Creates a new tuple by repeating the contents.                |
| Iteration                     | O(n)            | Standard for‑loop traversal.                                  |
| Hashing (`hash(tup)`)         | O(n)            | Combines the hashes of all elements.                          |
| Unpacking (`a, b, c = tup`)   | O(n)            | Assigns each element to a target.                             |

There are **no** `append`, `insert`, `remove`, `pop`, `sort`, or `reverse` methods — because mutation is disallowed. 
If you need a sorted version of a tuple, use `sorted(tup)`, which returns a **list**. Convert back with `tuple(sorted(tup))` 
if you need a tuple.

---

## Memory Usage

- A tuple has slightly less overhead than a list of the same length — no spare capacity, no resize metadata.
- The underlying array stores exactly `n` pointers; each pointer is 8 bytes on 64‑bit systems.
- CPython’s free list reuses short tuple allocations, making tuple creation cheap in tight loops.
- As with lists, the tuple only holds **references** to its elements; the elements themselves live elsewhere in memory.

In practice, for small collections, tuples are measurably faster to construct and iterate than lists, and use less memory.

---

## Tuples vs Lists

| Aspect                | Tuple                                      | List                                    |
|-----------------------|--------------------------------------------|-----------------------------------------|
| Mutability            | Immutable                                  | Mutable                                 |
| Syntax                | `(1, 2, 3)` or `1, 2, 3`                   | `[1, 2, 3]`                             |
| Hashable              | Yes (if all elements are hashable)         | No                                      |
| Usable as dict key    | Yes                                        | No                                      |
| Memory overhead       | Lower                                      | Higher (over‑allocation buffer)         |
| Creation speed        | Faster                                     | Slower                                  |
| Use case              | Fixed records, heterogeneous grouping      | Growing/shrinking homogeneous data      |

A useful rule of thumb from the Python community:

> **Lists are for homogeneous data of variable length.**  
> **Tuples are for heterogeneous records of fixed structure.**

For example, a list of user objects is a list; a single user record `(id, name, email)` is a tuple.

---

## When to Use (and Not Use) Tuples

✅ **Good use cases:**

- Returning **multiple values** from a function (`return x, y, z` implicitly returns a tuple).
- Representing a **fixed record** — e.g., an `(x, y)` coordinate, an `(r, g, b)` colour, a database row.
- Using a collection as a **dictionary key** or **set element**.
- Defining **constants** or **configuration** that should never change.
- Packing/unpacking data in parallel assignment: `a, b = b, a`.

❌ **Avoid when:**

- You need to **add, remove, or replace** elements over time — use a list.
- You need methods like `sort`, `reverse`, `append` — use a list.
- The collection represents a growing sequence of similar items — use a list.

---

## Code Example (Quick Overview)

```python
# Creating tuples
empty = ()
single = (42,)
point = (3, 4)
record = ("alice", 30, "engineer")

# Indexing and slicing
print(point[0])          # 3
print(record[1:])        # (30, 'engineer')

# Unpacking
x, y = point             # x = 3, y = 4
name, age, role = record

# Swapping without a temp variable
a, b = 1, 2
a, b = b, a              # a = 2, b = 1

# Returning multiple values from a function
def min_max(xs):
    return min(xs), max(xs)

lo, hi = min_max([3, 1, 4, 1, 5])

# Using a tuple as a dict key
locations = {}
locations[(40.71, -74.00)] = "New York"
locations[(34.05, -118.24)] = "Los Angeles"

# Iteration and membership
for value in record:
    print(value)

if "alice" in record:
    print("found")

# Tuple containing a mutable object – careful!
t = (1, 2, [3, 4])
t[2].append(5)           # allowed: the list inside can mutate
# t[2] = [9]             # NOT allowed: cannot reassign a tuple slot
```

For a more thorough demonstration of each operation, see [`operations.py`](operations.py).
