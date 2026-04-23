"""
Construct Binary Tree From Inorder + Postorder Traversals

LeetCode #106

---------------------------------------------------
The Mirror Of LC #105:

Preorder's first element is the root; postorder's LAST element is
the root. Everything else is symmetric:

    postorder = [..., left-sub-post, ..., right-sub-post, ROOT]

So we walk postorder BACKWARDS, taking roots off the end. Because we
consume the RIGHT subtree first (from the back), we must RECURSE
RIGHT BEFORE LEFT.

---------------------------------------------------
Why preorder-alone or postorder-alone isn't enough:

With just preorder (or just postorder), you CAN'T tell where the left
subtree ends and the right begins. Two different trees can share the
same preorder:

    [1, 2]    could be        1         or        1
                             /                     \
                            2                      2

Inorder gives the splitting info. (Preorder + postorder uniquely
determines the tree ONLY if every node has 0 or 2 children — i.e.
a "full" binary tree — because then the second-to-root preorder
element is always the root of the left subtree.)

---------------------------------------------------
Complexity:

    Time:  O(n).
    Space: O(n) map + O(h) recursion.
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from implementation import TreeNode, tree_from_list, tree_to_list, trees_equal


def build_tree(inorder, postorder):
    """
    Construct the tree from inorder + postorder (distinct values).

    Time:  O(n), Space: O(n).
    """
    inorder_idx = {val: i for i, val in enumerate(inorder)}
    post_ptr = [len(postorder) - 1]                # read postorder from the back

    def build(in_lo, in_hi):
        if in_lo >= in_hi:
            return None
        root_val = postorder[post_ptr[0]]
        post_ptr[0] -= 1
        root = TreeNode(root_val)
        mid = inorder_idx[root_val]
        # Postorder consumes RIGHT subtree before LEFT when read backwards
        root.right = build(mid + 1, in_hi)
        root.left = build(in_lo, mid)
        return root

    return build(0, len(inorder))


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #106 example: inorder = [9,3,15,20,7], postorder = [9,15,7,20,3]
    got = build_tree([9, 3, 15, 20, 7], [9, 15, 7, 20, 3])
    assert tree_to_list(got) == [3, 9, 20, None, None, 15, 7]

    # Single node
    assert tree_to_list(build_tree([1], [1])) == [1]
    assert build_tree([], []) is None

    # Left-skewed
    #   inorder=[4,3,2,1], postorder=[4,3,2,1]
    got = build_tree([4, 3, 2, 1], [4, 3, 2, 1])
    assert tree_to_list(got) == [1, 2, None, 3, None, 4]

    # Right-skewed
    #   inorder=[1,2,3,4], postorder=[4,3,2,1]
    got = build_tree([1, 2, 3, 4], [4, 3, 2, 1])
    assert tree_to_list(got) == [1, None, 2, None, 3, None, 4]

    # Round-trip
    from traversals.inorder.recursive import inorder_recursive
    from traversals.postorder.recursive import postorder_recursive

    import random
    random.seed(42)
    for _ in range(100):
        n = random.randint(1, 30)
        vals = random.sample(range(1000), n)

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
        ino = inorder_recursive(tree)
        post = postorder_recursive(tree)
        rebuilt = build_tree(ino, post)
        assert trees_equal(tree, rebuilt), (
            f"round-trip failed: in={ino}, post={post}"
        )

    print("All tests passed!")
