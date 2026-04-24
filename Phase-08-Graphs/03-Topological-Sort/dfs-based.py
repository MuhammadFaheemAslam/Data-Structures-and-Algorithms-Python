"""
dfs-based.py — Topological Sort Via DFS Post-Order

Instead of Kahn's in-degree bookkeeping, we can derive a topo order
from DFS: the REVERSE POST-ORDER of a DFS traversal is a valid topo
order.

---------------------------------------------------
Why Reverse Post-Order Works:

In post-order, a vertex is recorded AFTER all its descendants are
recorded. In a DAG, "descendants" via edges mean "everything reachable
from here". So post-order visits the "deepest" vertices first.

Reverse post-order inverts this: the vertex with no outgoing edges
(or with all its targets already emitted later in the reverse) comes
last — and when we reverse, it comes first, which means everything
pointing AWAY FROM it appears later. That's exactly the topo invariant.

---------------------------------------------------
Cycle Detection — Three-Color DFS:

To detect a cycle during DFS, classify each vertex with one of
three colors:

    WHITE — never visited
    GRAY  — visited, currently on the DFS recursion stack
    BLACK — visited, finished (subtree fully explored)

If DFS from u encounters a GRAY neighbour, that's a BACK EDGE —
a cycle. If every visited neighbour is BLACK (already finished)
or GRAY (skipped, because we handle it as an error), we're fine.

    WHITE → GRAY    on entry
    GRAY  → BLACK   on exit (post-order emit)

---------------------------------------------------
Complexity:

    Time:  O(V + E)
    Space: O(V) — colors + recursion stack
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


WHITE = 0
GRAY = 1
BLACK = 2


def topological_sort_dfs(graph):
    """
    Return a valid topo order, or None if the graph has a cycle.

    Uses DFS with three-color cycle detection.

    Time: O(V + E), Space: O(V).
    """
    if not graph.is_directed():
        raise ValueError("topological sort requires a directed graph")

    color = {v: WHITE for v in graph.vertices()}
    order = []                                     # post-order; will reverse at the end
    found_cycle = [False]

    def dfs(u):
        color[u] = GRAY
        for v in graph.neighbours_only(u):
            if color[v] == GRAY:
                found_cycle[0] = True
                return
            if color[v] == WHITE:
                dfs(v)
                if found_cycle[0]:
                    return
        color[u] = BLACK
        order.append(u)

    for v in graph.vertices():
        if color[v] == WHITE:
            dfs(v)
            if found_cycle[0]:
                return None

    order.reverse()
    return order


def has_cycle_dfs(graph):
    """Return True iff the directed graph has a cycle (DFS-based). O(V + E)."""
    return topological_sort_dfs(graph) is None


# =========================================================================
# Test — cross-check against Kahn's
# =========================================================================

def _is_valid_topo_order(graph, order):
    pos = {v: i for i, v in enumerate(order)}
    if set(pos) != set(graph.vertices()):
        return False
    for u in graph.vertices():
        for v in graph.neighbours_only(u):
            if pos[u] >= pos[v]:
                return False
    return True


if __name__ == "__main__":
    # Import Kahn's to cross-check
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "kahn", os.path.join(os.path.dirname(__file__), "kahn-bfs.py"))
    kahn = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(kahn)

    # DAG: both should succeed
    g = Graph(directed=True)
    for u, v in [(1, 2), (1, 3), (3, 4), (2, 4), (4, 5)]:
        g.add_edge(u, v)
    order = topological_sort_dfs(g)
    assert order is not None
    assert _is_valid_topo_order(g, order)

    # Cycle: both return None
    g = Graph(directed=True)
    g.add_edge("a", "b"); g.add_edge("b", "c"); g.add_edge("c", "a")
    assert topological_sort_dfs(g) is None
    assert has_cycle_dfs(g) is True

    # Self-loop
    g = Graph(directed=True)
    g.add_edge(1, 1)
    assert topological_sort_dfs(g) is None

    # Empty + isolated vertices
    assert topological_sort_dfs(Graph(directed=True)) == []

    g = Graph(directed=True)
    for v in ["x", "y", "z"]:
        g.add_vertex(v)
    order = topological_sort_dfs(g)
    assert set(order) == {"x", "y", "z"}

    # Undirected refuses
    ud = Graph()
    try:
        topological_sort_dfs(ud)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")

    # Disconnected DAG — each component ordered
    g = Graph(directed=True)
    g.add_edge(1, 2)
    g.add_edge(3, 4)
    order = topological_sort_dfs(g)
    assert order is not None and _is_valid_topo_order(g, order)

    # Stress: agreement with Kahn's on both DAG validity and cycle detection
    import random
    random.seed(42)
    for _ in range(200):
        V = random.randint(1, 20)
        g = Graph(directed=True)
        verts = list(range(V))
        random.shuffle(verts)
        for i, u in enumerate(verts):
            g.add_vertex(u)
            for v in verts[i + 1:]:
                if random.random() < 0.3:
                    g.add_edge(u, v)

        order_dfs = topological_sort_dfs(g)
        order_kahn = kahn.topological_sort(g)
        assert (order_dfs is None) == (order_kahn is None)
        if order_dfs is not None:
            assert _is_valid_topo_order(g, order_dfs)

    # Stress with SOME cycles injected
    for _ in range(200):
        V = random.randint(2, 20)
        g = Graph(directed=True)
        for u in range(V):
            for v in range(V):
                if u != v and random.random() < 0.15:
                    g.add_edge(u, v)
        dfs_result = has_cycle_dfs(g)
        kahn_result = kahn.has_cycle(g)
        assert dfs_result == kahn_result

    print("All tests passed!")
