r"""
BST Delete

LeetCode #450 — Delete Node in a BST

---------------------------------------------------
Why Delete Is The Tricky BST Operation:

Search and insert follow a single path. Delete has to handle THREE
different structural cases, plus a subtle pitfall: after replacing a
node's value with its successor, you must also REMOVE the original
successor, which can itself have a right subtree.

---------------------------------------------------
The Three Cases:

Case 1 — target has NO CHILDREN (leaf):
    Just delete it — its parent's pointer becomes None.

         5                     5
        / \        remove 3   / \
       3   8     ─────────▶  _   8
                              (3 gone)


Case 2 — target has ONE CHILD:
    Replace target with its only child.

         5                     5
        / \        remove 3   / \
       3   8     ─────────▶  2   8
       /
      2


Case 3 — target has TWO CHILDREN:
    Replace target's VALUE with its in-order SUCCESSOR's value
    (smallest in right subtree), then delete the successor from
    the right subtree. The successor is guaranteed to have NO LEFT
    child (it IS the leftmost in its subtree), so deleting it falls
    back into Case 1 or Case 2 — only one level of recursion.

         5                     6
        / \        remove 5   / \
       3   8     ─────────▶  3   8
          / \                   /
         6   9                 7   (successor 6 replaced; 6's right child promoted)
          \
           7

(You can also use the PREDECESSOR convention — largest in left subtree.
Both are correct. We use successor, which is the convention in most
textbooks.)

---------------------------------------------------
Complexity:

    Time:  O(h).
    Space: O(h) recursive stack.
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "01-Binary-Tree"))
from implementation import TreeNode, tree_from_list


def _leftmost(node):
    while node.left is not None:
        node = node.left
    return node


def delete(root, key):
    """
    Delete `key` from the BST rooted at `root`. Return the (possibly new) root.
    If `key` is absent, the tree is returned unchanged.

    Time:  O(h), Space: O(h).
    """
    if root is None:
        return None

    if key < root.val:
        root.left = delete(root.left, key)
    elif key > root.val:
        root.right = delete(root.right, key)
    else:
        # Found — handle the three cases.
        if root.left is None:
            return root.right                      # case 1 or 2 (no left child)
        if root.right is None:
            return root.left                       # case 2 (no right child)
        # Case 3 — two children.
        succ = _leftmost(root.right)
        root.val = succ.val
        root.right = delete(root.right, succ.val)
    return root


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Helper
    def inorder(node):
        if node is None:
            return []
        return inorder(node.left) + [node.val] + inorder(node.right)

    def is_bst(node, lo=float("-inf"), hi=float("inf")):
        if node is None:
            return True
        if not (lo < node.val < hi):
            return False
        return is_bst(node.left, lo, node.val) and is_bst(node.right, node.val, hi)

    # LC #450 example: [5,3,6,2,4,null,7], delete 3 → valid BSTs include
    # [5,4,6,2,null,null,7] or [5,2,6,null,4,null,7].
    root = tree_from_list([5, 3, 6, 2, 4, None, 7])
    root = delete(root, 3)
    assert is_bst(root)
    assert inorder(root) == [2, 4, 5, 6, 7]

    # Delete a leaf
    root = tree_from_list([5, 3, 6, 2, 4, None, 7])
    root = delete(root, 2)
    assert inorder(root) == [3, 4, 5, 6, 7]
    assert is_bst(root)

    # Delete a one-child node
    root = tree_from_list([5, 3, 6, 2, None, None, 7])
    root = delete(root, 3)
    assert inorder(root) == [2, 5, 6, 7]
    assert is_bst(root)

    # Delete root (two children)
    root = tree_from_list([5, 3, 6, 2, 4, None, 7])
    root = delete(root, 5)
    assert inorder(root) == [2, 3, 4, 6, 7]
    assert is_bst(root)

    # Delete root (one child)
    root = tree_from_list([5, 3])
    root = delete(root, 5)
    assert root.val == 3
    assert root.left is None and root.right is None

    # Delete root (leaf)
    root = tree_from_list([5])
    root = delete(root, 5)
    assert root is None

    # Key not present → unchanged tree
    root = tree_from_list([5, 3, 6])
    root = delete(root, 42)
    assert inorder(root) == [3, 5, 6]

    # Empty tree
    assert delete(None, 1) is None

    # Stress: delete in random order matches set behaviour
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

    for trial in range(50):
        keys = random.sample(range(500), 100)
        root = None
        truth = set()
        for k in keys:
            root = insert(root, k)
            truth.add(k)

        # Delete in random order, checking BST invariant + inorder match after each
        random.shuffle(keys)
        for k in keys:
            root = delete(root, k)
            truth.discard(k)
            assert is_bst(root), f"BST broken after deleting {k}"
            assert inorder(root) == sorted(truth)

        assert root is None

    print("All tests passed!")
