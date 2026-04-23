"""
Property: Symmetric Tree

LeetCode #101 — Symmetric Tree

A tree is SYMMETRIC around its root if, when you reflect it
left-to-right, you get the same tree back. Equivalently:

    root.left is a MIRROR IMAGE of root.right.

Two subtrees A and B are mirror images iff:

    A is None and B is None,  OR
    A.val == B.val
        AND mirror(A.left, B.right)
        AND mirror(A.right, B.left)

---------------------------------------------------
Example:

        1
       / \
      2   2
     / \ / \
    3  4 4  3          → symmetric ✓

        1
       / \
      2   2
       \   \
        3   3          → NOT symmetric
                         (left's right-child = 3, right's left-child = None)

---------------------------------------------------
Two Implementations:

    1. Recursive mirror check — natural and concise
    2. Iterative via queue — pull pairs (L, R) from a queue, check
       equality, enqueue (L.left, R.right) and (L.right, R.left)

Both O(n) time, O(h) space.

---------------------------------------------------
Not the same as "is mirror of another tree":

LC #226 INVERTS a tree in place (swap every node's children). That's a
different problem. Symmetric checks a PROPERTY; invert is a MUTATION.
"""

import os
import sys
from collections import deque

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from implementation import TreeNode, tree_from_list


# -------- Recursive --------

def is_symmetric(root):
    """
    Time:  O(n), Space: O(h).
    """
    if root is None:
        return True

    def mirror(a, b):
        if a is None and b is None:
            return True
        if a is None or b is None:
            return False
        return (a.val == b.val
                and mirror(a.left, b.right)
                and mirror(a.right, b.left))

    return mirror(root.left, root.right)


# -------- Iterative (queue of pairs) --------

def is_symmetric_iterative(root):
    """
    Time:  O(n), Space: O(w).
    """
    if root is None:
        return True

    queue = deque([(root.left, root.right)])
    while queue:
        a, b = queue.popleft()
        if a is None and b is None:
            continue
        if a is None or b is None or a.val != b.val:
            return False
        queue.append((a.left, b.right))
        queue.append((a.right, b.left))
    return True


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    cases = [
        ([], True),
        ([1], True),
        ([1, 2, 2], True),
        ([1, 2, 2, 3, 4, 4, 3], True),                      # LC example 1
        ([1, 2, 2, None, 3, None, 3], False),               # LC example 2
        ([1, 2, 2, 3, None, 3], False),                     # children shape differs
        ([1, 2, 2, 3, 4, 4, 3, 5, 6, 7, 8, 8, 7, 6, 5], True),
    ]

    for vals, expected in cases:
        tree = tree_from_list(vals)
        assert is_symmetric(tree) == expected, f"recursive mismatch on {vals}"
        assert is_symmetric_iterative(tree) == expected, f"iterative mismatch on {vals}"

    # Large symmetric tree (reflect a random left subtree to the right)
    import random
    random.seed(42)

    def build_random(depth, rng):
        if depth == 0 or rng.random() < 0.3:
            return None
        return TreeNode(rng.randint(0, 10),
                        left=build_random(depth - 1, rng),
                        right=build_random(depth - 1, rng))

    def mirror_of(node):
        if node is None:
            return None
        return TreeNode(node.val, left=mirror_of(node.right), right=mirror_of(node.left))

    for _ in range(50):
        left = build_random(5, random)
        right = mirror_of(left)
        root = TreeNode(0, left=left, right=right)
        assert is_symmetric(root)
        assert is_symmetric_iterative(root)

    print("All tests passed!")
