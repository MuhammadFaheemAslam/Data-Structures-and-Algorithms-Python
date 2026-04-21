# Python Dictionary – Theory

## Introduction

The Python `dict` is the workhorse of the language. It is an **ordered** collection of 
**key → value** pairs where every key must be **unique** and **hashable**. Internally, 
CPython itself is built on top of dicts — modules, classes, and object attributes are 
all stored in dictionaries under the hood — so any performance characteristic a dict has, 
Python as a whole has.

If a list answers *"what's at position i?"* and a set answers *"is X present?"*, a dict 
answers the most general question of the three:

> *"Given this key, what value is associated with it?"*

Dicts are built on the same hash‑table machinery that powers sets. That gives them 
**average O(1)** lookup, insertion, and deletion — the same constant‑time magic, but now 
you get to attach an arbitrary value to each key instead of just tracking presence.

In this document we'll cover how dicts work under the hood, their time complexities, the 
modern (3.7+) insertion‑order guarantee, and when a dict is the right tool versus a list 
or a set.

---

## Underlying Implementation

A Python dict is a **hash table**. Conceptually, each entry is a `(hash, key, value)` 
triple stored at a slot chosen by the key's hash. When you do `d[k] = v`:

1. Python computes `hash(k)`.
2. The hash selects a slot in the underlying array.
3. If the slot is empty, the triple is written there.
4. If the slot is full (a **collision**), Python probes neighbouring slots using an 
   open‑addressing scheme until it finds an empty one or an existing entry with the same key.

Lookups (`d[k]`, `k in d`) work identically: hash, jump to the slot, compare keys with `==`. 
On average this is **O(1)**, regardless of how many entries the dict already holds.

### Insertion-Order Preservation (CPython 3.6 / Python 3.7+)

Since Python 3.7 it is a **language guarantee** that dicts iterate in insertion order. 
Internally CPython splits a dict into two arrays:

1. A **sparse hash table** of slot indices (for O(1) lookup).
2. A **dense array of entries** in insertion order (for predictable iteration).

This design is often called the "compact dict." It saves memory compared to older 
implementations and — as a useful side effect — gives you ordered iteration for free.

> **Note:** Order preservation applies to iteration (`for k in d`, `d.keys()`, 
> `d.values()`, `d.items()`) and to `dict`'s view objects. It does **not** affect the 
> ordering of equality comparisons: `{"a": 1, "b": 2} == {"b": 2, "a": 1}` is `True`.

### Why Keys Must Be Hashable

For the O(1) lookup trick to work, Python must be able to compute `hash(key)`. This means:

- Immutable types (`int`, `float`, `str`, `tuple` of hashables, `frozenset`, …) work as keys.
- Mutable types (`list`, `dict`, `set`) are **not** hashable and cannot be keys.

```python
{"alice": 30, ("x", "y"): "point"}     # OK
{[1, 2]: "bad"}                        # TypeError: unhashable type: 'list'
```

Values, on the other hand, can be *anything* — lists, other dicts, functions, custom 
objects, whatever you need.

### Dynamic Resizing

Like sets, dicts resize to keep the load factor low (roughly below 2/3). A resize is O(n) 
because every entry must be rehashed into the new, larger table, but resizes are rare 
enough that the **amortized** cost of insertion stays O(1).

---

## Key Characteristics

| Property                      | Description                                                                  |
|-------------------------------|------------------------------------------------------------------------------|
| **Ordered**                   | Iterates in insertion order (Python 3.7+).                                   |
| **Unique keys**               | Re-assigning an existing key overwrites the old value.                       |
| **Mutable**                   | Keys and values can be added, changed, and removed after creation.           |
| **Keys must be hashable**     | Lists, dicts, and other sets cannot be keys.                                 |
| **Values can be anything**    | No restriction on value types.                                               |
| **Iterable**                  | Iterating a dict yields its **keys** by default.                             |
| **Not indexable by position** | `d[0]` looks up the key `0`, not the first item.                             |

