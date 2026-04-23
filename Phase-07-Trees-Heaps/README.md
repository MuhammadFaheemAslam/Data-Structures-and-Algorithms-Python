# Phase 07 — Trees & Heaps

Hierarchical data structures, where each node has a parent and zero or
more children. Trees are the first data structure where *recursion*
stops being a technique you can avoid and becomes the natural way to
reason.

This phase builds five tree-family structures from scratch:

| Module            | What it is                                               |
|-------------------|----------------------------------------------------------|
| 01-Binary-Tree    | The generic shape. Traversals, properties, construction. |
| 02-BST            | Binary tree with an ordering invariant — O(log n) search.|
| 03-AVL-Tree       | Self-balancing BST — *guaranteed* O(log n).              |
| 04-Heap           | Array-backed binary tree for priority queues + heapsort. |
| 05-Trie           | Branching tree keyed by string prefixes.                 |

## What we cover vs. what's elsewhere

Topics with a natural home in earlier/later phases — we reference them,
not re-explain:

- **Graph traversal (BFS/DFS on general graphs)**: Phase 08. A tree is
  the acyclic special case; BFS/DFS there is *strictly* more general
  than our level-order / DFS here.
- **Red-Black trees & B-trees**: Phase 11 (advanced trees).
- **Segment trees / Fenwick trees**: Phase 11.
- **`heapq` (Python's built-in)**: we USE it in Phase 03's heap sort
  and Phase 06's top-k-frequent; here we build one from scratch.
- **Priority queue problem archetypes**: Phase 02 introduces the
  pattern; module 04-Heap here instantiates it with the full data
  structure.

## Suggested order

01 → 02 → 04 covers the minimum viable interview prep. AVL (03) is a
deeper dive on balancing — safe to skip on a first pass and return to
before your first "system design with latency guarantees" interview.
Tries (05) stand alone; do them whenever strings become your problem.

## Complexity cheat-sheet

| Operation         | BT (arbitrary) | BST (avg) | BST (worst) | AVL | Binary Heap | Trie           |
|-------------------|----------------|-----------|-------------|-----|-------------|----------------|
| Search            | O(n)           | O(log n)  | O(n)        | O(log n) | O(n) for arbitrary, O(1) for top | O(L), L = key length |
| Insert            | O(n) / O(1) with parent-ptr | O(log n) | O(n) | O(log n) | O(log n) | O(L) |
| Delete            | O(n)           | O(log n)  | O(n)        | O(log n) | O(log n) | O(L) |
| Min / max         | O(n)           | O(log n)  | O(n)        | O(log n) | O(1)     | —              |
| In-order scan     | O(n)           | O(n) sorted | O(n) sorted | O(n) sorted | —    | —              |
