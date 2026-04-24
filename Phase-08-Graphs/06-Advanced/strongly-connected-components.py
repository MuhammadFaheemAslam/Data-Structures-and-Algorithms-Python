"""
strongly-connected-components.py — Tarjan's and Kosaraju's SCC Algorithms

A STRONGLY CONNECTED COMPONENT (SCC) of a DIRECTED graph is a maximal
set of vertices such that there's a directed path from every vertex
to every other. If we "collapse" each SCC into a single node, the
resulting graph — the CONDENSATION — is a DAG, which lets us apply
DAG algorithms (topological sort, longest path, etc.) to any directed
graph.

---------------------------------------------------
Why SCCs Matter:

- Control-flow graphs: SCCs are LOOPS. Everything outside SCCs is
  straight-line code.
- Reference cycles in garbage collection.
- "Who transitively depends on whom?" in dependency analysis.
- Implication graphs in 2-SAT: satisfiability iff no SCC contains
  both a variable and its negation.
- Social-network analysis: SCCs in a follow-graph are tightly-knit
  communities.

---------------------------------------------------
Two Classic Algorithms:

### 1. Kosaraju's — two DFS passes, O(V + E):

    pass 1: DFS on original graph; record vertices in POST-ORDER.
    pass 2: DFS on TRANSPOSE graph (all edges reversed), processing
            vertices in REVERSE post-order. Each tree in this DFS
            is one SCC.

Simple, easy to explain. Requires building the transpose.

### 2. Tarjan's — one DFS pass, O(V + E):

Maintain a DFS stack. For each vertex, track:
    - disc[v]  = DFS discovery time (index).
    - low[v]   = the lowest `disc` of any vertex REACHABLE from v's
                 subtree that's still on the DFS stack.

When we finish v and `low[v] == disc[v]`, pop the DFS stack until v
comes out — that's one SCC.

Slightly subtler. Single-pass. Same asymptotic. Slightly faster in
practice.

Both implemented here. Tarjan's is what you'd typically see in
textbooks and LC-style problems; Kosaraju's is the "explain the
concept" algorithm.

---------------------------------------------------
Complexity (both):

    Time:  O(V + E)
    Space: O(V)
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
# Tarjan's algorithm
# =========================================================================

def tarjan_scc(graph):
    """
    Return a list of SCCs (each a set of vertices) via Tarjan's algorithm.

    Time: O(V + E), Space: O(V).
    """
    if not graph.is_directed():
        raise ValueError("SCC is defined for DIRECTED graphs")

    disc = {}                                      # discovery time
    low = {}                                       # low-link
    on_stack = set()
    stack = []
    sccs = []
    time = [0]

    def strongconnect(u):
        disc[u] = low[u] = time[0]
        time[0] += 1
        stack.append(u)
        on_stack.add(u)

        for v in graph.neighbours_only(u):
            if v not in disc:
                # Tree edge — recurse
                strongconnect(v)
                low[u] = min(low[u], low[v])
            elif v in on_stack:
                # Back edge to a vertex on the current DFS stack
                low[u] = min(low[u], disc[v])
            # If v is visited but not on_stack, it's in a COMPLETED
            # SCC — ignore

        # If u is the root of its SCC, pop the stack until u comes out
        if low[u] == disc[u]:
            scc = set()
            while True:
                w = stack.pop()
                on_stack.discard(w)
                scc.add(w)
                if w == u:
                    break
            sccs.append(scc)

    for u in graph.vertices():
        if u not in disc:
            strongconnect(u)

    return sccs


# =========================================================================
# Kosaraju's algorithm
# =========================================================================

def kosaraju_scc(graph):
    """
    Return a list of SCCs via Kosaraju's two-pass algorithm.

    Time: O(V + E), Space: O(V + E) (transpose graph).
    """
    if not graph.is_directed():
        raise ValueError("SCC is defined for DIRECTED graphs")

    # Pass 1 — post-order on original graph
    order = []
    visited = set()

    def dfs1(u):
        stack = [(u, iter(graph.neighbours_only(u)))]
        visited.add(u)
        while stack:
            node, it = stack[-1]
            found_next = False
            for v in it:
                if v not in visited:
                    visited.add(v)
                    stack.append((v, iter(graph.neighbours_only(v))))
                    found_next = True
                    break
            if not found_next:
                order.append(node)                 # post-order emit
                stack.pop()

    for u in graph.vertices():
        if u not in visited:
            dfs1(u)

    # Pass 2 — DFS on transpose, processing in reverse post-order
    # Build transpose
    transpose = {u: [] for u in graph.vertices()}
    for u in graph.vertices():
        for v in graph.neighbours_only(u):
            transpose[v].append(u)

    sccs = []
    assigned = set()

    def dfs2(start):
        comp = set()
        stack = [start]
        assigned.add(start)
        while stack:
            u = stack.pop()
            comp.add(u)
            for v in transpose[u]:
                if v not in assigned:
                    assigned.add(v)
                    stack.append(v)
        return comp

    for u in reversed(order):
        if u not in assigned:
            sccs.append(dfs2(u))

    return sccs


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    def _to_frozen(scc_list):
        return {frozenset(c) for c in scc_list}

    # Classic 4-SCC example (CLRS-style):
    #   a → b → c → d
    #   ↑       ↓
    #   a ←──── d
    #       e → f
    #           ↓
    #           g
    g = Graph(directed=True)
    for u, v in [("a", "b"), ("b", "c"), ("c", "d"), ("d", "a"),
                  ("e", "f"), ("f", "g")]:
        g.add_edge(u, v)

    # SCCs: {a, b, c, d}, {e}, {f}, {g}
    tarjan_result = _to_frozen(tarjan_scc(g))
    kosaraju_result = _to_frozen(kosaraju_scc(g))
    expected = {frozenset({"a", "b", "c", "d"}), frozenset({"e"}),
                frozenset({"f"}), frozenset({"g"})}
    assert tarjan_result == expected
    assert kosaraju_result == expected

    # DAG: every vertex is its own SCC
    g = Graph(directed=True)
    for u, v in [(1, 2), (1, 3), (2, 4), (3, 4)]:
        g.add_edge(u, v)
    assert _to_frozen(tarjan_scc(g)) == {frozenset({i}) for i in range(1, 5)}
    assert _to_frozen(kosaraju_scc(g)) == {frozenset({i}) for i in range(1, 5)}

    # Single large cycle
    g = Graph(directed=True)
    for i in range(5):
        g.add_edge(i, (i + 1) % 5)
    assert _to_frozen(tarjan_scc(g)) == {frozenset({0, 1, 2, 3, 4})}
    assert _to_frozen(kosaraju_scc(g)) == {frozenset({0, 1, 2, 3, 4})}

    # Self-loop: singleton SCC (still a cycle)
    g = Graph(directed=True)
    g.add_edge("x", "x")
    assert _to_frozen(tarjan_scc(g)) == {frozenset({"x"})}
    assert _to_frozen(kosaraju_scc(g)) == {frozenset({"x"})}

    # Isolated vertex: singleton SCC
    g = Graph(directed=True)
    g.add_vertex("alone")
    g.add_edge(1, 2)
    sccs = _to_frozen(tarjan_scc(g))
    assert frozenset({"alone"}) in sccs

    # Empty
    empty = Graph(directed=True)
    assert tarjan_scc(empty) == []
    assert kosaraju_scc(empty) == []

    # Undirected refuses
    ud = Graph()
    try:
        tarjan_scc(ud)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError (tarjan)")
    try:
        kosaraju_scc(ud)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError (kosaraju)")

    # Stress: both algorithms must agree
    import random
    random.seed(42)
    for _ in range(200):
        V = random.randint(1, 15)
        g = Graph(directed=True)
        for i in range(V):
            g.add_vertex(i)
        for _ in range(random.randint(0, V * 2)):
            u = random.randint(0, V - 1)
            v = random.randint(0, V - 1)
            g.add_edge(u, v)

        assert _to_frozen(tarjan_scc(g)) == _to_frozen(kosaraju_scc(g))

    print("All tests passed!")
