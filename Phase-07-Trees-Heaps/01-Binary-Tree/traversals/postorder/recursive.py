"""
Postorder Traversal — Recursive

Order: LEFT, RIGHT, NODE

Postorder is what you want when:
    - You need to EVALUATE an EXPRESSION TREE (evaluate children, then
      combine at the operator node).
    - You need to DELETE / FREE a tree (delete children first so the
      node pointer is still valid while processing them).
    - You're computing aggregates like HEIGHT, DIAMETER — you need
      results from both children before you can compute the parent's
      value.

Example:
        1
       / \
      2   3    →  [2, 3, 1]
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from implementation import TreeNode, tree_from_list


def postorder_recursive(root):
    """
    Return values in postorder: left, right, node.

    Time:  O(n).
    Space: O(h).
    """
    result = []

    def walk(node):
        if node is None:
            return
        walk(node.left)
        walk(node.right)
        result.append(node.val)

    walk(root)
    return result


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    assert postorder_recursive(None) == []
    assert postorder_recursive(tree_from_list([1])) == [1]

    # LC #145 example: [1, None, 2, 3] → [3, 2, 1]
    assert postorder_recursive(tree_from_list([1, None, 2, 3])) == [3, 2, 1]

    # Balanced: [1, 2, 3] → [2, 3, 1]
    assert postorder_recursive(tree_from_list([1, 2, 3])) == [2, 3, 1]

    # BST (4,2,6,1,3,5,7) → postorder = [1, 3, 2, 5, 7, 6, 4]
    assert postorder_recursive(tree_from_list([4, 2, 6, 1, 3, 5, 7])) == [1, 3, 2, 5, 7, 6, 4]

    # The root of a postorder list is always the LAST element
    root = tree_from_list([10, 5, 15, 2, 8, 12, 20])
    post = postorder_recursive(root)
    assert post[-1] == 10                           # root comes last

    print("All tests passed!")
