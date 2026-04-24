"""
floyd-warshall.py — All-Pairs Shortest Paths

Floyd-Warshall computes the shortest path between EVERY PAIR of
vertices in O(V³) time and O(V²) space. One triple-loop, no heaps,
handles negative weights (just not negative cycles).

---------------------------------------------------
The Algorithm:

    dist[i][j] = w(i, j) if edge exists, else ∞
    dist[i][i] = 0

    for k in 0..V-1:
        for i in 0..V-1:
            for j in 0..V-1:
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

---------------------------------------------------
Why The `k` Loop Is OUTERMOST:

The invariant after iteration k of the outer loop is:

    "dist[i][j] is the shortest path from i to j USING ONLY
    VERTICES 0..k AS INTERMEDIATES."

After all V iterations, every vertex is available as an intermediate
→ dist[i][j] is the final shortest path.

This is a beautiful dynamic-programming formulation. Ask yourself:
"the shortest path from i to j is either (a) doesn't use vertex k,
already computed, or (b) uses k: i→k→j." Take the min.

---------------------------------------------------
When To Use It:

    - V is small (≤ few hundred). V³ grows fast.
    - You need ALL pairs (not just one source).
    - You want ONE short function for simplicity (it's 3 lines + init).
    - You may have negative weights (but not negative cycles).

For "single source, many queries" on large graphs, running Dijkstra
V times is usually faster — O(V · (V + E) log V).

---------------------------------------------------
Negative Cycle Detection:

After running the main loop, any vertex `v` with `dist[v][v] < 0`
is on a negative cycle. We expose this as a separate helper.

---------------------------------------------------
Complexity:

    Time:  O(V³)
    Space: O(V²)
"""

import os


def _import_graph():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "adjl", os.path.join(os.path.dirname(__file__), "..", "01-Representations", "adjacency-list.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Graph


Graph = _import_graph()


def floyd_warshall(graph):
    """
    Return a dict-of-dicts `dist[u][v]` = shortest-path distance
    (inf if no path, possibly negative if the graph allows).

    Does NOT check for negative cycles. Use `has_negative_cycle` for that.

    Time:  O(V³), Space: O(V²).
    """
    vertices = list(graph.vertices())
    INF = float("inf")

    dist = {u: {v: INF for v in vertices} for u in vertices}
    for u in vertices:
        dist[u][u] = 0
    for u, v, w in graph.edges():
        # For undirected graphs, graph.edges() yields each edge once, but
        # the underlying adjacency is symmetric. To be safe, fill both ways
        # if the graph is undirected.
        dist[u][v] = min(dist[u][v], w)
        if not graph.is_directed():
            dist[v][u] = min(dist[v][u], w)

    for k in vertices:
        for i in vertices:
            # Tiny optimization: if dist[i][k] is inf, inner loop can't help
            if dist[i][k] == INF:
                continue
            for j in vertices:
                nd = dist[i][k] + dist[k][j]
                if nd < dist[i][j]:
                    dist[i][j] = nd

    return dist


def has_negative_cycle(graph):
    """
    True iff the graph has a negative cycle. O(V³).
    """
    dist = floyd_warshall(graph)
    return any(dist[v][v] < 0 for v in dist)


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Small graph
    #       1 — 3 — 2
    #   0 <            > 3
    #       5 — 1 — 4
    g = Graph(directed=True)
    for u, v, w in [(0, 1, 3), (1, 2, 2), (2, 3, 4),
                     (0, 2, 10), (1, 3, 8), (0, 3, 15)]:
        g.add_edge(u, v, weight=w)

    dist = floyd_warshall(g)
    # Shortest paths:
    #   0→1 = 3 (direct)
    #   0→2 = 3+2 = 5 (via 1) — beats direct 10
    #   0→3 = 3+2+4 = 9 (via 1, 2) — beats 3+8=11 and 15
    assert dist[0][1] == 3
    assert dist[0][2] == 5
    assert dist[0][3] == 9
    assert dist[0][0] == 0
    assert dist[3][0] == float("inf")              # no path back

    # Undirected
    g = Graph()
    for u, v, w in [(0, 1, 2), (1, 2, 3), (2, 3, 1), (3, 0, 10)]:
        g.add_edge(u, v, weight=w)
    dist = floyd_warshall(g)
    # 0 → 3 directly = 10; but 0 → 1 → 2 → 3 = 2+3+1 = 6
    assert dist[0][3] == 6
    assert dist[3][0] == 6                         # symmetric in undirected

    # Negative weights (no cycle)
    g = Graph(directed=True)
    for u, v, w in [("a", "b", 5), ("b", "c", -3), ("c", "d", 2)]:
        g.add_edge(u, v, weight=w)
    dist = floyd_warshall(g)
    assert dist["a"]["d"] == 4
    assert not has_negative_cycle(g)

    # Negative cycle
    g = Graph(directed=True)
    for u, v, w in [(0, 1, 1), (1, 2, -3), (2, 0, 1)]:
        g.add_edge(u, v, weight=w)                 # cycle weight -1
    assert has_negative_cycle(g)

    # Empty graph
    empty = Graph()
    assert floyd_warshall(empty) == {}
    assert not has_negative_cycle(empty)

    # Single vertex
    one = Graph()
    one.add_vertex("lonely")
    d = floyd_warshall(one)
    assert d["lonely"]["lonely"] == 0
    assert not has_negative_cycle(one)

    # Stress: cross-check with Dijkstra (non-negative graphs)
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "dijk", os.path.join(os.path.dirname(__file__), "dijkstra.py"))
    dijk = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dijk)

    import random
    random.seed(42)
    for _ in range(50):
        V = random.randint(2, 10)
        g = Graph(directed=True)
        for i in range(V):
            g.add_vertex(i)
        for _ in range(random.randint(0, V * 2)):
            u, v = random.sample(range(V), 2)
            g.add_edge(u, v, weight=random.randint(0, 20))

        fw = floyd_warshall(g)
        for src in range(V):
            dj, _ = dijk.dijkstra(g, src)
            for tgt in range(V):
                assert fw[src][tgt] == dj[tgt]

    print("All tests passed!")
