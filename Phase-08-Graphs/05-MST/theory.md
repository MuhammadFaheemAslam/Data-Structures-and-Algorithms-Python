# Minimum Spanning Tree — Theory

Given a CONNECTED, UNDIRECTED, WEIGHTED graph `G = (V, E)`, a
**spanning tree** is a subset of edges that connects every vertex
using exactly `V - 1` edges (no cycles, no extras). A **minimum
spanning tree (MST)** is a spanning tree whose total edge weight is
minimum over all spanning trees.

If the graph has multiple connected components, you can't have a
single spanning tree — you get a **minimum spanning FOREST**, one
tree per component.

```
Graph (undirected, weighted):          One of its MSTs (weight 10):
        4                                     4
   A ─────── B                            A ─────── B
   │         │                            │
   2  │  3        ──▶                        2  │  (skipped)
   │         │                            │
   C ─────── D                            C ─────── D
        1                                     1

Total graph weight = 4 + 2 + 3 + 1 = 10
Spanning tree weight (A-B, A-C, C-D) = 4 + 2 + 1 = 7, but we need 3 edges.
A-B is 4, A-C is 2, C-D is 1; skipping B-D (3). Total = 7.
```

MST has V - 1 edges and no cycles — it's a *tree*.

---

## Where MSTs show up

- **Network design** — minimum-cost cabling between V offices.
- **Clustering** — cut the heaviest edge of an MST recursively to
  split points into clusters (single-link clustering).
- **Approximation algorithms** — MSTs underpin the 2-approximation
  for metric TSP.
- **Image segmentation** — pixel graphs with similarity-based weights.
- **Redundancy analysis** — ANY non-MST edge would form a cycle
  with the MST; the heaviest edge on that cycle is redundant in the
  sense that removing it from the full graph doesn't change
  connectivity.

---

## The two canonical algorithms

### Kruskal's algorithm (edge-centric)

Sort ALL edges by weight ascending. Add edges one by one; add an
edge IFF it doesn't form a cycle with the already-added edges.
Cycle detection is where **Union-Find** (disjoint-set) shines:
two vertices are in the same "connected-so-far" set iff adding the
edge between them would close a cycle.

```
sort edges by weight
uf = UnionFind(vertices)
mst = []
for (u, v, w) in sorted edges:
    if uf.find(u) != uf.find(v):
        uf.union(u, v)
        mst.append((u, v, w))
        if len(mst) == V - 1: break
```

**Time**: O(E log E) for the sort; Union-Find ops are near-constant.
**Good for**: sparse graphs, easy to reason about.

### Prim's algorithm (vertex-centric)

Grow the MST from one starting vertex, always adding the CHEAPEST
edge that connects a tree-vertex to a non-tree-vertex. Under the hood:
a min-heap of "candidate edges from the tree out".

```
heap = [(0, start)]
in_tree = set()
while heap:
    w, u = heappop(heap)
    if u in in_tree: continue
    in_tree.add(u)
    mst.append((predecessor[u], u, w))
    for (v, weight) in neighbours(u):
        if v not in in_tree:
            heappush(heap, (weight, v))
```

**Time**: O((V + E) log V) with a binary heap.
**Good for**: dense graphs (matrix-backed adjacency), or when you
only need the tree from one starting vertex.

---

## Why do they both work? — The cut property

The KEY THEOREM underlying every MST algorithm:

> **Cut Property**: For any cut (partition of V into S and V\S), the
> MINIMUM-WEIGHT edge crossing the cut is in SOME MST.

Kruskal's picks the global cheapest edge that bridges two disjoint
components (which IS a cut). Prim's always picks the cheapest edge
leaving the tree S = "vertices in tree so far". Both exploit the
same theorem; they just define the cut differently.

A corollary is the **Cycle Property**: for any cycle, the
HEAVIEST edge is NOT in ANY MST. (If it were, replacing it with any
other edge on the cycle would give a cheaper spanning tree.)

---

## Kruskal vs Prim — which to pick

| Aspect                         | Kruskal                | Prim                     |
|--------------------------------|------------------------|--------------------------|
| Natural representation         | Edge list               | Adjacency list + heap    |
| Sparse graphs                  | ✓ Usually faster         | Also fine                |
| Dense graphs                   | Edge sort dominates     | ✓ Heap-based             |
| Already-sorted edges           | ✓ Skip the sort          | Can't skip               |
| Parallelizable?                | ✓ Sort + parallel union  | Harder                   |
| MST of a DISCONNECTED graph    | Gives a spanning FOREST  | Only within one component|

Most introductions suggest Prim for dense, Kruskal for sparse —
accurate for classical complexity analysis, but for interview-scale
graphs either works. Kruskal's dependency on Union-Find makes it
the natural "test case" for that data structure (Phase 10).

---

## What's in this module

- [kruskal.py](kruskal.py) — with a small inline Union-Find (full treatment: Phase 10).
- [prim.py](prim.py) — heap-based, returns MST edges.

Both expose `mst(graph)` returning a list of edges. They also expose
`mst_weight(graph)` if you only want the total.
