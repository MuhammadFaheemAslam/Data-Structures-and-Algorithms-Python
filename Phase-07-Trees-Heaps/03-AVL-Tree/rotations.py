r"""
rotations.py — The 4 AVL Rotations, Standalone

Presented as standalone functions with ASCII diagrams, independent
of the full AVL implementation. Useful as a REFERENCE when debugging
AVL (or any self-balancing BST — red-black uses the same primitives).

Each rotation is O(1): a constant number of pointer updates.

---------------------------------------------------
Node shape (same as elsewhere in this phase):

    class AVLNode:
        val, left, right, height

height is kept ALWAYS UP TO DATE; rotations update it as part of the
rewiring. Balance factor = height(left) - height(right).

---------------------------------------------------
The four cases:

    LL — balance factor of node is +2, and node.left has bf ≥ 0.
         The imbalance is a "double-left" chain; fix with ONE right rotation.

    RR — balance factor is -2, and node.right has bf ≤ 0.
         Mirror of LL; ONE left rotation.

    LR — balance factor is +2, but node.left has bf < 0.
         Zig-zag shape; left-rotate the child, then right-rotate the node.

    RL — balance factor is -2, but node.right has bf > 0.
         Mirror of LR; right-rotate the child, then left-rotate the node.
"""


class AVLNode:
    """Node used in rotations and in implementation.py. Height-augmented."""
    __slots__ = ("val", "left", "right", "height")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        self.height = 1                            # leaf has height 1 in the "count-nodes" convention

    def __repr__(self):
        return f"AVLNode({self.val!r}, h={self.height})"


# =========================================================================
# Utilities
# =========================================================================

def height(node):
    """Height of a subtree. Convention: None has height 0, leaf has height 1."""
    return node.height if node is not None else 0


def update_height(node):
    """Recompute `node.height` from its children's heights."""
    node.height = 1 + max(height(node.left), height(node.right))


def balance_factor(node):
    """Return height(left) - height(right). None-safe."""
    if node is None:
        return 0
    return height(node.left) - height(node.right)


# =========================================================================
# The primitive rotations
# =========================================================================

def rotate_right(y):
    r"""
    Right-rotate at `y`. Returns the new root of the subtree (was y.left).

           y                  x
          / \                / \
         x   T3    ──▶      T1  y
        / \                    / \
       T1  T2                 T2  T3
    """
    x = y.left
    T2 = x.right

    # Rotate
    x.right = y
    y.left = T2

    # Update heights (y becomes a child of x, so update y first)
    update_height(y)
    update_height(x)

    return x


def rotate_left(x):
    r"""
    Left-rotate at `x`. Returns the new root of the subtree (was x.right).

          x                    y
         / \                  / \
        T1  y      ──▶       x   T3
           / \              / \
          T2 T3            T1 T2
    """
    y = x.right
    T2 = y.left

    # Rotate
    y.left = x
    x.right = T2

    # Update heights
    update_height(x)
    update_height(y)

    return y


# =========================================================================
# The four rotation cases (what callers typically dispatch to)
# =========================================================================
#
# In the full implementation, after inserting/deleting we call these
# based on the current balance factor at each node on the path back
# to the root.

def rotate_ll(z):
    r"""
    LL case:   z unbalanced to the left, z.left leaning further left.
               One right rotation on z fixes it.

            z                       y
           / \                     / \
          y   T4                  x   z
         / \                     / \ / \
        x  T3                   T1 T2 T3 T4
       / \
      T1 T2
    """
    return rotate_right(z)


def rotate_rr(z):
    """
    RR case:   z unbalanced to the right, z.right leaning further right.
               One left rotation on z fixes it.
    """
    return rotate_left(z)


def rotate_lr(z):
    r"""
    LR case:   z unbalanced to the left, z.left leaning RIGHT.
               Left-rotate z.left, then right-rotate z.

            z                      z                      x
           / \                    / \                    / \
          y   T4                 x  T4                  y   z
         / \                    / \                    / \ / \
        T1  x         ──▶      y  T3         ──▶    T1 T2 T3 T4
           / \                / \
          T2 T3             T1  T2
    """
    z.left = rotate_left(z.left)
    return rotate_right(z)


def rotate_rl(z):
    """
    RL case:   z unbalanced to the right, z.right leaning LEFT.
               Right-rotate z.right, then left-rotate z.
    """
    z.right = rotate_right(z.right)
    return rotate_left(z)


# =========================================================================
# Dispatch: given an unbalanced `node`, pick and apply the right rotation
# =========================================================================

def rebalance(node):
    """
    If `node` has balance factor outside [-1, +1], apply the appropriate
    rotation and return the subtree's new root. Otherwise return node.
    """
    update_height(node)
    bf = balance_factor(node)

    # LL or LR
    if bf > 1:
        if balance_factor(node.left) >= 0:
            return rotate_ll(node)                 # LL
        return rotate_lr(node)                     # LR

    # RR or RL
    if bf < -1:
        if balance_factor(node.right) <= 0:
            return rotate_rr(node)                 # RR
        return rotate_rl(node)                     # RL

    return node


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Build a trivial node tree and verify each rotation

    def build(val, left=None, right=None):
        n = AVLNode(val, left, right)
        update_height(n)
        return n

    def inorder(n):
        if n is None: return []
        return inorder(n.left) + [n.val] + inorder(n.right)

    # --- Simple right rotation -------
    #     30                  20
    #    /                   / \
    #   20       ──▶        10 30
    #  /
    # 10
    n10 = build(10)
    n20 = build(20, left=n10)
    n30 = build(30, left=n20)
    update_height(n20); update_height(n30)
    new_root = rotate_right(n30)
    assert new_root.val == 20
    assert new_root.left.val == 10
    assert new_root.right.val == 30
    assert new_root.height == 2
    assert inorder(new_root) == [10, 20, 30]

    # --- Simple left rotation -------
    #     10                  20
    #       \                / \
    #       20       ──▶    10 30
    #         \
    #         30
    n30 = build(30)
    n20 = build(20, right=n30)
    n10 = build(10, right=n20)
    update_height(n20); update_height(n10)
    new_root = rotate_left(n10)
    assert new_root.val == 20
    assert new_root.left.val == 10
    assert new_root.right.val == 30
    assert inorder(new_root) == [10, 20, 30]

    # --- LR rotation -------
    #     30                  20
    #    /                   / \
    #   10       ──▶        10 30
    #     \
    #     20
    n20 = build(20)
    n10 = build(10, right=n20)
    n30 = build(30, left=n10)
    update_height(n10); update_height(n30)
    new_root = rebalance(n30)
    assert new_root.val == 20
    assert inorder(new_root) == [10, 20, 30]

    # --- RL rotation -------
    #    10                  20
    #      \                / \
    #      30    ──▶       10 30
    #     /
    #    20
    n20 = build(20)
    n30 = build(30, left=n20)
    n10 = build(10, right=n30)
    update_height(n30); update_height(n10)
    new_root = rebalance(n10)
    assert new_root.val == 20
    assert inorder(new_root) == [10, 20, 30]

    # --- Balanced node shouldn't change -------
    n1 = build(1); n3 = build(3)
    n2 = build(2, left=n1, right=n3)
    update_height(n2)
    assert rebalance(n2) is n2

    print("All rotation tests passed!")
