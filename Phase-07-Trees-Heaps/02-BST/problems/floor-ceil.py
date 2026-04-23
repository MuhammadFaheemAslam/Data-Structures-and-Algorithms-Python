"""
Problem: Floor and Ceiling in a BST

Difficulty: Medium (classic interview; LeetCode variants #270, #272)

---------------------------------------------------
Definitions:

    floor(x)  = largest key in the BST that is  ≤ x,  or None if no such key exists.
    ceil(x)   = smallest key in the BST that is ≥ x, or None if no such key exists.

`x` does NOT need to be in the tree. Example (BST contains {2, 5, 7, 10}):

    floor(6) = 5        ceil(6) = 7
    floor(2) = 2        ceil(2) = 2                    (x itself is present)
    floor(1) = None     ceil(11) = None                (out of range)

---------------------------------------------------
The Algorithm (for floor — ceil is the mirror):

Walk down the tree, tracking the "best candidate" so far:

    if key == node.val:            return node.val        (exact match — can't improve)
    if key <  node.val:            go LEFT                (anything at node.val or higher is too big)
    if key >  node.val:            record node.val as best-so-far; go RIGHT

Why this works:
- If key is less than the current node, the node is too big, but its
  LEFT subtree might contain something ≤ key.
- If key is greater than the current node, the node IS a valid
  candidate; but the right subtree might have something bigger but
  still ≤ key, so try there.

Symmetric logic for ceil (swap the direction and the < / >).

---------------------------------------------------
Complexity:

    Time:  O(h) — single downward traversal.
    Space: O(1).

This is a "don't need recursion at all" kind of problem. If you
accidentally write an O(n) in-order version, you've missed the point
of using a BST.
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "01-Binary-Tree"))
from implementation import TreeNode, tree_from_list


def floor(root, key):
    """
    Return the largest value in the BST that is ≤ key, or None.

    Time:  O(h), Space: O(1).
    """
    best = None
    node = root
    while node is not None:
        if key == node.val:
            return node.val
        if key < node.val:
            node = node.left
        else:
            best = node.val                        # node is a valid floor candidate
            node = node.right
    return best


def ceil(root, key):
    """
    Return the smallest value in the BST that is ≥ key, or None.

    Time:  O(h), Space: O(1).
    """
    best = None
    node = root
    while node is not None:
        if key == node.val:
            return node.val
        if key > node.val:
            node = node.right
        else:
            best = node.val                        # node is a valid ceil candidate
            node = node.left
    return best


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # BST containing {2, 5, 7, 10, 15, 18, 22}
    root = tree_from_list([10, 5, 18, 2, 7, 15, 22])

    # Exact matches
    assert floor(root, 10) == 10
    assert ceil(root, 10) == 10
    assert floor(root, 2) == 2
    assert ceil(root, 2) == 2

    # Between-node queries
    assert floor(root, 6) == 5                     # 5 ≤ 6 < 7
    assert ceil(root, 6) == 7
    assert floor(root, 16) == 15
    assert ceil(root, 16) == 18
    assert floor(root, 100) == 22                  # largest in tree
    assert ceil(root, -5) == 2                     # smallest in tree

    # Out of range
    assert floor(root, 1) is None                  # nothing ≤ 1
    assert ceil(root, 100) is None                 # nothing ≥ 100

    # Empty tree
    assert floor(None, 5) is None
    assert ceil(None, 5) is None

    # Stress: compare against a sorted list
    import bisect
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

    def brute_floor(sorted_list, key):
        i = bisect.bisect_right(sorted_list, key) - 1
        return sorted_list[i] if i >= 0 else None

    def brute_ceil(sorted_list, key):
        i = bisect.bisect_left(sorted_list, key)
        return sorted_list[i] if i < len(sorted_list) else None

    for _ in range(50):
        keys = random.sample(range(-500, 500), 80)
        root = None
        for k in keys:
            root = insert(root, k)
        sorted_keys = sorted(keys)

        for _ in range(100):
            q = random.randint(-600, 600)
            assert floor(root, q) == brute_floor(sorted_keys, q), f"floor({q}) on {sorted_keys}"
            assert ceil(root, q) == brute_ceil(sorted_keys, q), f"ceil({q}) on {sorted_keys}"

    print("All tests passed!")
