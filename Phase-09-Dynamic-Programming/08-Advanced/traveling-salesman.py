"""
Traveling Salesman Problem — Held-Karp DP

Given an n×n distance matrix `dist`, find the minimum-cost
HAMILTONIAN CYCLE: a tour that visits every city exactly once and
returns to the start.

TSP is NP-hard — no polynomial-time algorithm is known. For small n,
we can solve it EXACTLY with bitmask DP (Held-Karp, 1962).

---------------------------------------------------
The Held-Karp Recurrence:

    State:   dp[mask][i] = min cost of any path starting at vertex 0,
                           visiting exactly the vertices in `mask`,
                           currently at vertex i.

    Base:    dp[{0}][0] = 0.
             dp[other][i] = +∞ initially.

    Trans.:  For every (mask, i) with bit i set in mask:
                for j not in mask:
                    new_mask = mask | (1 << j)
                    dp[new_mask][j] = min(dp[new_mask][j], dp[mask][i] + dist[i][j])

    Answer:  min over i > 0 of (dp[full_mask][i] + dist[i][0])

---------------------------------------------------
Complexity:

    Time:  O(n² · 2^n)
    Space: O(n · 2^n)

For n = 20: 2^20 × 400 ≈ 4 × 10⁸ ops — tight but feasible in a
compiled language; slow in pure Python but correct.

---------------------------------------------------
When You'd Actually Use This:

- Small-scale exact TSP (n ≤ 20) — e.g. optimal drilling path on a
  circuit board, small delivery routes.
- SUBPROBLEM of larger approximate algorithms — e.g. Christofides
  uses it on leaves of a tree of shortcuts.
- Educational / benchmark baseline against which heuristics
  (nearest-neighbour, 2-opt, simulated annealing) are compared.

For REAL-WORLD TSP (thousands of cities):
    - LP-based branch-and-cut (Concorde solver).
    - Lin-Kernighan and variants.
    - Heuristics with known approximation ratios.

Not this algorithm. But understanding Held-Karp makes those more
accessible.
"""


def tsp_min_cost(dist):
    """
    Return the minimum cost of a Hamiltonian cycle starting/ending at vertex 0.
    `dist[i][j]` is the cost of the edge from i to j; `float("inf")` means
    "no edge". Symmetric distances not required.

    Time:  O(n² · 2^n)
    Space: O(n · 2^n)
    """
    n = len(dist)
    if n == 0:
        return 0
    if n == 1:
        return dist[0][0]                         # self-loop cost (often 0)

    INF = float("inf")
    FULL = (1 << n) - 1

    # dp[mask][i] = min cost of a path from vertex 0, visiting exactly `mask`, ending at `i`
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0                                  # mask = just {0}, at vertex 0

    # Iterate masks in ascending popcount order — simple range works since
    # any sub-mask has smaller integer value than its super-mask (when
    # including the same low bit) isn't quite true in general, BUT we
    # ALWAYS extend from a smaller mask to a larger one, so computing
    # dp[new_mask] from dp[mask] with mask < new_mask is correct.
    for mask in range(1, 1 << n):
        if not (mask & 1):
            continue                              # vertex 0 must be in the mask
        for i in range(n):
            if not (mask >> i) & 1:
                continue
            if dp[mask][i] == INF:
                continue
            # Try extending to each j not yet visited
            remaining = (~mask) & FULL
            m = remaining
            while m:
                j_bit = m & -m                     # lowest set bit
                j = j_bit.bit_length() - 1
                m ^= j_bit
                new_mask = mask | j_bit
                cand = dp[mask][i] + dist[i][j]
                if cand < dp[new_mask][j]:
                    dp[new_mask][j] = cand

    # Final step: close the tour back to vertex 0
    best = INF
    for i in range(1, n):
        if dp[FULL][i] != INF:
            best = min(best, dp[FULL][i] + dist[i][0])

    return best


