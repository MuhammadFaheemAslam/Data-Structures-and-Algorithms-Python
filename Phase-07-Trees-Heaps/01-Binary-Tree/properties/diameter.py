"""
Property: Diameter

LeetCode #543 — Diameter of Binary Tree

The DIAMETER of a binary tree is the number of EDGES on the longest
path between any two nodes. That path may or may not pass through the
root, and its endpoints are both leaves.

Example:
        1
       / \
      2   3
     / \
    4   5

    Longest path: 4 - 2 - 5 = 2 edges, but also 4 - 2 - 1 - 3 = 3 edges.
    Diameter = 3.

---------------------------------------------------
The Key Insight:

For ANY node `n`, the longest path passing THROUGH `n` has length:

    height(n.left) + height(n.right) + 2

(if both subtrees are empty, that's 0 + 0 + 2 = 2 edges... wait, that's
wrong — if n is a leaf, longest through n is 0 edges). Let's adjust:

Using the "height in edges" convention where height(None) = -1, the
longest path through `n` is:

    (1 + height(n.left)) + (1 + height(n.right))
    = height(n.left) + height(n.right) + 2

For a leaf: height(None) + height(None) + 2 = -2 + 2 = 0. ✓

The diameter of the whole tree is the MAX of this quantity over all
nodes.

---------------------------------------------------
The Trap:

If you compute height(n.left) and height(n.right) AT EVERY NODE,
you're doing O(n) height computations each O(n) — overall O(n²).

Instead, fuse the two computations: a single recursive pass that
returns `height(node)` AND side-effects a max-diameter variable.

This "return one thing, update another" dual-purpose recursion is a
PATTERN that appears in many binary-tree problems:
    - max path sum      (returns best "downward" path, updates best overall)
    - longest ZigZag    (returns best ending-left / ending-right, updates best)
    - balanced check    (returns height, updates is_balanced)

Same template, different payload.

---------------------------------------------------
Complexity:

    Time:  O(n)
    Space: O(h) recursion stack
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from implementation import TreeNode, tree_from_list


def diameter(root):
    """
    Return the diameter (longest path in edges) of the binary tree.

    Uses a dual-purpose DFS that returns the height of each subtree
    while updating a captured `best` across all nodes.

    Time:  O(n).
    Space: O(h).
    """
    best = [0]                                     # mutable box for the closure

    def depth(node):
        """Return height in edges; -1 for empty. Updates `best` as a side effect."""
        if node is None:
            return -1
        left = depth(node.left)
        right = depth(node.right)
        # Path through this node = left+right+2 edges
        through = left + right + 2
        if through > best[0]:
            best[0] = through
        return 1 + max(left, right)

    depth(root)
    return best[0]


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    cases = [
        ([], 0),
        ([1], 0),
        ([1, 2], 1),
        ([1, 2, 3], 2),
        ([1, 2, 3, 4, 5], 3),                      # LC #543 example: 4-2-1-3 or similar
        ([1, 2, 3, 4, 5, None, None, 6, 7], 4),    # path 6-4-2-1-3 (4 edges)
        ([1, None, 2, None, 3, None, 4], 3),       # right chain
        ([4, -7, -3, None, None, -9, -3, 9, -7, -4,
          None, 6, None, -6, -6, None, None, 0, 6,
          5, None, 9, None, None, -1, -4, None, None,
          None, -2], 8),                           # LC sample large case
    ]
    for vals, expected in cases:
        tree = tree_from_list(vals)
        got = diameter(tree)
        assert got == expected, f"diameter({vals}) = {got}, expected {expected}"

    # Degenerate left chain of 10 nodes → diameter = 9 edges
    root = TreeNode(1)
    cur = root
    for i in range(2, 11):
        cur.left = TreeNode(i)
        cur = cur.left
    assert diameter(root) == 9

    print("All tests passed!")
