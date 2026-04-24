"""
Problem: Course Schedule (I and II)

Difficulty:
    Medium (LeetCode #207 — can-finish)
    Medium (LeetCode #210 — return an order)

---------------------------------------------------
Problem Statement:

You have `numCourses` courses, labelled 0..numCourses-1. Some
courses have prerequisites: each pair `[a, b]` means "to take a,
you must first take b".

    LC #207:  Return True iff it's POSSIBLE to finish all courses.
    LC #210:  Return ANY valid order, or [] if impossible.

Examples:
    numCourses = 2, prereqs = [[1, 0]]  →  True / order [0, 1]
    numCourses = 2, prereqs = [[1, 0], [0, 1]]  →  False / []   (cycle)

---------------------------------------------------
Why This Is The Canonical Topo-Sort Problem:

Prerequisites are directed edges: `prereq → course`. A valid
completion order is EXACTLY a topological order. If the prereq graph
has a cycle, there's no valid order.

    LC #207 = "is the graph a DAG?"
    LC #210 = "give me a topological order, or [] if impossible."

Both are one-line-of-Kahn's applications. We present the
solutions side by side.

---------------------------------------------------
Complexity:

    Time:  O(V + E)
    Space: O(V + E)

Where V = numCourses, E = len(prereqs).
"""

from collections import defaultdict, deque


# -------- LC #207: can-finish (boolean) --------

def can_finish(numCourses, prereqs):
    """
    Return True iff it's possible to complete all numCourses.

    Time:  O(V + E), Space: O(V + E).
    """
    adj = defaultdict(list)
    indeg = [0] * numCourses
    for a, b in prereqs:                           # [a, b] means b → a (prereq b before course a)
        adj[b].append(a)
        indeg[a] += 1

    queue = deque(i for i in range(numCourses) if indeg[i] == 0)
    taken = 0

    while queue:
        u = queue.popleft()
        taken += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)

    return taken == numCourses


# -------- LC #210: find-order --------

def find_order(numCourses, prereqs):
    """
    Return any valid completion order, or [] if impossible.

    Time:  O(V + E), Space: O(V + E).
    """
    adj = defaultdict(list)
    indeg = [0] * numCourses
    for a, b in prereqs:
        adj[b].append(a)
        indeg[a] += 1

    queue = deque(i for i in range(numCourses) if indeg[i] == 0)
    order = []

    while queue:
        u = queue.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)

    return order if len(order) == numCourses else []


# =========================================================================
# Test
# =========================================================================

def _is_valid_order(numCourses, prereqs, order):
    """Verify `order` lists every course once and respects all prereqs."""
    if sorted(order) != list(range(numCourses)):
        return False
    pos = {c: i for i, c in enumerate(order)}
    for a, b in prereqs:
        if pos[b] >= pos[a]:                       # b must come before a
            return False
    return True


if __name__ == "__main__":
    # LC #207 examples
    assert can_finish(2, [[1, 0]]) is True
    assert can_finish(2, [[1, 0], [0, 1]]) is False
    assert can_finish(1, []) is True
    assert can_finish(5, []) is True                # all isolated

    # Larger DAG
    prereqs = [[1, 0], [2, 1], [3, 2], [4, 2], [5, 3], [5, 4]]
    assert can_finish(6, prereqs) is True

    # LC #210 examples
    order = find_order(2, [[1, 0]])
    assert order == [0, 1]

    order = find_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]])
    assert _is_valid_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]], order)

    assert find_order(2, [[1, 0], [0, 1]]) == []   # cycle

    assert find_order(1, []) == [0]
    assert find_order(0, []) == []
    assert sorted(find_order(3, [])) == [0, 1, 2]

    # Self-loop IS a cycle (you'd need to take yourself first)
    assert can_finish(2, [[0, 0]]) is False
    assert find_order(2, [[0, 0]]) == []

    # Randomized: for random DAGs, find_order always succeeds and
    # output is always valid
    import random
    random.seed(42)
    for _ in range(200):
        V = random.randint(1, 15)
        perm = list(range(V))
        random.shuffle(perm)
        # Build edges obeying `perm` as a linearization
        prereqs = []
        for i in range(V):
            for j in range(i + 1, V):
                if random.random() < 0.3:
                    prereqs.append([perm[j], perm[i]])
        assert can_finish(V, prereqs)
        order = find_order(V, prereqs)
        assert _is_valid_order(V, prereqs, order)

    # Randomized: inject a cycle → must return False / []
    for _ in range(100):
        V = random.randint(2, 10)
        # Build a random graph WITH at least one cycle by adding a back-edge
        prereqs = []
        for i in range(V - 1):
            prereqs.append([i + 1, i])
        prereqs.append([0, V - 1])                 # back-edge closes the cycle
        assert can_finish(V, prereqs) is False
        assert find_order(V, prereqs) == []

    print("All tests passed!")
