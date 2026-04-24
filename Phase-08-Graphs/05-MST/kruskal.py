"""
kruskal.py — Kruskal's Minimum Spanning Tree Algorithm

Kruskal builds an MST by considering edges in ORDER OF WEIGHT, adding
each edge to the MST if (and only if) it doesn't form a cycle with
already-added edges.

Cycle detection needs "are u and v already in the same connected
component of the partial MST?" — that's exactly what Union-Find
answers in near-O(1).

---------------------------------------------------
The Algorithm:

    sort edges by weight
    uf = UnionFind(vertices)
    mst = []
    for (u, v, w) in sorted(edges):
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            mst.append((u, v, w))
            if len(mst) == V - 1: break           # all connected
    return mst

---------------------------------------------------
Disconnected graphs:

Kruskal naturally produces a MINIMUM SPANNING FOREST for disconnected
graphs — one tree per component. `len(mst)` ends up as V - (number of
components).

---------------------------------------------------
Union-Find (quick tour):

This module has a mini Union-Find inline. Phase 10 covers it properly
(union-by-rank, path-compression correctness proofs, α(n) amortization).

    find(x)        — canonical root of x's set
    union(x, y)    — merge the sets containing x and y
    connected(x, y) — True iff same set

We implement union-by-SIZE and path COMPRESSION — both standard
optimizations. Amortized α(n) per operation, ~constant for practical n.

---------------------------------------------------
Complexity:

    Time:  O(E log E)     — dominated by sorting edges
    Space: O(V + E)
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


# =========================================================================
# Mini Union-Find (full version in Phase 10)
# =========================================================================

class _UnionFind:
    """Union-by-size + path-compression DSU. Near-constant amortized."""

    def __init__(self, items):
        items = list(items)                        # materialize once; callers may pass a generator
        self._parent = {x: x for x in items}
        self._size = {x: 1 for x in items}
        self._num_sets = len(self._parent)

    def find(self, x):
        """Find the canonical root, compressing the path as we go."""
        root = x
        while self._parent[root] != root:
            root = self._parent[root]
        # Compress
        while self._parent[x] != root:
            self._parent[x], x = root, self._parent[x]
        return root

    def union(self, x, y):
        """Merge sets. Returns True if a merge happened (different sets)."""
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        # Attach smaller under larger
        if self._size[rx] < self._size[ry]:
            rx, ry = ry, rx
        self._parent[ry] = rx
        self._size[rx] += self._size[ry]
        self._num_sets -= 1
        return True

    def num_sets(self):
        return self._num_sets


# =========================================================================
# Kruskal's MST
# =========================================================================

def mst(graph):
    """
    Return a list of (u, v, weight) MST edges, sorted by weight ascending.

    For disconnected graphs, returns a minimum spanning FOREST.

    Time: O(E log E), Space: O(V + E).
    """
    if graph.is_directed():
        raise ValueError("MST is defined for UNDIRECTED graphs")

    vertices = list(graph.vertices())
    edges = sorted(graph.edges(), key=lambda e: e[2])

    uf = _UnionFind(vertices)
    result = []
    target = max(0, len(vertices) - 1)             # V-1 edges in a tree

    for u, v, w in edges:
        if uf.union(u, v):
            result.append((u, v, w))
            if len(result) == target:
                break                              # early exit: MST complete

    return result


def mst_weight(graph):
    """Total weight of the MST (or MSF)."""
    return sum(w for _u, _v, w in mst(graph))


def is_connected(graph):
    """Shortcut: build MST and check that it spans every vertex."""
    if len(graph) == 0:
        return True
    return len(mst(graph)) == len(graph) - 1


# =========================================================================
# Test
# =========================================================================

def _mst_is_valid(graph, tree_edges):
    """Verify tree_edges is a spanning tree (or forest) of graph."""
    # 1. All edges exist in the graph
    for u, v, w in tree_edges:
        assert graph.has_edge(u, v), f"edge {u}-{v} not in graph"
        assert graph.weight(u, v) == w

    # 2. Acyclic & connects components properly
    uf = _UnionFind(graph.vertices())
    for u, v, _w in tree_edges:
        assert uf.union(u, v), f"edge {u}-{v} creates a cycle"

    # 3. |edges| = V - #components (a forest covering every vertex)
    V = len(graph)
    components = uf.num_sets()
    assert len(tree_edges) == V - components

    return True


if __name__ == "__main__":
    # Canonical example (from theory.md diagram):
    #        4
    #   A ─────── B
    #   │         │
    #   2         3
    #   │         │
    #   C ─────── D
    #        1
    g = Graph()
    for u, v, w in [("A", "B", 4), ("A", "C", 2), ("B", "D", 3), ("C", "D", 1)]:
        g.add_edge(u, v, weight=w)

    t = mst(g)
    # MST picks A-C (2), C-D (1), then either A-B (4) or B-D (3).
    # Kruskal considers ascending weight: 1, 2, 3, 4.
    # So: C-D (1), A-C (2), B-D (3). Total = 6.
    assert mst_weight(g) == 6
    assert len(t) == 3                             # V - 1

    # Triangle: 3 edges of weights 1, 2, 3 — MST takes the two cheapest
    g = Graph()
    for u, v, w in [(1, 2, 1), (2, 3, 2), (1, 3, 3)]:
        g.add_edge(u, v, weight=w)
    assert mst_weight(g) == 3                      # 1 + 2
    assert _mst_is_valid(g, mst(g))

    # Single vertex: empty MST
    g = Graph()
    g.add_vertex("lonely")
    assert mst(g) == []
    assert mst_weight(g) == 0

    # Disconnected: minimum spanning forest
    g = Graph()
    for u, v, w in [(0, 1, 5), (2, 3, 7)]:
        g.add_edge(u, v, weight=w)
    t = mst(g)
    assert len(t) == 2                             # V(4) - 2 components = 2
    assert mst_weight(g) == 12
    assert not is_connected(g)

    # Empty
    assert mst(Graph()) == []
    assert is_connected(Graph())                   # vacuously "connected"

    # Directed graph refuses
    d = Graph(directed=True)
    try:
        mst(d)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")

    # Stress: every output is a valid MST AND has weight ≤ any random spanning tree
    import random
    random.seed(42)

    def brute_spanning_tree_weight(graph):
        """Construct ANY spanning tree via BFS; return its weight (upper bound on MST)."""
        if len(graph) <= 1:
            return 0
        start = next(iter(graph.vertices()))
        from collections import deque
        parent = {start: None}
        queue = deque([start])
        total = 0
        while queue:
            u = queue.popleft()
            for v, w in graph.neighbours(u):
                if v not in parent:
                    parent[v] = u
                    total += w
                    queue.append(v)
        return total

    for _ in range(200):
        V = random.randint(1, 15)
        g = Graph()
        for i in range(V):
            g.add_vertex(i)
        # Random edges
        for _ in range(random.randint(0, V * 2)):
            u = random.randint(0, V - 1)
            v = random.randint(0, V - 1)
            if u != v:
                g.add_edge(u, v, weight=random.randint(1, 100))

        tree = mst(g)
        _mst_is_valid(g, tree)
        # MST weight ≤ BFS spanning tree weight (whenever the graph is connected)
        if is_connected(g):
            assert mst_weight(g) <= brute_spanning_tree_weight(g)

    print("All tests passed!")
