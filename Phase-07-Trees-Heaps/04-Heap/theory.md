# Binary Heap — Theory

A **binary heap** is a complete binary tree stored in a FLAT ARRAY,
with the property that every parent's value is ≤ its children's (a
**min-heap**), or ≥ (a **max-heap**). The heap gives you O(1) access
to the min (or max) and O(log n) insert / extract, which makes it the
canonical backing data structure for a **priority queue**.

```
Min-heap:                     Array representation:
       1                      [1, 3, 5, 4, 8, 7, 9]
      / \                      0  1  2  3  4  5  6
     3   5
    / \ / \
   4  8 7  9
```

---

## The array trick — why a heap doesn't need pointers

For a node at index `i` in the array:

```
parent(i) = (i - 1) // 2
left(i)   = 2*i + 1
right(i)  = 2*i + 2
```

A complete tree's level-order flattening IS the array — no `left`/
`right` pointers, no memory allocation per node. Cache-friendly,
easy to resize (just `append` / `pop`), and `heapify` can re-
structure a whole array in-place.

This works ONLY for COMPLETE trees. General BSTs can't be stored
this way because they have arbitrary gaps.

---

## The two basic operations

### `sift_up(i)` — used after insertion

Append the new element to the END of the array, then bubble it
UPWARD while it's smaller than its parent:

```
while i > 0 and heap[parent(i)] > heap[i]:
    swap(heap, i, parent(i))
    i = parent(i)
```

Each iteration moves the element up one level. Tree height is
`log n`, so at most `log n` comparisons and swaps. **O(log n)**.

### `sift_down(i)` — used after extracting the root

Replace the root with the LAST element; shrink the array; then
bubble the new root DOWNWARD while it's greater than its smallest
child:

```
while i has a child:
    pick smaller child j
    if heap[j] < heap[i]:
        swap(heap, i, j)
        i = j
    else: break
```

Also **O(log n)**.

---

## `heapify` — why it's O(n), not O(n log n)

Given an arbitrary array, you can convert it into a valid heap in
O(n) by running `sift_down` from index `n//2 - 1` backwards to 0:

```
def heapify(arr):
    for i in range(len(arr) // 2 - 1, -1, -1):
        sift_down(arr, i)
```

Naïve analysis: we run `sift_down` on n/2 elements, each O(log n)
→ seemingly O(n log n). But the actual cost is bounded by the sum
of heights of nodes in a complete tree, which is **O(n)** — most
nodes are near the bottom and cost O(1) each.

Formally:
```
    Σ (h=0 to log n) ⌈n / 2^(h+1)⌉ · h  =  O(n)
```

This is why heapsort runs in O(n log n) with **O(n)** setup cost —
and why "heapify-then-extract-all" beats "push-all-then-extract-all"
by a constant factor.

---

## Complexities

| Operation             | Time        | Notes                                  |
|-----------------------|-------------|----------------------------------------|
| `peek` / `top`        | O(1)        | root is always at index 0              |
| `push`                | O(log n)    | sift up                                |
| `pop` (extract root)  | O(log n)    | sift down                              |
| `heapify` (build)     | O(n)        | bottom-up sift-down                    |
| `heapsort`            | O(n log n)  | heapify + n extractions                |
| Find arbitrary key    | O(n)        | no order on siblings                   |
| Delete arbitrary key  | O(n)  (find) + O(log n) (fix) | O(log n) if you already know the index |
| Merge two heaps       | O(n)        | no faster way for binary heaps         |

---

## Min-heap vs max-heap

They're symmetric — swap all comparisons. Python's `heapq` is ONLY
a min-heap; to get a max-heap, you negate values on push and pop.
See `implementation/max-heap.py` for that trick.

---

## Where heaps show up

- **Priority queues** — job scheduling, packet routing, simulations.
- **Dijkstra / Prim / A\*** — every graph-algorithm intro. Phase 08.
- **Top-K selection** — LC #215, #347, #703. See `problems/k-largest.py`.
- **Median-of-stream** — two heaps in opposing orientations.
  See `problems/find-median.py`.
- **Heap sort** — in-place O(n log n) sort. See `heap-sort.py`.

Anywhere you'd say "give me the next smallest / largest, repeatedly",
a heap is the first data structure to reach for.

---

## Heap vs. sorted list vs. BST

| Need                      | Heap     | Sorted list | BST      |
|---------------------------|----------|-------------|----------|
| Peek min/max              | O(1)     | O(1)        | O(log n) |
| Insert                    | O(log n) | O(n)        | O(log n) |
| Remove min/max            | O(log n) | O(1)        | O(log n) |
| Search arbitrary          | O(n)     | O(log n)    | O(log n) |
| Range queries             | ❌       | O(log n + k) | O(log n + k) |
| In-order scan             | ❌       | O(n)        | O(n)     |
| Cache behaviour           | ✓✓✓      | ✓           | ✗        |

Rule: **if you only need one end** (just min or just max) and don't
care about ordering the rest, heap. If you need search, BST. If you
rarely insert and often scan, sorted list.

---

## What's in this module

- `implementation/min-heap.py` — `MinHeap` class from scratch.
- `implementation/max-heap.py` — `MaxHeap` class (mirror).
- `implementation/heapify.py` — the standalone `heapify` routine
  + proof that it's O(n).
- `priority-queue.py` — priority queue built on top of a min-heap,
  supporting priority updates and stable ordering.
- `heap-sort.py` — in-place O(n log n) heapsort.
- `problems/` — the five canonical heap problems (top-k, merge-k,
  median, task-scheduler).
