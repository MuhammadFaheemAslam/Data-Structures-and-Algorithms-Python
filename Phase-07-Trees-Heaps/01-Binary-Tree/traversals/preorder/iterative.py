"""
Preorder Traversal — Iterative

Pre-order is the EASIEST traversal to convert to iterative form: you
just emulate the call stack with an explicit stack, pushing RIGHT
before LEFT so that LEFT is popped first (LIFO).

---------------------------------------------------
The Algorithm:

    push root.
    while stack:
        pop and VISIT node.
        push node.right (if any), then node.left (if any).

Each node is pushed once and popped once → O(n) total.

There's also a O(1)-space Morris-style preorder (left as an exercise;
conceptually similar to morris.py in ../inorder/).
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from implementation import TreeNode, tree_from_list


def preorder_iterative(root):
    """
    Iterative preorder with an explicit stack.

    Time:  O(n).
    Space: O(h) — for the stack.
    """
    if root is None:
        return []

    result = []
    stack = [root]

    while stack:
        node = stack.pop()
        result.append(node.val)
        # Push right FIRST so left is processed next (LIFO)
        if node.right is not None:
            stack.append(node.right)
        if node.left is not None:
            stack.append(node.left)

    return result


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    from recursive import preorder_recursive

    cases = [
        [],
        [1],
        [1, 2, 3],
        [1, None, 2, 3],
        [4, 2, 6, 1, 3, 5, 7],
        [5, 4, None, 3, None, 2, None, 1],
        [1, None, 2, None, 3, None, 4],
    ]
    for c in cases:
        tree = tree_from_list(c)
        assert preorder_iterative(tree) == preorder_recursive(tree), f"mismatch on {c}"

    # Stress random
    import random
    random.seed(42)
    for _ in range(200):
        n = random.randint(0, 50)
        vals = [random.randint(0, 100) if random.random() < 0.85 else None for _ in range(n)]
        if vals and vals[0] is None:
            vals[0] = 0
        tree = tree_from_list(vals)
        assert preorder_iterative(tree) == preorder_recursive(tree)

    print("All tests passed!")
