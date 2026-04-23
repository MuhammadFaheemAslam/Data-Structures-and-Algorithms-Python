"""
implementation.py — AVL Tree (self-balancing BST)

Every node stores its HEIGHT. After inserts and deletes, we walk back
up the path, recompute heights, and rotate wherever the balance
factor falls outside [-1, +1]. The rotations themselves come from
rotations.py.

Invariant (checked by `is_avl()`):
    for every node:  |height(left) - height(right)| ≤ 1

---------------------------------------------------
API:

    tree = AVLTree()
    tree.insert(5)
    tree.insert(3)
    5 in tree          # True
    tree.remove(3)
    list(tree)         # sorted iteration
    tree.min(), tree.max()

---------------------------------------------------
Complexity (worst case, not just average):

    search:    O(log n)
    insert:    O(log n) — may trigger ≤1 rotation (or 1 double rotation)
    delete:    O(log n) — may trigger up to O(log n) rotations
    iterate:   O(n)

Guaranteed, not amortized. That's AVL's whole pitch.
"""

from rotations import (
    AVLNode,
    height,
    update_height,
    balance_factor,
    rotate_left,
    rotate_right,
)


class AVLTree:
    """Self-balancing BST. No duplicates; insert of an existing key is a no-op."""

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

    def height(self):
        return height(self._root)

    def root(self):
        return self._root

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def contains(self, key):
        node = self._root
        while node is not None:
            if key == node.val:
                return True
            node = node.left if key < node.val else node.right
        return False

    def __contains__(self, key):
        return self.contains(key)

    # ------------------------------------------------------------------
    # Min / max
    # ------------------------------------------------------------------

    def min(self):
        if self._root is None:
            raise LookupError("min() on empty AVL tree")
        node = self._root
        while node.left is not None:
            node = node.left
        return node.val

    def max(self):
        if self._root is None:
            raise LookupError("max() on empty AVL tree")
        node = self._root
        while node.right is not None:
            node = node.right
        return node.val

    # ------------------------------------------------------------------
    # Insert
    # ------------------------------------------------------------------

    def insert(self, key):
        """
        O(log n). Insert `key`. No-op if already present.
        """
        before = self._size
        self._root = self._insert(self._root, key)
        return self._size > before                 # True iff a new node was added

    def _insert(self, node, key):
        if node is None:
            self._size += 1
            return AVLNode(key)

        if key < node.val:
            node.left = self._insert(node.left, key)
        elif key > node.val:
            node.right = self._insert(node.right, key)
        else:
            return node                            # duplicate, no-op

        return self._rebalance(node)

    # ------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------

    def remove(self, key):
        """O(log n). Remove `key`. Raises KeyError if absent."""
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
            # Found — handle the three cases.
            if node.left is None:
                self._size -= 1
                return node.right
            if node.right is None:
                self._size -= 1
                return node.left
            # Two children: replace with in-order successor, then delete it
            succ = self._leftmost(node.right)
            node.val = succ.val
            node.right = self._remove(node.right, succ.val)

        return self._rebalance(node)

    @staticmethod
    def _leftmost(node):
        while node.left is not None:
            node = node.left
        return node

    # ------------------------------------------------------------------
    # Rebalance — same dispatch logic as rotations.rebalance, but inlined
    # so we can use self._root elsewhere consistently.
    # ------------------------------------------------------------------

    def _rebalance(self, node):
        update_height(node)
        bf = balance_factor(node)

        # Left-heavy
        if bf > 1:
            if balance_factor(node.left) < 0:
                node.left = rotate_left(node.left)
            return rotate_right(node)

        # Right-heavy
        if bf < -1:
            if balance_factor(node.right) > 0:
                node.right = rotate_right(node.right)
            return rotate_left(node)

        return node

    # ------------------------------------------------------------------
    # Iteration
    # ------------------------------------------------------------------

    def __iter__(self):
        """In-order iteration — yields keys in sorted order."""
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
        return f"AVLTree([{', '.join(repr(v) for v in self)}])"


# =========================================================================
# Invariant checker — used in testing
# =========================================================================

def is_avl(root):
    """True iff `root` is a valid AVL tree (BST + height-balanced)."""
    def check(node, lo, hi):
        if node is None:
            return True, 0
        if not (lo < node.val < hi):
            return False, 0
        ok_l, h_l = check(node.left, lo, node.val)
        if not ok_l:
            return False, 0
        ok_r, h_r = check(node.right, node.val, hi)
        if not ok_r:
            return False, 0
        if abs(h_l - h_r) > 1:
            return False, 0
        # Verify stored height matches computed
        expected_h = 1 + max(h_l, h_r)
        if node.height != expected_h:
            return False, 0
        return True, expected_h

    ok, _ = check(root, float("-inf"), float("inf"))
    return ok


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    import math
    import random

    # --- Basic ops ---
    t = AVLTree()
    assert t.is_empty()
    assert 5 not in t

    for x in [5, 3, 8, 1, 4, 7, 9]:
        t.insert(x)
    assert is_avl(t.root())
    assert list(t) == [1, 3, 4, 5, 7, 8, 9]
    assert 4 in t and 6 not in t
    assert t.min() == 1 and t.max() == 9
    assert len(t) == 7

    # Duplicate insert
    t.insert(5)
    assert len(t) == 7

    # --- AVL vs naive BST: sorted insertion stays balanced ---
    t = AVLTree()
    for i in range(1, 1024):
        t.insert(i)
    assert is_avl(t.root())
    # Perfectly balanced height for 1023 nodes = 10 (log2(1024))
    # AVL doesn't guarantee perfect height; theoretical bound is ~1.44 log2(n)
    assert t.height() <= int(math.ceil(1.44 * math.log2(1023 + 1))) + 1
    print(f"After inserting 1..1023, AVL height = {t.height()} (perfect would be 10)")

    # --- Deletion ---
    t = AVLTree()
    for x in [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]:
        t.insert(x)
    assert is_avl(t.root())

    t.remove(50)                                   # root with two children
    assert 50 not in t
    assert is_avl(t.root())
    assert list(t) == [10, 20, 25, 30, 35, 40, 45, 60, 70, 80]

    t.remove(10)                                   # leaf
    assert is_avl(t.root())

    # --- Stress: 10k operations, AVL invariant holds throughout ---
    random.seed(42)
    t = AVLTree()
    truth = set()

    for step in range(10_000):
        op = random.choice(["insert", "remove", "contains"])
        x = random.randint(0, 500)
        if op == "insert":
            t.insert(x)
            truth.add(x)
        elif op == "remove":
            if x in truth:
                t.remove(x)
                truth.discard(x)
        else:
            assert (x in t) == (x in truth)

        # Every 100 steps, verify the invariant + ordering
        if step % 100 == 0:
            assert is_avl(t.root()), f"broken after step {step}"
            assert list(t) == sorted(truth)
            assert len(t) == len(truth)

    assert is_avl(t.root())
    assert list(t) == sorted(truth)
    print(f"Stress test: 10000 mixed ops, final size = {len(t)}, height = {t.height()}")
    if truth:
        n = len(t)
        print(f"   theoretical AVL height bound: ≤ 1.44 log2(n+2) = "
              f"{1.44 * math.log2(n + 2):.1f}")

    # --- Missing key remove raises ---
    try:
        t.remove(-1)
    except KeyError:
        pass
    else:
        raise AssertionError("expected KeyError")

    print("\nAll tests passed!")
