r"""
Problem: Lowest Common Ancestor of a Binary Tree

Difficulty: Medium (LeetCode #236)

---------------------------------------------------
Problem Statement:

Given the root of a binary tree and two nodes `p` and `q` that are
both guaranteed to exist in the tree, return their LOWEST COMMON
ANCESTOR — the deepest node that has both `p` and `q` as descendants.
A node is considered a descendant of itself.

Example:
        3
       / \
      5   1
     / \ / \
    6  2 0  8
       / \
      7   4

    lca(5, 1) = 3
    lca(5, 4) = 5       (a node is its own descendant)

---------------------------------------------------
The Classic Recursion:

Call LCA on left and right subtrees:

    lca(node) returns:
        None                — if neither p nor q is in this subtree
        the found node       — if exactly one of p, q is in this subtree
        the LCA itself       — if both are

The combining logic is beautiful: at any node, look at
`left = lca(node.left)` and `right = lca(node.right)`:

    if left and right       → p and q are SPLIT between subtrees → THIS node is the LCA
    if left only            → both are in left, so left already has the answer
    if right only           → both are in right
    if neither              → not in this subtree, return None
    if node itself is p or q → return node  (p/q might be its own descendant)

Remarkably, this handles the "descendant of itself" case for free:
when we hit p or q, we return it without checking children; any
ancestor with this result AND a non-None other-side result becomes
the LCA.

---------------------------------------------------
Complexity:

    Time:  O(n)
    Space: O(h) recursion

---------------------------------------------------
Variant Not Covered Here: LCA of a BST (LC #235) — there you can use
the BST invariant to walk down in O(h) without recursing into both
subtrees. See ../../02-BST/problems/ in a later session.
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from implementation import TreeNode, tree_from_list


def lowest_common_ancestor(root, p, q):
    """
    Return the LCA of nodes p and q (both guaranteed present in tree).

    Time:  O(n), Space: O(h).
    """
    if root is None or root is p or root is q:
        return root

    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)

    if left and right:
        return root                                # split across this node
    return left if left is not None else right


# =========================================================================
# Helpers for testing: find node by value in a tree
# =========================================================================

def find_node(root, val):
    if root is None:
        return None
    if root.val == val:
        return root
    return find_node(root.left, val) or find_node(root.right, val)


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #236 example tree
    vals = [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4]
    tree = tree_from_list(vals)

    cases = [
        (5, 1, 3),
        (5, 4, 5),                                 # node is its own descendant
        (6, 4, 5),
        (7, 4, 2),
        (6, 7, 5),
        (0, 8, 1),
        (3, 3, 3),                                 # p == q == root
        (3, 4, 3),
    ]
    for p_val, q_val, expected_val in cases:
        p = find_node(tree, p_val)
        q = find_node(tree, q_val)
        lca = lowest_common_ancestor(tree, p, q)
        assert lca.val == expected_val, (
            f"lca({p_val}, {q_val}) = {lca.val}, expected {expected_val}"
        )

    # Edge: small tree
    simple = tree_from_list([1, 2])
    p = find_node(simple, 1)
    q = find_node(simple, 2)
    assert lowest_common_ancestor(simple, p, q).val == 1

    # Randomized cross-check using ancestor-set brute force
    def ancestors(root, target, path=None):
        """Return list of nodes from root down to target (inclusive), or None if not found."""
        if root is None:
            return None
        if path is None:
            path = []
        path = path + [root]
        if root is target:
            return path
        return (ancestors(root.left, target, path) or
                ancestors(root.right, target, path))

    def brute_lca(root, p, q):
        path_p = ancestors(root, p)
        path_q = ancestors(root, q)
        # Walk both paths from root, last shared node is the LCA
        lca = root
        for a, b in zip(path_p, path_q):
            if a is b:
                lca = a
            else:
                break
        return lca

    import random
    random.seed(42)
    for _ in range(200):
        n = random.randint(2, 40)
        vals = list(range(n))
        random.shuffle(vals)
        # Build random tree
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
        # Pick two random nodes (by walking to random positions)
        all_nodes = []
        def collect(node):
            if node is None: return
            all_nodes.append(node)
            collect(node.left)
            collect(node.right)
        collect(tree)
        p = random.choice(all_nodes)
        q = random.choice(all_nodes)
        expected = brute_lca(tree, p, q)
        got = lowest_common_ancestor(tree, p, q)
        assert got is expected, f"disagreement on p={p.val}, q={q.val}"

    print("All tests passed!")
