"""
Problem: Binary Tree Maximum Path Sum

Difficulty: Hard (LeetCode #124)

---------------------------------------------------
Problem Statement:

A PATH in a binary tree is a sequence of nodes where each adjacent pair
is connected by an edge. A node can appear at most once. The path does
NOT need to pass through the root.

Return the maximum possible SUM of node values along any path.
Node values can be NEGATIVE, so longer is not always better.

Example:
        -10
        /  \
       9    20
           /  \
          15   7

    Best path: 15 -> 20 -> 7 = 42.  (Ignoring -10 helps — it's negative.)

---------------------------------------------------
The Pattern (Again):

Same dual-purpose DFS as diameter.py and balanced.py:

    gain(node) = max DOWNWARD gain endable at this node
               = max(0, node.val + max(gain(left), gain(right)))
                   ^ the "0" means "skip this subtree if it drags us down"
               but NOTE: node itself must be included in `gain`,
                          otherwise you can't CHAIN through it.
               Actually: gain = node.val + max(0, max(gain_left, gain_right))

    best so far (side-effect): max over all nodes of
        node.val + max(0, gain_left) + max(0, gain_right)

The subtle trick: `gain` returns the best path ENDING at this node and
going DOWNWARD only (so it can be extended by the parent). `best` is
the best path that might PEAK at this node (using both children).

---------------------------------------------------
Complexity:

    Time:  O(n).
    Space: O(h).
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from implementation import TreeNode, tree_from_list


def max_path_sum(root):
    """
    Return the max path sum over any path in the tree.

    Time: O(n), Space: O(h).
    """
    # None case: LC guarantees at least one node, but handle defensively.
    if root is None:
        return 0

    best = [float("-inf")]

    def gain(node):
        """Max downward gain ending at `node`. Updates `best` with peaks through here."""
        if node is None:
            return 0
        # Use 0 as "skip this subtree" — don't force a negative gain on ourselves
        left_gain = max(gain(node.left), 0)
        right_gain = max(gain(node.right), 0)

        # Best PATH that peaks at this node
        peak_here = node.val + left_gain + right_gain
        if peak_here > best[0]:
            best[0] = peak_here

        # Best DOWNWARD continuation from this node (for parent to extend)
        return node.val + max(left_gain, right_gain)

    gain(root)
    return best[0]


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    cases = [
        ([1, 2, 3], 6),                            # LC example: 2-1-3
        ([-10, 9, 20, None, None, 15, 7], 42),     # LC example 2: 15-20-7
        ([1], 1),
        ([-3], -3),                                # single negative node
        ([-3, -2, -1], -1),                        # best is just the -1
        ([2, -1], 2),                              # skip the -1
        ([1, 2], 3),
        ([1, -2, -3, 1, 3, -2, None, -1], 3),      # LC variant
        ([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1], 48),  # LC #124 medium
    ]
    for vals, expected in cases:
        tree = tree_from_list(vals)
        got = max_path_sum(tree)
        assert got == expected, f"max_path_sum({vals}) = {got}, expected {expected}"

    # Brute force cross-check: enumerate every simple path by peak node.
    # A simple path in a tree has a unique highest point (its "peak"); from
    # there, it descends 0 or more steps into each subtree.
    def downward_sums(node):
        """Yield the sum of every downward path starting at `node` (non-empty)."""
        if node is None:
            return
        yield node.val
        for s in downward_sums(node.left):
            yield node.val + s
        for s in downward_sums(node.right):
            yield node.val + s

    def brute_max_path_sum(root):
        if root is None:
            return 0
        best = float("-inf")
        def walk(node):
            nonlocal best
            if node is None:
                return
            # Single-node path
            best = max(best, node.val)
            # Path descending only one side from this peak
            for s in downward_sums(node.left):
                best = max(best, node.val + s)
            for s in downward_sums(node.right):
                best = max(best, node.val + s)
            # Path crossing through this peak (left-down + node + right-down)
            left_sums = list(downward_sums(node.left))
            right_sums = list(downward_sums(node.right))
            for ls in left_sums:
                for rs in right_sums:
                    best = max(best, ls + node.val + rs)
            walk(node.left)
            walk(node.right)
        walk(root)
        return best

    import random
    random.seed(42)
    for _ in range(100):
        n = random.randint(1, 8)
        vals = [random.randint(-20, 20) if random.random() < 0.8 else None for _ in range(n)]
        if vals[0] is None:
            vals[0] = 0
        tree = tree_from_list(vals)
        expected = brute_max_path_sum(tree)
        got = max_path_sum(tree)
        assert got == expected, f"vals={vals}, got {got}, expected {expected}"

    print("All tests passed!")
