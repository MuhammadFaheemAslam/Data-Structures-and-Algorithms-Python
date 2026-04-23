"""
Inorder Traversal — Iterative (explicit stack)

Same result as the recursive version, but using our OWN stack instead
of the call stack. This is the canonical LC #94 "iterative" answer
and is worth memorizing because:

    - You can pause and resume mid-traversal. (This is how BSTIterator
      in LC #173 is implemented — see ../02-BST/problems/bst-iterator.py.)
    - You avoid Python's recursion limit (~1000 by default).

---------------------------------------------------
The Algorithm:

    Keep pushing LEFT children onto a stack until None.
    Pop. Visit the popped node. Move to its RIGHT child.
    Repeat.

Each node is pushed exactly once and popped exactly once → O(n) total.
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from implementation import TreeNode, tree_from_list


def inorder_iterative(root):
    """
    Iterative inorder using an explicit stack.

    Time:  O(n).
    Space: O(h).
    """
    result = []
    stack = []
    node = root

    while node is not None or stack:
        # Phase 1 — dive left, pushing everything we pass.
        while node is not None:
            stack.append(node)
            node = node.left

        # Phase 2 — pop, visit, then step to right subtree.
        node = stack.pop()
        result.append(node.val)
        node = node.right

    return result


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    from recursive import inorder_recursive

    cases = [
        [],
        [1],
        [1, 2, 3],
        [1, None, 2, 3],
        [4, 2, 6, 1, 3, 5, 7],                                 # balanced BST
        [5, 4, None, 3, None, 2, None, 1],                     # left chain
        [1, None, 2, None, 3, None, 4],                        # right chain
    ]
    for c in cases:
        tree = tree_from_list(c)
        assert inorder_iterative(tree) == inorder_recursive(tree), f"mismatch on {c}"

    # Stress random
    import random
    random.seed(42)
    for _ in range(200):
        n = random.randint(0, 50)
        vals = [random.randint(0, 100) if random.random() < 0.85 else None for _ in range(n)]
        # ensure first val isn't None (tree_from_list requires a root)
        if vals and vals[0] is None:
            vals[0] = 0
        tree = tree_from_list(vals)
        assert inorder_iterative(tree) == inorder_recursive(tree)

    print("All tests passed!")
