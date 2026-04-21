# Hashing — Theory

## Introduction

**Hashing** is the single most valuable algorithmic technique in all
of interviewing and competitive programming. More specific optimizations
exist, but none gets pulled out more often, and none has a bigger
average speedup per line of code.

The core idea, stripped to its essence:

> *Replace a linear search with a constant-time lookup.*

That one sentence is the entire technique. Every hashing problem
reduces to recognising that a brute force does a search-inside-a-loop,
and that the search can be swapped for a dict/set lookup — turning
O(n²) into O(n) at the cost of O(n) extra memory.

Phase 01 introduced Python's `set` and `dict` as data structures.
This module is about *using them as an algorithmic weapon*.

---

## The Four Hashing Patterns

Almost every hashing problem you'll ever see is one of these four shapes:

### 1. "Have I seen X before?" — Set of visited

The most basic pattern. Maintain a `set` of things seen so far; each
new item is a single `in` check away from its answer.

```python
seen = set()
for x in arr:
    if x in seen:
        return True                       # duplicate / revisit / cycle / …
    seen.add(x)
return False
```

Used for: Contains Duplicate, Cycle detection (as a hash-set alternative
to fast-slow pointers), Visited nodes in graph search, First unique
element, "find the first repeated".

### 2. "Has X's partner already been seen?" — Dict of value → position

The generalization of pattern 1. Instead of just recording that you've
seen X, record *where*. Then for each new value, you can ask "has its
partner (defined by some rule) been seen, and at what index?"

```python
seen = {}                                 # value -> index
for i, x in enumerate(arr):
    partner = something_of(x)             # e.g., target - x
    if partner in seen:
        return (seen[partner], i)         # found the pair
    seen[x] = i
return None
```

Used for: Two Sum, Contains Duplicate II (within k indices), First
non-repeating character, Longest consecutive sequence.

### 3. "How many of each?" — Frequency counter

A dict mapping value → count. Enables O(1) queries on frequencies
(how often did X appear? which value appears most often?) at O(n)
building cost.

```python
counts = {}
for x in arr:
    counts[x] = counts.get(x, 0) + 1

# Now you can ask:
max(counts, key=counts.get)               # most frequent value
sum(1 for c in counts.values() if c == 1) # count of unique values
```

Used for: Majority element, Top-K frequent, Anagram detection, Valid
anagram, Character frequency, Count distinct.

This pattern is important enough that it has its own Phase-02 / 02 /
module: **08-Frequency-Counting**.

### 4. "What's X's group?" — Dict of signature → list/set

Group items by some canonical "signature". Items with the same
signature end up in the same bucket.

```python
groups = {}
for item in items:
    sig = signature(item)                 # canonical form
    groups.setdefault(sig, []).append(item)
return list(groups.values())
```

Used for: Group Anagrams, Group Shifted Strings, Array of Subarrays
sharing a property.

All four patterns share the same shape: a one-line "is X in the dict?"
replaces an O(n) scan. The difference is only in what you're putting
in the dict.

---

## Why It Works — The O(1) Average Lookup

Dicts and sets in Python are **hash tables**. Under normal workloads,
any `x in d`, `d[x]`, and `d[x] = v` is **O(1) average**. See
Phase-01 / 03-Python-BuiltIn-DSA / 03-Set / time-complexity.md for
the details.

That O(1) is what lets you replace a nested loop with a flat loop:

- Brute force: `for each x in arr: for each y in arr: …` → O(n²).
- Hashing: `for each x in arr: dict.lookup(…)` → O(n) amortized.

The cost: O(n) extra memory for the dict. For almost every problem
you'll see, that memory is a bargain compared to the time savings.

---

## When to Reach for Hashing

Strong signals:

