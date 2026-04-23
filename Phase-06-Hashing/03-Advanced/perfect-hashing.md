# Perfect Hashing

A **perfect hash function** maps a KNOWN, FIXED set of `n` keys to
distinct buckets *with no collisions at all*. "Known and fixed" is the
critical constraint — perfect hashing is built for STATIC data.

If your set of keys:

- never changes (compile-time constants, reserved keywords, look-up
  tables, bundled data), AND
- needs to be queried extremely fast (no chain walks, no probing),

then perfect hashing gives you **worst-case O(1)** lookup. Not amortized,
not average — guaranteed worst case.

---

## Two flavours

| Kind              | Collisions allowed? | Guarantee                     | Space         |
|-------------------|---------------------|-------------------------------|---------------|
| **Perfect hash**  | No                  | O(1) worst-case lookup        | `m ≥ n` slots |
| **Minimal perfect hash (MPHF)** | No   | O(1) worst-case lookup; `m = n` | exactly `n` slots |

A minimal perfect hash fills its table 100%. Regular perfect hashing
may leave ~25-50% of slots empty but is easier to construct.

---

## When you see it in the wild

Perfect hashing isn't an everyday tool, but it's surprisingly common
under the hood of things you use every day:

- **Compilers** — C `switch` statements on strings (the `gperf` tool
  generates a perfect hash of your keywords; GCC's C compiler uses
  one for C keywords).
- **CDN routing** — static route tables at edge nodes.
- **Large static dictionaries** — bioinformatics k-mer lookups, chess
  position tables, spell-check dictionaries.
- **Immutable config** — the set of HTTP header names, the set of
  ISO-3166 country codes, a game's asset-name → ID table.
- **Cuckoo-filter variants** — perfect-hash-backed set membership for
  massive static sets.

The common thread: data is LOADED ONCE at startup and never changed.
That's the "static" in "static perfect hashing".

---

## Why it's not just "use a hash table"

Regular hash tables have:

- **Average** O(1), **worst-case** O(n). Fine for dynamic workloads,
  but the tail latency of a ~5% probability of a long probe chain is
  unacceptable for hot code paths.
- Memory overhead from load-factor slack (25-50% empty slots is
  typical).
- Cache unfriendliness on collisions (pointer-chases for chaining,
  probe walks for open addressing).

Perfect hashing removes all three: a single hash computes the bucket,
and the bucket is guaranteed to be the right one. No probing loop, no
chain walk, no tail latency.

---

## How perfect hashes are constructed

The three dominant techniques:

### 1. Two-level (FKS) scheme — Fredman-Komlós-Szemerédi, 1984

The classic theoretical result. Store `n` keys in `O(n)` space with
`O(1)` worst-case lookup.

```
Top level (size n):
    Pick a universal hash h1 mapping keys to n buckets.
    Most buckets have 0 or 1 key; some have collisions.

Bottom level (per bucket with k keys):
    Allocate a secondary table of size k².
    Pick a universal hash h2 mapping those k keys to k² slots.
    With probability > 1/2 there are NO collisions.
    If there are, try a different h2 (try until you find one — average O(1) tries).
```

**Lookup**: compute h1(key) → bucket, then h2(key) → slot within
that bucket. Two hash operations, both O(1).

**Space**: The sum of squared bucket sizes is O(n) in expectation,
so total space is O(n).

### 2. CHD (Compress-Hash-Displace) — Belazzougui et al., 2009

A practical algorithm used in real libraries (e.g. cmph, GNU gperf for
large key sets).

```
Pick a random hash g1 partitioning keys into r buckets, sorted largest-first.
For each bucket in order:
    Try many "displacement values" d.
    The bucket's keys hash to (g2(key) + d) mod m.
    Pick the first d that doesn't collide with previously placed keys.
Store the d values compactly; at query time, do:
    (g2(key) + d[g1(key)]) mod m
```

Space: ~1.6 bits per key for minimal perfect hashing. Remarkable.

### 3. RecSplit — Esposito et al., 2020

The current space-efficiency champion. Achieves ~1.5 bits per key
(approaching the information-theoretic lower bound of ~1.44).
Works by recursively splitting the key set into small subsets and
searching for a perfect hash for each subset separately. Highly
parallelizable. Used in DuckDB, genomic databases, etc.

---

## A tiny worked example: n = 5 keys

Imagine we have keys `{"apple", "banana", "cherry", "date", "elderberry"}`.
We want a perfect hash into 5 slots.

```
Try h(s) = (sum of char codes) mod 5:

    "apple"       → 530 mod 5 → 0
    "banana"      → 625 mod 5 → 0      ← collision with "apple"
    ...
```

That doesn't work. Try a different hash — e.g. `(sum * 31) mod 5`. If
that still collides, keep trying different parameters. For 5 keys, we
almost always find a working hash within a handful of tries.

A generator like `gperf` does exactly this: tries hashes with
structured parameters (which characters to consider, how to weight
them) until it finds one that's collision-free on your specific keys.
The final "generated code" is a one-liner — very fast to run.

---

## Why we don't implement it here

An educational implementation of FKS is ~150 lines and doesn't
illuminate the core "hashing" concepts more than the open-addressing
and chaining versions we've already built. It shows up in courses
as a *theoretical* result more often than a practical exercise.

If you *do* want to play with it:

- [`gperf`](https://www.gnu.org/software/gperf/) — the classic;
  generates C code for your specific key set.
- [`cmph`](https://cmph.sourceforge.net/) — C minimal perfect hash
  library (implements CHD, BDZ, etc.).
- `perfect-hash` (PyPI) — a Python port of gperf-style perfect hashing.

---

## Key takeaways

1. **Perfect hashing is for static data** — if your keys are fixed at
   build time, you can have *guaranteed* O(1) lookup with no wasted
   space.
2. **It's practical, not just theoretical** — real compilers, real
   databases, and real CDNs use it.
3. **Space bounds are astonishing** — 1.5-1.6 bits per key for
   minimal perfect hashing. A HashSet needs ≥ 32 bits per key (a
   pointer) plus overhead. For billion-key static data sets, the
   savings are enormous.
4. **Not for dynamic workloads** — adding or removing a key forces
   you to rebuild, which is a batch-scale operation, not interactive.

For **dynamic** workloads with worst-case guarantees, the answer is
[**cuckoo hashing**](https://en.wikipedia.org/wiki/Cuckoo_hashing)
(each key has k possible positions; inserts evict and re-place on
collision) — worst-case O(1) lookup, expected O(1) insert. Often
paired with perfect hashing for the "seal the set" step when a static
snapshot is needed.
