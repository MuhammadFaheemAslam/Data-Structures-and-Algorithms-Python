# HashMap — Theory

## Introduction

A **hash table** (or **hash map**) is the data structure behind
Python's `dict`, Java's `HashMap`, Rust's `HashMap`, and every
cache, index, or "key → value" lookup in production software.

The promise is remarkable:

> *O(1) average-case insert, lookup, and delete — regardless of how
> many keys are stored.*

This is achieved by combining three ideas:

1. **A big array** of "buckets" (or "slots").
2. **A hash function** that maps any key to a bucket index in O(1).
3. **A collision-resolution strategy** for when two keys land in
   the same bucket.

Everything in this module is some variation on those three pieces.

---

## The Basic Idea

Imagine you want to store key-value pairs where keys are English
words (`"alice"`, `"bob"`, `"charlie"`). You COULD store them in a
list and search linearly — O(n) per lookup, unusable at scale.

Instead:

1. Pick a hash function `h(key)` that maps any key to an integer
   in the range `[0, N)` where `N` is your array size (say, 8).
2. Store the pair at `buckets[h(key)]`.
3. To look up: compute `h(key)` again, then check `buckets[h(key)]`.

If `h` is well-designed, different keys map to different buckets
with high probability — giving us O(1) lookup.

```
     buckets       keys stored in each bucket
     ────────      ──────────────────────────
     [0] ───→
     [1] ───→  "bob"    (h("bob") = 1)
     [2] ───→
     [3] ───→  "alice"  (h("alice") = 3)
     [4] ───→  "charlie", "diana"  (← COLLISION!)
     [5] ───→
     [6] ───→
     [7] ───→
```

The bucket 4 shows the **collision problem**: two different keys
hashed to the same index. Every real-world hash function has
collisions (there are ∞ possible keys and only N buckets). The
question is how to RESOLVE them.

---

## Collision Resolution — Two Main Strategies

### Strategy 1: Separate Chaining

Each bucket stores a LIST of `(key, value)` pairs that hashed to
it. Lookup scans the list for a matching key.

```
[0] → []
[1] → [("bob", 25)]
[2] → []
[3] → [("alice", 30)]
[4] → [("charlie", 28), ("diana", 42)]   ← two entries in one bucket
[5] → []
...
```

- **Insert**: compute hash, append to the bucket's list.
- **Lookup**: compute hash, scan the bucket's list for matching key.
- **Delete**: compute hash, remove from the bucket's list.

When bucket sizes stay small (say, at most 1–2 entries on average),
each operation is effectively O(1). When they grow larger — say,
many keys all hash to bucket 4 — operations degrade toward O(n).

Covered in `chaining.py`.

### Strategy 2: Open Addressing

Each bucket stores at most ONE entry. On collision, find the NEXT
empty bucket using some PROBING SEQUENCE.

```
[0]  empty
[1]  ("bob", 25)
[2]  empty
[3]  ("alice", 30)
[4]  ("charlie", 28)        ← hashed here, this bucket was empty
[5]  ("diana", 42)          ← hashed to 4, it was taken, linear-probe to 5
[6]  empty
[7]  empty
```

Probing sequences:

- **Linear probing**: try h(k), h(k)+1, h(k)+2, ... (mod N).
- **Quadratic probing**: try h(k), h(k)+1², h(k)+2², ...
- **Double hashing**: try h(k), h(k)+h'(k), h(k)+2h'(k), ...

Covered in `open-addressing.py`.

---

## Chaining vs Open Addressing — Comparison

| Property                   | Separate Chaining     | Open Addressing       |
|----------------------------|-----------------------|-----------------------|
| Max load factor            | > 1 is OK (say, 5-10) | < 1 (typically ~0.7)  |
| Cache behaviour            | Poor (linked lists)   | **Good** (contiguous) |
| Memory overhead            | Pointer per entry     | Often less            |
| Simple to implement        | **Yes**               | Needs careful delete  |
| Handles hash clustering    | Yes                   | Suffers under clustering |
| Used in practice           | Java HashMap (mostly) | Python, Rust, Go      |

Modern implementations lean toward **open addressing** because of
cache-friendliness. CPython's `dict` uses open addressing with a
probing sequence derived from the hash value (it's not exactly
linear/quadratic/double-hashing — it's a custom scheme tuned for
the CPython object model).

---

## Load Factor and Resizing

**Load factor** = number of entries / number of buckets.

As the table fills up:
- Collisions become more frequent.
- Bucket sizes (in chaining) or probe sequences (in open addressing)
  grow longer.
- O(1) average performance degrades.

To maintain O(1), hash tables **resize** when the load factor
crosses a threshold:

1. Allocate a NEW, larger array (typically 2× the old size).
2. **Rehash** every existing entry: compute its hash modulo the NEW
   array size, put it in its new position.
3. Free the old array.

Resize is an O(n) operation, but it happens rarely (once per
doubling), so **amortized cost per insert stays O(1)**. Same
amortized analysis as dynamic arrays (see Phase 04 / 01-Array).

### Typical Load-Factor Thresholds

| Strategy          | Resize when load factor exceeds |
|-------------------|---------------------------------|
| Separate chaining | 0.75 or 1.0                     |
| Open addressing   | 0.5 to 0.75                     |

