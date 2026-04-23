"""
Inorder Traversal — Morris (O(1) space)

Morris traversal does inorder in O(n) time using ZERO extra space
beyond the tree itself. No recursion, no explicit stack.

The trick: TEMPORARILY use empty `right` pointers of left-subtree
predecessors to thread back to the current node. After visiting,
we undo the threading. The tree is structurally unchanged when the
traversal finishes.

---------------------------------------------------
The Algorithm:

For the current node `cur`:

    1. If cur.left is None:
         visit cur; move cur = cur.right.

    2. Else, find the INORDER PREDECESSOR `pred` of cur
       (= the rightmost node of cur.left):

        a. If pred.right is None:
             set pred.right = cur        (create thread)
             move cur = cur.left.        (descend)

        b. Else (pred.right == cur — we're back via the thread):
             set pred.right = None       (undo thread)
             visit cur.
             move cur = cur.right.       (ascend to inorder-next)

Each edge is traversed at most 3 times (down, up via thread, undo),
so total work is O(n). Space: O(1).

---------------------------------------------------
When You'd Actually Use This:

Rarely, in Python — stack frames are cheap. Common in embedded / systems
contexts where stack depth or heap allocation is constrained. It's also
a favourite interview curiosity.

The PRINCIPLE generalizes, though: threaded trees (Knuth, TAOCP vol.3)
store inorder successor/predecessor pointers persistently, giving O(1)
inorder iteration. Morris is the "temporary threading" variant.
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from implementation import TreeNode, tree_from_list, trees_equal
import copy


def inorder_morris(root):
    """
    Inorder traversal in O(1) extra space using tree threading.

    Time:  O(n) — each node is touched O(1) times amortized.
    Space: O(1).
    """
    result = []
    cur = root

    while cur is not None:
        if cur.left is None:
            # No left subtree — visit and move right
            result.append(cur.val)
            cur = cur.right
            continue

        # Find inorder predecessor: rightmost node in left subtree.
        # Stop if we reach a thread that points back to cur.
        pred = cur.left
        while pred.right is not None and pred.right is not cur:
            pred = pred.right

        if pred.right is None:
            # Thread NOT yet set → set it, descend left
            pred.right = cur
            cur = cur.left
        else:
            # Thread is set (pred.right == cur) → we've finished the left
            # subtree. Undo thread, visit, step right.
            pred.right = None
            result.append(cur.val)
            cur = cur.right

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
        [4, 2, 6, 1, 3, 5, 7],
        [5, 4, None, 3, None, 2, None, 1],
        [1, None, 2, None, 3, None, 4],
    ]
    for c in cases:
        tree = tree_from_list(c)
        original_shape = copy.deepcopy(tree)
        got = inorder_morris(tree)
        expected = inorder_recursive(tree)
        assert got == expected, f"wrong result on {c}: got {got}, expected {expected}"
        # Morris should leave the tree structurally unchanged
        assert trees_equal(tree, original_shape), f"tree mutated after morris on {c}"

    # Stress random
    import random
    random.seed(42)
    for _ in range(200):
        n = random.randint(0, 50)
        vals = [random.randint(0, 100) if random.random() < 0.85 else None for _ in range(n)]
        if vals and vals[0] is None:
            vals[0] = 0
        tree = tree_from_list(vals)
        original = copy.deepcopy(tree)
        assert inorder_morris(tree) == inorder_recursive(tree)
        assert trees_equal(tree, original), "morris left tree modified"

    print("All tests passed!")