---

## Creating Dictionaries

```python
empty = {}                             # empty dict
scores = {"alice": 90, "bob": 85}      # literal
pairs  = dict(alice=90, bob=85)        # keyword form (keys must be valid identifiers)
from_pairs = dict([("a", 1), ("b", 2)])# from an iterable of key/value tuples
zipped = dict(zip(["a", "b"], [1, 2])) # zip two parallel iterables
comp = {x: x * x for x in range(5)}    # dict comprehension
```

> **Common pitfall:** `{}` is an **empty dict**, not an empty set. To create an empty 
> set, use `set()`.

---

## Accessing Values

Python gives you three ways to get a value. They behave differently when the key is missing:

| Form                | Missing-key behavior                          | When to use                          |
|---------------------|-----------------------------------------------|--------------------------------------|
| `d[k]`              | Raises `KeyError`                             | The key MUST exist.                  |
| `d.get(k)`          | Returns `None`                                | Missing is expected; None is fine.   |
| `d.get(k, default)` | Returns `default`                             | Missing is expected; want a fallback.|
| `d.setdefault(k, v)`| Inserts `v` if missing, returns existing value| Lazy-initialize a key.              |

```python
d = {"a": 1}
d["a"]                 # 1
d["b"]                 # KeyError
d.get("b")             # None – no exception
d.get("b", 0)          # 0
d.setdefault("b", 0)   # 0 (and now d == {"a": 1, "b": 0})
```

---

## Common Operations and Their Complexities

| Operation                     | Time Complexity | Notes                                                 |
|-------------------------------|-----------------|-------------------------------------------------------|
| Access (`d[k]`)               | O(1) average    | Hash + slot compare.                                  |
| Assignment (`d[k] = v`)       | O(1) average    | May trigger a resize (amortized O(1)).                |
| Delete (`del d[k]`)           | O(1) average    | Raises `KeyError` if `k` absent.                      |
| Membership (`k in d`)         | O(1) average    | Only checks KEYS, not values.                         |
| `d.get(k, default)`           | O(1) average    | Same as indexing, with a fallback.                    |
| `d.pop(k)`                    | O(1) average    | Removes and returns the value.                        |
| `d.popitem()`                 | O(1)            | Removes and returns the **last-inserted** pair.       |
| `d.setdefault(k, v)`          | O(1) average    | Insert‑if‑missing, return value.                      |
| `d.update(other)`             | O(k)            | k = number of keys being added/updated.               |
| Length (`len(d)`)             | O(1)            | Size stored as an attribute.                          |
| Iteration                     | O(n)            | In insertion order.                                   |
| `d.keys()` / `.values()` / `.items()` | O(1)    | Returns a **view** object, not a list.                |
| Copy (`d.copy()`)             | O(n)            | Shallow copy.                                         |

**Key insight — `in` on a dict checks KEYS, not values:**
```python
d = {"a": 1}
"a" in d    # True
1 in d      # False!  – `in` checks keys
1 in d.values()  # True – but this is O(n)
```

---

## Merging and Updating

Python 3.9+ gives you two clean ways to combine dicts:

```python
a = {"x": 1, "y": 2}
b = {"y": 20, "z": 3}

merged = a | b          # 3.9+: new dict {"x": 1, "y": 20, "z": 3}
a |= b                  # 3.9+: update a in place
a.update(b)             # works on all versions: same as |=
```

The `|` operator creates a **new** dict. For right‑side wins on key collisions, put the 
"winning" dict on the right.

---

## Dictionary Views

`d.keys()`, `d.values()`, and `d.items()` return **view objects** — not lists. Views are:

- **Live:** they reflect future changes to the dict.
- **Iterable:** you can `for` over them.
- **Set‑like** (for keys and items): they support `&`, `|`, `-`, `^`.
- **Memory‑cheap:** they don't copy the underlying data.

