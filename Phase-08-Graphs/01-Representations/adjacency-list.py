"""
adjacency-list.py — Graph as a dict of neighbour lists

This is the representation 95% of graph problems use. Most algorithms
in subsequent modules import `Graph` from here.

---------------------------------------------------
Design Choices:

    - Vertices can be any hashable value (int, str, tuple). We treat
      them opaquely.
    - Edges can be weighted. Unweighted = weight 1 (convention).
    - Both directed and undirected graphs use the SAME class; pass
      `directed=True/False` at construction.

---------------------------------------------------
API:

    g = Graph()                     # undirected by default
    g = Graph(directed=True)
    g.add_edge(u, v)                # unweighted
    g.add_edge(u, v, weight=3)      # weighted
    g.neighbours(u)                 # iter of (neighbour, weight)
    g.has_edge(u, v)                # O(deg(u))
    g.vertices(), g.edges()
    g.remove_edge(u, v)
    len(g)                          # number of vertices
"""

from collections import defaultdict


class Graph:
    """
    Adjacency-list graph. Vertices are any hashable value.

    Internal state:
        _adj[u] = {v1: w1, v2: w2, ...}   dict-of-dicts, so edge lookup is O(1)
    Using a dict instead of a list for the inner level means:
        - has_edge(u, v)      is O(1)
        - remove_edge(u, v)   is O(1)
        - update weight       is O(1)
    at the cost of slightly more memory than a plain list.
    """

    def __init__(self, directed=False):
        self._adj = defaultdict(dict)
        self._directed = directed
        self._vertices = set()                     # explicit, so isolated vertices are tracked

    # ------------------------------------------------------------------
    # Vertices / edges
    # ------------------------------------------------------------------

    def add_vertex(self, u):
        """Add `u` as an isolated vertex if it isn't already present."""
        self._vertices.add(u)
        _ = self._adj[u]                           # ensure key exists in defaultdict

    def add_edge(self, u, v, weight=1):
        """
        Add edge u → v (directed) or u ↔ v (undirected).
        If the edge already exists, its weight is UPDATED to `weight`.
        """
        self._vertices.add(u); self._vertices.add(v)
        self._adj[u][v] = weight
        if not self._directed:
            self._adj[v][u] = weight

    def remove_edge(self, u, v):
        """Remove edge u → v (or u ↔ v). Raises KeyError if absent."""
        if v not in self._adj.get(u, {}):
            raise KeyError(f"no edge {u} → {v}")
        del self._adj[u][v]
        if not self._directed:
            del self._adj[v][u]

    def has_edge(self, u, v):
        """O(1). True iff u → v exists."""
        return v in self._adj.get(u, {})

    def weight(self, u, v):
        """Return the weight of edge u → v. Raises KeyError if absent."""
        return self._adj[u][v]

    # ------------------------------------------------------------------
    # Iteration
    # ------------------------------------------------------------------

    def neighbours(self, u):
        """Iter of (neighbour, weight) pairs for vertex u. Empty if u unknown."""
        return self._adj.get(u, {}).items()

    def neighbours_only(self, u):
        """Iter of just neighbour vertices (without weights). Handy for unweighted algorithms."""
        return iter(self._adj.get(u, {}))

    def vertices(self):
        """Iter of all vertices (including isolated)."""
        return iter(self._vertices)

    def edges(self):
        """
        Iter of (u, v, weight) triples. For undirected graphs, each edge
        is yielded ONCE (u < v, using object ids' hash ordering if no
        natural order; for canonical output, sort vertices first).
        """
        seen = set()
        for u, neighbours in self._adj.items():
            for v, w in neighbours.items():
                if not self._directed:
                    key = frozenset((u, v)) if u != v else (u,)
                    if key in seen:
                        continue
                    seen.add(key)
                yield (u, v, w)

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def __len__(self):
        """Number of vertices."""
        return len(self._vertices)

    def num_edges(self):
        total = sum(len(nbrs) for nbrs in self._adj.values())
        return total if self._directed else total // 2

    def is_directed(self):
        return self._directed

    def __contains__(self, u):
        """`u in graph` checks vertex membership."""
        return u in self._vertices

    def __repr__(self):
        kind = "directed" if self._directed else "undirected"
        return f"Graph({kind}, V={len(self)}, E={self.num_edges()})"


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Undirected, unweighted
    g = Graph()
    for u, v in [("a", "b"), ("b", "c"), ("c", "a"), ("d", "e")]:
        g.add_edge(u, v)
    assert len(g) == 5
    assert g.num_edges() == 4
    assert g.has_edge("a", "b") and g.has_edge("b", "a")           # undirected
    assert not g.has_edge("a", "d")
    assert set(g.neighbours_only("a")) == {"b", "c"}

    # Directed
    d = Graph(directed=True)
    d.add_edge(1, 2); d.add_edge(2, 3); d.add_edge(1, 3)
    assert d.has_edge(1, 2)
    assert not d.has_edge(2, 1)
    assert d.num_edges() == 3

    # Weighted: update in place
    w = Graph()
    w.add_edge("x", "y", weight=5)
    assert w.weight("x", "y") == 5
    w.add_edge("x", "y", weight=9)                                 # re-add updates
    assert w.weight("x", "y") == 9
    assert w.num_edges() == 1

    # Isolated vertex
    g = Graph()
    g.add_vertex("loner")
    assert "loner" in g
    assert list(g.neighbours("loner")) == []

    # Remove edge
    g = Graph()
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.remove_edge(0, 1)
    assert not g.has_edge(0, 1)
    assert g.has_edge(1, 2)
    try:
        g.remove_edge(0, 1)
    except KeyError:
        pass
    else:
        raise AssertionError("expected KeyError")

    # Self-loop
    g = Graph(directed=True)
    g.add_edge("x", "x")
    assert g.has_edge("x", "x")
    assert g.num_edges() == 1

    # Edges() for undirected yields each edge once
    g = Graph()
    edge_pairs = [(1, 2), (2, 3), (1, 3), (3, 4)]
    for u, v in edge_pairs:
        g.add_edge(u, v)
    listed = [(u, v) for u, v, _ in g.edges()]
    # Each {u,v} frozenset should appear once
    seen = set()
    for u, v in listed:
        seen.add(frozenset((u, v)))
    assert seen == {frozenset(p) for p in edge_pairs}

    # Stress: reference against manual adj set
    import random
    random.seed(42)
    g = Graph(directed=True)
    ref = set()
    for _ in range(2000):
        u, v = random.randint(0, 50), random.randint(0, 50)
        op = random.choice(["add", "remove", "has"])
        if op == "add":
            g.add_edge(u, v)
            ref.add((u, v))
        elif op == "remove" and (u, v) in ref:
            g.remove_edge(u, v)
            ref.discard((u, v))
        else:
            assert g.has_edge(u, v) == ((u, v) in ref)

    assert set((u, v) for u, v, _ in g.edges()) == ref
    print("All tests passed!")
