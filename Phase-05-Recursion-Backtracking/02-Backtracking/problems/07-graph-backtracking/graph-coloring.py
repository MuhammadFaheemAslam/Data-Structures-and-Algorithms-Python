"""
Problem: Graph Coloring (m-Colourability)

Difficulty: Hard (m-colourability is NP-complete for m ≥ 3)

---------------------------------------------------
Problem Statement:

Given an undirected graph and an integer `m`, assign a colour from
{0, 1, ..., m-1} to each vertex such that NO TWO ADJACENT VERTICES
share the same colour.

Return:
    - True (and optionally the assignment) if a valid colouring exists.
    - False if not.

---------------------------------------------------
Famous Result: The Four-Colour Theorem:

Any PLANAR graph (graph drawable in 2D without edge crossings) is
4-colourable. Proved in 1976 with computer assistance — the first
major theorem whose proof relied on exhaustive case-checking by a
computer.

For general (non-planar) graphs, m-colourability for m ≥ 3 is NP-complete.

---------------------------------------------------
The Backtracking Algorithm:

For each vertex in order:
    For each colour c in 0..m-1:
        If c doesn't conflict with any already-coloured neighbour:
            Assign c to this vertex
            Recurse to the next vertex
            If success, propagate up
            Otherwise, unassign c
    If no colour worked, return False.

---------------------------------------------------
Pruning:

1. Try colours in ORDER, skipping any that would conflict.
2. Assign to the **most-constrained vertex first** (MRV on the
   vertex with the fewest legal colours remaining). This
   dramatically reduces search depth on dense graphs.

We implement the basic version here; MRV is left as an exercise.
"""


# =========================================================================
# Basic m-Colouring via Backtracking
# =========================================================================

def can_color(graph, m):
    """
    True iff the graph is `m`-colourable.

    `graph`: dict mapping vertex → list of neighbour vertices.
             Edges are assumed UNDIRECTED (both directions present).

    Time:  O(m^n) worst case
    Space: O(n) for the colouring array
    """
    vertices = sorted(graph.keys())
    n = len(vertices)
    if n == 0:
        return True

    colour = {}                                    # vertex → colour

    def is_safe(v, c):
        """True if we can give `v` colour `c` without conflict."""
        for nbr in graph[v]:
            if colour.get(nbr) == c:
                return False
        return True

    def backtrack(idx):
        if idx == n:
            return True                            # all vertices coloured

        v = vertices[idx]
        for c in range(m):
            if is_safe(v, c):
                colour[v] = c
                if backtrack(idx + 1):
                    return True
                del colour[v]
        return False

    return backtrack(0)


def find_colouring(graph, m):
    """
    Return a valid m-colouring (dict vertex → colour) if one exists,
    else None.
    """
    vertices = sorted(graph.keys())
    n = len(vertices)
    if n == 0:
        return {}

    colour = {}

    def is_safe(v, c):
        for nbr in graph[v]:
            if colour.get(nbr) == c:
                return False
        return True

    def backtrack(idx):
        if idx == n:
            return True

        v = vertices[idx]
        for c in range(m):
            if is_safe(v, c):
                colour[v] = c
                if backtrack(idx + 1):
                    return True
                del colour[v]
        return False

    if backtrack(0):
        return colour
    return None


# =========================================================================
# Chromatic Number — Minimum m for Which a Graph Is Colourable
# =========================================================================

def chromatic_number(graph):
    """
    Return the smallest m such that `graph` is m-colourable.

    Time:  exponential — try m = 1, 2, 3, ... until a colouring works.
    Space: O(n)

    By the Four Colour Theorem, any planar graph has chromatic number ≤ 4.
    A complete graph K_n needs exactly n colours.
    """
    if not graph:
        return 0
    for m in range(1, len(graph) + 1):
        if can_color(graph, m):
            return m
    return len(graph)                             # fallback (should never hit)


# =========================================================================
# Test
# =========================================================================

def is_valid_colouring(graph, colouring):
    """Check that no edge connects same-coloured vertices."""
    for v, neighbours in graph.items():
        if v not in colouring:
            return False
        for nbr in neighbours:
            if colouring.get(nbr) == colouring[v]:
                return False
    return True


if __name__ == "__main__":
    # Complete graph K4 — needs 4 colours
    K4 = {0: [1, 2, 3], 1: [0, 2, 3], 2: [0, 1, 3], 3: [0, 1, 2]}
    assert not can_color(K4, 3)
    assert can_color(K4, 4)
    assert chromatic_number(K4) == 4
    print(f"K4: chromatic = {chromatic_number(K4)} (expected 4)")

    # Triangle K3 — needs 3 colours
    K3 = {0: [1, 2], 1: [0, 2], 2: [0, 1]}
    assert not can_color(K3, 2)
    assert can_color(K3, 3)
    assert chromatic_number(K3) == 3
    print(f"K3: chromatic = {chromatic_number(K3)} (expected 3)")

    # Bipartite graph (even cycle C4) — 2 colours suffice
    C4 = {0: [1, 3], 1: [0, 2], 2: [1, 3], 3: [0, 2]}
    assert can_color(C4, 2)
    assert chromatic_number(C4) == 2
    print(f"C4: chromatic = {chromatic_number(C4)} (expected 2)")

    # Odd cycle C5 — needs 3 colours (NOT bipartite)
    C5 = {0: [1, 4], 1: [0, 2], 2: [1, 3], 3: [2, 4], 4: [0, 3]}
    assert not can_color(C5, 2)
    assert can_color(C5, 3)
    assert chromatic_number(C5) == 3
    print(f"C5: chromatic = {chromatic_number(C5)} (expected 3)")

    # Trivial cases
    assert chromatic_number({}) == 0
    assert chromatic_number({0: []}) == 1
    assert chromatic_number({0: [], 1: []}) == 1                       # no edges → 1 colour

    # Star graph — centre + leaves — 2 colours
    STAR = {0: [1, 2, 3, 4], 1: [0], 2: [0], 3: [0], 4: [0]}
    assert chromatic_number(STAR) == 2
    print(f"Star (1 centre + 4 leaves): chromatic = 2")

    # Get and verify a colouring
    col = find_colouring(K4, 4)
    assert col is not None
    assert is_valid_colouring(K4, col)
    print(f"\nK4 with 4 colours: {col}")

    col = find_colouring(C5, 3)
    assert is_valid_colouring(C5, col)
    print(f"C5 with 3 colours: {col}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Applications of Graph Colouring:
    #
    #   - **Register allocation** in compilers: variables that are
    #     "live" at the same time are edges in an interference graph;
    #     CPU registers are the "colours."
    #   - **Scheduling**: courses that share students form a graph;
    #     time slots are colours.
    #   - **Frequency assignment** in cellular networks: nearby towers
    #     can't use the same frequency.
    #   - **Map colouring**: the original motivating example.
    #
    # Real-world graph-colouring solvers use backtracking + MRV +
    # constraint propagation. For very large graphs, heuristics like
    # DSATUR (Degree of Saturation) give good colourings quickly
    # but without a guarantee of optimality.
    # ---------------------------------------------------------------
