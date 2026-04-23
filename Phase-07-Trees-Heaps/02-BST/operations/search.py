"""
BST Search

LeetCode #700 — Search in a Binary Search Tree

---------------------------------------------------
The Algorithm:

    search(node, key):
        while node and node.val != key:
            node = node.left if key < node.val else node.right
        return node

Three outcomes per step:
    - key == node.val  → found, return node.
    - key <  node.val  → recurse left.
    - key >  node.val  → recurse right.

If we fall off the tree (node is None), the key isn't present.

---------------------------------------------------
Complexity:

    Time:  O(h) — walks a single root-to-leaf path.
    Space: O(1) iterative, O(h) recursive.

For a BALANCED tree, h = log n. For a degenerate (chain) tree, h = n.
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "01-Binary-Tree"))
from implementation import TreeNode, tree_from_list


# -------- Iterative --------

def search(root, key):
    """
    Return the node whose value equals `key`, or None if absent.

    Time:  O(h), Space: O(1).
    """
    node = root
    while node is not None:
        if key == node.val:
            return node
        node = node.left if key < node.val else node.right
    return None


# -------- Recursive --------

def search_recursive(root, key):
    """Same contract, recursive form. Time O(h), Space O(h)."""
    if root is None or root.val == key:
        return root
    if key < root.val:
        return search_recursive(root.left, key)
    return search_recursive(root.right, key)


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #700 example
    bst = tree_from_list([4, 2, 7, 1, 3])
    assert search(bst, 2).val == 2
    assert search(bst, 5) is None

    # Tree of the classic BST used throughout this module
    bst = tree_from_list([8, 3, 10, 1, 6, None, 14, None, None, 4, 7, 13])
    for k in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
        assert search(bst, k).val == k
        assert search_recursive(bst, k).val == k

    for k in [0, 2, 5, 9, 11, 12, 15, 100]:
        assert search(bst, k) is None
        assert search_recursive(bst, k) is None

    # Empty
    assert search(None, 1) is None
    assert search_recursive(None, 1) is None

    # Stress: build a BST from random inserts, verify all ops agree with set
    import random
    random.seed(42)

    def insert(root, key):
        if root is None:
            return TreeNode(key)
        if key < root.val:
            root.left = insert(root.left, key)
        elif key > root.val:
            root.right = insert(root.right, key)
        return root

    root = None
    truth = set()
    for _ in range(500):
        k = random.randint(0, 200)
        root = insert(root, k)
        truth.add(k)

    for k in range(-10, 220):
        expected = k in truth
        assert (search(root, k) is not None) == expected
        assert (search_recursive(root, k) is not None) == expected

    print("All tests passed!")
