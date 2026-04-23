"""
Problem: Kth Smallest Element in a BST

Difficulty: Medium (LeetCode #230)

---------------------------------------------------
Problem:

Given the root of a BST and integer `k` (1-indexed), return the k-th
smallest value.

---------------------------------------------------
The Core Observation:

In-order traversal of a BST yields values in SORTED order. So the
k-th smallest is simply the k-th value produced by an in-order walk.

    in-order → [1, 3, 4, 6, 7, 8, 10, 13, 14]
                         ^
                      k=4 gives 6

---------------------------------------------------
Two implementations:

    A) Recursive with early exit (once we've emitted k values, stop).
    B) Iterative in-order using an explicit stack — cleanest form of
       "stop after k" because we advance the traversal one step at a
       time.

---------------------------------------------------
Follow-up — Dynamic Case:

If the BST is INSERTED INTO and DELETED FROM between kthSmallest queries,
re-walking the whole tree each time is O(n). Maintain a SUBTREE SIZE in
each node instead — then kthSmallest becomes O(h):

    kthSmallest(node, k):
        left_size = size(node.left)
        if k == left_size + 1: return node.val
        if k <= left_size:     return kthSmallest(node.left, k)
        return kthSmallest(node.right, k - left_size - 1)

The size must be maintained on every insert/delete (O(h) extra work).
This is a classic ORDER-STATISTICS TREE — covered in Phase 11.

---------------------------------------------------
Complexity:

    Time:  O(h + k) — walk down to smallest + k steps.
    Space: O(h).
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "01-Binary-Tree"))
from implementation import TreeNode, tree_from_list


# -------- Iterative in-order with early exit --------

def kth_smallest(root, k):
    """
    Return the k-th smallest value (1-indexed).

    Time:  O(h + k), Space: O(h).
    """
    stack = []
    node = root
    count = 0

    while node is not None or stack:
        while node is not None:
            stack.append(node)
            node = node.left
        node = stack.pop()
        count += 1
        if count == k:
            return node.val
        node = node.right

    raise IndexError(f"k={k} exceeds tree size")


# -------- Recursive variant (for comparison) --------

def kth_smallest_recursive(root, k):
    """
    Walk in-order; short-circuit when we've emitted k values.

    Time:  O(h + k) best case, O(n) if the short-circuit doesn't fire.
    Space: O(h).
    """
    remaining = [k]
    answer = [None]

    def walk(node):
        if node is None or answer[0] is not None:
            return
        walk(node.left)
        if answer[0] is not None:
            return
        remaining[0] -= 1
        if remaining[0] == 0:
            answer[0] = node.val
            return
        walk(node.right)

    walk(root)
    if answer[0] is None:
        raise IndexError(f"k={k} exceeds tree size")
    return answer[0]


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #230 examples
    assert kth_smallest(tree_from_list([3, 1, 4, None, 2]), 1) == 1
    assert kth_smallest(tree_from_list([5, 3, 6, 2, 4, None, None, 1]), 3) == 3

    # Single node
    assert kth_smallest(tree_from_list([42]), 1) == 42

    # All values for a full BST
    bst = tree_from_list([8, 3, 10, 1, 6, None, 14, None, None, 4, 7, 13])
    sorted_vals = [1, 3, 4, 6, 7, 8, 10, 13, 14]
    for k, expected in enumerate(sorted_vals, 1):
        assert kth_smallest(bst, k) == expected
        assert kth_smallest_recursive(bst, k) == expected

    # k out of range
    try:
        kth_smallest(bst, 100)
    except IndexError:
        pass
    else:
        raise AssertionError("expected IndexError")

    # Stress: insert random distinct keys, check kth matches sorted list
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

    for _ in range(50):
        keys = random.sample(range(1000), 50)
        root = None
        for key in keys:
            root = insert(root, key)
        truth = sorted(keys)
        for k in range(1, len(truth) + 1):
            assert kth_smallest(root, k) == truth[k - 1]
            assert kth_smallest_recursive(root, k) == truth[k - 1]

    print("All tests passed!")
