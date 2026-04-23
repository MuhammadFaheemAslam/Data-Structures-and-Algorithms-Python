"""
Level-Order Traversal — Breadth-First Search

Order: root, then all depth-1 nodes L→R, then all depth-2 L→R, ...

Level-order is a GRAPH BFS applied to a tree. The pattern is universal:

    queue ← root
    while queue non-empty:
        dequeue node, visit
        enqueue children

This scales unchanged from trees to general graphs — see Phase 08.

---------------------------------------------------
Two Output Formats:

    level_order(root)           → flat list    [1, 2, 3, 4, 5]
    level_order_by_level(root)  → list of lists [[1], [2, 3], [4, 5]]
                                  (LC #102)

The by-level version is slightly more useful for LC because many
problems care about per-level aggregates (right-view, averages,
zigzag).

---------------------------------------------------
Complexity:

    Time:  O(n).
    Space: O(w) where w = max tree width. For a balanced tree, w = n/2.
"""

import os
import sys
from collections import deque

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from implementation import TreeNode, tree_from_list


def level_order(root):
    """
    Flat list of all values in level order.

    Time:  O(n).
    Space: O(w).
    """
    if root is None:
        return []

    result = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        result.append(node.val)
        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)
    return result


def level_order_by_level(root):
    """
    List of lists: one inner list per level.

    The trick: BEFORE processing a level, capture the queue's length.
    That many dequeues = exactly one level's worth of nodes.

    Time:  O(n).
    Space: O(w).
    """
    if root is None:
        return []

    result = []
    queue = deque([root])
    while queue:
        level_size = len(queue)
        level = []
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        result.append(level)
    return result


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Flat level order
    assert level_order(None) == []
    assert level_order(tree_from_list([1])) == [1]
    assert level_order(tree_from_list([1, 2, 3])) == [1, 2, 3]
    assert level_order(tree_from_list([3, 9, 20, None, None, 15, 7])) == [3, 9, 20, 15, 7]

    # By-level (LC #102)
    assert level_order_by_level(None) == []
    assert level_order_by_level(tree_from_list([1])) == [[1]]
    assert level_order_by_level(tree_from_list([3, 9, 20, None, None, 15, 7])) == [[3], [9, 20], [15, 7]]
    assert level_order_by_level(tree_from_list([1, 2, 3, 4, 5, 6, 7])) == [[1], [2, 3], [4, 5, 6, 7]]

    # Gaps don't produce empty levels
    assert level_order_by_level(tree_from_list([1, 2, None, 3])) == [[1], [2], [3]]

    print("All tests passed!")
