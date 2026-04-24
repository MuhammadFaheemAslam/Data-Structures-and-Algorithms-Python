# Shortest Path — Theory

Given a graph and two vertices `s` and `t`, the SHORTEST PATH problem
asks for a path from s to t whose total cost is minimum. The
definition of "cost" depends on the graph:

- Unweighted: number of edges.
- Weighted: sum of edge weights.

Depending on the graph's properties (directed?, weighted?, negative
weights?, dense?), different algorithms are optimal:

| Graph type                                    | Algorithm            | Time                   |
|-----------------------------------------------|----------------------|------------------------|
| Unweighted (weights = 1)                       | BFS                  | O(V + E)               |
| Non-negative weights                           | Dijkstra             | O((V + E) log V)       |
| Arbitrary weights (may be negative, no neg cycle) | Bellman-Ford    | O(V · E)               |
| All-pairs, moderate V                          | Floyd-Warshall       | O(V³)                  |
| DAG (any weights)                              | Topo-order relax     | O(V + E)               |
| Non-negative, dense, large V                   | Dijkstra + Fibonacci heap | O(E + V log V)    |

---

## The core operation — "relax"

Every shortest-path algorithm is built on **edge relaxation**:

```
relax(u, v):
    if dist[u] + weight(u, v) < dist[v]:
        dist[v] = dist[u] + weight(u, v)
        parent[v] = u
```

"Going through u to reach v is shorter than what I had before —
update my estimate." The differences between algorithms are in
WHICH ORDER they relax edges.

- **BFS**: relaxes in BFS order (layer by layer).
- **Dijkstra**: relaxes in order of current shortest-distance
  estimate (priority queue).
- **Bellman-Ford**: relaxes every edge, V - 1 times.
- **Floyd-Warshall**: relaxes every pair through every intermediate
  vertex.
- **DAG topo-relax**: relaxes in topological order.

---

## Why Dijkstra needs non-negative weights

Dijkstra's invariant: once a vertex is popped from the priority queue,
its distance is FINAL. The argument:

> "This vertex's distance is `d`. Any UNPROCESSED path to it must go
>  through some other unprocessed vertex w, whose current estimate is
>  ≥ d (because we pop smallest first). Adding more non-negative
>  edges can only grow the total. So no better path exists."

The moment you allow a NEGATIVE edge, the step "adding more edges can
only grow the total" breaks — a later negative edge could shorten the
path below `d`. Dijkstra would miss it.

For graphs with negative weights, use **Bellman-Ford** (which also
detects negative cycles — crucial in currency-arbitrage or any
"infinite profit loop" setup).

---

## Why Bellman-Ford's V - 1 passes?

A shortest path has at most V - 1 edges (no repeated vertices in
optimal paths — if it repeats, you can cut the loop and shorten
unless it's a negative cycle). So after V - 1 rounds of "relax every
edge", every shortest-path prefix of length ≤ V - 1 has been
relaxed into `dist`. If we do a V-th round and STILL relax something,
there's a negative cycle.

---

## Floyd-Warshall — the all-pairs hammer

Instead of running Dijkstra V times from every vertex, compute all
V² shortest paths in a single O(V³) triple-loop:

```
dist[i][j] = weight(i, j)    or ∞ if no edge
for k in V:
    for i in V:
        for j in V:
            dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
```

The `k` loop is outermost: "using only vertices 0..k as intermediates,
what's the shortest path from i to j?". After all V iterations of k,
every vertex is available as an intermediate — so `dist[i][j]` is
the final shortest path.

Handles negative weights (no negative cycles). For V ≤ few hundred,
Floyd-Warshall is often the simplest + fastest option, even though
its Big-O is worse than Dijkstra's.

---

## Unweighted = BFS. Don't overthink it.

If all weights are equal (including weight-1 unweighted), BFS is
strictly superior to Dijkstra: same result, no heap overhead,
trivial implementation. Phase 07's `bfs_distances` is your
shortest-path function.

If weights are all 0 or 1 (rare), the **0-1 BFS** variant uses a
deque and runs in O(V + E) — a niche but useful trick.

---

## What's in this module

- [bfs-unweighted.py](bfs-unweighted.py) — shortest-path special case with weights = 1.
- [dijkstra.py](dijkstra.py) — classic non-negative-weight shortest path.
- [bellman-ford.py](bellman-ford.py) — single-source shortest path + negative cycle detection.
- [floyd-warshall.py](floyd-warshall.py) — all-pairs shortest path.
- [problems/network-delay-time.py](problems/network-delay-time.py) — LC #743, straight Dijkstra.
- [problems/cheapest-flights-k-stops.py](problems/cheapest-flights-k-stops.py) — LC #787, "at most K stops" is the subtle twist.
