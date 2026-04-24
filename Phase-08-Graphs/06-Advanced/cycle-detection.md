# Cycle Detection — Theory

Detecting cycles is a basic graph question with surprisingly different
algorithms depending on the graph's type.

---

## Undirected graphs

A cycle in an undirected graph is an alternating sequence of vertices
and edges that starts and ends at the same vertex, with every edge
USED ONCE. The simplest cycle: `u → v → u` via a single edge —
but that's not counted because the edge is repeated. The smallest
real cycle is a triangle: three distinct vertices in a loop.

### BFS / DFS with a parent pointer

```python
def has_cycle_undirected(graph):
    visited = set()
    def dfs(u, parent):
        visited.add(u)
        for v in neighbours(u):
            if v not in visited:
                if dfs(v, u):
                    return True
            elif v != parent:           # visited, and not the edge we came from → cycle
                return True
        return False
    return any(dfs(u, None) for u in vertices if u not in visited)
```

Key idea: if DFS encounters an ALREADY-VISITED neighbour that ISN'T
our parent in the DFS tree, we've found a back-edge — a cycle.

Time O(V + E), Space O(V).

### Union-Find

Alternative: process every edge; if the two endpoints are already in
the same set, we've closed a cycle. Otherwise, union them.

```python
def has_cycle_uf(graph):
    uf = UnionFind(vertices)
    for (u, v) in edges:
        if uf.connected(u, v):
            return True
        uf.union(u, v)
    return False
```

Same Big-O, different constants. Useful when edges arrive as a STREAM
and you can't easily do a full DFS.

---

## Directed graphs

"Cycle" in a directed graph means a directed sequence u₁ → u₂ → ...
→ uₖ → u₁. The undirected "skip the parent" trick doesn't work —
a back-edge through the parent is a legitimate 2-cycle.

### DFS three-color

```
WHITE — unvisited
GRAY  — on the current DFS recursion stack
BLACK — finished (subtree fully explored)

def dfs(u):
    color[u] = GRAY
    for v in neighbours(u):
        if color[v] == GRAY: return CYCLE   # back-edge to stack
        if color[v] == WHITE and dfs(v):
            return CYCLE
    color[u] = BLACK
    return NO_CYCLE
```

Seeing a GRAY neighbour means we've looped back to an ancestor on
the current DFS path. That IS the cycle.

O(V + E), O(V).

Already implemented in `03-Topological-Sort/dfs-based.py` —
topological sort and directed-cycle-detection are THE SAME algorithm;
the topo sort fails exactly when a cycle is present.

### Kahn's algorithm (in-degree BFS)

Process vertices with in-degree 0, decrement in-degrees as you emit.
If fewer than V vertices emitted, there's a cycle.

Implemented in `03-Topological-Sort/kahn-bfs.py`.

---

## Special case: self-loops

A self-loop `u → u` is a length-1 cycle. Most algorithms handle it
naturally:

- Undirected DFS: self-loop makes `v == parent = u`, but by the
  "not the parent" test above, it's a cycle EXCEPT that you need
  a small guard — convention varies. Some implementations count
  self-loops, some don't. We count them.
- Directed three-color DFS: visiting u → u sees u as GRAY → CYCLE.
  Works out.
- Kahn's: u → u gives indeg[u] += 1. Never reaches 0, never emits.
  CYCLE detected correctly.

---

## Special case: multi-edges in undirected graphs

If we allow PARALLEL edges (two distinct edges between u and v),
the "skip parent" heuristic needs to be careful. Our `adjacency-list.py`
uses a dict-of-dicts, which disallows parallel edges by design —
re-adding an edge just updates the weight. So parallel-edge cycles
aren't a concern for us.

---

## Where this shows up

- Detecting DEADLOCKS in operating systems — the "wait-for graph" of
  processes waiting on resources. Cycle = deadlock.
- Detecting DEPENDENCY CYCLES in build systems, imports, schemas.
- Detecting CURRENCY ARBITRAGE — a negative-cost cycle in an
  exchange-rate graph. (See 04-Shortest-Path/bellman-ford.py.)
- Garbage collection — unreachable reference cycles.
- Detecting when a binary relation is NOT a valid partial order
  (it should be a DAG).

---

## Cross-reference

Cycle detection in **directed** graphs is covered in:

- [03-Topological-Sort/kahn-bfs.py](../03-Topological-Sort/kahn-bfs.py) — `has_cycle`
- [03-Topological-Sort/dfs-based.py](../03-Topological-Sort/dfs-based.py) — `has_cycle_dfs`

In **undirected** graphs, the DFS-with-parent variant is about
15 lines — implement it as an exercise. A Union-Find version appears
implicitly in Kruskal's MST: if `union(u, v)` returns False, adding
(u, v) would have closed a cycle.

For NEGATIVE cycles in weighted directed graphs:

- [04-Shortest-Path/bellman-ford.py](../04-Shortest-Path/bellman-ford.py) — V-th pass
- [04-Shortest-Path/floyd-warshall.py](../04-Shortest-Path/floyd-warshall.py) — `has_negative_cycle`
