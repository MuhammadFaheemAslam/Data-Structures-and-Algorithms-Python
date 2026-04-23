"""
Problem: Generate Binary Numbers from 1 to n

Difficulty: Easy (GeeksforGeeks classic)

---------------------------------------------------
Problem Statement:

Given an integer n, generate the binary representations of all
integers from 1 to n, IN ORDER, using only a queue.

    n = 5  →  ["1", "10", "11", "100", "101"]

Constraint: use a QUEUE. The point of the problem is to see the
queue-based BFS pattern; any integer-to-binary conversion works
directly, but the queue technique is elegant and generalizable.

---------------------------------------------------
Why a Queue Works — the BFS Connection:

Think of binary strings as nodes in a BINARY TREE:

                           ""  (root — representing the empty string)
                          /  \
                         1    (invalid — leading zero)
                        / \
                       10  11
                      /  \  /  \
                     100 101 110 111

(We skip the invalid leading-zero branch.)

**Level-order traversal** of the non-leading-zero subtree produces
the binary numbers in sorted numerical order. Level-order = BFS =
queue-based traversal.

The algorithm:
    queue = ["1"]                              # start with "1"
    result = []
    while len(result) < n:
        s = queue.popleft()
        result.append(s)
        queue.append(s + "0")                  # children: append 0
        queue.append(s + "1")                  # and append 1
    return result

Each new string is formed by appending "0" or "1" to an existing
string — exactly how children are generated in BFS.

---------------------------------------------------
Time:   O(n · L) where L is the average binary length ≈ log n
Space:  O(n · L) for the queue and output

---------------------------------------------------
"""

from collections import deque


# =========================================================================
# Solution 1: Queue-Based BFS — The Intended Approach
# =========================================================================

def generate_binary_bfs(n):
    """
    Generate binary representations of 1..n using a queue.

    Time:  O(n · L)
    Space: O(n · L)
    """
    if n <= 0:
        return []

    result = []
    queue = deque(["1"])

    while len(result) < n:
        s = queue.popleft()
        result.append(s)
        queue.append(s + "0")
        queue.append(s + "1")

    return result


# =========================================================================
# Solution 2: Direct Conversion (For Comparison)
# =========================================================================

def generate_binary_direct(n):
    """
    Direct solution: format each i from 1 to n in binary.

    Time:  O(n · L)
    Space: O(n · L)

    Works equally well; doesn't use a queue. Shown to validate the
    BFS solution's output.
    """
    return [bin(i)[2:] for i in range(1, n + 1)]


# =========================================================================
# Variant: Generate the First n Binary Numbers WITHOUT Duplicates
# =========================================================================

def generate_binary_set(n, start="1"):
    """
    More generic: start from a given prefix and BFS outward.
    Useful for problems like "generate all k-digit binary numbers,"
    or "generate all strings matching a wildcard pattern."
    """
    if n <= 0:
        return []

    result = []
    queue = deque([start])
    while len(result) < n:
        if not queue:
            break
        s = queue.popleft()
        result.append(s)
        queue.append(s + "0")
        queue.append(s + "1")
    return result


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    # Canonical cases
    cases = [
        (0,   []),
        (1,   ["1"]),
        (2,   ["1", "10"]),
        (5,   ["1", "10", "11", "100", "101"]),
        (10,  ["1", "10", "11", "100", "101", "110", "111", "1000", "1001", "1010"]),
    ]

    for n, expected in cases:
        got_bfs = generate_binary_bfs(n)
        got_direct = generate_binary_direct(n)
        assert got_bfs == expected
        assert got_direct == expected
        print(f"generate_binary({n}) = {got_bfs}")

    # Verify that BFS and direct give the same output for many n
    for n in range(1, 50):
        assert generate_binary_bfs(n) == generate_binary_direct(n)

    print("\nStress test: BFS and direct agree for all n in [1, 50)")

    # Demo: why BFS is elegant — each new string is built from an existing one
    print("\nBFS trace for n = 7:")
    queue = deque(["1"])
    result = []
    while len(result) < 7:
        s = queue.popleft()
        result.append(s)
        print(f"   emit {s!r}, enqueue {s + '0'!r}, {s + '1'!r}; queue now {list(queue)}")
        queue.append(s + "0")
        queue.append(s + "1")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Related Queue-BFS Problems:
    #
    #   - Level-order tree traversal (Phase 07 Trees)
    #   - Shortest path in unweighted graphs (Phase 08 Graphs)
    #   - Word ladder (LC #127) — BFS over word transformations
    #   - Rotting Oranges (LC #994) — BFS over a grid
    #   - Open the Lock (LC #752) — BFS over states
    #
    # Anywhere you need to visit elements in "discovery order" — that's
    # a queue's job. Generating binary numbers is the tiniest instance.
    # ---------------------------------------------------------------
