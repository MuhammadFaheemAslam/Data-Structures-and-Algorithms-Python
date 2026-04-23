"""
implementation.py — Binary Search Tree

A full BST class with search, insert, delete, min, max, and inorder.
The individual operations are also broken out into `operations/` files
with more detail; here we focus on the container view: a class that
maintains the BST invariant as you add and remove keys.

Uses the same TreeNode from ../01-Binary-Tree/implementation.py so
LC-style `tree_from_list` tests work without changes.

---------------------------------------------------
Design Notes:

    - No duplicates: inserting an existing key is a no-op.
    - Values must be mutually comparable (numbers, strings, tuples, etc.).
    - Ops are O(h); unbalanced insertion sequences degrade to O(n).
    - Deletion uses the INORDER SUCCESSOR convention for the two-child case.
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "01-Binary-Tree"))
from implementation import TreeNode


class BST:
    """Binary search tree. Values must be comparable. No duplicates."""

    def __init__(self):
        self._root = None
        self._size = 0

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._root is None

    def root(self):
        """Expose the root TreeNode. Useful for traversals."""
        return self._root

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def contains(self, key):
        """O(h). True iff `key` is in the tree."""
        node = self._root
        while node is not None:
            if key == node.val:
                return True
            node = node.left if key < node.val else node.right
        return False

    def __contains__(self, key):
        return self.contains(key)

    # ------------------------------------------------------------------
    # Insert
    # ------------------------------------------------------------------

    def insert(self, key):
        """O(h). Insert `key`. No-op if already present."""
        if self._root is None:
            self._root = TreeNode(key)
            self._size += 1
            return

        node = self._root
        while True:
            if key == node.val:
                return                             # already present
            if key < node.val:
                if node.left is None:
                    node.left = TreeNode(key)
                    self._size += 1
                    return
                node = node.left
            else:
                if node.right is None:
                    node.right = TreeNode(key)
                    self._size += 1
                    return
                node = node.right

    # ------------------------------------------------------------------
    # Min / Max
    # ------------------------------------------------------------------

    def min(self):
        """O(h). Smallest key. Raises if empty."""
        if self._root is None:
            raise LookupError("min() on empty BST")
        return self._leftmost(self._root).val

    def max(self):
        """O(h). Largest key. Raises if empty."""
        if self._root is None:
            raise LookupError("max() on empty BST")
        node = self._root
        while node.right is not None:
            node = node.right
        return node.val

    @staticmethod
    def _leftmost(node):
        while node.left is not None:
            node = node.left
        return node

    # ------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------

    def remove(self, key):
        """
        O(h). Remove `key`. Raises KeyError if absent.

        Two-child case: replace this node's value with its IN-ORDER
        SUCCESSOR (= smallest key in right subtree), then remove that
        successor recursively (which by construction has at most one child).
        """
        before = self._size
        self._root = self._remove(self._root, key)
        if self._size == before:
            raise KeyError(key)

    def _remove(self, node, key):
        if node is None:
            return None
        if key < node.val:
            node.left = self._remove(node.left, key)
        elif key > node.val:
            node.right = self._remove(node.right, key)
        else:
            # Found it
            if node.left is None:
                self._size -= 1
                return node.right
            if node.right is None:
                self._size -= 1
                return node.left
            # Two children: copy successor value, delete successor
            succ = BST._leftmost(node.right)
            node.val = succ.val
            node.right = self._remove(node.right, succ.val)
        return node

    # ------------------------------------------------------------------
    # Iteration
    # ------------------------------------------------------------------

    def __iter__(self):
        """In-order iteration — yields keys in sorted order. O(n) total."""
        stack = []
        node = self._root
        while node is not None or stack:
            while node is not None:
                stack.append(node)
                node = node.left
            node = stack.pop()
            yield node.val
            node = node.right

    def __repr__(self):
        return f"BST([{', '.join(repr(v) for v in self)}])"


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Basic insert / contains / iter
    t = BST()
    assert t.is_empty() and len(t) == 0
    assert 3 not in t

    for x in [5, 3, 8, 1, 4, 7, 9]:
        t.insert(x)
    assert len(t) == 7
    assert list(t) == [1, 3, 4, 5, 7, 8, 9]        # in-order sorted
    assert 4 in t and 6 not in t

    # Duplicate insert is a no-op
    t.insert(5)
    assert len(t) == 7

    # Min / max
    assert t.min() == 1
    assert t.max() == 9

    # Delete — leaf
    t.remove(1)
    assert 1 not in t
    assert list(t) == [3, 4, 5, 7, 8, 9]

    # Delete — one child
    t.remove(3)
    assert list(t) == [4, 5, 7, 8, 9]

    # Delete — two children (5 is root with both children)
    t.remove(5)
    assert 5 not in t
    assert list(t) == [4, 7, 8, 9]

    # Delete — root with one child remaining
    t.remove(4)
    t.remove(9)
    t.remove(8)
    assert list(t) == [7]

    t.remove(7)
    assert t.is_empty()

    # Delete missing — KeyError
    try:
        t.remove(42)
    except KeyError:
        pass
    else:
        raise AssertionError("expected KeyError")

    # Empty min/max
    try:
        t.min()
    except LookupError:
        pass
    else:
        raise AssertionError("expected LookupError")

    # Stress: 1000 random ops vs sorted list (ground truth)
    import random
    random.seed(42)
    t = BST()
    truth = set()

    for _ in range(5_000):
        op = random.choice(["insert", "contains", "remove"])
        x = random.randint(0, 200)
        if op == "insert":
            t.insert(x)
            truth.add(x)
        elif op == "contains":
            assert (x in t) == (x in truth)
        else:
            if x in truth:
                t.remove(x)
                truth.discard(x)

        assert len(t) == len(truth)

    # Final state
    assert list(t) == sorted(truth)
    if truth:
        assert t.min() == min(truth)
        assert t.max() == max(truth)

    print(f"Stress test: 5000 random ops, final size={len(t)}")
    print("All tests passed!")
