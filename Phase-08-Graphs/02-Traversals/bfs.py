"""
bfs.py — Breadth-First Search on a Graph

BFS explores a graph LEVEL BY LEVEL, using a FIFO queue. From a
starting vertex, it visits all vertices at distance 1 before any at
distance 2, and so on.

---------------------------------------------------
The Algorithm:

    queue ← [start]
    visited ← {start}
    while queue non-empty:
        u = queue.popleft()
        VISIT u
        for each neighbour v of u:
            if v not in visited:
                visited.add(v)
                queue.append(v)

Each vertex is enqueued and visited AT MOST ONCE → O(V + E).

---------------------------------------------------
Two Canonical Outputs:

    bfs_order(start)      — list of vertices in the order they were visited
    bfs_distances(start)  — dict of {vertex: distance-from-start in edges}
                             = SHORTEST PATH in an unweighted graph

Both are in this file; both share the same traversal code.

---------------------------------------------------
Why BFS Gives Shortest Paths (unweighted):

BFS visits vertices in non-decreasing order of distance from `start`.
The first time a vertex is enqueued, its distance is FINAL — no
future path can be shorter, because BFS has already processed all
shorter distances before reaching this level.

This is the reason BFS is the go-to tool for unweighted-shortest-path
problems (word ladder, rotting oranges, open the lock, etc.).

---------------------------------------------------
Complexity:

    Time:  O(V + E)
    Space: O(V) — for visited + queue
"""

from collections import deque
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "01-Representations"))


def _import_graph():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "adjl", os.path.join(os.path.dirname(__file__), "..", "01-Representations", "adjacency-list.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Graph


Graph = _import_graph()


def bfs_order(graph, start):
    """
    Return the list of vertices reachable from `start`, in BFS order.

    Time: O(V + E), Space: O(V).
    """
    if start not in graph:
        return []

    order = []
    visited = {start}
    queue = deque([start])

    while queue:
        u = queue.popleft()
        order.append(u)
        for v in graph.neighbours_only(u):
            if v not in visited:
                visited.add(v)
                queue.append(v)

    return order


def bfs_distances(graph, start):
    """
    Return {vertex: shortest-distance-from-start-in-edges}. Unreachable
    vertices are not in the dict.

    For an unweighted graph, this IS the shortest-path algorithm.

    Time: O(V + E), Space: O(V).
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


def bfs_path(graph, start, target):
    """
    Return a shortest-path list [start, ..., target], or None if no path.

    Time: O(V + E), Space: O(V).
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
            # Reconstruct path from parent pointers
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

    return None                                    # unreachable


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Example graph:
    #    0 — 1 — 3
    #    |   |
    #    2   4
    g = Graph()
    for u, v in [(0, 1), (0, 2), (1, 3), (1, 4)]:
        g.add_edge(u, v)

    assert bfs_order(g, 0) == [0, 1, 2, 3, 4] or bfs_order(g, 0) == [0, 2, 1, 4, 3]
    # (neighbour order is dict-insertion-order; both outputs are valid BFS)
    # Check distances instead — those are deterministic
    d = bfs_distances(g, 0)
    assert d == {0: 0, 1: 1, 2: 1, 3: 2, 4: 2}

    # bfs_path returns a shortest path
    p = bfs_path(g, 0, 3)
    assert p == [0, 1, 3]

    # Start == target
    assert bfs_path(g, 0, 0) == [0]

    # Disconnected → unreachable
    g.add_vertex("X")
    assert "X" not in bfs_distances(g, 0)
    assert bfs_path(g, 0, "X") is None

    # Unknown vertex
    assert bfs_order(g, "nowhere") == []
    assert bfs_distances(g, "nowhere") == {}

    # Directed: one-way connection
    d = Graph(directed=True)
    d.add_edge(1, 2); d.add_edge(2, 3); d.add_edge(3, 1)           # cycle
    assert bfs_distances(d, 1) == {1: 0, 2: 1, 3: 2}
    assert bfs_distances(d, 3) == {3: 0, 1: 1, 2: 2}

    # Stress: BFS distances should never exceed V - 1
    import random
    random.seed(42)
    for _ in range(200):
        V = random.randint(1, 20)
        g = Graph()
        for i in range(V):
            g.add_vertex(i)
        # Add random edges to create varied connectivity
        for _ in range(random.randint(0, V * 2)):
            g.add_edge(random.randint(0, V - 1), random.randint(0, V - 1))
        start = random.randint(0, V - 1)
        d = bfs_distances(g, start)
        assert d[start] == 0
        for v, dist in d.items():
            assert 0 <= dist <= V - 1
        # Paths actually walk the graph
        for target in d:
            p = bfs_path(g, start, target)
            assert p is not None and len(p) == d[target] + 1
            for i in range(len(p) - 1):
                assert g.has_edge(p[i], p[i + 1])

    print("All tests passed!")