1. **You're about to write a nested loop that scans the same data
   twice.** This is the #1 indicator. Look for `for i: for j: if
   some(arr[i], arr[j])`. That inner scan is a hash-lookup in disguise.
2. **The problem says "find", "count", or "group".** Each maps directly
   to one of the four patterns above.
3. **The input is unsorted** and sorting isn't acceptable. (If it IS
   sorted, two pointers often beats hashing — no extra memory.)
4. **You need to maintain state across iterations** that's cheap to
   query but grows with n (e.g., "characters seen so far").

Weak signals:

5. **Duplicates matter.** When the problem cares about repetition,
   a frequency map is almost always involved.
6. **You're tracking positions, not just values.** The dict's value
   can hold the index of occurrence (pattern 2) — cheap and useful.

---

## When NOT to Use Hashing

- **Sorted input and you only need a scalar answer.** Two Pointers
  wins: O(n) time AND O(1) space. Use hashing when sorting would
  cost information (you need original indices) or be too slow (O(n)
  hashing beats O(n log n) sorting).
- **The values aren't hashable.** Lists, dicts, sets, mutable custom
  objects — none can be dict keys. Convert to tuples / frozensets
  first.
- **You need ordering or range queries.** Dicts preserve insertion
  order in Python 3.7+, but they don't support "find the smallest key
  greater than X". For that, a balanced BST / sorted structure is
  needed.
- **Memory is extremely tight.** Hashing's O(n) space can be a killer
  on problems with n = 10^7+. Two pointers, prefix sum, or in-place
  tricks are the alternatives.

---

## Hashing vs Related Techniques

| Technique            | Shape                                   | Space     |
|----------------------|-----------------------------------------|-----------|
| **Hashing**          | `dict/set` of values → positions / counts | O(n)    |
| **Two Pointers**     | Two indices on SORTED array             | O(1)      |
| **Sliding Window**   | Two indices + window-state dict         | O(k)      |
| **Prefix Sum + Hash**| Cumulative sum + hash → O(n) subarray queries | O(n) |
| **Frequency Counting**| Specialization of hashing for counts   | O(n)      |

Two Pointers and Hashing are the two "obvious" options for Two Sum:

- On sorted input: Two Pointers — O(n) time, O(1) space.
- On unsorted input: Hashing — O(n) time, O(n) space.

For most pair-search problems, your first question should be "is the
input sorted?" If yes, two pointers. If no, hashing.

---

## Canonical Examples

### Two Sum — LeetCode #1

Dict of value → index; for each new x, look up `target - x`.

### Group Anagrams — LeetCode #49

Dict of sorted-string (signature) → list of words.

### First Unique Character — LeetCode #387

Counter pass + second pass to find the first with count 1.

### Longest Consecutive Sequence — LeetCode #128

Set of all values; for each x that is the "start" of a run (no x-1 in
set), walk x+1, x+2, … counting the run length.

### Subarray Sum Equals K — LeetCode #560

Prefix sum + hashing: dict of `prefix_sum → count`. For each new
running sum, look up how many prior prefixes had `sum - k`.

### Contains Duplicate — LeetCode #217

Drop into a set; compare set length to array length.

In every case, the data structure is the same (dict or set); only the
key/value schema differs.

---

## Two Practical Patterns That Come Up a Lot

### The `seen` set pattern (one-pass deduplication with order preserved)

```python
result = []
seen = set()
for x in items:
    if x not in seen:
        seen.add(x)
        result.append(x)
```

Keeps the first occurrence of each value in order. Faster than
`list(dict.fromkeys(items))` only in constant factors — but more explicit.

### The counter subtract pattern (anagram / permutation check)

```python
from collections import Counter
return Counter(s) == Counter(t)           # anagram check
```

Two dicts of char → count — equal if and only if the multisets match.

---

## Complexity

- **Building / scanning:** O(n) time, O(n) space (for the dict/set).
- **Each lookup / insert:** O(1) average, O(n) worst case (with
  adversarial hash collisions — almost never in practice).

The "O(n) space" is almost the only cost. For most problems it's an
easy tradeoff — you're trading space for a giant time win.

---

## Common Pitfalls

- **Using a list where a set/dict should be.** `x in list` is O(n);
  the "bug" is algorithmic, not syntactic. A 10-line hashing solution
  with `if x in some_list` becomes O(n²) silently. Watch for this —
  it's one of the most common "accidentally quadratic" patterns in
  real-world Python.
- **Not initializing correctly.** In the Subarray Sum Equals K pattern,
  forgetting `prefix_counts[0] = 1` causes all subarrays starting at
  index 0 to be missed. See Phase-02 / 02 / 03-Prefix-Sum for details.
- **Using mutable types as keys.** `d[[1, 2]] = 3` raises TypeError
  (lists unhashable). Convert to tuple / frozenset.
- **Expensive key computation.** If your key is a sorted string or
  sorted tuple, building it is O(k log k) per item. That's fine, but
  budget for it in the complexity analysis.
- **Rebuilding the hash every iteration.** A dict built inside a loop
  that could be built once turns O(n) into O(n²). Move setup out of
  the loop.

---

## Key Takeaways

1. **Hashing = replace search with lookup.** That's the entire
   technique. Four patterns cover almost every problem.
2. **Use a set when you only care about presence.** Use a dict when
   you also need a value (index, count, group).
3. **The tradeoff is O(n) space for O(n) time.** Almost always worth it.
4. **On sorted input, check two pointers first** — same time, O(1)
   space. Use hashing when two pointers doesn't apply.
5. **Unhashable types need conversion.** Tuples, frozensets, or
   canonical strings.
6. **The "seen" set pattern and "complement lookup" pattern show up
   CONSTANTLY.** Memorize both skeletons.

For the template, see [`template.py`](template.py). For two worked
problems (Two Sum + Group Anagrams — one per common pattern), see
[`problems/`](problems/).
