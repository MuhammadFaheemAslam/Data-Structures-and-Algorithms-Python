"""
Problem: Cheapest Flights Within K Stops

Difficulty: Medium (LeetCode #787)

---------------------------------------------------
Problem Statement:

Given `flights = [[from, to, price], ...]`, find the cheapest flight
from `src` to `dst` with AT MOST `K` STOPS (= K + 1 edges).
Return -1 if impossible.

Example:
    n = 3, flights = [[0,1,100], [1,2,100], [0,2,500]]
    src = 0, dst = 2, k = 1 (at most 1 stop, = 2 edges)
    → 200  (path 0 → 1 → 2; only 1 intermediate stop, 2 edges total)

    With k = 0 (no stops, just direct):
    → 500  (direct 0 → 2)

---------------------------------------------------
Why Plain Dijkstra Fails:

Dijkstra's invariant — "once popped, the distance is final" —
BREAKS when we also have to track the HOP COUNT. A cheaper-but-longer
path that exceeds K stops is useless even if it has the best cost so
far, so "shortest cost" isn't the only minimum we care about.

    Counterexample:
        0 → A → B → dst       cost 1, stops 2
        0 → dst                cost 100, stops 0
        K = 0 → cheap path FAILS (too many stops), must pick expensive
        K = 2 → cheap path WINS

A plain Dijkstra wouldn't hold onto both candidates when they reach
an intermediate node.

---------------------------------------------------
Two Correct Approaches:

    1. BFS by levels (modified Bellman-Ford):
       Relax every edge K + 1 rounds. At round r, dist holds the
       cheapest cost to reach each vertex with AT MOST r edges.
       O(K · E).

    2. Dijkstra augmented with hop count:
       Push (cost, hops, vertex) instead of (cost, vertex). Don't
       skip vertices just because you've seen them cheaper — only
       skip paths that exceed K stops.
       O((V + E · K) log V) — slower worst case but often faster in
       practice due to heap's greedy behavior.

We implement BOTH. The BFS/Bellman-Ford version is the "easier to
reason about" standard interview answer.

---------------------------------------------------
Complexity:

    Bellman-Ford-style: O((K + 1) · E)
    Modified Dijkstra:  O(E · K log V) worst case

Both return the cheapest cost or -1.
"""

from collections import defaultdict, deque
import heapq


# -------- Solution 1: Bellman-Ford by levels --------

def find_cheapest_price_bellman_ford(n, flights, src, dst, k):
    """
    Time:  O((k + 1) · E), Space: O(n).
    """
    INF = float("inf")
    dist = [INF] * n
    dist[src] = 0

    # Do k + 1 rounds (k stops → k + 1 edges max)
    for _ in range(k + 1):
        # Use a snapshot so this round's relaxations don't affect each other
        # (otherwise a single round could relax two edges in a chain, overcounting)
        snap = dist[:]
        for u, v, price in flights:
            if snap[u] != INF and snap[u] + price < dist[v]:
                dist[v] = snap[u] + price

    return dist[dst] if dist[dst] != INF else -1


# -------- Solution 2: Modified Dijkstra (carries hop count) --------

def find_cheapest_price_dijkstra(n, flights, src, dst, k):
    """
    Time:  O(E · K log V) worst case, Space: O(V + E).
    """
    adj = defaultdict(list)
    for u, v, price in flights:
        adj[u].append((v, price))

    # heap of (cost, stops_used, node)
    # stops_used is HOPS = (edges so far), not LC's "K stops" notation
    heap = [(0, 0, src)]
    # For a given (node, stops), track the min cost we've seen; anything
    # worse can be pruned. (Without this, the heap can blow up.)
    best = {}

    while heap:
        cost, stops, u = heapq.heappop(heap)
        if u == dst:
            return cost
        if stops > k:
            continue                                # too many stops already — k stops = k+1 edges
        # Prune if we've seen this (node, stops) cheaper
        key = (u, stops)
        if key in best and best[key] <= cost:
            continue
        best[key] = cost
        for v, w in adj[u]:
            heapq.heappush(heap, (cost + w, stops + 1, v))

    return -1


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #787 examples
    assert find_cheapest_price_bellman_ford(3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1) == 200
    assert find_cheapest_price_bellman_ford(3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0) == 500
    assert find_cheapest_price_dijkstra(3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1) == 200
    assert find_cheapest_price_dijkstra(3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0) == 500

    # Edge: src == dst → 0 (even with k = 0)
    assert find_cheapest_price_bellman_ford(5, [], 2, 2, 0) == 0
    assert find_cheapest_price_dijkstra(5, [], 2, 2, 0) == 0

    # Unreachable
    assert find_cheapest_price_bellman_ford(3, [[0, 1, 5]], 0, 2, 10) == -1
    assert find_cheapest_price_dijkstra(3, [[0, 1, 5]], 0, 2, 10) == -1

    # Longer detour vs direct
    #   0 → 1 → 2 → 3   chain cost 10 (3 edges, 2 stops)
    #   0 → 3           direct cost 50 (1 edge, 0 stops)
    flights = [[0, 1, 3], [1, 2, 3], [2, 3, 4], [0, 3, 50]]
    for f in (find_cheapest_price_bellman_ford, find_cheapest_price_dijkstra):
        assert f(4, flights, 0, 3, 0) == 50        # need direct
        assert f(4, flights, 0, 3, 1) == 50        # still must be direct (1 stop allows 2 edges; chain needs 3)
        assert f(4, flights, 0, 3, 2) == 10        # chain fits: 3 edges, 2 stops

    # Cycle doesn't trap the algorithm (hops bound terminates it)
    flights = [[0, 1, 1], [1, 2, 1], [2, 0, 1]]     # cycle 0↔1↔2
    for f in (find_cheapest_price_bellman_ford, find_cheapest_price_dijkstra):
        assert f(3, flights, 0, 2, 5) == 2

    # Stress: cross-check both solutions
    import random
    random.seed(42)
    for _ in range(200):
        n = random.randint(1, 10)
        edges = []
        for _ in range(random.randint(0, n * n)):
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v:
                edges.append([u, v, random.randint(1, 100)])
        src = random.randint(0, n - 1)
        dst = random.randint(0, n - 1)
        k = random.randint(0, n)

        a = find_cheapest_price_bellman_ford(n, edges, src, dst, k)
        b = find_cheapest_price_dijkstra(n, edges, src, dst, k)
        assert a == b, f"mismatch at n={n}, edges={edges}, src={src}, dst={dst}, k={k}: BF={a}, DJ={b}"

    print("All tests passed!")