```python
d = {"a": 1, "b": 2, "c": 3}
keys = d.keys()
d["d"] = 4
print(keys)             # dict_keys(['a', 'b', 'c', 'd'])  – reflects the new key

# Set-style operations on keys
d1 = {"a": 1, "b": 2}
d2 = {"b": 20, "c": 3}
d1.keys() & d2.keys()   # {'b'}
d1.keys() - d2.keys()   # {'a'}
```

---

## Memory Usage

- A dict pre‑allocates a hash table larger than the number of entries.
- Each entry is roughly 3 pointers (hash, key, value) on 64‑bit systems.
- Dicts use **more memory per item than a list**; the trade is O(1) key lookup.
- The dict only holds **references** — actual key and value objects live elsewhere.

---

## Dicts vs Lists vs Sets

| Aspect                 | List                 | Set                  | Dict                            |
|------------------------|----------------------|----------------------|---------------------------------|
| Shape                  | ordered sequence     | unordered bag        | key → value mapping             |
| Allows duplicates?     | Yes                  | No                   | Keys unique; values anything     |
| Membership cost        | O(n)                 | **O(1) avg**         | **O(1) avg** (on keys)          |
| Preserves order?       | Yes                  | No                   | Yes (insertion order)           |
| Can you index?         | Yes (`lst[i]`)       | No                   | By key, not position            |
| Typical use            | Ordered sequence     | Presence / dedup     | Lookup / association            |

Rule of thumb:

> **List** — ordered sequence of things.  
> **Set** — "is X present?" / uniqueness.  
> **Dict** — "what value goes with key X?" — by far the most used of the three.

---

## When to Use (and Not Use) Dicts

✅ **Good use cases:**

- Looking up a value by a key in O(1): usernames, IDs, config settings, cached results.
- **Counting** occurrences (`counts[word] += 1` — see also `collections.Counter`).
- **Grouping** items by a key (`groups[tag].append(item)`).
- **Memoization** of expensive function calls.
- JSON data — maps almost 1:1 onto Python dicts.
- Representing graphs as adjacency maps: `graph["A"] = ["B", "C"]`.

❌ **Avoid when:**

- You only care about presence, not about any associated value — use a `set`.
- The keys are consecutive small integers — a plain `list` is simpler and faster.
- Your keys are mutable (lists, dicts) — convert them to tuples or `frozenset` first.
- You need to preserve a **custom** ordering — use `sorted(d.items())` on each access, or 
  reach for a different data structure.

---

## Code Example (Quick Overview)

```python
# Creating
scores = {"alice": 90, "bob": 85}

# Access
print(scores["alice"])          # 90
print(scores.get("carol", 0))   # 0  – missing key, default returned

# Insert / update / delete
scores["carol"] = 78            # insert
scores["alice"] = 95            # update
del scores["bob"]               # delete
scores.pop("unknown", None)     # safe delete

# Membership – checks KEYS
print("alice" in scores)        # True
print(95 in scores)             # False

# Iteration
for name in scores:                     # keys
    print(name)
for name, score in scores.items():      # pairs
    print(name, "->", score)

# Counting idiom
from collections import Counter
words = ["a", "b", "a", "c", "a", "b"]
counts = {}
for w in words:
    counts[w] = counts.get(w, 0) + 1    # {'a': 3, 'b': 2, 'c': 1}

# Grouping idiom
pairs = [("fruit", "apple"), ("veg", "carrot"), ("fruit", "pear")]
groups = {}
for category, item in pairs:
    groups.setdefault(category, []).append(item)
# groups = {'fruit': ['apple', 'pear'], 'veg': ['carrot']}

# Dict comprehension
squared = {x: x * x for x in range(5)}  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# Merging (Python 3.9+)
defaults = {"debug": False, "port": 8080}
override = {"port": 9000}
config = defaults | override            # {'debug': False, 'port': 9000}
```

For a more thorough demonstration of each operation, see [`operations.py`](operations.py).
