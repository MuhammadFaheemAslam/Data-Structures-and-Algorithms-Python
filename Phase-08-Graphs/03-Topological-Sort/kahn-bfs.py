"""
kahn-bfs.py — Topological Sort Via Kahn's Algorithm

Kahn's algorithm produces a topological order by repeatedly emitting
vertices with IN-DEGREE 0 (no remaining dependencies), peeling them
off the graph.

---------------------------------------------------
The Algorithm:

    1. Compute in-degree for every vertex.
    2. Queue ← every vertex with in-degree 0.
    3. While queue is non-empty:
         u = queue.popleft()
         emit u
         for each v in outgoing-neighbours(u):
             indeg[v] -= 1
             if indeg[v] == 0:
                 queue.append(v)
    4. If we emitted fewer than V vertices → CYCLE. No topo order.

Each vertex enqueued once and dequeued once → O(V + E).

---------------------------------------------------
Deterministic Variants:

Swap the FIFO queue for a MIN-HEAP to get the LEXICOGRAPHICALLY
SMALLEST topo order. This matters for problems that ask for a
canonical result (LC #269 "alien dictionary", LC #1203
"project-management").

We include both.

---------------------------------------------------
Complexity:

    Time:  O(V + E)
    Space: O(V)
"""

from collections import deque
import heapq
import os


def _import_graph():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "adjl", os.path.join(os.path.dirname(__file__), "..", "01-Representations", "adjacency-list.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Graph


Graph = _import_graph()


# -------- Core Kahn's algorithm --------

def topological_sort(graph):
    """
    Return a valid topological order, or None if the graph has a cycle.

    Uses FIFO — whichever ready vertex was discovered first comes out first.

    Time: O(V + E), Space: O(V).
    """
    if not graph.is_directed():
        raise ValueError("topological sort requires a directed graph")

    indeg = _in_degrees(graph)

    queue = deque(v for v in graph.vertices() if indeg[v] == 0)
    order = []

    while queue:
        u = queue.popleft()
        order.append(u)
        for v in graph.neighbours_only(u):
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)

    if len(order) != len(graph):
        return None                                # cycle detected
    return order


# -------- Lexicographically smallest topo order (LC #269 style) --------

def lexicographic_topological_sort(graph):
    """
    Return the lexicographically smallest valid topo order, or None if cyclic.

    Uses a MIN-HEAP instead of a FIFO queue so that ready vertices
    come out in sorted order. Vertex type must support `<`.

    Time: O((V + E) log V), Space: O(V).
    """
    if not graph.is_directed():
        raise ValueError("topological sort requires a directed graph")

    indeg = _in_degrees(graph)

    heap = [v for v in graph.vertices() if indeg[v] == 0]
    heapq.heapify(heap)
    order = []

    while heap:
        u = heapq.heappop(heap)
        order.append(u)
        for v in graph.neighbours_only(u):
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(heap, v)

    if len(order) != len(graph):
        return None
    return order


# -------- Cycle detection (same idea, just return bool) --------

def has_cycle(graph):
    """Return True iff the directed graph has a cycle. O(V + E)."""
    return topological_sort(graph) is None


# -------- Shared: compute in-degrees --------

def _in_degrees(graph):
    indeg = {v: 0 for v in graph.vertices()}
    for u in graph.vertices():
        for v in graph.neighbours_only(u):
            indeg[v] += 1
    return indeg


# =========================================================================
# Test
# =========================================================================

def _is_valid_topo_order(graph, order):
    """Verify every edge u → v has pos[u] < pos[v] in the given order."""
    pos = {v: i for i, v in enumerate(order)}
    if set(pos) != set(graph.vertices()):
        return False
    for u in graph.vertices():
        for v in graph.neighbours_only(u):
            if pos[u] >= pos[v]:
                return False
    return True


if __name__ == "__main__":
    # Classic DAG (course prerequisites):
    #   intro_cs → ds → algos → os
    #   intro_cs → math → algos
    g = Graph(directed=True)
    for u, v in [("intro_cs", "ds"), ("intro_cs", "math"),
                 ("ds", "algos"), ("math", "algos"), ("algos", "os")]:
        g.add_edge(u, v)

    order = topological_sort(g)
    assert order is not None
    assert _is_valid_topo_order(g, order)
    assert order[0] == "intro_cs"                   # only vertex with indeg 0
    assert order[-1] == "os"                        # only vertex with outdeg 0

    # Cycle: should return None
    g = Graph(directed=True)
    g.add_edge(1, 2); g.add_edge(2, 3); g.add_edge(3, 1)
    assert topological_sort(g) is None
    assert has_cycle(g) is True

    # DAG with a self-loop → that's a cycle too
    g = Graph(directed=True)
    g.add_edge("a", "a")
    assert topological_sort(g) is None

    # Empty graph
    empty = Graph(directed=True)
    assert topological_sort(empty) == []

    # Isolated vertices
    g = Graph(directed=True)
    for v in ["a", "b", "c"]:
        g.add_vertex(v)
    order = topological_sort(g)
    assert set(order) == {"a", "b", "c"}

    # Undirected refuses
    ud = Graph()
    try:
        topological_sort(ud)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")

    # Lexicographic smallest: deterministic
    #   1 → 3, 2 → 3, both roots {1, 2}
    g = Graph(directed=True)
    g.add_edge(1, 3); g.add_edge(2, 3)
    lex = lexicographic_topological_sort(g)
    assert lex == [1, 2, 3]                         # 1 < 2 so emitted first

    g = Graph(directed=True)
    g.add_edge(2, 3); g.add_edge(1, 3)              # order of add irrelevant
    assert lexicographic_topological_sort(g) == [1, 2, 3]

    # Stress: every output of topological_sort must be a valid topo order
    import random
    random.seed(42)
    for _ in range(200):
        V = random.randint(1, 20)
        g = Graph(directed=True)
        # Generate a random DAG by ordering vertices and only adding u→v when u<v
        verts = list(range(V))
        random.shuffle(verts)
        for i, u in enumerate(verts):
            g.add_vertex(u)
            for v in verts[i + 1:]:
                if random.random() < 0.3:
                    g.add_edge(u, v)

        order = topological_sort(g)
        assert order is not None                    # random DAGs are acyclic by construction
        assert _is_valid_topo_order(g, order)
        assert _is_valid_topo_order(g, lexicographic_topological_sort(g))

    print("All tests passed!")
