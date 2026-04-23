"""
implementation.py — Binary Tree core: TreeNode + helpers

Everything else in this module imports TreeNode from here. We also
provide a few helpers used by tests across all sub-files:

    tree_from_list(vals)          — build a binary tree from LC-style
                                     level-order list (None for gaps)
    tree_to_list(root)            — inverse: flatten to LC level-order list,
                                     trimming trailing Nones
    trees_equal(a, b)              — structural equality
    pretty_print(root)             — ASCII visualisation for debugging

The `tree_from_list` format matches what LeetCode uses for all its
tree problems, e.g. [1, 2, 3, None, 4] builds:

        1
       / \
      2   3
       \
        4
"""

from collections import deque


# =========================================================================
# The TreeNode
# =========================================================================

class TreeNode:
    """
    Binary-tree node. Using __slots__ to save memory and catch typos.
    """
    __slots__ = ("val", "left", "right")

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode({self.val})"


# =========================================================================
# Construction / deconstruction
# =========================================================================

def tree_from_list(vals):
    """
    Build a binary tree from a level-order list with None for gaps.

    This matches LeetCode's tree-literal format exactly. Example:

        [1, 2, 3, None, 4]
            1
           / \
          2   3
           \
            4

    Time: O(n), Space: O(n).
    """
    if not vals or vals[0] is None:
        return None

    root = TreeNode(vals[0])
    queue = deque([root])
    i = 1
    n = len(vals)

    while queue and i < n:
        node = queue.popleft()

        # Left child
        if i < n and vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1

        # Right child
        if i < n and vals[i] is not None:
            node.right = TreeNode(vals[i])
            queue.append(node.right)
        i += 1

    return root


def tree_to_list(root):
    """
    Serialize a tree to LC-style level-order list with None for gaps.
    Trailing Nones are trimmed so equal trees produce equal lists.
    """
    if root is None:
        return []

    result = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            result.append(None)
        else:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)

    # Trim trailing Nones
    while result and result[-1] is None:
        result.pop()
    return result


def trees_equal(a, b):
    """True iff two trees have the same shape AND same node values."""
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    return (a.val == b.val
            and trees_equal(a.left, b.left)
            and trees_equal(a.right, b.right))


# =========================================================================
# Pretty-print (for debugging)
# =========================================================================

def pretty_print(root):
    """
    Print a tree in a compact indented form. Convenient for debugging.

    Output is "right subtree on top, then node, then left subtree" so
    reading top-to-bottom corresponds to right-to-left of the tree.
    """
    def _walk(node, depth):
        if node is None:
            return
        _walk(node.right, depth + 1)
        print("    " * depth + str(node.val))
        _walk(node.left, depth + 1)

    _walk(root, 0)


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Empty
    assert tree_from_list([]) is None
    assert tree_to_list(None) == []

    # Single node
    root = tree_from_list([1])
    assert root.val == 1 and root.left is None and root.right is None
    assert tree_to_list(root) == [1]

    # LC example: [1,2,3,None,4]
    root = tree_from_list([1, 2, 3, None, 4])
    assert root.val == 1
    assert root.left.val == 2
    assert root.right.val == 3
    assert root.left.left is None
    assert root.left.right.val == 4
    assert tree_to_list(root) == [1, 2, 3, None, 4]

    # Round-trip a bunch of shapes
    shapes = [
        [],
        [1],
        [1, 2],
        [1, None, 2],
        [3, 9, 20, None, None, 15, 7],                        # LC #104 example
        [1, 2, 2, 3, 4, 4, 3],                                # LC #101 symmetric
        [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1],   # LC #113
    ]
    for s in shapes:
        assert tree_to_list(tree_from_list(s)) == s, f"round-trip failed: {s}"

    # Equality
    a = tree_from_list([1, 2, 3])
    b = tree_from_list([1, 2, 3])
    c = tree_from_list([1, 3, 2])
    assert trees_equal(a, b)
    assert not trees_equal(a, c)
    assert trees_equal(None, None)
    assert not trees_equal(None, a)

    print("All tests passed!")

    # Visual demo
    print("\nTree [3, 9, 20, None, None, 15, 7]:")
    pretty_print(tree_from_list([3, 9, 20, None, None, 15, 7]))
