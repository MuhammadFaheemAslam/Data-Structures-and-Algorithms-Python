# 02 — Sorting

Sorting is arguably the most studied topic in computer science. This
section organizes the classical sorts into **three families**, each
useful for different inputs:

| # | Family                   | Cost               | When it wins                              |
|---|--------------------------|--------------------|-------------------------------------------|
| 1 | **Basic Sorting**        | O(n²)              | Tiny n, already-sorted data, teaching     |
| 2 | **Efficient Sorting**    | O(n log n)         | General-purpose; the practical default    |
| 3 | **Non-Comparison Sorting** | O(n + k) / O(d·n) | Small integer / bounded-range keys        |

The boundary between families matters because **they have different
complexity lower bounds**:

- Comparison-based sorting has a theoretical lower bound of **Ω(n log n)**
  — you can't do better without changing the rules.
- Non-comparison sorts **break that bound** by exploiting the keys'
  structure (digits, value ranges) directly.

So "which sort is fastest?" is the wrong question. The right question is:
*"What's the shape of my input?"*

---

## The Sorting Decision Flowchart

```
Is n small (≤ ~16)?
    → Insertion Sort (adaptive, low overhead, tiny constants)

Are the keys small integers in a known range?
    → Counting Sort  (if k = O(n)) or Radix Sort  (if d is bounded)

Is the distribution uniform over a known range?
    → Bucket Sort  (expected O(n))

Do you need STABILITY?
    → Merge Sort  (stable, guaranteed O(n log n))
    (Or Python's sorted()/Timsort, which is also stable)

Is memory tight?
    → Heap Sort  (O(1) extra, guaranteed O(n log n))
       or Quick Sort  (O(log n) stack, faster in practice)

Anything else?
    → Merge Sort  (or just use Python's sorted() / Timsort)
```

---

## Folder Layout

```
02-Sorting/
├── 01-Basic-Sorting/           ← O(n²) — pedagogical + insertion sort's production niche
│   ├── 01-Bubble-Sort/
│   ├── 02-Selection-Sort/
│   └── 03-Insertion-Sort/
├── 02-Efficient-Sorting/       ← O(n log n) — the practical defaults
│   ├── 01-Merge-Sort/
│   ├── 02-Quick-Sort/
│   └── 03-Heap-Sort/
└── 03-Non-Comparison-Sorting/  ← O(n + k) — break the comparison bound
    ├── 01-Counting-Sort/
    ├── 02-Radix-Sort/
    └── 03-Bucket-Sort/
```

Each algorithm folder typically contains:

- One or more `.py` files — the algorithm and its variants.
- An `analysis.md` (where applicable) — complexity, stability,
  edge-case discussion.
- A `problems/` folder (where applicable) — practice / test problems.

---

## The Four Key Properties of a Sorting Algorithm

Every sort is characterized by four things. When picking a sort, ask
about each one:

| Property       | What it means                                             | Who cares?                    |
|----------------|-----------------------------------------------------------|-------------------------------|
| **Time**       | Big-O best / average / worst                              | Everyone                      |
| **Space**      | Auxiliary memory (not counting the input)                 | Memory-constrained systems    |
| **Stability**  | Preserves order of equal keys                             | Multi-key sorts (name then age) |
| **In place**   | Mutates input with only O(log n) extra space              | Large-array scenarios          |

And three more that matter less often:

- **Adaptive:** faster on already-sorted / nearly-sorted input.
- **Online:** can sort as data arrives (doesn't need to see all of it first).
- **External:** can sort more data than fits in memory.

---

## The Production Landscape

Most real-world sorts aren't any of the "classical" algorithms
unmodified — they're **hybrids** that combine multiple techniques:

| Language / Library       | Sort                 | Composition                              |
|--------------------------|----------------------|------------------------------------------|
| Python (`sorted()`, `.sort()`)  | **Timsort**   | merge sort + insertion sort (runs ≤ 32)  |
| Java `Arrays.sort(Object[])`     | Timsort       | same                                     |
| Java `Arrays.sort(int[])`        | **Dual-pivot Quicksort** | quicksort + insertion sort       |
| C++ `std::sort`                  | **Introsort** | quicksort + heap sort + insertion sort   |
| Rust `Vec::sort`                 | Timsort       | same                                     |
| Rust `Vec::sort_unstable`        | **pdqsort**   | quicksort + heap sort + insertion sort   |

So understanding insertion sort, merge sort, quicksort, and heap sort
isn't just pedagogical — it's the foundation every production sort
builds on. The hybrid algorithms switch BETWEEN the classical ones
based on input size and structure.

---

## Outcome

By the end of this section you should be able to:

1. **Implement any of the 9 sorts from memory.** Bubble, selection,
   insertion, merge, quick, heap, counting, radix, bucket.
2. **Pick correctly.** Given an input shape and constraints, reach
   for the right sort without thinking.
3. **Reason about stability, memory, and worst cases.** Know which
   algorithms can and can't be combined with which constraints.
4. **Recognize hybrid sorts in the wild.** Timsort, introsort, pdqsort
   all become visible as compositions of what you learned here.
