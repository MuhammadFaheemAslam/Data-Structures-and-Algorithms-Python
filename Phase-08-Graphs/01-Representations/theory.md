# Graph Representations — Theory

A graph of `V` vertices and `E` edges can be stored in three main
ways. The choice isn't purely aesthetic — different representations
make different operations cheap, and picking the wrong one turns an
O(V + E) algorithm into O(V²) or worse.

---

## The three representations

### 1. Adjacency list

For each vertex `u`, store a list of its neighbours:

```
adj[0] = [1, 2]
adj[1] = [0, 3]
adj[2] = [0]
adj[3] = [1]
```

**Memory**: O(V + E). Each edge appears once (directed) or twice
(undirected). This is the workhorse — 95% of the time, "graph"
means "adjacency list" unless you say otherwise.

**Cheap**: iterate neighbours of u → O(deg(u)).
**Expensive**: "is there an edge u → v?" → O(deg(u)).

### 2. Adjacency matrix

A V×V boolean (or weight) matrix where `M[u][v]` is 1 (or the
edge weight) iff there's an edge from u to v.

```
     0  1  2  3
  0  0  1  1  0
  1  1  0  0  1
  2  1  0  0  0
  3  0  1  0  0
```

**Memory**: O(V²) — INDEPENDENT of how many edges you actually have.

**Cheap**: "is there an edge u → v?" → O(1). Matrix-algebra on paths
(e.g. reachability via powers of the matrix) is possible.
**Expensive**: iterating neighbours of u → O(V), even if u has only
1 neighbour.

Good for **DENSE** graphs (E ≈ V²) or when you do lots of edge-
existence queries. Small, fixed V. Floyd-Warshall uses this.

### 3. Edge list

A list of `(u, v)` or `(u, v, weight)` tuples.

```
edges = [(0, 1), (0, 2), (1, 3)]
```

**Memory**: O(E).

**Cheap**: iterate ALL edges.
**Expensive**: "neighbours of u" → O(E) scan.

Good for algorithms that process every edge: **Kruskal's MST**,
**Bellman-Ford**, or as an I/O format for converting to another rep.

---

## When to pick which

| Need                          | Best rep            |
|-------------------------------|---------------------|
| BFS / DFS / traversals        | Adjacency list      |
| Edge-existence O(1) queries   | Adjacency matrix    |
| Lots of edges, dense graph    | Adjacency matrix    |
| Small V (≤ few hundred)       | Any (matrix is fine)|
| Huge sparse graph             | Adjacency list      |
| Floyd-Warshall                | Adjacency matrix    |
| Kruskal, Bellman-Ford         | Edge list           |
| Streaming edges from a file   | Edge list           |

---

## Directed vs undirected (and how each rep encodes it)

- **Directed**: an edge u → v is stored once. In adjacency list,
  only `adj[u]` contains v. In matrix, only `M[u][v] = 1`.
- **Undirected**: store each edge BOTH ways. `adj[u].append(v)` AND
  `adj[v].append(u)`. In matrix, both `M[u][v]` and `M[v][u]` are set.

**Watch out**: an undirected edge list still stores each edge ONCE.
If your algorithm expects to see every directed edge and you feed
it an undirected edge list, you'll miss half the "neighbour"
connections.

---

## Weights

For weighted graphs:

- **Adjacency list**: store `(neighbour, weight)` tuples instead of
  bare neighbours. `adj[u] = [(v, 5), (w, 2)]`.
- **Adjacency matrix**: `M[u][v] = weight`, with a sentinel
  (usually `inf` or 0, depending on convention) meaning "no edge".
- **Edge list**: `(u, v, weight)` triples.

Negative weights are legal for some algorithms (Bellman-Ford)
but not others (Dijkstra). Module 04-Shortest-Path has the full
discussion.

---

## Practical Python-isms

- Use `defaultdict(list)` for adjacency lists — no explicit key
  initialization.
- `set()` of edges is useful for dedup when building the graph
  from a raw edge stream.
- For dense matrices, `numpy` is ~10× faster than nested lists,
  but we stick with pure Python for clarity in this phase.
- Vertex identifiers can be ANYTHING hashable (strings, tuples, ints).
  Our implementations default to ints 0..V-1 for ergonomics.

---

## What's in this module

- [adjacency-list.py](adjacency-list.py) — the default graph class
  we use throughout Phase 08.
- [adjacency-matrix.py](adjacency-matrix.py) — same API; matrix-backed.
  Lets us show memory/query differences side-by-side.
- [edge-list.py](edge-list.py) — a minimal "graph as edges"
  container, plus conversion helpers to/from the other two.
