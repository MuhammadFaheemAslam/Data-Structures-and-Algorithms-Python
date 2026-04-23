"""
Property: Height / Maximum Depth

LeetCode #104 — Maximum Depth of Binary Tree

HEIGHT of a tree is the number of EDGES from root to its deepest leaf.
DEPTH of a node is the number of edges from root to that node.

LC #104 asks for the "maximum depth" measured in NODES (root has depth 1,
which is h+1 where h is the edge-height). Both conventions are common;
we expose the LC convention as `max_depth` and the edge convention as
`height`.

---------------------------------------------------
The Classic Recursion:

    height(None) = -1                  (empty tree has no edges)
    height(node) = 1 + max(height(left), height(right))

Convert to the LC "depth in nodes" convention:

    max_depth(None) = 0
    max_depth(node) = 1 + max(max_depth(left), max_depth(right))

O(n) time, O(h) space — classic tree DP.
"""

import os
import sys
from collections import deque

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from implementation import TreeNode, tree_from_list


def max_depth(root):
    """
    LC #104: max depth measured in NODES (root has depth 1, None has depth 0).

    Time:  O(n).
    Space: O(h) — recursion stack.
    """
    if root is None:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


def height(root):
    """
    Height in EDGES. Empty tree has height -1; single node has height 0.

    Time:  O(n), Space: O(h).
    """
    if root is None:
        return -1
    return 1 + max(height(root.left), height(root.right))


def max_depth_iterative(root):
    """
    Iterative via BFS: count the number of levels.

    Time:  O(n), Space: O(w).
    """
    if root is None:
        return 0

    depth = 0
    queue = deque([root])
    while queue:
        depth += 1
        for _ in range(len(queue)):
            node = queue.popleft()
            if node.left is not None:  queue.append(node.left)
            if node.right is not None: queue.append(node.right)
    return depth


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    cases = [
        ([], 0),
        ([1], 1),
        ([1, 2], 2),
        ([1, 2, 3], 2),
        ([3, 9, 20, None, None, 15, 7], 3),        # LC example
        ([1, 2, 3, 4, None, None, 5, 6], 4),
        ([1, None, 2, None, 3, None, 4], 4),       # right chain
        ([1, 2, None, 3, None, 4, None, 5], 5),    # left chain
    ]

    for vals, expected in cases:
        tree = tree_from_list(vals)
        assert max_depth(tree) == expected, f"max_depth failed on {vals}"
        assert max_depth_iterative(tree) == expected, f"iterative failed on {vals}"
        # height = max_depth - 1 (for non-empty), or -1 for empty
        assert height(tree) == expected - 1

    # Single-node edge case for height
    assert height(tree_from_list([42])) == 0
    assert height(None) == -1

    print("All tests passed!")
