"""
bellman-ford.py — Single-Source Shortest Paths With (Possibly Negative) Weights

Bellman-Ford handles graphs that Dijkstra can't: those with NEGATIVE
edge weights. It also DETECTS negative cycles, which is the killer
feature for applications like currency-arbitrage and game-loop
exploits.

---------------------------------------------------
The Algorithm:

    dist[start] = 0;  dist[other] = ∞
    for i = 1..V - 1:                     # V - 1 rounds
        for each edge (u, v, w):
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # One more pass to detect negative cycles:
    for each edge (u, v, w):
        if dist[u] + w < dist[v]:
            NEGATIVE CYCLE DETECTED

Any shortest path has at most V - 1 edges. Each full-edge-pass
relaxes every "one-more-edge" extension. After V - 1 passes, we've
found every shortest path of length ≤ V - 1 edges. A V-th round that
still relaxes something means some vertex's distance can be
decreased indefinitely → negative cycle on the path to it.

---------------------------------------------------
Why Use It Instead Of Dijkstra?

Dijkstra is O((V + E) log V); Bellman-Ford is O(V · E). Factor of V
slower. You ONLY reach for Bellman-Ford when Dijkstra can't be
used — i.e. negative weights.

Applications where negative weights arise:
    - Currency exchange rates (log of exchange rates → shortest path = best arbitrage).
    - Network protocols with "credit" or discount edges.
    - Some DP formulations where the cost function allows negative values.

If your graph has non-negative weights, use Dijkstra.

---------------------------------------------------
Complexity:

    Time:  O(V · E)
    Space: O(V)

Returns:
    (dist_dict, parent_dict) if no negative cycle reachable from start,
    else None.
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


def bellman_ford(graph, start):
    """
    Return (dist, parent) or None if a negative cycle is REACHABLE from start.

    Time:  O(V · E), Space: O(V).
    """
    if start not in graph:
        raise KeyError(start)

    dist = {v: float("inf") for v in graph.vertices()}
    parent = {v: None for v in graph.vertices()}
    dist[start] = 0

    V = len(graph)
    edges = list(graph.edges())

    # Phase 1 — V - 1 rounds of edge relaxation
    for _ in range(V - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] != float("inf") and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                changed = True
        if not changed:
            break                                  # optimization: no change this round → done

    # Phase 2 — negative-cycle detection
    for u, v, w in edges:
        if dist[u] != float("inf") and dist[u] + w < dist[v]:
            return None                            # negative cycle reachable from start

    return dist, parent


def shortest_path(graph, start, target):
    """
    Return a shortest path [start, ..., target], or None if unreachable
    or if a negative cycle is present on some path.

    Time:  O(V · E).
    """
    result = bellman_ford(graph, start)
    if result is None:
        return None                                # negative cycle detected
    dist, parent = result
    if dist.get(target, float("inf")) == float("inf"):
        return None
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
    # Non-negative: same answer as Dijkstra
    g = Graph(directed=True)
    for u, v, w in [(0, 1, 2), (1, 2, 3), (0, 2, 6)]:
        g.add_edge(u, v, weight=w)
    dist, _ = bellman_ford(g, 0)
    assert dist == {0: 0, 1: 2, 2: 5}

    # Negative weights (no cycle)
    g = Graph(directed=True)
    for u, v, w in [("s", "a", 5), ("a", "b", -3), ("b", "c", 2), ("s", "c", 7)]:
        g.add_edge(u, v, weight=w)
    dist, _ = bellman_ford(g, "s")
    # s → a → b → c costs 5 + -3 + 2 = 4, vs direct s → c = 7
    assert dist == {"s": 0, "a": 5, "b": 2, "c": 4}

    # Negative cycle → returns None
    g = Graph(directed=True)
    for u, v, w in [(0, 1, 1), (1, 2, -3), (2, 0, 1)]:
        g.add_edge(u, v, weight=w)                 # cycle weight: 1 + -3 + 1 = -1 < 0
    assert bellman_ford(g, 0) is None

    # Negative self-loop
    g = Graph(directed=True)
    g.add_edge(0, 0, weight=-1)
    assert bellman_ford(g, 0) is None

    # Unreachable negative cycle — still returns the dist (cycle isn't from start)
    g = Graph(directed=True)
    for u, v, w in [(0, 1, 1), (2, 3, 1), (3, 2, -10)]:
        g.add_edge(u, v, weight=w)                 # 2↔3 is a negative cycle but not from 0
    dist, _ = bellman_ford(g, 0)
    assert dist[0] == 0 and dist[1] == 1
    assert dist[2] == float("inf") and dist[3] == float("inf")

    # Path reconstruction
    g = Graph(directed=True)
    for u, v, w in [(0, 1, 1), (1, 2, 1), (2, 3, 1), (0, 3, 10)]:
        g.add_edge(u, v, weight=w)
    assert shortest_path(g, 0, 3) == [0, 1, 2, 3]

    # Unreachable
    g = Graph(directed=True)
    g.add_edge(0, 1, weight=5)
    g.add_vertex(99)
    assert shortest_path(g, 0, 99) is None

    # Cross-check against Dijkstra on non-negative graphs
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "dijk", os.path.join(os.path.dirname(__file__), "dijkstra.py"))
    dijk = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dijk)

    import random
    random.seed(42)
    for _ in range(100):
        V = random.randint(2, 15)
        g = Graph(directed=True)
        for i in range(V):
            g.add_vertex(i)
        for _ in range(random.randint(0, V * 2)):
            u, v = random.sample(range(V), 2)
            g.add_edge(u, v, weight=random.randint(0, 20))

        start = random.randint(0, V - 1)
        bf_res = bellman_ford(g, start)
        assert bf_res is not None                  # no negative weights, no cycle
        dist_bf, _ = bf_res
        dist_dk, _ = dijk.dijkstra(g, start)
        assert dist_bf == dist_dk

    print("All tests passed!")