Open addressing needs a LOWER load factor because probing sequences
degrade rapidly as the table fills. At load factor 0.9, linear
probing can require scanning 10+ slots per lookup.

---

## A Good Hash Function

Requirements:

1. **Deterministic** — `hash(x)` always returns the same value.
2. **Uniform distribution** — should map keys roughly evenly across
   the output range. Clustering (many keys hashing to the same
   bucket) is the enemy of hash-table performance.
3. **Fast to compute** — if hashing takes longer than comparing,
   you've defeated the point.
4. **Small changes in input → large changes in output** (the
   "avalanche" property) — two similar keys shouldn't collide.

### How Python Does It

Python's `hash()`:
- Integers: `hash(n) == n` for small ints (literally the identity).
- Strings/bytes: SipHash — a cryptographic hash with a per-process
  random seed. This prevents "hash collision DoS attacks" where
  a malicious client sends keys designed to all collide in your
  server's hash table.
- Tuples: combines the hashes of their elements.
- Custom objects: `object.__hash__` uses `id(self) // 16` by default.
  You can override `__hash__` to customize.

Covered in `hash-functions.py`.

---

## When Hash Tables Go Wrong

### 1. Adversarial Input (Collision Attack)

Before Python added hash randomization (Python 3.3, circa 2012), an
attacker could send a dict with keys designed to all hash to the
same bucket. Every insert/lookup became O(n), and parsing a
"normal-looking" JSON object could take seconds.

SipHash + a random per-process seed fixes this for strings/bytes.
For custom objects with `__hash__`, YOU are responsible for making
them resistant.

### 2. Bad `__hash__` That Doesn't Match `__eq__`

If `a == b` then `hash(a) == hash(b)` MUST hold. Otherwise:
- Insert `a`, look up `b` (equal to `a` by `__eq__`): might hash to
  a DIFFERENT bucket, look up fails, returns "not found."
- Your dict is silently broken.

Always override `__hash__` and `__eq__` as a pair, and make sure
they use the SAME FIELDS.

### 3. Mutable Objects as Keys

If you insert an object as a key and then MUTATE it, its hash
probably changes — and you can no longer find it in the dict.

Python blocks this for `list`, `dict`, `set` (they're unhashable).
Tuples are fine (immutable). For custom classes, you have to be
disciplined.

### 4. Excessive Load Factor from Forgetting to Resize

Every production hash table implementation resizes automatically.
When you implement your own, make sure the resize logic actually
fires — or you'll silently slow down as the table fills.

---

## Time and Space Complexity

| Operation   | Average   | Worst case                      |
|-------------|-----------|--------------------------------|
| Insert      | O(1)      | O(n) (all keys collide)         |
| Lookup      | O(1)      | O(n) (all keys collide)         |
| Delete      | O(1)      | O(n)                            |
| Iterate     | O(n)      | O(n)                            |
| Resize      | O(n)      | O(n)                            |

Space: O(n) for the entries plus O(N) for the bucket array
(typically N = 2n). Total is O(n), but the constant is larger
than for a plain array.

---

## Hash Tables vs Other Structures

| Structure              | Find    | Insert  | Delete  | Ordered? | Memory   |
|------------------------|---------|---------|---------|----------|----------|
| **Hash table**         | O(1)    | O(1)    | O(1)    | No       | O(n)     |
| Sorted array           | O(log n)| O(n)    | O(n)    | Yes      | O(n)     |
| Balanced BST           | O(log n)| O(log n)| O(log n)| Yes      | O(n)     |
| Trie                   | O(k)    | O(k)    | O(k)    | Prefix   | O(Σ · k) |

Hash tables win on SPEED for simple membership/lookup. They lose to
trees when you need ORDERED iteration, range queries, or consistent
worst-case bounds.

---

## Why Python Uses `dict` for Everything

You'll notice `dict` is the most-used data structure in Python by a
wide margin — it's the implementation behind:

- Every module's namespace (`module.__dict__`).
- Every object's attributes (`obj.__dict__`).
- Every class's methods.
- Import tables, exception handlers, switch-statement dispatches.

This is because dict lookup is fast enough to be "free" in
interpreter code. Some operations in CPython's internals are literally
4 pointer operations — one hash, one mod, one compare, one dereference.

Understanding what a hash table IS makes you much more aware of
when Python code is cheap vs expensive.

---

## Key Takeaways

1. **Hash tables = array + hash function + collision resolution.**
   That's the whole structure.
2. **Two main strategies:** separate chaining (list per bucket) or
   open addressing (probe for an empty slot).
3. **O(1) average but O(n) worst case.** Load factor is the knob
   that controls this.
4. **Resize by doubling** keeps amortized insert O(1).
5. **Hash randomization** (SipHash in Python) prevents
   collision-based DoS attacks.
6. **`hash()` and `__eq__` must be consistent.** If `a == b`, then
   `hash(a) == hash(b)`. Otherwise your dict is silently broken.

Now we implement each piece:

- [`hash-functions.py`](hash-functions.py) — what makes a good hash.
- [`chaining.py`](chaining.py) — HashMap with separate chaining.
- [`open-addressing.py`](open-addressing.py) — HashMap with linear/quadratic probing.
- [`problems/design-hashmap.py`](problems/design-hashmap.py) — LC #706.
- [`problems/lru-cache.py`](problems/lru-cache.py) — LC #146 on top of our HashMap.
