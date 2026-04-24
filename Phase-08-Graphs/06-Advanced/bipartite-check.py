"""
Problem: Is Graph Bipartite?

Difficulty: Medium (LeetCode #785)

---------------------------------------------------
A graph is BIPARTITE if its vertex set can be split into two sides
A and B such that EVERY edge goes between the sides — no edge has
both endpoints in A or both in B.

Equivalently: the graph is 2-COLORABLE. You can color every vertex
with one of two colors such that every edge connects differently-
colored vertices.

    Bipartite:      1 — 2     (1 gets "red", 2 gets "blue")
                    │
                    3 — 4     (3 is blue, 4 is red)

    NOT bipartite:  1 — 2 — 3 — 1   (odd cycle)
                    (the cycle 1-2-3-1 forces a color conflict)

---------------------------------------------------
The Key Fact — Odd Cycles:

    A graph is BIPARTITE if and only if it has NO ODD-LENGTH CYCLE.

Any odd cycle prevents 2-coloring: walk around it and you'll land
on the same vertex with two different colors. Even cycles are fine.

---------------------------------------------------
The Algorithm — BFS 2-Coloring:

For each unvisited vertex, start a BFS and ALTERNATE colors as you
advance by one BFS level. If we ever find an edge connecting two
same-colored vertices, we've found an odd cycle → not bipartite.

    color = {}
    for each vertex u:
        if u not in color:
            color[u] = 0
            queue = [u]
            while queue:
                v = queue.popleft()
                for w in neighbours(v):
                    if w not in color:
                        color[w] = 1 - color[v]
                        queue.append(w)
                    elif color[w] == color[v]:
                        return False          # same-color edge → odd cycle
    return True

---------------------------------------------------
Where Bipartiteness Matters:

- **Matching problems**: bipartite graphs admit PERFECT-MATCHING
  algorithms (Hopcroft-Karp, Hungarian) that are much faster than
  general-graph matching.
- **Graph 2-coloring**: same thing, different framing.
- **Scheduling**: "pair up tasks with machines / students with rooms"
  — bipartite structure lets you solve in polynomial time.
- **Crosswords and Sudoku on bipartite constraint graphs**.
- **Chemistry**: bond-diagram analyses.

---------------------------------------------------
Complexity:

    Time:  O(V + E)
    Space: O(V)
"""

from collections import defaultdict, deque


# -------- LC #785 API (adjacency list as list-of-lists) --------

def is_bipartite(graph):
    """
    LC #785 API: `graph` is a list where graph[i] is the list of neighbours of vertex i.

    Time:  O(V + E), Space: O(V).
    """
    n = len(graph)
    color = [-1] * n

    for start in range(n):
        if color[start] != -1:
            continue
        color[start] = 0
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]
                    queue.append(v)
                elif color[v] == color[u]:
                    return False

    return True


# -------- Alternative: same algorithm exposing the coloring --------

def bipartition(graph):
    """
    Return (side_A, side_B) tuple if the graph is bipartite; None otherwise.
    `graph` is the same list-of-lists format.

    Time: O(V + E), Space: O(V).
    """
    n = len(graph)
    color = [-1] * n

    for start in range(n):
        if color[start] != -1:
            continue
        color[start] = 0
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]
                    queue.append(v)
                elif color[v] == color[u]:
                    return None

    A = {i for i in range(n) if color[i] == 0}
    B = {i for i in range(n) if color[i] == 1}
    return (A, B)


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #785 examples
    #   Graph 1:  0 — 1      Graph 2:  0 — 1 — 2 — 3 — 0  (4-cycle, bipartite)
    #              \ /                           \_/_/
    #               2
    # LC format: for each i, graph[i] = neighbours of i
    g1 = [[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]]
    # Vertex 0 connects to 1, 2, 3. Vertex 1 connects to 0, 2. That forms an
    # odd cycle 0-1-2-0 → NOT bipartite.
    assert is_bipartite(g1) is False

    g2 = [[1, 3], [0, 2], [1, 3], [0, 2]]         # 4-cycle: 0-1-2-3-0
    assert is_bipartite(g2) is True

    # Disconnected: bipartite component + isolated vertex
    g3 = [[1], [0], []]
    assert is_bipartite(g3) is True

    # Single vertex, no edges
    assert is_bipartite([[]])

    # Empty
    assert is_bipartite([]) is True

    # Self-loop → odd cycle of length 1
    g = [[0]]
    assert is_bipartite(g) is False

    # Complete graph K3 (triangle) — not bipartite
    g = [[1, 2], [0, 2], [0, 1]]
    assert is_bipartite(g) is False

    # Complete bipartite K_{3,3}: two sets {0, 1, 2} and {3, 4, 5}, all cross edges
    g = [[3, 4, 5], [3, 4, 5], [3, 4, 5],
         [0, 1, 2], [0, 1, 2], [0, 1, 2]]
    assert is_bipartite(g) is True
    parts = bipartition(g)
    assert parts is not None
    A, B = parts
    assert A == {0, 1, 2} and B == {3, 4, 5} or A == {3, 4, 5} and B == {0, 1, 2}

    # Stress: cross-check with "contains odd cycle" brute force
    def brute_has_odd_cycle(graph):
        n = len(graph)
        for start in range(n):
            # BFS from `start`; compute distances
            dist = {start: 0}
            queue = deque([start])
            while queue:
                u = queue.popleft()
                for v in graph[u]:
                    if v not in dist:
                        dist[v] = dist[u] + 1
                        queue.append(v)
                    else:
                        # If (dist[v] + dist[u]) is EVEN, the implied cycle via
                        # BFS tree is ODD in length — actually this check is subtle.
                        # Easier: two neighbours with SAME parity of BFS depth imply
                        # an odd cycle.
                        if (dist[u] + dist[v]) % 2 == 0 and u != v:
                            return True
                        # Self-loops:
                        if u == v:
                            return True
        return False

    import random
    random.seed(42)
    for _ in range(200):
        n = random.randint(1, 10)
        # Build undirected adjacency in LC format
        graph = [[] for _ in range(n)]
        for _ in range(random.randint(0, n * n // 2)):
            u, v = random.randint(0, n - 1), random.randint(0, n - 1)
            if v not in graph[u]:
                graph[u].append(v)
                if u != v and u not in graph[v]:
                    graph[v].append(u)
        is_b = is_bipartite(graph)
        # odd-cycle check: is_b == True  ↔  no odd cycle
        # Our brute is a less-elegant version that relies on BFS parity; keep
        # the primary test as "bipartition is a valid coloring" instead.
        if is_b:
            parts = bipartition(graph)
            assert parts is not None
            A, B = parts
            # Every edge must cross A and B
            for u, nbrs in enumerate(graph):
                for v in nbrs:
                    assert (u in A and v in B) or (u in B and v in A), (
                        f"edge {u}-{v} same side"
                    )
        else:
            assert bipartition(graph) is None

    print("All tests passed!")
