"""
Problem: BST Iterator

Difficulty: Medium (LeetCode #173)

---------------------------------------------------
Problem:

Design an iterator over a BST that supports:

    next()    -> returns the NEXT smallest value          (advance in-order)
    has_next() -> true iff there are more values

Constraints:
    next() and has_next() must be O(1) AMORTIZED.
    Space: O(h), not O(n) — you can't just pre-compute the whole traversal.

---------------------------------------------------
The Idea:

An in-order traversal can be PAUSED at any point using the iterative
stack-based formulation. At each state, the stack contains:
`[root-to-current-leftmost]`. The next value is `stack.top().val`;
after popping and emitting it, push the stack path of its right
subtree's leftmost.

---------------------------------------------------
Why It's O(1) Amortized:

Each node is pushed exactly once and popped exactly once during the
iterator's lifetime, so total work across N next() calls is O(N).
Individual calls may do O(h) work, but averaged over all calls, each
is O(1).

This is a textbook AMORTIZATION argument — same reasoning as dynamic
array push.

---------------------------------------------------
Variants:

    - Reverse iterator: same idea, mirrored (stack path goes RIGHT).
    - Bidirectional: more complex; you need to maintain both a "done"
      set and direction state. Usually easier to precompute in-order
      into an array for bi-directional use.

---------------------------------------------------
Complexity:

    Construction: O(h).
    next() / has_next(): O(1) amortized, O(h) worst case.
    Space: O(h).
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "01-Binary-Tree"))
from implementation import TreeNode, tree_from_list


class BSTIterator:
    """In-order iterator over a BST. O(1) amortized next / has_next."""

    def __init__(self, root):
        self._stack = []
        self._push_left_path(root)

    def _push_left_path(self, node):
        """Push the left-spine starting from `node` onto the stack."""
        while node is not None:
            self._stack.append(node)
            node = node.left

    def has_next(self):
        """True iff there's another value. O(1)."""
        return bool(self._stack)

    def next(self):
        """Return the next in-order value. O(1) amortized."""
        if not self._stack:
            raise StopIteration
        node = self._stack.pop()
        # After yielding this node, the next in-order is the leftmost of its right subtree.
        self._push_left_path(node.right)
        return node.val


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #173 example: [7,3,15,null,null,9,20]
    # In-order: [3, 7, 9, 15, 20]
    tree = tree_from_list([7, 3, 15, None, None, 9, 20])
    it = BSTIterator(tree)
    assert it.next() == 3
    assert it.next() == 7
    assert it.has_next() is True
    assert it.next() == 9
    assert it.has_next() is True
    assert it.next() == 15
    assert it.has_next() is True
    assert it.next() == 20
    assert it.has_next() is False

    # next() past end → StopIteration
    try:
        it.next()
    except StopIteration:
        pass
    else:
        raise AssertionError("expected StopIteration")

    # Empty tree
    it = BSTIterator(None)
    assert not it.has_next()

    # Single node
    it = BSTIterator(tree_from_list([42]))
    assert it.has_next()
    assert it.next() == 42
    assert not it.has_next()

    # Stress: iterator output must match sorted inserted keys
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

    for _ in range(100):
        keys = random.sample(range(1000), random.randint(0, 100))
        root = None
        for k in keys:
            root = insert(root, k)

        it = BSTIterator(root)
        got = []
        while it.has_next():
            got.append(it.next())
        assert got == sorted(keys)

    # Stack-depth check: for a balanced BST of n nodes, stack should
    # never exceed ceil(log2(n+1)) at any point during iteration.
    import math
    balanced_keys = list(range(1, 32))             # 31 keys
    # Build a balanced tree manually for a clean bound
    def build_balanced(lo, hi):
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        return TreeNode(balanced_keys[mid],
                        left=build_balanced(lo, mid - 1),
                        right=build_balanced(mid + 1, hi))
    root = build_balanced(0, len(balanced_keys) - 1)
    it = BSTIterator(root)
    max_stack = len(it._stack)
    while it.has_next():
        it.next()
        max_stack = max(max_stack, len(it._stack))
    assert max_stack <= math.ceil(math.log2(len(balanced_keys) + 1)) + 1

    print(f"All tests passed! Balanced 31-node tree max stack depth: {max_stack}")
