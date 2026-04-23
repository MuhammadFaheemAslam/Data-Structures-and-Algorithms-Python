# Phase 03 — Searching & Sorting

Phase 01 gave you the built-in tools. Phase 02 gave you the paradigms
and techniques. Phase 03 is about the **classical algorithms every
interview expects** — the ones so fundamental that they have names
from the 1950s and 60s and are still the right answers today.

Two families, each housed in its own umbrella folder:

1. **Searching** (`01-Searching/`) — finding one or more values inside a collection.
2. **Sorting** (`02-Sorting/`) — rearranging a collection into a chosen order.

Both families are large because they're so foundational. Almost every
downstream algorithm in Phase 04+ (trees, graphs, DP) either builds on
these directly or assumes you know them cold.

The two umbrellas keep each half discoverable as a single unit. Within
**Sorting**, we further split by complexity family: basic (O(n²)),
efficient (O(n log n)), and non-comparison (O(n + k)).

---

## What This Phase Covers

### 01 — Searching

| # | Algorithm            | Core idea                                          |
|---|----------------------|----------------------------------------------------|
| 1 | Linear Search        | Scan left to right. The baseline.                  |
| 2 | Binary Search        | Halve the search range; the O(log n) classic.      |
| 3 | Jump Search          | Jump √n at a time, then linear within the block.   |
| 4 | Exponential Search   | Double the range until overshoot, then binary.     |
| 5 | Ternary Search       | Divide by three; for unimodal functions.           |

Binary Search alone has enough depth for a whole module — four
canonical *variations* (first/last occurrence, lower/upper bound) and
classic problems (rotated array, peak element, integer square root).
We'll treat it with that depth.

### 02 — Sorting (see [`02-Sorting/README.md`](02-Sorting/README.md) for details)

All sorts live under one umbrella, organized by complexity family:

#### 02 / 01 — Basic Sorting — O(n²)

| # | Algorithm       | Why it exists                                         |
|---|-----------------|-------------------------------------------------------|
| 1 | Bubble Sort     | The "first sort anyone learns"; terrible in practice. |
| 2 | Selection Sort  | O(n²) but O(n) swaps — rare edge-case use.            |
| 3 | Insertion Sort  | Adaptive; the fastest sort for nearly-sorted data or tiny n. |

These exist for pedagogical reasons and still appear in interviews.
Also, insertion sort is the inner routine of production sorts like
Timsort (for runs ≤ 32 elements), so understanding it is not wasted.

#### 02 / 02 — Efficient Sorting — O(n log n)

| # | Algorithm   | Key property                                                |
|---|-------------|-------------------------------------------------------------|
| 1 | Merge Sort  | Guaranteed O(n log n), stable, O(n) extra space.            |
| 2 | Quick Sort  | Fast in practice, in place, O(n²) worst case, unstable.     |
| 3 | Heap Sort   | Guaranteed O(n log n), in place, unstable; uses a heap.     |

The three efficient sorts are the ones you'll reach for in real code.
Python's `list.sort()` is **Timsort** — a hybrid merge/insertion sort
that builds on these foundations.

#### 02 / 03 — Non-Comparison Sorting — O(n + k)

| # | Algorithm       | When it beats comparison sorts                       |
|---|-----------------|------------------------------------------------------|
| 1 | Counting Sort   | Small integer keys; k = max value.                   |
| 2 | Radix Sort      | Fixed-width integers / strings; O(d · n).            |
| 3 | Bucket Sort     | Uniformly distributed floats; good average case.     |

These break the O(n log n) lower bound for comparison sorts by not
comparing elements — they use the keys' STRUCTURE directly (digits,
value ranges, buckets). They dominate comparison sorts on the right
inputs, but are useless on general data.

---

## Why This Phase Matters

Searching and sorting are the most **frequently invoked** primitives
in computer science. They're also the most-asked topics in interviews.
By the end of this phase you should be able to:

- Pick the right search algorithm based on input shape (sorted /
  unsorted, small / big, cached / streaming).
- Pick the right sort based on data properties (comparison / key-based,
  need for stability, in-place vs extra memory, worst-case guarantees).
- Implement any of the 14 algorithms above from memory in under five
  minutes.
- Recognize Timsort, introsort, pdqsort, and other hybrid algorithms
  as **compositions** of the primitives in this phase.

---

## The Sorting Decision Flowchart

```
Is the input small (n ≤ 16)?
    → Insertion Sort
    (used as the base case of many production sorts)

Is the key a small integer in a known range?
    → Counting Sort  (k ≤ ~10n)  or  Radix Sort  (integers, strings)

Is the distribution uniform over a known range?
    → Bucket Sort

Do you need STABILITY?
    → Merge Sort  (or stable variants of Quick Sort / Heap Sort,
                    which don't exist natively)

Is memory tight?
    → Quick Sort  (in place)  or  Heap Sort  (in place, guaranteed O(n log n))

Anything else?
    → Merge Sort  (or Python's sorted() / Timsort)
```

---

## Folder Layout

```
Phase-03-Searching-Sorting/
├── README.md                          ← you are here
├── 01-Searching/
│   ├── README.md                      ← searching decision flowchart + complexity matrix
│   ├── 01-Linear-Search/
│   ├── 02-Binary-Search/              ← has variations/ and problems/ subfolders
│   ├── 03-Jump-Search/
│   ├── 04-Exponential-Search/
│   └── 05-Ternary-Search/
└── 02-Sorting/
    ├── README.md                      ← sorting decision flowchart + property matrix
    ├── 01-Basic-Sorting/              ← O(n²)
    │   ├── 01-Bubble-Sort/
    │   ├── 02-Selection-Sort/
    │   └── 03-Insertion-Sort/
    ├── 02-Efficient-Sorting/          ← O(n log n)
    │   ├── 01-Merge-Sort/
    │   ├── 02-Quick-Sort/
    │   └── 03-Heap-Sort/
    └── 03-Non-Comparison-Sorting/     ← O(n + k)
        ├── 01-Counting-Sort/
        ├── 02-Radix-Sort/
        └── 03-Bucket-Sort/
```

Unlike Phase 02 (which had a rigid `theory.md / template.py / problems/`
shape), Phase 03 is structured around CONCRETE IMPLEMENTATIONS. Each
module typically has:

- One or more `.py` files — the algorithm and its variants.
- An `analysis.md` (for basic sorts) — detailed complexity / stability /
  edge-case discussion.
- A `problems/` or `problems.md` — practice / test problems.

Some modules have additional structure (e.g., `variations/` for binary
search, extra variants like `random-pivot.py` for quick sort) that
reflects the algorithm's internal richness.

---

## Outcome

By the end of this phase you should be able to:

1. **Choose correctly.** Given a problem and its input shape, pick
   the fastest appropriate search or sort in under 30 seconds.
2. **Implement from memory.** Each of the 14 algorithms should be
   writable without notes.
3. **Reason about stability, memory, and worst cases.** Know which
   algorithms can and can't be combined with other constraints.
4. **Recognize hybrid algorithms in the wild.** Timsort, introsort,
   pdqsort, and production sorts are all visible as compositions of
   the primitives here.
