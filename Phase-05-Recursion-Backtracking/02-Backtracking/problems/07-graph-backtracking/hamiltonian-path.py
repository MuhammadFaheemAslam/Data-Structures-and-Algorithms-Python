"""
Problem: Hamiltonian Path / Cycle

Difficulty: Hard (NP-complete)

---------------------------------------------------
Problem Statement:

A HAMILTONIAN PATH in a graph visits EVERY vertex EXACTLY ONCE.
A HAMILTONIAN CYCLE is a Hamiltonian path that also returns to the
start.

Given a graph (as an adjacency list or matrix), determine whether
a Hamiltonian path/cycle exists.

This is the classic NP-complete problem — no known polynomial
algorithm. Backtracking gives exponential worst-case but often
fast-enough performance for small n (≤ ~20).

---------------------------------------------------
Why Backtracking:

At each step we choose a NEXT vertex from our current position's
neighbours, preferring one not yet visited. If no valid next vertex
exists, BACKTRACK and try a different earlier choice. If we visit
all n vertices, we've found a Hamiltonian path.

The apply/revert pattern:
    apply:   path.append(v); visited.add(v)
    revert:  path.pop();     visited.remove(v)

---------------------------------------------------
Pruning Strategies (from optimization-techniques.md):

1. **Skip visited neighbours** — essential feasibility pruning.
2. **Degree check** — any vertex with degree < 2 can't be on a cycle
   (except start/end of a path).
3. **Most-constrained first** — try the neighbour with the fewest
   unvisited neighbours. (MRV-like; not implemented here but a
   standard optimization.)

---------------------------------------------------
Complexity:

    Time:  O(n!) worst case — try every permutation of vertices
    Space: O(n) path + O(n) visited
"""


# =========================================================================
# Hamiltonian Path (Any Start)
# =========================================================================

def has_hamiltonian_path(graph):
    """
    True iff the graph has a Hamiltonian path (visits every vertex
    once, any start and end vertex).

    `graph`: dict mapping vertex → list of neighbour vertices
             OR a list-of-lists (graph[v] = list of neighbours).

    Time:  O(n!)
    Space: O(n)
    """
    vertices = list(graph.keys()) if isinstance(graph, dict) else list(range(len(graph)))
    n = len(vertices)

    if n == 0:
        return True
    if n == 1:
        return True

    def neighbours(v):
        return graph[v] if isinstance(graph, (dict, list)) else []

    def backtrack(path, visited):
        if len(path) == n:
            return True

        current = path[-1]
        for nxt in neighbours(current):
            if nxt in visited:
                continue

            path.append(nxt)
            visited.add(nxt)

            if backtrack(path, visited):
                return True

            path.pop()
            visited.remove(nxt)

        return False

    # Try every vertex as a possible starting point
    for start in vertices:
        if backtrack([start], {start}):
            return True
    return False


def find_hamiltonian_path(graph):
    """
    Return a Hamiltonian path (as a list of vertices) if one exists,
    else None.
    """
    vertices = list(graph.keys()) if isinstance(graph, dict) else list(range(len(graph)))
    n = len(vertices)

    if n == 0:
        return []
    if n == 1:
        return vertices[:]

    def neighbours(v):
        return graph[v] if isinstance(graph, (dict, list)) else []

    def backtrack(path, visited):
        if len(path) == n:
            return path[:]                         # snapshot

        current = path[-1]
        for nxt in neighbours(current):
            if nxt in visited:
                continue

            path.append(nxt)
            visited.add(nxt)

            result = backtrack(path, visited)
            if result:
                return result

            path.pop()
            visited.remove(nxt)

        return None

    for start in vertices:
        result = backtrack([start], {start})
        if result:
            return result
    return None


# =========================================================================
# Hamiltonian Cycle
# =========================================================================

