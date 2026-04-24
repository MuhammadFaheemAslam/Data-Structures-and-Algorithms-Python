"""
edge-list.py — Graph as a flat list of edges

The simplest representation: just a list of (u, v, weight) tuples.
You can't efficiently answer "neighbours of u?" without scanning
everything, but some algorithms only need to ITERATE ALL EDGES:

    - Kruskal's MST              (sort by weight, scan)
    - Bellman-Ford               (V-1 rounds of "relax every edge")
    - Reading a graph from file  (edges are the natural input format)

This module also provides CONVERSION functions between the three
representations — useful when an algorithm needs one shape and
you've got data in another.
"""


class EdgeListGraph:
    """Graph as a list of (u, v, weight) tuples."""

    def __init__(self, directed=False):
        self._edges = []
        self._vertices = set()
        self._directed = directed

    # ------------------------------------------------------------------
    # Building
    # ------------------------------------------------------------------

    def add_vertex(self, u):
        self._vertices.add(u)

    def add_edge(self, u, v, weight=1):
        """O(1). Append edge; does NOT dedupe."""
        self._edges.append((u, v, weight))
        self._vertices.add(u); self._vertices.add(v)

    # ------------------------------------------------------------------
    # Iteration
    # ------------------------------------------------------------------

    def edges(self):
        """Iter of (u, v, weight) triples in insertion order."""
        return iter(self._edges)

    def vertices(self):
        return iter(self._vertices)

    def __len__(self):
        return len(self._vertices)

    def num_edges(self):
        return len(self._edges)

    def is_directed(self):
        return self._directed

    def __repr__(self):
        kind = "directed" if self._directed else "undirected"
        return f"EdgeListGraph({kind}, V={len(self)}, E={self.num_edges()})"


# =========================================================================
# Conversion helpers
# =========================================================================

def edge_list_to_adj_dict(edge_list, directed=False):
    """
    Convert an edge-list graph into a dict-of-dict adjacency representation:

        {u: {v1: w1, v2: w2, ...}, ...}

    Useful when you've been handed edges and want O(1) edge lookup.
    """
    adj = {}
    for u, v, w in edge_list.edges():
        adj.setdefault(u, {})[v] = w
        if not directed and u != v:
            adj.setdefault(v, {})[u] = w
    for v in edge_list.vertices():
        adj.setdefault(v, {})                      # ensure isolated vertices present
    return adj


def edge_list_to_matrix(edge_list, V, directed=False):
    """
    Convert to a V×V matrix. Vertices must be ints in 0..V-1.
    """
    m = [[None] * V for _ in range(V)]
    for u, v, w in edge_list.edges():
        m[u][v] = w
        if not directed and u != v:
            m[v][u] = w
    return m


def adj_dict_to_edge_list(adj, directed=False):
    """
    Inverse of edge_list_to_adj_dict. For undirected graphs, each edge
    emitted ONCE.
    """
    out = EdgeListGraph(directed=directed)
    seen = set()
    for u, nbrs in adj.items():
        out.add_vertex(u)
        for v, w in nbrs.items():
            if not directed:
                key = frozenset((u, v)) if u != v else (u,)
                if key in seen:
                    continue
                seen.add(key)
            out.add_edge(u, v, w)
    return out


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Basic build
    g = EdgeListGraph()
    for u, v, w in [(0, 1, 5), (1, 2, 3), (0, 2, 4)]:
        g.add_edge(u, v, w)
    assert g.num_edges() == 3
    assert len(g) == 3
    assert list(g.edges()) == [(0, 1, 5), (1, 2, 3), (0, 2, 4)]

    # Edge-list → dict → edge-list round-trip
    adj = edge_list_to_adj_dict(g, directed=False)
    # adj should have entries both ways
    assert adj[0] == {1: 5, 2: 4}
    assert adj[1] == {0: 5, 2: 3}
    assert adj[2] == {1: 3, 0: 4}

    # Round-trip
    g2 = adj_dict_to_edge_list(adj, directed=False)
    # Edges may appear in a different order, but the SET of canonical edges matches
    canon_a = {frozenset((u, v)): w for u, v, w in g.edges()}
    canon_b = {frozenset((u, v)): w for u, v, w in g2.edges()}
    assert canon_a == canon_b

    # Matrix conversion
    m = edge_list_to_matrix(g, V=3, directed=False)
    assert m[0][1] == 5 and m[1][0] == 5
    assert m[1][2] == 3 and m[2][1] == 3
    assert m[0][2] == 4 and m[2][0] == 4
    assert m[1][1] is None

    # Directed variant
    d = EdgeListGraph(directed=True)
    d.add_edge(1, 2, 10)
    d.add_edge(2, 3, 20)
    adj = edge_list_to_adj_dict(d, directed=True)
    assert adj[1] == {2: 10}
    assert adj[2] == {3: 20}
    assert 1 not in adj[2]                         # not inserted back
    assert adj[3] == {}                            # terminal vertex

    # Isolated vertex
    g = EdgeListGraph()
    g.add_vertex("loner")
    g.add_edge("a", "b")
    adj = edge_list_to_adj_dict(g)
    assert adj["loner"] == {}

    # Self-loop preserved
    g = EdgeListGraph(directed=True)
    g.add_edge("x", "x", 7)
    adj = edge_list_to_adj_dict(g, directed=True)
    assert adj["x"] == {"x": 7}

    print("All tests passed!")
