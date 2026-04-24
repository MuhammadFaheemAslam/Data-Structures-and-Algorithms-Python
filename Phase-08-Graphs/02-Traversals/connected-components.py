"""
connected-components.py — Finding All Connected Components

A CONNECTED COMPONENT of an undirected graph is a maximal set of
vertices such that every pair is reachable from each other. The
problem is "group vertices into their components."

---------------------------------------------------
The Algorithm:

Iterate over ALL vertices. For each one not yet in any component,
run BFS (or DFS) starting there — everything it reaches is one
component. Repeat until every vertex has been covered.

    for v in vertices:
        if v not in visited:
            component = bfs(v)             # or dfs(v) — same result
            record component
            visited ∪= component

Each vertex + edge touched exactly once → O(V + E).

---------------------------------------------------
Variants:

    connected_components(graph)       → list[set[vertex]]
    num_components(graph)              → int
    component_of(graph, vertex)        → set of vertices in v's component
    is_connected(graph)                → True iff only 1 component

---------------------------------------------------
Directed Graphs — Note The Difference:

For DIRECTED graphs, "reachable from" is asymmetric, so the right
notion becomes STRONGLY CONNECTED COMPONENTS (SCC) — a different
algorithm (Tarjan or Kosaraju). We handle SCC in 06-Advanced.

If you call `connected_components` on a directed graph, it
interprets edges as undirected for the purpose of grouping — i.e.
it finds the UNDERLYING-UNDIRECTED components. Not what you usually
want, so we check `is_directed()` and refuse in that case.

---------------------------------------------------
Complexity:

    Time:  O(V + E)
    Space: O(V) for visited + component storage
"""

import os
import sys
from collections import deque


def _import_graph():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "adjl", os.path.join(os.path.dirname(__file__), "..", "01-Representations", "adjacency-list.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Graph


Graph = _import_graph()


def _bfs_component(graph, start, visited):
    """Return the set of all vertices reachable from `start`, updating `visited`."""
    component = {start}
    visited.add(start)
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in graph.neighbours_only(u):
            if v not in visited:
                visited.add(v)
                component.add(v)
                queue.append(v)
    return component


def connected_components(graph):
    """
    Return a list of the graph's connected components (each component
    is a set of vertices).

    Time: O(V + E), Space: O(V).
    """
    if graph.is_directed():
        raise ValueError("connected_components is for undirected graphs; "
                         "use strongly_connected_components for directed graphs")

    visited = set()
    components = []
    for v in graph.vertices():
        if v not in visited:
            components.append(_bfs_component(graph, v, visited))
    return components


def num_components(graph):
    """O(V + E). Count of connected components."""
    return len(connected_components(graph))


def component_of(graph, vertex):
    """O(V + E). Set of vertices in the same component as `vertex`."""
    if vertex not in graph:
        return set()
    return _bfs_component(graph, vertex, set())


def is_connected(graph):
    """O(V + E). True iff the graph has exactly one component covering all vertices."""
    return num_components(graph) == 1


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Two-component graph
    # Component 1: {0, 1, 2}    Component 2: {3, 4}
    g = Graph()
    for u, v in [(0, 1), (1, 2), (3, 4)]:
        g.add_edge(u, v)

    comps = connected_components(g)
    comp_sets = [frozenset(c) for c in comps]
    assert frozenset({0, 1, 2}) in comp_sets
    assert frozenset({3, 4}) in comp_sets
    assert len(comps) == 2
    assert num_components(g) == 2
    assert component_of(g, 0) == {0, 1, 2}
    assert component_of(g, 3) == {3, 4}
    assert not is_connected(g)

    # Isolated vertex is its own component
    g.add_vertex("loner")
    assert num_components(g) == 3
    assert component_of(g, "loner") == {"loner"}

    # Single fully-connected graph
    g = Graph()
    for u, v in [(0, 1), (1, 2), (2, 3), (3, 0)]:
        g.add_edge(u, v)
    assert is_connected(g)
    assert connected_components(g) == [{0, 1, 2, 3}]

    # Empty graph
    empty = Graph()
    assert connected_components(empty) == []
    assert num_components(empty) == 0
    assert is_connected(empty) is False            # no components; not "connected"

    # Unknown vertex
    assert component_of(g, "nowhere") == set()

    # Directed should refuse
    d = Graph(directed=True)
    try:
        connected_components(d)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for directed graph")

    # Stress: components are a PARTITION
    import random
    random.seed(42)
    for _ in range(200):
        V = random.randint(1, 30)
        g = Graph()
        for i in range(V):
            g.add_vertex(i)
        for _ in range(random.randint(0, V)):
            g.add_edge(random.randint(0, V - 1), random.randint(0, V - 1))

        comps = connected_components(g)
        all_vs = set()
        for c in comps:
            # Components are disjoint
            assert not (c & all_vs)
            all_vs |= c
        # Components cover every vertex
        assert all_vs == set(g.vertices())
        # Every vertex agrees on its component
        for v in g.vertices():
            found = next(c for c in comps if v in c)
            assert component_of(g, v) == found

    print("All tests passed!")
