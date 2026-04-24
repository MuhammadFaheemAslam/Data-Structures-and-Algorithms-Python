# Phase 08 — Graphs

A **graph** is a set of **nodes** (vertices) and **edges** between them.
Almost everything that's a "network" in the real world is a graph:

- Road networks, flight routes, social follow relationships.
- Web page links, dependency graphs, git commit ancestry.
- Chess boards, maze cells, code control-flow.

Trees are the acyclic special case of graphs. The techniques from
Phase 07 — BFS, DFS, recursion — all generalize here; the difference
is that graphs can have **cycles** and **disconnected components**, so
most algorithms need a `visited` set.

---

## What we cover in this phase

| Module                  | Content                                                    |
|-------------------------|------------------------------------------------------------|
| 01-Representations      | Adjacency list, matrix, edge list — tradeoffs             |
| 02-Traversals           | BFS, DFS (recursive & iterative), connected components    |
| 03-Topological-Sort     | Kahn's algorithm and DFS-based; course-schedule, alien-dict |
| 04-Shortest-Path        | BFS (unweighted), Dijkstra, Bellman-Ford, Floyd-Warshall  |
| 05-MST                  | Kruskal (with Union-Find) and Prim                         |
| 06-Advanced             | Cycle detection, SCC, bridges/articulation, bipartite check |

## What's covered in other phases

- **Union-Find**: Phase 10 proper — we USE it in Kruskal here.
- **Tree BFS/DFS on a tree node**: Phase 07, `01-Binary-Tree`.
- **Dynamic programming on DAGs** (longest path, counting paths):
  hinted at in topological sort; full treatment in Phase 09.
- **Graph problems with heavy string/regex preprocessing**:
  Phase 12 (strings).

## Graph vocabulary you'll see throughout

| Term                | Meaning                                               |
|---------------------|-------------------------------------------------------|
| `V`, `E`            | number of vertices / edges                             |
| directed / undirected | edges have/don't have direction                      |
| weighted            | edges carry a numeric cost                             |
| cyclic / DAG        | has cycles / is directed-acyclic                       |
| connected           | every vertex reachable from every other (undirected)   |
| strongly connected  | every vertex reachable from every other (directed)    |
| dense / sparse      | E ≈ V² vs E ≈ V                                       |

## Complexity cheat-sheet (graphs with V vertices, E edges)

| Algorithm                    | Time                       |
|------------------------------|----------------------------|
| BFS / DFS                    | O(V + E)                   |
| Connected components         | O(V + E)                   |
| Topological sort             | O(V + E)                   |
| Dijkstra (binary heap)       | O((V + E) log V)           |
| Bellman-Ford                 | O(V · E)                   |
| Floyd-Warshall               | O(V³)                      |
| Kruskal MST (with Union-Find)| O(E log E)                 |
| Prim MST (binary heap)       | O((V + E) log V)           |
| Tarjan SCC / bridges         | O(V + E)                   |

The "BFS/DFS is O(V + E)" point is the bedrock: it applies to
traversal, cycle detection, bipartite check, connected components,
and topological sort (the DFS variant). Many tree algorithms you've
seen are this O(V + E) with `V = n`, `E = n - 1`.

## Recommended order

01 → 02 → 03 → 05 → 04 → 06.

Shortest-path (04) is the module with the deepest theoretical content,
and it's worth doing AFTER topological sort and MST since both are
simpler and build intuition for weighted-graph reasoning.
