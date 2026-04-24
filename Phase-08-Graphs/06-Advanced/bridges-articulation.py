"""
bridges-articulation.py — Tarjan's Bridges and Articulation Points

In an UNDIRECTED graph:

    A BRIDGE (or cut edge) is an edge whose removal DISCONNECTS the
    graph. Equivalently: no cycle contains it.

    An ARTICULATION POINT (or cut vertex) is a vertex whose removal
    — along with all its incident edges — disconnects the graph.

Classic example:
        A — B — C
            │
            D — E

    Bridges: A-B, B-C, B-D, D-E   (every edge is a bridge in a tree)
    Articulation points: B, D

---------------------------------------------------
Why They Matter:

- **Network resilience** — bridges are single points of failure. A
  backbone network with a bridge can be severed by one cable cut.
- **Biconnected components** — bridge-less subgraphs. Used in robust
  routing and fault-tolerant circuit design.
- **Graph robustness metrics** — counting articulation points tells
  you how "connected" the graph really is.
- **Social / transport networks** — "which intersection, if closed,
  strands some neighbourhood?"

---------------------------------------------------
The Algorithm — Tarjan's DFS With Low-Link:

Augment DFS with:
    disc[v]  = discovery time of v (DFS index)
    low[v]   = minimum of disc[v] and disc of any vertex reachable
               from v's subtree via a BACK EDGE (not the edge to the
               parent)

After finishing child `c` of parent `u`:
    (EDGE IS A BRIDGE)     if low[c] > disc[u]    (no back-edge past u)
    (u IS AN ARTICULATION) if low[c] >= disc[u] AND u isn't the DFS root

For the DFS ROOT: it's an articulation iff it has MORE THAN ONE child
in the DFS tree (meaning the two children's subtrees can't reach each
other without going through the root).

---------------------------------------------------
Complexity:

    Time:  O(V + E)
    Space: O(V)

---------------------------------------------------
Notes:

- Parallel edges make finding "bridges" trickier: an edge duplicated
  between u and v isn't a bridge. Our Graph class doesn't store
  parallel edges (dict-of-dicts), so this isn't a concern here.
- Multi-edges that are self-loops are never bridges.
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


def bridges(graph):
    """
    Return a list of bridges (edges whose removal disconnects the graph).
    Each bridge is a frozenset({u, v}) for canonical hashing.

    Time: O(V + E), Space: O(V).
    """
    if graph.is_directed():
        raise ValueError("bridges are defined for UNDIRECTED graphs")

    disc = {}
    low = {}
    time = [0]
    result = []

    def dfs(u, parent):
        disc[u] = low[u] = time[0]
        time[0] += 1
        for v in graph.neighbours_only(u):
            if v not in disc:
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    result.append(frozenset((u, v)))
            elif v != parent:                      # back-edge
                low[u] = min(low[u], disc[v])

    for u in graph.vertices():
        if u not in disc:
            dfs(u, None)

    return result


def articulation_points(graph):
    """
    Return the set of articulation points (cut vertices).

    Time: O(V + E), Space: O(V).
    """
    if graph.is_directed():
        raise ValueError("articulation points are defined for UNDIRECTED graphs")

    disc = {}
    low = {}
    time = [0]
    result = set()

    def dfs(u, parent):
        disc[u] = low[u] = time[0]
        time[0] += 1
        children = 0
        for v in graph.neighbours_only(u):
            if v not in disc:
                children += 1
                dfs(v, u)
                low[u] = min(low[u], low[v])
                # Non-root articulation test
                if parent is not None and low[v] >= disc[u]:
                    result.add(u)
            elif v != parent:
                low[u] = min(low[u], disc[v])
        # Root articulation test: ≥ 2 children in DFS tree
        if parent is None and children > 1:
            result.add(u)

    for u in graph.vertices():
        if u not in disc:
            dfs(u, None)

    return result


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Chain graph: every internal vertex is articulation; every edge is bridge
    #   0 — 1 — 2 — 3
    g = Graph()
    for i in range(3):
        g.add_edge(i, i + 1)
    assert articulation_points(g) == {1, 2}
    expected_bridges = {frozenset({0, 1}), frozenset({1, 2}), frozenset({2, 3})}
    assert set(bridges(g)) == expected_bridges

    # Cycle: NO bridges, NO articulation
    g = Graph()
    for i in range(5):
        g.add_edge(i, (i + 1) % 5)
    assert articulation_points(g) == set()
    assert bridges(g) == []

    # Y-shape:
    #    0 — 1 — 2
    #        │
    #        3
    # Articulation: 1. Bridges: all three edges.
    g = Graph()
    for u, v in [(0, 1), (1, 2), (1, 3)]:
        g.add_edge(u, v)
    assert articulation_points(g) == {1}
    assert set(bridges(g)) == {frozenset({0, 1}), frozenset({1, 2}), frozenset({1, 3})}

    # Two triangles joined by a single edge:
    #   1 — 2       4 — 5
    #    \ /         \ /
    #     3 ───────── 6
    # Edge 3-6 is a bridge; 3 and 6 are articulation points.
    g = Graph()
    for u, v in [(1, 2), (2, 3), (3, 1), (4, 5), (5, 6), (6, 4), (3, 6)]:
        g.add_edge(u, v)
    assert bridges(g) == [frozenset({3, 6})]
    assert articulation_points(g) == {3, 6}

    # Empty / single vertex
    assert bridges(Graph()) == []
    assert articulation_points(Graph()) == set()

    g = Graph()
    g.add_vertex("alone")
    assert bridges(g) == []
    assert articulation_points(g) == set()

    # Two isolated components (no articulations in either if both are cycles)
    g = Graph()
    for u, v in [(1, 2), (2, 3), (3, 1)]:
        g.add_edge(u, v)
    for u, v in [(4, 5), (5, 6), (6, 4)]:
        g.add_edge(u, v)
    assert bridges(g) == []
    assert articulation_points(g) == set()

    # Directed refuses
    d = Graph(directed=True)
    try:
        bridges(d)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError (bridges)")
    try:
        articulation_points(d)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError (articulation_points)")

    # Stress: brute-force verification
    from collections import deque

    def _count_components_ignoring(graph, ignored_vertices=(), ignored_edges=()):
        """
        Number of connected components of the graph, treating `ignored_vertices`
        as non-existent and `ignored_edges` (as frozensets) as missing.
        """
        ignored_v = set(ignored_vertices)
        ignored_e = set(ignored_edges)
        visited = set()
        count = 0
        for v in graph.vertices():
            if v in ignored_v or v in visited:
                continue
            count += 1
            q = deque([v])
            visited.add(v)
            while q:
                u = q.popleft()
                for w in graph.neighbours_only(u):
                    if w in ignored_v:
                        continue
                    if frozenset((u, w)) in ignored_e:
                        continue
                    if w not in visited:
                        visited.add(w)
                        q.append(w)
        return count

    def brute_bridges(graph):
        """An edge is a bridge iff removing it increases component count."""
        edges_snapshot = [(u, v) for u, v, _w in graph.edges()]
        baseline = _count_components_ignoring(graph)
        result = set()
        for u, v in edges_snapshot:
            if _count_components_ignoring(graph, ignored_edges=[frozenset((u, v))]) > baseline:
                result.add(frozenset((u, v)))
        return result

    def brute_articulation(graph):
        """A vertex is articulation iff removing it increases "component count minus 1 for itself"."""
        baseline = _count_components_ignoring(graph)
        result = set()
        for v in list(graph.vertices()):
            # After removing v, we expect (baseline - 1) if v was in a component
            # that would collapse to nothing. Otherwise components change.
            # Cleanest: check if any two former neighbours are now disconnected
            # (without going through v).
            nbrs = list(graph.neighbours_only(v))
            if len(nbrs) < 2:
                continue                           # can't disconnect anything
            # Check if all pairs of nbrs still connected without v
            first = nbrs[0]
            visited = {first}
            q = deque([first])
            while q:
                u = q.popleft()
                if u == v:
                    continue
                for w in graph.neighbours_only(u):
                    if w == v or w in visited:
                        continue
                    visited.add(w)
                    q.append(w)
            if any(n not in visited for n in nbrs[1:]):
                result.add(v)
        return result

    import random
    random.seed(42)
    for _ in range(100):
        V = random.randint(1, 10)
        g = Graph()
        for i in range(V):
            g.add_vertex(i)
        for _ in range(random.randint(0, V)):
            u = random.randint(0, V - 1)
            v = random.randint(0, V - 1)
            if u != v:
                g.add_edge(u, v)

        fast_b = set(bridges(g))
        brute_b = brute_bridges(g)
        assert fast_b == brute_b, f"bridges mismatch: fast={fast_b}, brute={brute_b}"

        fast_a = articulation_points(g)
        brute_a = brute_articulation(g)
        assert fast_a == brute_a, f"articulation mismatch: fast={fast_a}, brute={brute_a}"

    print("All tests passed!")
