# Phase 06 — Hashing

Hashing is the single most powerful optimization in interview
programming. "Replace a linear search with a constant-time lookup"
is the trick behind roughly half of all O(n) solutions to problems
that look like they should be O(n²).

By now you've USED hashing extensively:

- **Phase 01 / 03 / 03-Set & 04-Dictionary** — Python's `set` and
  `dict` with complexity analysis.
- **Phase 02 / 02 / 07-Hashing-Technique** — the four hashing
  patterns (seen, complement lookup, counting, grouping).
- **Phase 02 / 02 / 08-Frequency-Counting** — Counter patterns.
- **Phase 04 / 03-Linked-List / 02-DLL** — LRU Cache via hash + DLL.

Phase 06 is the **deep dive**: how do hash tables *actually work*?
What does CPython do when you write `d[key] = value`? Why are
`set` and `dict` operations O(1) average — and under what
adversarial conditions do they become O(n)?

---

## What This Phase Covers

### 01 — HashMap (From Scratch)

The substrate of `dict`, `Counter`, `defaultdict`, and every
hash-based cache in existence. Implement it two different ways to
internalize the tradeoffs:

- **`hash-functions.py`** — What makes a hash function "good"?
  Polynomial hashing for strings, FNV, CPython's SipHash-inspired
  `hash()`. Why hash randomization exists.
- **`chaining.py`** — Collisions resolved by storing a LINKED LIST
  (or dynamic array) per bucket. The CPython `dict` originally used
  this strategy.
- **`open-addressing.py`** — Collisions resolved by PROBING for the
  next empty slot. Linear probing, quadratic probing, double
  hashing. What CPython's `dict` uses today.
- Load factor, rehashing, and resize strategy.
- Two problems: LC #706 (Design HashMap) and LC #146 (LRU Cache)
  rebuilt on top of our HashMap.

### 02 — HashSet (From Scratch)

A set is a HashMap where only keys matter (no values). We'll build
one on top of our HashMap and solve classic set-based problems:

- **Happy Number** (LC #202) — cycle detection via set.
- **Longest Consecutive Sequence** (LC #128) — O(n) with clever set use.
- **Design HashSet** (LC #705) — interview exercise.

### 03 — Advanced

Topics beyond textbook hash tables:

- **Bloom filter** — probabilistic "definitely not in set" lookups.
  Used by databases, web caches, bitcoin nodes.
- **Consistent hashing** — distribute keys across N servers with
  minimal reshuffling when N changes. The backbone of distributed
  caches (memcached, Cassandra).
- **Perfect hashing** — hash functions with ZERO collisions on a
  known, fixed key set.

### 04 — Problems

Larger hashing-driven problems that don't fit neatly in the module-
level sub-folders:

- **Top-K Frequent Elements** (LC #347) — hash + heap.
- **Subarray Sum Equals K** (LC #560) — prefix-sum + hash.
- **Design Twitter** (LC #355) — composite structure.

---

## Why Build Hash Tables By Hand?

Three reasons:

1. **You'll understand WHY dict operations are O(1) average.**
   It's not magic — it's a very specific combination of good hash
   function, load-factor management, and probing strategy.
2. **You'll understand WHY they're O(n) worst case.** Adversarial
   inputs can force all keys to collide. CPython mitigates this
   with hash randomization; knowing HOW is useful for security work
   (algorithmic-complexity DoS attacks).
3. **You'll see the fundamental space-time tradeoff.** Hash tables
   trade O(n) memory for O(1) lookups. Every other "turn O(n) into
   O(1)" trick you learn borrows this basic structure.

In production Python, you'll use `dict`. Always. But knowing what
`dict` *is* makes you a better programmer — and an infinitely better
interviewee.

---

## Folder Layout

```
Phase-06-Hashing/
├── README.md                            ← you are here
├── 01-HashMap/
│   ├── theory.md
│   ├── hash-functions.py
│   ├── chaining.py
│   ├── open-addressing.py
│   └── problems/
│       ├── design-hashmap.py           ← LC #706
│       └── lru-cache.py                ← LC #146
├── 02-HashSet/
│   ├── theory.md
│   ├── implementation.py
│   └── problems/
│       ├── design-hashset.py           ← LC #705
│       ├── happy-number.py             ← LC #202
│       └── longest-consecutive.py      ← LC #128
├── 03-Advanced/
│   ├── bloom-filter.py
│   ├── consistent-hashing.py
│   └── perfect-hashing.md
└── 04-Problems/
    ├── top-k-frequent.py                ← LC #347
    ├── subarray-sum-k.py                ← LC #560
    └── design-twitter.py                ← LC #355
```

---

## Outcome

By the end of Phase 06 you should be able to:

1. **Implement a hash table from scratch**, both with chaining and
   with open addressing.
2. **Reason about load factor, rehashing, and when O(1) degrades
   to O(n).**
3. **Explain why Python's `dict` uses open addressing** and what
   SipHash prevents.
4. **Pick between hash-based and tree-based structures** based on
   operation mix (many inserts? ordered iteration? range queries?).
5. **Recognize and apply** Bloom filters, consistent hashing, and
   perfect hashing when the problem calls for them.

Phase 07 (Trees & Heaps) introduces the alternative: TREE-based
structures where you trade O(1) for O(log n) but gain ordering.
The choice between hash and tree is the second-most-important
data-structure decision in algorithm design, right after array vs
linked list.
