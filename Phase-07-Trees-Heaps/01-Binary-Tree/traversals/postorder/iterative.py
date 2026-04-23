"""
Postorder Traversal — Iterative

Postorder is the TRICKIEST traversal to iterativize because the node
must be visited AFTER both its children — but when we pop the node
from a stack, we can't yet know whether we've "finished" its children
without extra tracking.

Two common techniques:

    A) Reverse-of-modified-preorder: process in ROOT, RIGHT, LEFT order
       (a preorder variant), then REVERSE the output. Elegant & short.

    B) Explicit "visited" marker on the stack: push a sentinel so we
       know when we're coming back up. O(n) but heavier.

We implement both. (A) is shorter and idiomatic; (B) is what you'd
use if you need to process nodes one-at-a-time without buffering
the whole output.
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from implementation import TreeNode, tree_from_list


# -------- Approach A: reverse of "modified preorder" (root, right, left) --------

def postorder_iterative(root):
    """
    Visit in root → right → left using a stack (a preorder variant),
    then reverse the output to get left → right → root.

    Time:  O(n).
    Space: O(h).
    """
    if root is None:
        return []

    result = []
    stack = [root]
    while stack:
        node = stack.pop()
        result.append(node.val)                    # root first
        # push LEFT before RIGHT so right is popped/visited first
        if node.left is not None:
            stack.append(node.left)
        if node.right is not None:
            stack.append(node.right)

    return list(reversed(result))


# -------- Approach B: "visited" marker on the stack --------

_VISITED = object()


def postorder_iterative_marker(root):
    """
    Push (VISITED, node) the second time we encounter a node; then
    when we pop a VISITED marker, we know its children are already done.

    Time:  O(n).
    Space: O(h).
    """
    if root is None:
        return []

    result = []
    stack = [root]
    while stack:
        top = stack.pop()
        if isinstance(top, tuple) and top[0] is _VISITED:
            result.append(top[1].val)
            continue

        node = top
        # Push in order: (VISITED marker), right, left so that
        # left is popped & processed first.
        stack.append((_VISITED, node))
        if node.right is not None:
            stack.append(node.right)
        if node.left is not None:
            stack.append(node.left)

    return result


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    from recursive import postorder_recursive

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
        expected = postorder_recursive(tree)
        assert postorder_iterative(tree) == expected, f"reverse-preorder mismatch on {c}"
        assert postorder_iterative_marker(tree) == expected, f"marker mismatch on {c}"

    # Stress random
    import random
    random.seed(42)
    for _ in range(200):
        n = random.randint(0, 50)
        vals = [random.randint(0, 100) if random.random() < 0.85 else None for _ in range(n)]
        if vals and vals[0] is None:
            vals[0] = 0
        tree = tree_from_list(vals)
        expected = postorder_recursive(tree)
        assert postorder_iterative(tree) == expected
        assert postorder_iterative_marker(tree) == expected

    print("All tests passed!")
