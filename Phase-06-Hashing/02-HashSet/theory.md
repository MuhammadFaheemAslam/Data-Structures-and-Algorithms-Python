# HashSet — Theory

A **hash set** is a collection of **unique** elements with O(1) average `add`,
`remove`, and `contains`. It's a hash map where the "value" payload is
meaningless — only the keys matter.

Python gives us `set` and `frozenset` as built-ins. Internally they use the
same open-addressing technique as `dict`. So why study HashSet separately?

1. You'll be asked to implement one in interviews (LC #705).
2. The *use cases* are different from a map's — `set` problems almost always
   reduce to "dedupe + membership test in O(1)".
3. A handful of classical problems (happy number, longest consecutive
   sequence, intersection of arrays) have clean, surprising solutions once
   you think "what if I just put this in a set?"

---

## HashSet vs HashMap

|                   | HashMap                       | HashSet                       |
|-------------------|-------------------------------|-------------------------------|
| Stores            | `(key, value)` pairs          | just `key` (or "element")     |
| Question it answers | "what's the value for k?"   | "have I seen this before?"    |
| Python            | `dict`                        | `set`                         |
| Implementation    | buckets of `(k, v)` tuples    | buckets of `k` (or a map with dummy values) |

**Implementation shortcut**: a HashSet is literally a HashMap where you
ignore the value. In interviews you can often answer "Design HashSet" by
saying: "I'll reuse my HashMap and store the element as both key and
sentinel value." That's an acceptable answer — but the standalone version
is ~20% smaller and faster, so in this module we build it from scratch.

---

## Why HashSet is so useful

Most "fast lookup" problems have the same shape:

1. Scan input once, inserting things into a set.
2. Scan again (or the same scan), querying "is X in the set?"

This pattern converts MANY O(n²) brute-force solutions into O(n):

| Problem                               | Brute force | With HashSet |
|---------------------------------------|-------------|--------------|
| Has-duplicate? (LC #217)              | O(n²) pairs | O(n)         |
| Two-Sum (LC #1)                       | O(n²) pairs | O(n)         |
| Intersection of two arrays (LC #349)  | O(n·m)      | O(n+m)       |
| Longest consecutive sequence (LC #128)| O(n log n)  | **O(n)**     |
| Happy Number (LC #202)                | needs cycle detection | O(1) per step via set |

The wins are biggest when a problem seems to need *sorting*. If you only
need ORDER-INDEPENDENT queries ("is X here?"), sorting is overkill — a set
gives you the same in O(n) expected.

---

## Set operations

Unlike a map, a set has first-class `union`, `intersection`, `difference`,
and `symmetric_difference` operations — because a set is a MATHEMATICAL
object with those defined.

```python
a = {1, 2, 3}
b = {2, 3, 4}

a | b          # {1, 2, 3, 4}       union
a & b          # {2, 3}             intersection
a - b          # {1}                difference (in a, not in b)
a ^ b          # {1, 4}             symmetric difference (in exactly one)
```

All four are O(|a| + |b|) using a hash-based implementation.

We implement these in `implementation.py`.

---

## Hashable elements

Python's `set` (and our implementation) only accepts **hashable** elements.
Anything immutable with a well-defined `__hash__` is hashable:

    ✓   int, float, bool, str, tuple-of-hashables, frozenset, None
    ✗   list, dict, set (they're mutable — could hash to one bucket now,
        another bucket after mutation)

This is enforced by `hash(x)` raising `TypeError` on unhashable types.
The reason — mutation after insertion would make the element unfindable —
is the same pitfall we covered in the HashMap theory.

---

## frozenset

Sometimes you want a set to be a key IN another set or dict. You can't
use a regular `set` (it's mutable; not hashable), so Python provides
`frozenset`:

```python
fs = frozenset([1, 2, 3])
seen = {fs}                            # set of sets!
seen.add(frozenset([4, 5]))
```

This shows up in problems like "group anagrams" (where the key could be
a frozenset of letter counts) and "dedupe lists" (`set(tuple(x) for x in
list_of_lists)`).

---

## Complexity summary

| Operation                 | Average | Worst   |
|---------------------------|---------|---------|
| `add(x)`                  | O(1)    | O(n)    |
| `remove(x)`               | O(1)    | O(n)    |
| `x in s`                  | O(1)    | O(n)    |
| `len(s)`                  | O(1)    | O(1)    |
| `a.union(b)`              | O(|a|+|b|) | —    |
| `a.intersection(b)`       | O(min(|a|,|b|)) | — |
| `a.difference(b)`         | O(|a|)  | —       |
| iterate all elements      | O(n)    | —       |

Same guarantees as a hash map, with the same "bad hash / adversarial
input" caveats. Python's `set` uses the same SipHash randomization that
`dict` uses, so it's safe against collision attacks out of the box.

---

## Cross-references

- **Phase 02 — 06-hashing-technique.md**: the "use a set for O(1) lookup"
  pattern (two-sum, has-duplicate) is covered at the *algorithmic* level
  there; here we're interested in the *implementation*.
- **Phase 04 — linked-list problems**: "detect cycle" uses `set-of-nodes`
  as a simple (if not optimal) substitute for Floyd's algorithm.
- **Phase 01 — python-specifics**: `set`, `frozenset`, and set
  comprehensions are introduced there.

The `problems/` directory in this module highlights a few classics
that *only* become elegant once you reach for a set.
