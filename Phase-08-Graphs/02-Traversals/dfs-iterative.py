"""
dfs-iterative.py — DFS With An Explicit Stack

Same algorithm as the recursive version, but using our own stack
instead of the call stack. Two reasons to use this:

    1. Large graphs (V > ~1000): Python's default recursion limit
       would blow up.
    2. You want to pause/resume/save state — can't do that with
       recursion easily.

---------------------------------------------------
The Algorithm:

    stack = [start]
    visited = set()
    while stack:
        u = stack.pop()
        if u in visited: continue        # <-- important: we might push duplicates
        visited.add(u)
        VISIT u
        for v in neighbours(u):
            if v not in visited:
                stack.append(v)

Note the "check on POP" — not on push — because the same vertex can
be pushed multiple times before any visit happens. Example:
A — B — C and A — C: push B and C from A; push C again from B. If we
don't check on pop, we'd visit C twice.

Alternative: mark-visited on PUSH instead of POP. Both work; we use
check-on-pop because it most closely mirrors the recursive version
and is the "safe default" that works even with multiple pushes.

---------------------------------------------------
Postorder Without Recursion:

Iterative postorder is trickier — we need to know when all of a
vertex's children are done. Technique: push a `(u, False)` to
indicate "enter u", and after pushing children, push `(u, True)` as
a marker to emit u. When we pop `(u, True)`, children are done.

We include both pre-order and post-order iterative variants.
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


# -------- Preorder --------

def dfs_preorder_iter(graph, start):
    """
    Iterative preorder DFS.

    Note: neighbour traversal order differs from the recursive version
    because we push to a stack (LIFO). To match recursive preorder
    exactly, reverse the neighbours before pushing.

    Time: O(V + E), Space: O(V).
    """
    if start not in graph:
        return []

    order = []
    visited = set()
    stack = [start]

    while stack:
        u = stack.pop()
        if u in visited:
            continue
        visited.add(u)
        order.append(u)
        # Push neighbours; they'll be popped LIFO, so reverse to mirror recursion
        nbrs = list(graph.neighbours_only(u))
        for v in reversed(nbrs):
            if v not in visited:
                stack.append(v)

    return order


# -------- Postorder --------

def dfs_postorder_iter(graph, start):
    """
    Iterative postorder DFS using a "visited-marker" pattern:

        Push (u, False) → "enter u"
        On pop (u, False):
            Push (u, True)  → "will emit u when this pops"
            Push every unvisited neighbour as (v, False)
        On pop (u, True): emit u

    Time: O(V + E), Space: O(V).
    """
    if start not in graph:
        return []

    order = []
    visited = set()
    stack = [(start, False)]

    while stack:
        u, done = stack.pop()
        if done:
            order.append(u)
            continue
        if u in visited:
            continue
        visited.add(u)
        # Re-push as "done" — will emit after all children processed
        stack.append((u, True))
        nbrs = list(graph.neighbours_only(u))
        for v in reversed(nbrs):
            if v not in visited:
                stack.append((v, False))

    return order


# =========================================================================
# Test — cross-check against recursive version
# =========================================================================

if __name__ == "__main__":
    # Import the recursive versions for comparison
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "dfsr", os.path.join(os.path.dirname(__file__), "dfs-recursive.py"))
    dfsr = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dfsr)

    # Small graph
    g = Graph()
    for u, v in [(0, 1), (0, 2), (1, 3), (1, 4)]:
        g.add_edge(u, v)

    assert dfs_preorder_iter(g, 0) == dfsr.dfs_preorder(g, 0)
    assert dfs_postorder_iter(g, 0) == dfsr.dfs_postorder(g, 0)

    # Empty
    empty = Graph()
    assert dfs_preorder_iter(empty, "any") == []
    assert dfs_postorder_iter(empty, "any") == []

    # Single isolated vertex
    g = Graph()
    g.add_vertex(42)
    assert dfs_preorder_iter(g, 42) == [42]
    assert dfs_postorder_iter(g, 42) == [42]

    # Directed cycle: neither variant loops
    cyc = Graph(directed=True)
    cyc.add_edge(1, 2); cyc.add_edge(2, 3); cyc.add_edge(3, 1)
    assert sorted(dfs_preorder_iter(cyc, 1)) == [1, 2, 3]
    assert sorted(dfs_postorder_iter(cyc, 1)) == [1, 2, 3]

    # Large chain — recursive would blow up; iterative shouldn't
    big = Graph(directed=True)
    for i in range(5000):
        big.add_edge(i, i + 1)
    pre = dfs_preorder_iter(big, 0)
    assert pre == list(range(5001))
    post = dfs_postorder_iter(big, 0)
    assert post == list(range(5000, -1, -1))

    # Stress: iterative and recursive must agree on smaller random graphs
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

        assert dfs_preorder_iter(g, start) == dfsr.dfs_preorder(g, start)
        assert dfs_postorder_iter(g, start) == dfsr.dfs_postorder(g, start)

    print("All tests passed!")
