"""
BST Insert

LeetCode #701 — Insert into a Binary Search Tree

---------------------------------------------------
The Algorithm:

Find where `key` WOULD be if we searched for it. That's the spot
to attach. Two cases:

    - Tree is empty              → new root.
    - Walk down following <, >   → when we'd step into a None child,
                                    attach here.

No rebalancing. No rotations. The shape of the tree depends purely
on the order of inserts. (This is exactly why AVL / red-black trees
add balancing — see module 03-AVL-Tree.)

---------------------------------------------------
Duplicate Handling (module-wide convention):

Inserting an existing key is a NO-OP. The tree returned is the same
tree that was passed in, including size.

---------------------------------------------------
Complexity:

    Time:  O(h).
    Space: O(1) iterative, O(h) recursive.
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "01-Binary-Tree"))
from implementation import TreeNode, tree_from_list


# -------- Iterative --------

def insert(root, key):
    """
    Insert `key` into the BST rooted at `root`. Return the (possibly new) root.

    Time:  O(h), Space: O(1).
    """
    new_node = TreeNode(key)
    if root is None:
        return new_node

    node = root
    while True:
        if key == node.val:
            return root                            # no-op on duplicate
        if key < node.val:
            if node.left is None:
                node.left = new_node
                return root
            node = node.left
        else:
            if node.right is None:
                node.right = new_node
                return root
            node = node.right


# -------- Recursive --------

def insert_recursive(root, key):
    """Recursive insert. Time O(h), Space O(h)."""
    if root is None:
        return TreeNode(key)
    if key < root.val:
        root.left = insert_recursive(root.left, key)
    elif key > root.val:
        root.right = insert_recursive(root.right, key)
    # equal → no-op
    return root


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Empty tree → single node
    root = insert(None, 5)
    assert root.val == 5
    assert root.left is None and root.right is None

    # Smaller key → left, larger key → right
    root = insert(root, 3)
    root = insert(root, 8)
    assert root.left.val == 3
    assert root.right.val == 8

    # Nested
    root = insert(root, 1)
    root = insert(root, 4)
    assert root.left.left.val == 1
    assert root.left.right.val == 4

    # Duplicate is a no-op
    before = (root.val, root.left.val, root.right.val,
              root.left.left.val, root.left.right.val)
    root = insert(root, 5)
    after = (root.val, root.left.val, root.right.val,
             root.left.left.val, root.left.right.val)
    assert before == after

    # Check BST invariant holds after arbitrary inserts
    def inorder(node):
        if node is None:
            return []
        return inorder(node.left) + [node.val] + inorder(node.right)

    # Both iterative and recursive must match
    import random
    random.seed(42)
    for _ in range(50):
        keys = [random.randint(0, 100) for _ in range(50)]
        a = None
        b = None
        for k in keys:
            a = insert(a, k)
            b = insert_recursive(b, k)
        seq = inorder(a)
        assert seq == sorted(set(keys))
        assert inorder(b) == seq

    # Worst case: strictly ascending → chain on the right
    root = None
    for i in range(10):
        root = insert(root, i)
    # Every node only has a right child
    n = root
    for i in range(10):
        assert n.val == i
        assert n.left is None
        n = n.right

    print("All tests passed!")