def tsp_optimal_tour(dist):
    """
    Return (min_cost, tour) where tour is a list of vertices starting and
    ending at 0. Uses the same DP but with parent pointers for reconstruction.

    Time:  O(n² · 2^n)
    Space: O(n · 2^n)
    """
    n = len(dist)
    if n == 0:
        return (0, [])
    if n == 1:
        return (dist[0][0], [0, 0])

    INF = float("inf")
    FULL = (1 << n) - 1

    dp = [[INF] * n for _ in range(1 << n)]
    parent = [[-1] * n for _ in range(1 << n)]
    dp[1][0] = 0

    for mask in range(1, 1 << n):
        if not (mask & 1):
            continue
        for i in range(n):
            if not (mask >> i) & 1 or dp[mask][i] == INF:
                continue
            remaining = (~mask) & FULL
            m = remaining
            while m:
                j_bit = m & -m
                j = j_bit.bit_length() - 1
                m ^= j_bit
                new_mask = mask | j_bit
                cand = dp[mask][i] + dist[i][j]
                if cand < dp[new_mask][j]:
                    dp[new_mask][j] = cand
                    parent[new_mask][j] = i

    # Find the best ending vertex for the full-mask state
    best_cost = INF
    best_end = -1
    for i in range(1, n):
        if dp[FULL][i] + dist[i][0] < best_cost:
            best_cost = dp[FULL][i] + dist[i][0]
            best_end = i

    if best_end == -1:
        return (INF, [])

    # Reconstruct tour by walking parent pointers
    tour = []
    mask = FULL
    cur = best_end
    while cur != -1:
        tour.append(cur)
        prev = parent[mask][cur]
        mask ^= (1 << cur)
        cur = prev
    tour.reverse()
    tour.append(0)                                # close the cycle
    return (best_cost, tour)


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Triangle (n=3): only two possible tours, both of cost = sum of all edges
    dist = [
        [0, 1, 2],
        [1, 0, 3],
        [2, 3, 0],
    ]
    # 0 → 1 → 2 → 0: 1 + 3 + 2 = 6
    # 0 → 2 → 1 → 0: 2 + 3 + 1 = 6
    assert tsp_min_cost(dist) == 6
    cost, tour = tsp_optimal_tour(dist)
    assert cost == 6
    assert tour[0] == 0 and tour[-1] == 0
    assert sorted(tour[:-1]) == [0, 1, 2]

    # Unit square (n=4):
    #     0---1
    #     |   |
    #     3---2
    # Edge lengths: 0-1=1, 1-2=1, 2-3=1, 3-0=1, 0-2=sqrt(2)~1.414, 1-3=sqrt(2)~1.414
    import math
    s = math.sqrt(2)
    dist = [
        [0, 1, s, 1],
        [1, 0, 1, s],
        [s, 1, 0, 1],
        [1, s, 1, 0],
    ]
    # Best tour: 0 → 1 → 2 → 3 → 0 (or reverse) = 4
    assert abs(tsp_min_cost(dist) - 4.0) < 1e-9
    cost, tour = tsp_optimal_tour(dist)
    assert abs(cost - 4.0) < 1e-9

    # Single vertex (trivial cycle)
    assert tsp_min_cost([[0]]) == 0

    # Empty
    assert tsp_min_cost([]) == 0

    # Asymmetric (directed) distances
    dist = [
        [0, 10, 15, 20],
        [5,  0,  9, 10],
        [6, 13,  0, 12],
        [8,  8,  9,  0],
    ]
    # Brute force: enumerate every permutation starting at 0
    import itertools
    def brute_tsp(dist):
        n = len(dist)
        if n <= 1:
            return 0
        best = float("inf")
        for perm in itertools.permutations(range(1, n)):
            total = dist[0][perm[0]]
            for a, b in zip(perm, perm[1:]):
                total += dist[a][b]
            total += dist[perm[-1]][0]
            if total < best:
                best = total
        return best

    assert tsp_min_cost(dist) == brute_tsp(dist)

    # Stress: random graphs, fast vs brute
    import random
    random.seed(42)
    for _ in range(30):
        n = random.randint(1, 7)
        dist = [[0 if i == j else random.randint(1, 50) for j in range(n)] for i in range(n)]
        assert tsp_min_cost(dist) == brute_tsp(dist)

        if n >= 2:
            cost, tour = tsp_optimal_tour(dist)
            assert cost == brute_tsp(dist)
            # Validate tour
            assert tour[0] == 0 and tour[-1] == 0
            assert sorted(tour[:-1]) == list(range(n))
            actual_cost = sum(dist[tour[i]][tour[i + 1]] for i in range(n))
            assert actual_cost == cost

    print("All tests passed!")
