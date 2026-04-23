# Where Self-Balancing BSTs Actually Show Up

AVL is one flavour of self-balancing BST; red-black is another.
Different production systems pick different variants for different
reasons, but the ideas are the same — rotations on insert/delete to
bound the height. Here's a tour of where you meet them.

---

## 1. Language-standard "sorted map" containers

Almost every language that ships an **ordered map** or **ordered set**
backs it with a self-balancing BST:

| Language        | Container                         | Backing DS         |
|-----------------|-----------------------------------|--------------------|
| C++             | `std::map`, `std::set`            | Red-black tree     |
| Java            | `TreeMap`, `TreeSet`              | Red-black tree     |
| Scala           | `TreeMap`, `TreeSet`              | Red-black tree     |
| Rust            | `BTreeMap`, `BTreeSet`            | **B-tree** (for cache locality)  |
| Go              | `container/tree` (rare)           | Red-black in many packages |
| Haskell         | `Data.Map`, `Data.Set`            | Size-balanced BST  |

Python is the odd one out — the standard library has `dict` and
`set` (hash-backed, no ordering), but no ordered-container primitive.
`sortedcontainers` (pip) fills the gap with a different data
structure (a 2-level "sorted list of sorted lists") that works
better for Python's cache behaviour than a linked-node BST.

Why red-black over AVL? Red-black allows a slightly looser balance
bound (path ≤ 2× the shortest), which means fewer rotations on
insert/delete. For **mixed read/write** workloads, that makes
red-black win on average. AVL tightens the bound (path ≤ 1.44 log n),
giving slightly faster *lookups* at the cost of more rotation work.

---

## 2. Kernel schedulers

The **Linux CFS** (Completely Fair Scheduler — the default process
scheduler since 2007) uses a red-black tree keyed by `vruntime`
("virtual runtime"). At every scheduling decision:

- The leftmost node of the tree is the next process to run
  (lowest vruntime = most owed CPU).
- After a process runs, its vruntime increases; re-insert.

O(log n) scheduling decisions with guaranteed worst-case latency.
A hash table can't do this (no ordering), and a heap can only see
the minimum (no deletion of arbitrary processes when they sleep /
block).

---

## 3. Databases — B-tree indexes

Almost every relational DB uses a **B-tree** for primary indexes:
PostgreSQL, MySQL/InnoDB, Oracle, SQLite. A B-tree is a self-
balancing tree where each node holds many keys (typically 100-1000),
which minimizes the number of DISK PAGES touched per lookup.

B-trees are the RIGHT generalization of "balanced BST" for
disk-resident data: high fanout → shallow tree → few page reads.
The balancing algorithm is different (no rotations — instead
node splits and merges), but the *spirit* is identical: keep the
height logarithmic in the data size, always.

LSM-trees (used by Cassandra, RocksDB, LevelDB) are the competing
shape for *write-heavy* workloads.

---

## 4. Network packet scheduling

Traffic-shaping algorithms at the network-device level keep per-flow
packet queues in a self-balancing BST keyed by "next deadline" or
"virtual time". Each packet enqueue / dequeue is O(log n) where n is
the number of active flows. Linux's HTB and HFSC qdiscs both use
red-black variants.

---

## 5. Interval trees / augmented BSTs

Classic BST + one extra field per node (`max-endpoint-in-subtree`)
becomes an **interval tree** that answers "which stored intervals
overlap [a, b]?" in O(log n + k). Used in:

- Genomics pipelines (overlapping read alignments).
- Calendar and reservation systems ("is this time slot free?").
- Computational geometry (horizontal-line sweeps).
- Compilers — register-allocation interval intersection queries.

The underlying "balanced BST + per-node augmentation" pattern is
everywhere. See Phase 11's segment-tree / Fenwick-tree / interval-
tree modules for details.

---

## 6. Order-statistics queries

If you augment each node with a `subtree_size` integer, the same
tree answers "what's the kth smallest?" and "how many elements are
< X?" in O(log n). Applications:

- **Online gradebooks / leaderboards**: rank queries as scores
  change.
- **Percentile estimation** (approx quantile).
- **Financial tick data**: "how many prices below $X in the last
  hour?"

Python's `sortedcontainers.SortedList` gives you this in constant
factors that beat pure BSTs, by storing buckets in memory arrays.
But the Big-O is the same.

---

## 7. When AVL specifically wins

Given that red-black is the usual default, when would you specifically
reach for AVL?

- **Workloads with many more lookups than mutations** — AVL's tighter
  balance pays off on the hot reads. Classic example: a mostly-static
  configuration index that gets loaded and then queried billions of
  times.
- **Embedded systems with tight latency tails** — AVL's bound of
  `h ≤ 1.44 log₂ n` is tighter than red-black's `h ≤ 2 log₂(n+1)`,
  so the 99.99th-percentile lookup is a few percent faster.
- **When you need to reason explicitly about height** — academic
  and verified-code settings. The AVL invariant is simpler and
  more mechanically checkable.

For most everyday engineering, red-black is the right default. But
every self-balancing BST is doing the same dance: rotations to keep
h = O(log n), one invariant at a time.
