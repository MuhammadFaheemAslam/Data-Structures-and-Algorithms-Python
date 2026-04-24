"""
prim.py — Prim's Minimum Spanning Tree Algorithm

Prim grows the MST from a single starting vertex. At each step, it
adds the CHEAPEST edge from the tree-so-far to a vertex outside the
tree.

---------------------------------------------------
The Algorithm (heap-based, O((V + E) log V)):

    in_tree = {start}
    heap = [(weight, u, v) for u=start, v in neighbours(start)]
    mst = []

    while heap AND len(in_tree) < V:
        w, u, v = heappop(heap)
        if v in in_tree: continue                  # stale entry
        in_tree.add(v)
        mst.append((u, v, w))
        for (nbr, weight) in neighbours(v):
            if nbr not in in_tree:
                heappush(heap, (weight, v, nbr))

Each edge pushed and popped at most once. With a binary heap:
O((V + E) log V).

---------------------------------------------------
Starting Vertex:

Prim needs a starting vertex. The CHOICE doesn't affect correctness
(the set of MST edges may differ, but total weight is identical
if the MST is unique, and equals the minimum if it isn't).

For a disconnected graph, Prim only spans the COMPONENT containing
`start`. Use Kruskal if you need a spanning FOREST.

---------------------------------------------------
Complexity:

    Time:  O((V + E) log V) with a binary heap
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


def mst(graph, start=None):
    """
    Return MST edges (u, v, weight) as a list.

    Requires the graph to be UNDIRECTED. For disconnected graphs, only
    the component containing `start` is spanned — use Kruskal for the
    minimum spanning forest over all components.

    Time:  O((V + E) log V), Space: O(V + E).
    """
    if graph.is_directed():
        raise ValueError("MST is defined for UNDIRECTED graphs")

    if len(graph) == 0:
        return []

    if start is None:
        start = next(iter(graph.vertices()))

    if start not in graph:
        raise KeyError(start)

    in_tree = {start}
    result = []
    heap = []

    # Seed the heap with edges leaving `start`
    for v, w in graph.neighbours(start):
        heapq.heappush(heap, (w, start, v))

    while heap and len(in_tree) < len(graph):
        w, u, v = heapq.heappop(heap)
        if v in in_tree:
            continue                                # stale entry
        in_tree.add(v)
        result.append((u, v, w))
        for nbr, weight in graph.neighbours(v):
            if nbr not in in_tree:
                heapq.heappush(heap, (weight, v, nbr))

    return result


def mst_weight(graph, start=None):
    """Total weight of Prim's MST (from `start`, or an arbitrary vertex)."""
    return sum(w for _u, _v, w in mst(graph, start))


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Cross-check against Kruskal on the same graph
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "kr", os.path.join(os.path.dirname(__file__), "kruskal.py"))
    kr = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(kr)

    # Canonical 4-node example
    g = Graph()
    for u, v, w in [("A", "B", 4), ("A", "C", 2), ("B", "D", 3), ("C", "D", 1)]:
        g.add_edge(u, v, weight=w)
    assert mst_weight(g) == 6
    assert mst_weight(g) == kr.mst_weight(g)

    # Triangle
    g = Graph()
    for u, v, w in [(1, 2, 1), (2, 3, 2), (1, 3, 3)]:
        g.add_edge(u, v, weight=w)
    assert mst_weight(g) == 3

    # Single vertex: empty MST
    g = Graph()
    g.add_vertex("lonely")
    assert mst(g) == []
    assert mst_weight(g) == 0

    # Start can be any vertex — weight is the same
    g = Graph()
    for u, v, w in [("A", "B", 4), ("A", "C", 2), ("B", "D", 3), ("C", "D", 1)]:
        g.add_edge(u, v, weight=w)
    weights = {mst_weight(g, start) for start in ["A", "B", "C", "D"]}
    assert weights == {6}

    # Directed refuses
    d = Graph(directed=True)
    try:
        mst(d)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")

    # Unknown start
    g = Graph()
    g.add_edge(0, 1, weight=5)
    try:
        mst(g, start=99)
    except KeyError:
        pass
    else:
        raise AssertionError("expected KeyError")

    # Disconnected: Prim only spans one component
    g = Graph()
    for u, v, w in [(0, 1, 5), (2, 3, 7)]:
        g.add_edge(u, v, weight=w)
    assert mst_weight(g, start=0) == 5             # only component {0, 1}
    assert mst_weight(g, start=2) == 7             # only component {2, 3}
    # Kruskal, by contrast, returns BOTH:
    assert kr.mst_weight(g) == 12

    # Stress: Prim and Kruskal agree on connected graphs
    import random
    random.seed(42)
    for _ in range(200):
        V = random.randint(2, 15)
        # Build a random CONNECTED graph (chain + random extras)
        g = Graph()
        for i in range(V):
            g.add_vertex(i)
        # Spanning chain ensures connectivity
        for i in range(V - 1):
            g.add_edge(i, i + 1, weight=random.randint(1, 100))
        # Random extra edges
        for _ in range(random.randint(0, V)):
            u, v = random.sample(range(V), 2)
            g.add_edge(u, v, weight=random.randint(1, 100))

        assert mst_weight(g) == kr.mst_weight(g)

    print("All tests passed!")
