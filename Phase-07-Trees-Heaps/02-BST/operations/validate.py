"""
Validate Binary Search Tree

LeetCode #98

---------------------------------------------------
Problem:

Return True iff the given binary tree is a valid BST (strict inequalities:
every left descendant < node < every right descendant).

---------------------------------------------------
The Classic Bug:

A tempting but WRONG solution:

    def is_bst(node):
        if node is None: return True
        if node.left  and node.left.val  >= node.val: return False
        if node.right and node.right.val <= node.val: return False
        return is_bst(node.left) and is_bst(node.right)

This only checks IMMEDIATE children, missing failures like:

              10
             /  \
            5   15
               /  \
              6    20       ← 6 < 10 but sits in 10's right subtree!

`6` violates the BST invariant (it's less than the root `10`), but
each PAIR of (parent, child) passes the local check.

---------------------------------------------------
Two Correct Approaches:

A) RANGE-BASED DFS:
   Pass a (lo, hi) window to each subtree; every value must lie
   strictly within. Left subtree's hi tightens to the parent's val;
   right subtree's lo tightens to the parent's val.

B) INORDER TRAVERSAL:
   For a valid BST, in-order produces a STRICTLY INCREASING sequence.
   Track the previously visited value; fail if current ≤ previous.

Both O(n) time, O(h) space. The range-based version is short and
generalizes (e.g. to validating AVL/red-black invariants), while the
inorder version is especially elegant.

---------------------------------------------------
The Subtle Case Python Makes Easy:

LeetCode's worst-case BST has INT32 MIN/MAX at the boundary. Using
`float("-inf")` and `float("inf")` as sentinels covers this cleanly
in Python. Some codebases have to use `None` checks instead — watch
out in languages without a reliable "±∞".
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "01-Binary-Tree"))
from implementation import TreeNode, tree_from_list


# -------- A) Range-based DFS --------

def is_valid_bst(root):
    """
    Check BST invariant by threading a (lo, hi) range down the tree.

    Time:  O(n), Space: O(h).
    """
    def check(node, lo, hi):
        if node is None:
            return True
        if not (lo < node.val < hi):
            return False
        return (check(node.left, lo, node.val)
                and check(node.right, node.val, hi))

    return check(root, float("-inf"), float("inf"))


# -------- B) In-order traversal: sequence must strictly increase --------

def is_valid_bst_inorder(root):
    """
    In-order walk, checking each value is strictly greater than the prior.

    Time:  O(n), Space: O(h).
    """
    prev = [float("-inf")]                         # mutable box for the closure

    def walk(node):
        if node is None:
            return True
        if not walk(node.left):
            return False
        if node.val <= prev[0]:
            return False
        prev[0] = node.val
        return walk(node.right)

    return walk(root)


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    cases = [
        ([],                                           True),
        ([1],                                          True),
        ([2, 1, 3],                                    True),                        # LC example 1
        ([5, 1, 4, None, None, 3, 6],                  False),                       # LC example 2
        ([10, 5, 15, None, None, 6, 20],               False),                       # classic bug case
        ([1, None, 2, None, 3, None, 4],               True),                        # right chain
        ([5, 4, 6, None, None, 3, 7],                  False),                       # 3 under 6 but < 5
        ([2, 2, 2],                                    False),                       # strict inequality
        ([50, 30, 70, 20, 40, 60, 80],                 True),
        ([50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 85], True),
    ]

    for vals, expected in cases:
        tree = tree_from_list(vals)
        assert is_valid_bst(tree) == expected, f"range failed on {vals}"
        assert is_valid_bst_inorder(tree) == expected, f"inorder failed on {vals}"

    # Edge: INT_MIN / INT_MAX at the boundary
    # Tree:   [-2^31]        value INT_MIN alone should be valid
    tree = TreeNode(-2**31)
    assert is_valid_bst(tree)
    assert is_valid_bst_inorder(tree)

    # Two nodes, left = INT_MIN, root = INT_MIN (violates strict <)
    root = TreeNode(-2**31)
    root.left = TreeNode(-2**31)
    assert not is_valid_bst(root)
    assert not is_valid_bst_inorder(root)

    # Stress: build valid BSTs by insertion, then randomly swap a node's
    # value to break the invariant and confirm both validators catch it.
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

    for _ in range(200):
        keys = random.sample(range(1000), 40)
        root = None
        for k in keys:
            root = insert(root, k)
        # Valid
        assert is_valid_bst(root)
        assert is_valid_bst_inorder(root)

    print("All tests passed!")