def has_hamiltonian_cycle(graph):
    """
    True iff the graph has a Hamiltonian cycle (a Hamiltonian path
    that returns to the starting vertex).

    Works on undirected or directed graphs.

    Time:  O(n!)
    Space: O(n)
    """
    vertices = list(graph.keys()) if isinstance(graph, dict) else list(range(len(graph)))
    n = len(vertices)

    if n == 0:
        return True                                # vacuously true
    if n == 1:
        return True                                # a single vertex is a trivial cycle

    def neighbours(v):
        return graph[v] if isinstance(graph, (dict, list)) else []

    # WLOG start at the first vertex — any Hamiltonian cycle includes it
    start = vertices[0]

    def backtrack(path, visited):
        if len(path) == n:
            # Must return to `start` to form a cycle
            return start in neighbours(path[-1])

        current = path[-1]
        for nxt in neighbours(current):
            if nxt in visited:
                continue

            path.append(nxt)
            visited.add(nxt)

            if backtrack(path, visited):
                return True

            path.pop()
            visited.remove(nxt)

        return False

    return backtrack([start], {start})


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Simple 4-node complete graph
    K4 = {
        0: [1, 2, 3],
        1: [0, 2, 3],
        2: [0, 1, 3],
        3: [0, 1, 2],
    }
    assert has_hamiltonian_path(K4) is True
    assert has_hamiltonian_cycle(K4) is True
    path = find_hamiltonian_path(K4)
    print(f"K4 — Hamiltonian path: {path}")
    assert path is not None and len(path) == 4
    print()

    # Path graph P4: 0 - 1 - 2 - 3 (linear chain)
    P4 = {
        0: [1],
        1: [0, 2],
        2: [1, 3],
        3: [2],
    }
    # Has a path (0-1-2-3) but no cycle (ends don't connect)
    assert has_hamiltonian_path(P4) is True
    assert has_hamiltonian_cycle(P4) is False
    print(f"P4 — path: {find_hamiltonian_path(P4)}, cycle: {has_hamiltonian_cycle(P4)}")
    print()

    # Two disconnected components — no HAM path
    DISC = {
        0: [1],
        1: [0],
        2: [3],
        3: [2],
    }
    assert has_hamiltonian_path(DISC) is False
    print(f"Disconnected graph — path exists? {has_hamiltonian_path(DISC)}")
    print()

    # Triangle + dangling edge (star): no Hamiltonian cycle but has a path
    GRAPH = {
        0: [1, 2],
        1: [0, 2, 3],
        2: [0, 1],
        3: [1],
    }
    assert has_hamiltonian_path(GRAPH) is True
    assert has_hamiltonian_cycle(GRAPH) is False
    print(f"Triangle + extension — path: {find_hamiltonian_path(GRAPH)}, cycle: False")
    print()

    # Empty graph
    assert has_hamiltonian_path({}) is True
    assert has_hamiltonian_cycle({}) is True

    # Single vertex, no edges
    assert has_hamiltonian_path({0: []}) is True
    assert has_hamiltonian_cycle({0: []}) is True

    # Two disconnected vertices
    assert has_hamiltonian_path({0: [], 1: []}) is False

    # Cycle graph C5 (5-cycle)
    C5 = {
        0: [1, 4],
        1: [0, 2],
        2: [1, 3],
        3: [2, 4],
        4: [0, 3],
    }
    assert has_hamiltonian_cycle(C5) is True
    print(f"5-cycle: Hamiltonian cycle exists? {has_hamiltonian_cycle(C5)}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Why Hamiltonian Path Is NP-Complete:
    #
    #   No polynomial-time algorithm is known. The decision version
    #   ("does a Hamiltonian path exist?") is NP-complete, and the
    #   optimization version (TSP, Travelling Salesman) is also NP-hard.
    #
    # Backtracking handles n up to ~20 comfortably. For larger n:
    #   - DP with bitmask:  O(n² · 2^n) — works up to ~22
    #     (see Phase 02 / 01 / 04-Dynamic-Programming / problems / knapsack.py
    #      for the general bitmask-DP pattern).
    #   - For truly large n: approximation algorithms (Christofides),
    #     heuristics (Lin-Kernighan), or specialized solvers (Concorde).
    # ---------------------------------------------------------------
