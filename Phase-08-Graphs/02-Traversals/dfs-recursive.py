"""
dfs-recursive.py — Depth-First Search (Recursive)

DFS goes AS DEEP AS POSSIBLE before backtracking. The recursive
formulation is the natural one — it matches the structure of the
problem.

---------------------------------------------------
The Algorithm:

    visited = set()

    def dfs(u):
        visited.add(u)
        VISIT u
        for v in neighbours(u):
            if v not in visited:
                dfs(v)

Each vertex is entered once → O(V + E) total.

---------------------------------------------------
Three Canonical Outputs:

    dfs_preorder(start)   — visit u BEFORE recursing (most common)
    dfs_postorder(start)  — visit u AFTER recursing
    dfs_reachable(start)  — the set of reachable vertices

Pre-order is what you want for "visit and act on each node".
Post-order is useful for topological sorting and some DP-on-graphs
patterns (children done before parent).

---------------------------------------------------
Recursion Depth Warning:

Python's default recursion limit is 1000. On a long chain graph,
recursive DFS will blow the stack. If V > ~1000, use the iterative
version in dfs-iterative.py.

---------------------------------------------------
Complexity:

    Time:  O(V + E)
    Space: O(V) — visited set + O(h) recursion stack (h ≤ V)
"""

import os
import sys


def _import_graph():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "adjl", os.path.join(os.path.dirname(__file__), "..", "01-Representations", "adjacency-list.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Graph


Graph = _import_graph()


def dfs_preorder(graph, start):
    """
    DFS from `start`, recording each vertex WHEN FIRST VISITED.

    Time: O(V + E), Space: O(V).
    """
    if start not in graph:
        return []

    order = []
    visited = set()

    def walk(u):
        visited.add(u)
        order.append(u)
        for v in graph.neighbours_only(u):
            if v not in visited:
                walk(v)

    walk(start)
    return order


def dfs_postorder(graph, start):
    """
    DFS from `start`, recording each vertex AFTER its subtree is done.

    Used for topological sort (reverse postorder) and dead-code detection.

    Time: O(V + E), Space: O(V).
    """
    if start not in graph:
        return []

    order = []
    visited = set()

    def walk(u):
        visited.add(u)
        for v in graph.neighbours_only(u):
            if v not in visited:
                walk(v)
        order.append(u)                            # <-- record AFTER children

    walk(start)
    return order


def dfs_reachable(graph, start):
    """Return the set of vertices reachable from `start`. O(V + E)."""
    if start not in graph:
        return set()
    visited = set()

    def walk(u):
        visited.add(u)
        for v in graph.neighbours_only(u):
            if v not in visited:
                walk(v)

    walk(start)
    return visited


def has_path(graph, start, target):
    """
    True iff `target` is reachable from `start`. O(V + E) worst case;
    short-circuits when target is found.
    """
    if start not in graph or target not in graph:
        return False
    if start == target:
        return True
    visited = {start}

    def walk(u):
        if u == target:
            return True
        for v in graph.neighbours_only(u):
            if v not in visited:
                visited.add(v)
                if walk(v):
                    return True
        return False

    return walk(start)


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Graph:
    #    0 — 1 — 3
    #    |   |
    #    2   4
    g = Graph()
    for u, v in [(0, 1), (0, 2), (1, 3), (1, 4)]:
        g.add_edge(u, v)

    # Preorder visits start first
    pre = dfs_preorder(g, 0)
    assert pre[0] == 0
    assert set(pre) == {0, 1, 2, 3, 4}

    # Postorder visits leaves first, start last
    post = dfs_postorder(g, 0)
    assert post[-1] == 0
    assert set(post) == {0, 1, 2, 3, 4}

    # Reachable
    assert dfs_reachable(g, 0) == {0, 1, 2, 3, 4}

    # Path detection
    assert has_path(g, 0, 4) is True
    assert has_path(g, 0, 0) is True
    assert has_path(g, 0, "not-there") is False

    # Disconnected
    g.add_vertex("X")
    g.add_edge("X", "Y")
    assert dfs_reachable(g, 0) == {0, 1, 2, 3, 4}
    assert dfs_reachable(g, "X") == {"X", "Y"}
    assert has_path(g, 0, "Y") is False

    # Cycle: DFS should not loop
    cyc = Graph(directed=True)
    cyc.add_edge(1, 2); cyc.add_edge(2, 3); cyc.add_edge(3, 1)
    assert dfs_preorder(cyc, 1) == [1, 2, 3] or dfs_preorder(cyc, 1) == [1, 2, 3]

    # Stress: every DFS should visit exactly the reachable set
    import random
    random.seed(42)
    for _ in range(200):
        V = random.randint(1, 30)
        g = Graph()
        for i in range(V):
            g.add_vertex(i)
        for _ in range(random.randint(0, V * 2)):
            g.add_edge(random.randint(0, V - 1), random.randint(0, V - 1))

        start = random.randint(0, V - 1)
        pre = dfs_preorder(g, start)
        post = dfs_postorder(g, start)
        reach = dfs_reachable(g, start)

        assert set(pre) == reach
        assert set(post) == reach
        assert len(pre) == len(reach)
        # Start is always pre[0] and post[-1]
        assert pre[0] == start
        assert post[-1] == start

    print("All tests passed!")
