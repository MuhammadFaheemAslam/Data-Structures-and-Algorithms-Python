"""
Property: Height-Balanced?

LeetCode #110 — Balanced Binary Tree

A tree is HEIGHT-BALANCED if, for every node, the heights of its left
and right subtrees differ by AT MOST 1.

---------------------------------------------------
The Naive (O(n log n)) Approach:

    def is_balanced(node):
        if node is None: return True
        return (abs(height(node.left) - height(node.right)) <= 1
                and is_balanced(node.left)
                and is_balanced(node.right))

Each height() call is O(n), and we call it at every node → O(n · log n)
for balanced trees, O(n²) for skewed. Too slow for large inputs.

---------------------------------------------------
The O(n) Fix — Short-Circuit Height:

Have the recursion RETURN the height, but return a sentinel (-1, say)
to mean "this subtree is unbalanced — stop bothering". The parent sees
-1 and propagates it. When recursion returns, the root's result tells
us balance:

    height ≥ 0  → balanced, and the height is what's returned
    height < 0  → unbalanced

Single O(n) pass, one return value, no redundant work. Classic.

This is the SAME pattern as diameter.py and max-path-sum.py — a DFS
that returns a "useful-for-parent" value and also short-circuits /
side-effects for the global answer.
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from implementation import TreeNode, tree_from_list


# -------- O(n) — short-circuit via sentinel height --------

def is_balanced(root):
    """
    Return True iff every subtree has |height(left) - height(right)| ≤ 1.

    Time:  O(n).
    Space: O(h).
    """
    def check(node):
        """Return height if balanced, -1 if we've already found an imbalance."""
        if node is None:
            return 0
        left = check(node.left)
        if left == -1:
            return -1
        right = check(node.right)
        if right == -1:
            return -1
        if abs(left - right) > 1:
            return -1
        return 1 + max(left, right)

    return check(root) != -1


# -------- O(n log n) — for comparison --------

def is_balanced_naive(root):
    """
    Naive: at every node, recompute both subtree heights from scratch.

    Time:  O(n log n) balanced, O(n²) skewed.
    """
    def height(node):
        if node is None:
            return 0
        return 1 + max(height(node.left), height(node.right))

    if root is None:
        return True
    return (abs(height(root.left) - height(root.right)) <= 1
            and is_balanced_naive(root.left)
            and is_balanced_naive(root.right))


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    cases = [
        ([], True),
        ([1], True),
        ([1, 2, 3], True),
        ([3, 9, 20, None, None, 15, 7], True),             # LC example 1
        ([1, 2, 2, 3, 3, None, None, 4, 4], False),         # LC example 2
        ([1, None, 2, None, 3], False),                     # right chain
        ([1, 2, None, 3, None, 4], False),                  # left chain
        ([1, 2, 3, 4, 5, 6, 7], True),                      # perfect
    ]

    for vals, expected in cases:
        tree = tree_from_list(vals)
        assert is_balanced(tree) == expected, f"is_balanced({vals}) expected {expected}"
        assert is_balanced_naive(tree) == expected

    # Stress random: both methods must agree
    import random
    random.seed(42)
    for _ in range(200):
        n = random.randint(0, 50)
        vals = [random.randint(0, 100) if random.random() < 0.85 else None for _ in range(n)]
        if vals and vals[0] is None:
            vals[0] = 0
        tree = tree_from_list(vals)
        assert is_balanced(tree) == is_balanced_naive(tree)

    print("All tests passed!")
