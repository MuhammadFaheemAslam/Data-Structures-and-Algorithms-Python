"""
Problem: Network Delay Time

Difficulty: Medium (LeetCode #743)

---------------------------------------------------
Problem Statement:

A signal is sent from node `k` in a network of `n` nodes. Edge
`(u, v, w)` means u can send a signal to v with delay w.

Return the MINIMUM TIME for ALL nodes to receive the signal, or -1
if some node is unreachable.

Example:
    times = [[2,1,1], [2,3,1], [3,4,1]], n = 4, k = 2
    → 2    (node 2 immediately, node 1 at t=1, node 3 at t=1, node 4 at t=2)

---------------------------------------------------
Why This Is Pure Dijkstra:

"Minimum time for ALL nodes to receive the signal" = the MAXIMUM of
the shortest distances from `k` to each other node. This is exactly
the output of single-source Dijkstra; we then take the max.

If any node's distance is infinity → unreachable → return -1.

---------------------------------------------------
Complexity:

    Time:  O((V + E) log V)
    Space: O(V + E)
"""

import heapq
from collections import defaultdict


def network_delay_time(times, n, k):
    """
    Min time for all n nodes to receive the signal from node k.
    Return -1 if any node is unreachable.

    Time:  O((V + E) log V), Space: O(V + E).
    """
    # Build adjacency list: u → [(v, w), ...]
    adj = defaultdict(list)
    for u, v, w in times:
        adj[u].append((v, w))

    # Dijkstra from k
    INF = float("inf")
    dist = {i: INF for i in range(1, n + 1)}
    dist[k] = 0
    heap = [(0, k)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))

    max_delay = max(dist.values())
    return -1 if max_delay == INF else max_delay


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC examples
    assert network_delay_time([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2) == 2
    assert network_delay_time([[1, 2, 1]], 2, 1) == 1
    assert network_delay_time([[1, 2, 1]], 2, 2) == -1             # can't reach 1 from 2

    # Single node: signal already at source, time 0
    assert network_delay_time([], 1, 1) == 0

    # Multiple nodes but disconnected → -1
    assert network_delay_time([[1, 2, 5]], 3, 1) == -1

    # Ring 1 → 2 → 3 → 1 but starting at 1 — we only care about reaching 2 and 3
    assert network_delay_time([[1, 2, 1], [2, 3, 1], [3, 1, 1]], 3, 1) == 2

    # Multiple edges between same pair (Dijkstra takes the min)
    assert network_delay_time([[1, 2, 10], [1, 2, 3]], 2, 1) == 3

    # Star: source connects directly to every node
    times = [[1, i, i] for i in range(2, 11)]
    assert network_delay_time(times, 10, 1) == 10                  # max weight (to node 10)

    # Stress: compare with "run Dijkstra from every starting node"
    import random
    random.seed(42)
    for _ in range(100):
        n = random.randint(1, 15)
        num_edges = random.randint(0, n * n)
        times = []
        for _ in range(num_edges):
            u = random.randint(1, n)
            v = random.randint(1, n)
            if u != v:
                times.append([u, v, random.randint(1, 100)])
        start = random.randint(1, n)

        # Brute-force: build adj, do Dijkstra, compare
        adj = defaultdict(list)
        for u, v, w in times:
            adj[u].append((v, w))
        INF = float("inf")
        dist = {i: INF for i in range(1, n + 1)}
        dist[start] = 0
        heap = [(0, start)]
        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue
            for v, w in adj[u]:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(heap, (nd, v))
        max_d = max(dist.values())
        expected = -1 if max_d == INF else max_d

        assert network_delay_time(times, n, start) == expected

    print("All tests passed!")
