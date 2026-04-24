"""
Problem: Clone Graph

Difficulty: Medium (LeetCode #133)

---------------------------------------------------
Problem Statement:

Given a reference to a node in a connected undirected graph, return
a DEEP COPY — a fresh graph that has the same shape but all new
Node objects.

    class Node:
        val: int
        neighbors: list[Node]

---------------------------------------------------
Why This Is The Canonical Graph-Traversal Problem:

Cloning requires TWO things per node:
    1. Visit every reachable node.                 ← graph traversal
    2. Map OLD → NEW so repeat visits return the same clone.
                                                     ← hash map

Without the map, recursion would infinitely loop on any cycle.
With the map, the traversal naturally terminates and produces the
shape we want.

The pattern — "DFS + hash map to avoid reprocessing" — generalizes
to MANY problems: memoized DP on a graph, longest-path, subtree
serialization. This problem is the simplest case.

---------------------------------------------------
Complexity:

    Time:  O(V + E) — each node visited once, each edge traversed once.
    Space: O(V) for the map + O(V) recursion stack.
"""


class Node:
    """The LC graph node format."""
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


# -------- Solution 1: DFS --------

def clone_graph_dfs(node):
    """
    Recursive DFS clone. O(V + E) time, O(V) space.
    """
    if node is None:
        return None

    old_to_new = {}

    def walk(old):
        if old in old_to_new:
            return old_to_new[old]
        clone = Node(old.val)
        old_to_new[old] = clone                    # IMPORTANT: register BEFORE recursing
                                                   # otherwise cycles loop forever
        clone.neighbors = [walk(nbr) for nbr in old.neighbors]
        return clone

    return walk(node)


# -------- Solution 2: BFS --------

from collections import deque


def clone_graph_bfs(node):
    """
    Iterative BFS clone. Handy when V is large and Python's
    recursion limit is a concern.

    O(V + E) time, O(V) space.
    """
    if node is None:
        return None

    old_to_new = {node: Node(node.val)}
    queue = deque([node])

    while queue:
        old = queue.popleft()
        for nbr in old.neighbors:
            if nbr not in old_to_new:
                old_to_new[nbr] = Node(nbr.val)
                queue.append(nbr)
            old_to_new[old].neighbors.append(old_to_new[nbr])

    return old_to_new[node]


# =========================================================================
# Helpers for testing
# =========================================================================

def build_graph_from_adj(adj):
    """
    Build an LC-style graph from an adjacency list in {val: [nbr_vals]} form.

    Values must be unique. Returns the Node with the smallest val (so the
    caller has a deterministic starting point).

    LC convention: 1-indexed vertex values.
    """
    if not adj:
        return None
    nodes = {v: Node(v) for v in adj}
    for v, nbrs in adj.items():
        nodes[v].neighbors = [nodes[n] for n in nbrs]
    return nodes[min(adj)]


def graph_to_adj(node):
    """Serialize a Node graph back to an adjacency dict for comparison."""
    if node is None:
        return {}
    adj = {}
    seen = {node}
    queue = deque([node])
    while queue:
        cur = queue.popleft()
        adj[cur.val] = sorted(nbr.val for nbr in cur.neighbors)
        for nbr in cur.neighbors:
            if nbr not in seen:
                seen.add(nbr)
                queue.append(nbr)
    return adj


def graphs_are_disjoint(a, b):
    """True iff no Node object is shared between the two graphs."""
    a_nodes = set()
    if a is not None:
        queue = deque([a])
        while queue:
            n = queue.popleft()
            if id(n) in a_nodes:
                continue
            a_nodes.add(id(n))
            queue.extend(n.neighbors)
    # Walk b; none of its Nodes should appear in a_nodes
    if b is not None:
        queue = deque([b])
        seen = set()
        while queue:
            n = queue.popleft()
            if id(n) in seen:
                continue
            seen.add(id(n))
            if id(n) in a_nodes:
                return False
            queue.extend(n.neighbors)
    return True


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #133 example: 4-node ring
    #     1 — 2
    #     |   |
    #     4 — 3
    orig = build_graph_from_adj({
        1: [2, 4],
        2: [1, 3],
        3: [2, 4],
        4: [1, 3],
    })

    for cloner in (clone_graph_dfs, clone_graph_bfs):
        cloned = cloner(orig)
        # Same shape
        assert graph_to_adj(cloned) == graph_to_adj(orig)
        # Fresh nodes
        assert graphs_are_disjoint(orig, cloned)

    # None → None
    assert clone_graph_dfs(None) is None
    assert clone_graph_bfs(None) is None

    # Single node, no neighbors
    orig = Node(1)
    cloned = clone_graph_dfs(orig)
    assert cloned is not None
    assert cloned is not orig
    assert cloned.val == 1 and cloned.neighbors == []

    # Self-loop
    orig = Node(1)
    orig.neighbors = [orig]
    cloned = clone_graph_dfs(orig)
    assert cloned is not orig
    assert cloned.neighbors[0] is cloned           # cloned self-loop too

    # Triangle
    orig = build_graph_from_adj({1: [2, 3], 2: [1, 3], 3: [1, 2]})
    cloned = clone_graph_bfs(orig)
    assert graph_to_adj(cloned) == graph_to_adj(orig)
    assert graphs_are_disjoint(orig, cloned)

    # Stress: random graphs, both cloners produce the same shape as the original
    import random
    random.seed(42)
    for _ in range(100):
        V = random.randint(1, 20)
        adj = {v: [] for v in range(1, V + 1)}
        for u in range(1, V + 1):
            for w in range(u + 1, V + 1):
                if random.random() < 0.3:
                    adj[u].append(w)
                    adj[w].append(u)
        if not any(adj.values()):
            continue
        orig = build_graph_from_adj(adj)
        orig_adj = graph_to_adj(orig)
        for cloner in (clone_graph_dfs, clone_graph_bfs):
            cloned = cloner(orig)
            assert graph_to_adj(cloned) == orig_adj
            assert graphs_are_disjoint(orig, cloned)

    print("All tests passed!")
