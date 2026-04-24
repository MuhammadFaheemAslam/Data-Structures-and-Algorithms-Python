"""
adjacency-matrix.py — Graph as a V×V weight matrix

Fixed-V graph with O(1) edge lookup and O(V²) memory regardless of
edge count. Useful for dense graphs, Floyd-Warshall, or when V is
small and you want the simplest possible edge-existence check.

---------------------------------------------------
Design:

    - V must be declared at construction (matrix needs a fixed size).
    - Vertices are integers 0..V-1.
    - Sentinel for "no edge" is `None` (distinct from weight 0, which
      is a legitimate weight).
    - Weight 1 is the default for unweighted graphs.
"""


class MatrixGraph:
    """V×V weight-matrix graph. V is fixed at construction."""

    def __init__(self, V, directed=False):
        self._V = V
        self._directed = directed
        self._m = [[None] * V for _ in range(V)]
        self._edge_count = 0

    # ------------------------------------------------------------------
    # Vertices / edges
    # ------------------------------------------------------------------

    def add_edge(self, u, v, weight=1):
        """O(1). Add or update edge u → v. Edge count is logical (undirected counted once)."""
        self._check(u); self._check(v)
        if self._m[u][v] is None:
            self._edge_count += 1
        self._m[u][v] = weight
        if not self._directed:
            self._m[v][u] = weight                 # mirror cell; one logical edge

    def remove_edge(self, u, v):
        """O(1). Remove edge u → v. Raises KeyError if absent."""
        if self._m[u][v] is None:
            raise KeyError(f"no edge {u} → {v}")
        self._m[u][v] = None
        self._edge_count -= 1
        if not self._directed and u != v:
            self._m[v][u] = None

    def has_edge(self, u, v):
        """O(1). True iff u → v exists."""
        return 0 <= u < self._V and 0 <= v < self._V and self._m[u][v] is not None

    def weight(self, u, v):
        """O(1). Weight of edge u → v. Raises KeyError if absent."""
        w = self._m[u][v] if 0 <= u < self._V and 0 <= v < self._V else None
        if w is None:
            raise KeyError(f"no edge {u} → {v}")
        return w

    # ------------------------------------------------------------------
    # Iteration
    # ------------------------------------------------------------------

    def neighbours(self, u):
        """
        O(V). Iter of (neighbour, weight) for vertex u.

        (THE cost of using a matrix: listing neighbours scans a whole row.)
        """
        self._check(u)
        for v, w in enumerate(self._m[u]):
            if w is not None:
                yield (v, w)

    def neighbours_only(self, u):
        """O(V). Iter of neighbour vertices (no weights)."""
        return (v for v, _w in self.neighbours(u))

    def vertices(self):
        return range(self._V)

    def edges(self):
        """Iter of (u, v, weight) triples. Undirected: each edge once."""
        seen = set()
        for u in range(self._V):
            for v in range(self._V):
                if self._m[u][v] is None:
                    continue
                if not self._directed:
                    key = frozenset((u, v)) if u != v else (u,)
                    if key in seen:
                        continue
                    seen.add(key)
                yield (u, v, self._m[u][v])

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def __len__(self):
        return self._V

    def num_edges(self):
        return self._edge_count

    def is_directed(self):
        return self._directed

    def as_matrix(self):
        """Return a copy of the underlying matrix (for Floyd-Warshall etc.)."""
        return [row[:] for row in self._m]

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _check(self, u):
        if not (0 <= u < self._V):
            raise IndexError(f"vertex {u} out of range [0, {self._V})")

    def __repr__(self):
        kind = "directed" if self._directed else "undirected"
        return f"MatrixGraph({kind}, V={self._V}, E={self.num_edges()})"


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Basic undirected
    g = MatrixGraph(5)
    for u, v in [(0, 1), (1, 2), (2, 0), (3, 4)]:
        g.add_edge(u, v)
    assert g.num_edges() == 4
    assert g.has_edge(0, 1) and g.has_edge(1, 0)
    assert not g.has_edge(0, 3)
    assert set(g.neighbours_only(0)) == {1, 2}
    assert list(g.neighbours_only(4)) == [3]

    # Directed
    d = MatrixGraph(3, directed=True)
    d.add_edge(0, 1); d.add_edge(1, 2)
    assert d.has_edge(0, 1)
    assert not d.has_edge(1, 0)
    assert d.num_edges() == 2

    # Weight update in place
    w = MatrixGraph(3)
    w.add_edge(0, 1, weight=5)
    assert w.weight(0, 1) == 5
    w.add_edge(0, 1, weight=9)
    assert w.weight(0, 1) == 9
    assert w.num_edges() == 1

    # Remove edge
    g = MatrixGraph(3)
    g.add_edge(0, 1)
    g.remove_edge(0, 1)
    assert not g.has_edge(0, 1)
    try:
        g.remove_edge(0, 1)
    except KeyError:
        pass
    else:
        raise AssertionError("expected KeyError")

    # Out-of-range
    try:
        g.add_edge(0, 99)
    except IndexError:
        pass
    else:
        raise AssertionError("expected IndexError")

    # Self-loop
    g = MatrixGraph(3, directed=True)
    g.add_edge(0, 0)
    assert g.has_edge(0, 0)
    assert g.num_edges() == 1

    # Cross-check against adj-list rep on same graph
    import importlib.util, os, sys
    spec = importlib.util.spec_from_file_location(
        "adjl", os.path.join(os.path.dirname(__file__), "adjacency-list.py"))
    adjl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(adjl)

    import random
    random.seed(42)
    V = 30
    m = MatrixGraph(V, directed=True)
    l = adjl.Graph(directed=True)
    for _ in range(200):
        u, v = random.randint(0, V - 1), random.randint(0, V - 1)
        m.add_edge(u, v, weight=u + v)
        l.add_edge(u, v, weight=u + v)

    for u in range(V):
        m_nbrs = sorted(m.neighbours(u))
        l_nbrs = sorted(l.neighbours(u))
        assert m_nbrs == l_nbrs

    assert m.num_edges() == l.num_edges()

    print("All tests passed!")
