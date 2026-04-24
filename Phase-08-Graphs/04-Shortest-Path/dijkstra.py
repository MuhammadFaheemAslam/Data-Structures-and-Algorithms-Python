"""
dijkstra.py — Single-Source Shortest Paths With Non-Negative Weights

Dijkstra's algorithm computes shortest paths from a source vertex to
ALL other vertices, in a graph where every edge weight is ≥ 0.

---------------------------------------------------
The Algorithm:

    dist[start] = 0;  dist[other] = ∞
    heap = [(0, start)]                         # (tentative-dist, vertex)
    while heap:
        d, u = heappop(heap)
        if d > dist[u]: continue                # stale entry; already processed
        for (v, w) in neighbours(u):
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                heappush(heap, (dist[v], v))

Each vertex is POPPED at most once (further entries are stale and
skipped). Total pops ≤ V; total pushes = once per edge relax = O(E).
So O((V + E) log V) with a binary heap.

---------------------------------------------------
Why Stale-Entry Handling Matters:

In Dijkstra with a binary heap, we can't DECREASE a vertex's key in
place. Instead, we push a FRESH entry each time we find a better
distance. The old entry is still in the heap — stale — and when it
pops, we notice (`d > dist[u]`) and skip it.

Alternative: an INDEXED priority queue with decrease-key support.
That gives O(V log V + E) (Fibonacci heap) or O((V + E) log V) with
an indexed binary heap. More complex; rarely worth it in Python.

---------------------------------------------------
Non-Negative Weights Required:

With a single negative edge, Dijkstra's "once popped, distance is
final" invariant breaks — a later negative edge could create a
shorter path we've already committed to. Use Bellman-Ford instead.
No warning is raised if you feed negative weights — YOU are
responsible for checking.

---------------------------------------------------
Complexity:

    Time:  O((V + E) log V)
    Space: O(V + E)
"""

import heapq
import os


def _import_graph():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "adjl", os.path.join(os.path.dirname(__file__), "..", "01-Representations", "adjacency-list.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Graph


Graph = _import_graph()


def dijkstra(graph, start):
    """
    Return (dist, parent) where:
        dist[v]   = shortest distance from start to v (or inf if unreachable)
        parent[v] = predecessor of v on a shortest path (or None)

    Time:  O((V + E) log V), Space: O(V).

    Raises ValueError if any edge has negative weight.
    """
    if start not in graph:
        raise KeyError(start)

    dist = {v: float("inf") for v in graph.vertices()}
    parent = {v: None for v in graph.vertices()}
    dist[start] = 0
    heap = [(0, start)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue                                # stale entry
        for v, w in graph.neighbours(u):
            if w < 0:
                raise ValueError(f"Dijkstra: negative edge {u}→{v} weight {w}")
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heapq.heappush(heap, (nd, v))

    return dist, parent


def shortest_path(graph, start, target):
    """
    Return a shortest path [start, ..., target], or None if unreachable.

    Time: O((V + E) log V), Space: O(V).
    """
    dist, parent = dijkstra(graph, start)
    if target not in dist or dist[target] == float("inf"):
        return None
    # Reconstruct
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = parent[node]
    return list(reversed(path))


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Classic example
    #   A ─1─ B ─2─ C
    #   │           │
    #   4          5
    #   │           │
    #   D ──── 1 ── E
    g = Graph()
    for u, v, w in [("A", "B", 1), ("B", "C", 2), ("A", "D", 4),
                     ("C", "E", 5), ("D", "E", 1)]:
        g.add_edge(u, v, weight=w)

    dist, _parent = dijkstra(g, "A")
    assert dist == {"A": 0, "B": 1, "C": 3, "D": 4, "E": 5}

    # Path reconstruction
    assert shortest_path(g, "A", "E") == ["A", "B", "C", "E"] or \
           shortest_path(g, "A", "E") == ["A", "D", "E"]
    # Both paths have total weight 5 — which is returned depends on relax order
    # (deterministic in this graph: A→B→C→E = 1+2+5=8? let's verify
    # Actually: A→D→E = 4+1=5,  A→B→C→E = 1+2+5=8
    # So A→D→E wins
    assert shortest_path(g, "A", "E") == ["A", "D", "E"]

    # Unreachable
    g.add_vertex("X")
    dist, _ = dijkstra(g, "A")
    assert dist["X"] == float("inf")
    assert shortest_path(g, "A", "X") is None

    # Start == target
    dist, _ = dijkstra(g, "A")
    assert dist["A"] == 0
    assert shortest_path(g, "A", "A") == ["A"]

    # Directed graph
    d = Graph(directed=True)
    d.add_edge(0, 1, weight=2); d.add_edge(1, 2, weight=3); d.add_edge(0, 2, weight=6)
    dist, _ = dijkstra(d, 0)
    assert dist == {0: 0, 1: 2, 2: 5}
    assert shortest_path(d, 0, 2) == [0, 1, 2]
    assert shortest_path(d, 2, 0) is None           # no reverse edges

    # Negative edge → raises
    neg = Graph(directed=True)
    neg.add_edge(0, 1, weight=-1)
    try:
        dijkstra(neg, 0)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError on negative edge")

    # Unknown start
    try:
        dijkstra(g, "nowhere")
    except KeyError:
        pass
    else:
        raise AssertionError("expected KeyError")

    # Stress: compare against a brute-force O(V²) Dijkstra
    def brute_dijkstra(graph, start):
        dist = {v: float("inf") for v in graph.vertices()}
        dist[start] = 0
        unvisited = set(graph.vertices())
        while unvisited:
            u = min(unvisited, key=lambda v: dist[v])
            if dist[u] == float("inf"):
                break
            unvisited.remove(u)
            for v, w in graph.neighbours(u):
                if v in unvisited and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
        return dist

    import random
    random.seed(42)
    for _ in range(100):
        V = random.randint(2, 20)
        g = Graph(directed=True)
        for i in range(V):
            g.add_vertex(i)
        for _ in range(random.randint(0, V * 2)):
            u, v = random.sample(range(V), 2)
            g.add_edge(u, v, weight=random.randint(0, 20))

        start = random.randint(0, V - 1)
        fast, _ = dijkstra(g, start)
        slow = brute_dijkstra(g, start)
        assert fast == slow, f"mismatch at V={V}, start={start}"

    print("All tests passed!")
