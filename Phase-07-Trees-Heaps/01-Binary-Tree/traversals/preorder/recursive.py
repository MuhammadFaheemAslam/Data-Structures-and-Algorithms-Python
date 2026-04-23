"""
Preorder Traversal — Recursive

Order: NODE, LEFT, RIGHT

Preorder is what you want when:
    - You're SERIALIZING a tree (you need the root BEFORE its children,
      so you can reconstruct from the first value you read).
    - You're COPYING / CLONING a tree recursively.
    - You're printing a directory tree (parent before children).

Example:
        1
       / \
      2   3    →  [1, 2, 3]
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from implementation import TreeNode, tree_from_list


def preorder_recursive(root):
    """
    Return values in preorder: node, left subtree, right subtree.

    Time:  O(n).
    Space: O(h) recursion stack.
    """
    result = []

    def walk(node):
        if node is None:
            return
        result.append(node.val)
        walk(node.left)
        walk(node.right)

    walk(root)
    return result


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    assert preorder_recursive(None) == []
    assert preorder_recursive(tree_from_list([1])) == [1]

    # LC #144 example: [1, None, 2, 3] → [1, 2, 3]
    assert preorder_recursive(tree_from_list([1, None, 2, 3])) == [1, 2, 3]

    # Balanced: [1, 2, 3] → [1, 2, 3]
    assert preorder_recursive(tree_from_list([1, 2, 3])) == [1, 2, 3]

    # The preorder of a BST is NOT sorted (that's inorder's job)
    assert preorder_recursive(tree_from_list([4, 2, 6, 1, 3, 5, 7])) == [4, 2, 1, 3, 6, 5, 7]

    # Right-skewed: preorder is the order of insertion for a right chain
    assert preorder_recursive(tree_from_list([1, None, 2, None, 3])) == [1, 2, 3]

    print("All tests passed!")
