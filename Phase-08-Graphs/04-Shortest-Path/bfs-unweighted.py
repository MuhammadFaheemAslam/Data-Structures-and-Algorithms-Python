"""
bfs-unweighted.py — Shortest Path In Unweighted Graphs

If every edge has the SAME weight (including the weight-1 unweighted
case), BFS is the shortest-path algorithm. No heap, no priority queue.

---------------------------------------------------
Why BFS Suffices:

BFS explores vertices in non-decreasing order of distance from
`start`. When we first enqueue v, its distance is FINAL — any later
path would be at least as long (since BFS processes closer vertices
first).

This is exactly the shortest-path problem for unweighted graphs.

---------------------------------------------------
Two Canonical Outputs:

    shortest_distance(g, s, t) → int or None
    shortest_path(g, s, t)     → list[vertex] or None

Both use the same BFS; they differ only in what they record along
the way.

---------------------------------------------------
Cross-Reference:

02-Traversals/bfs.py already exposes bfs_distances and bfs_path. This
file reshapes them as explicit "shortest-path APIs" with a focus on
"single source, single target" queries and clearer documentation.
"""

from collections import deque
import os


def _import_graph():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "adjl", os.path.join(os.path.dirname(__file__), "..", "01-Representations", "adjacency-list.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Graph


Graph = _import_graph()


def shortest_distance(graph, start, target):
    """
    Return the minimum number of edges from `start` to `target`, or
    None if no path exists.

    Time:  O(V + E), Space: O(V).
    """
    if start not in graph or target not in graph:
        return None
    if start == target:
        return 0

    visited = {start}
    queue = deque([(start, 0)])
    while queue:
        u, d = queue.popleft()
        for v in graph.neighbours_only(u):
            if v == target:
                return d + 1
            if v not in visited:
                visited.add(v)
                queue.append((v, d + 1))
    return None


def shortest_path(graph, start, target):
    """
    Return a shortest path [start, ..., target], or None if unreachable.

    Time:  O(V + E), Space: O(V).
    """
    if start not in graph or target not in graph:
        return None
    if start == target:
        return [start]

    parent = {start: None}
    queue = deque([start])
    while queue:
        u = queue.popleft()
        if u == target:
            path = []
            node = target
            while node is not None:
                path.append(node)
                node = parent[node]
            return list(reversed(path))
        for v in graph.neighbours_only(u):
            if v not in parent:
                parent[v] = u
                queue.append(v)
    return None


def all_shortest_distances(graph, start):
    """
    Return a dict {vertex: min-distance-from-start}. Unreachable vertices
    are absent.

    Time:  O(V + E).
    """
    if start not in graph:
        return {}
    dist = {start: 0}
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in graph.neighbours_only(u):
            if v not in dist:
                dist[v] = dist[u] + 1
                queue.append(v)
    return dist


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Linear chain: 0 — 1 — 2 — 3 — 4
    g = Graph()
    for i in range(4):
        g.add_edge(i, i + 1)
    assert shortest_distance(g, 0, 4) == 4
    assert shortest_path(g, 0, 4) == [0, 1, 2, 3, 4]

    # Two branches: shortest wins
    g = Graph()
    # Long path: 0 - 1 - 2 - 3 - 4 (length 4)
    # Short path: 0 - 5 - 4           (length 2)
    for u, v in [(0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (5, 4)]:
        g.add_edge(u, v)
    assert shortest_distance(g, 0, 4) == 2
    assert shortest_path(g, 0, 4) == [0, 5, 4]

    # Start == target
    assert shortest_distance(g, 0, 0) == 0
    assert shortest_path(g, 0, 0) == [0]

    # Unreachable → None
    g = Graph()
    g.add_edge(0, 1)
    g.add_vertex(99)
    assert shortest_distance(g, 0, 99) is None
    assert shortest_path(g, 0, 99) is None

    # Unknown vertex
    assert shortest_distance(g, 0, "?") is None
    assert shortest_path(g, 0, "?") is None

    # Directed: one-way
    d = Graph(directed=True)
    d.add_edge(1, 2); d.add_edge(2, 3)
    assert shortest_distance(d, 1, 3) == 2
    assert shortest_distance(d, 3, 1) is None      # no way back

    # all_shortest_distances: BFS layers
    g = Graph()
    for u, v in [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)]:
        g.add_edge(u, v)
    assert all_shortest_distances(g, 0) == {0: 0, 1: 1, 2: 1, 3: 2, 4: 3}

    # Stress: output paths match the returned distances
    import random
    random.seed(42)
    for _ in range(200):
        V = random.randint(1, 25)
        g = Graph()
        for i in range(V):
            g.add_vertex(i)
        for _ in range(random.randint(0, V * 2)):
            g.add_edge(random.randint(0, V - 1), random.randint(0, V - 1))

        start = random.randint(0, V - 1)
        all_d = all_shortest_distances(g, start)
        for target in range(V):
            d = shortest_distance(g, start, target)
            p = shortest_path(g, start, target)
            if target in all_d:
                assert d == all_d[target]
                assert p is not None and len(p) == d + 1
                # Path is actually in the graph
                for i in range(len(p) - 1):
                    assert g.has_edge(p[i], p[i + 1])
            else:
                assert d is None
                assert p is None

    print("All tests passed!")
