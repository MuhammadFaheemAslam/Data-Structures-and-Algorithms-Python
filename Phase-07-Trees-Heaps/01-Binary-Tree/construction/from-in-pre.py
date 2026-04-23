"""
Construct Binary Tree From Preorder + Inorder Traversals

LeetCode #105

---------------------------------------------------
The Theorem:

Given the preorder and inorder traversals of a binary tree with
DISTINCT values, the tree is UNIQUELY determined.

Why:
    - The FIRST element of PREORDER is always the root.
    - That element's position in INORDER splits inorder into:
          left subtree's inorder | [root] | right subtree's inorder
    - The sizes of those halves tell us how to split PREORDER:
          [root] | left subtree's preorder | right subtree's preorder

Recurse on the halves. Base case: empty range → None.

---------------------------------------------------
Naïve implementation:

    def build(preorder, inorder):
        if not preorder: return None
        root_val = preorder[0]
        mid = inorder.index(root_val)           # O(n) per call
        root = TreeNode(root_val)
        root.left  = build(preorder[1:1+mid],  inorder[:mid])
        root.right = build(preorder[1+mid:],   inorder[mid+1:])
        return root

This is O(n²) because of inorder.index and slicing. The fast version
below is O(n):

    - Build inorder_idx: value → index in inorder (hash map)       O(n)
    - Use a preorder POINTER instead of slicing                     O(1) per step
    - Pass index RANGES instead of copies                           O(1) per call

---------------------------------------------------
Complexity:

    Time:  O(n).
    Space: O(n) for the map + O(h) recursion.
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from implementation import TreeNode, tree_from_list, trees_equal, tree_to_list


def build_tree(preorder, inorder):
    """
    Construct the tree from preorder + inorder (distinct values).

    Time:  O(n), Space: O(n).
    """
    inorder_idx = {val: i for i, val in enumerate(inorder)}
    pre_ptr = [0]                                  # mutable pointer into preorder

    def build(in_lo, in_hi):
        """Construct subtree from inorder[in_lo:in_hi]."""
        if in_lo >= in_hi:
            return None
        root_val = preorder[pre_ptr[0]]
        pre_ptr[0] += 1
        root = TreeNode(root_val)
        mid = inorder_idx[root_val]
        # IMPORTANT: build LEFT first — preorder consumes the left
        # subtree before the right.
        root.left = build(in_lo, mid)
        root.right = build(mid + 1, in_hi)
        return root

    return build(0, len(inorder))


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #105 example: preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
    #   Tree: [3, 9, 20, None, None, 15, 7]
    got = build_tree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])
    assert tree_to_list(got) == [3, 9, 20, None, None, 15, 7]

    # Single node
    assert tree_to_list(build_tree([1], [1])) == [1]
    assert build_tree([], []) is None

    # Left-skewed: pre=[1,2,3,4], in=[4,3,2,1]
    got = build_tree([1, 2, 3, 4], [4, 3, 2, 1])
    assert tree_to_list(got) == [1, 2, None, 3, None, 4]

    # Right-skewed: pre=[1,2,3,4], in=[1,2,3,4]
    got = build_tree([1, 2, 3, 4], [1, 2, 3, 4])
    assert tree_to_list(got) == [1, None, 2, None, 3, None, 4]

    # Round-trip: for random trees, build(preorder, inorder) should reproduce them
    from traversals.inorder.recursive import inorder_recursive
    from traversals.preorder.recursive import preorder_recursive
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "traversals", "inorder"))
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "traversals", "preorder"))

    import random
    random.seed(42)
    for _ in range(100):
        # Generate a tree with distinct values
        n = random.randint(1, 30)
        vals = random.sample(range(1000), n)
        # Build a random tree using the values
        def build_random(vals):
            if not vals:
                return None
            root = TreeNode(vals[0])
            rest = vals[1:]
            split = random.randint(0, len(rest))
            root.left = build_random(rest[:split])
            root.right = build_random(rest[split:])
            return root
        tree = build_random(vals)

        pre = preorder_recursive(tree)
        ino = inorder_recursive(tree)
        rebuilt = build_tree(pre, ino)
        assert trees_equal(tree, rebuilt), f"round-trip failed for pre={pre}, in={ino}"

    print("All tests passed!")
