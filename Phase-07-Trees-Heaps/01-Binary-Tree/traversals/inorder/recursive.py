"""
Inorder Traversal — Recursive

Order: LEFT, NODE, RIGHT

For a BST, inorder produces the values in SORTED order. That's the
canonical use of inorder traversal — if you're going to do ONE thing
with a BST besides search/insert/delete, it's inorder.

Example:
        1
       / \
      2   3    →  [2, 1, 3]
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from implementation import TreeNode, tree_from_list


def inorder_recursive(root):
    """
    Return a list of values in inorder (left, node, right).

    Time:  O(n).
    Space: O(h) recursion stack, where h is tree height.
    """
    result = []

    def walk(node):
        if node is None:
            return
        walk(node.left)
        result.append(node.val)
        walk(node.right)

    walk(root)
    return result


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Empty tree
    assert inorder_recursive(None) == []

    # Single node
    assert inorder_recursive(tree_from_list([1])) == [1]

    # LC #94 example: [1, None, 2, 3] → [1, 3, 2]
    root = tree_from_list([1, None, 2, 3])
    assert inorder_recursive(root) == [1, 3, 2]

    # Balanced: [1, 2, 3] → [2, 1, 3]
    assert inorder_recursive(tree_from_list([1, 2, 3])) == [2, 1, 3]

    # BST invariant: inorder should be sorted for a valid BST
    bst = tree_from_list([4, 2, 6, 1, 3, 5, 7])
    got = inorder_recursive(bst)
    assert got == sorted(got)
    assert got == [1, 2, 3, 4, 5, 6, 7]

    # Left-skewed chain
    left_skew = tree_from_list([5, 4, None, 3, None, 2, None, 1])
    assert inorder_recursive(left_skew) == [1, 2, 3, 4, 5]

    print("All tests passed!")
