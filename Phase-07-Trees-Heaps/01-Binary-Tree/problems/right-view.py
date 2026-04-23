r"""
Problem: Binary Tree Right Side View

Difficulty: Medium (LeetCode #199)

---------------------------------------------------
Problem Statement:

Standing on the right side of a binary tree, what do you see?
Return the values of the nodes visible from the right, from top to
bottom.

        1           <- 1
       / \
      2   3         <- 3
       \   \
        5   4       <- 4

    Right view: [1, 3, 4]

Equivalently: for each LEVEL, return the RIGHTMOST node's value.

---------------------------------------------------
Two Natural Approaches:

    A) BFS: at each level, remember only the LAST node's value.
       Time O(n), Space O(w).

    B) DFS right-first: recurse RIGHT before LEFT; the first node we
       visit at each depth is the rightmost. Track the max depth seen
       so far.
       Time O(n), Space O(h).

Both are below. DFS is slightly cleverer and 3-4 lines; BFS is the
"just follow the obvious definition" version.

---------------------------------------------------
Variants:

    - Left side view: mirror image — recurse LEFT first.
    - Top / bottom view: column-indexed traversal — each column's
      topmost (or bottommost) node. Distinct problem, similar BFS.
    - Boundary of tree (LC #545): combines these.
"""

import os
import sys
from collections import deque

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from implementation import TreeNode, tree_from_list


# -------- A) BFS: take the last node of each level --------

def right_side_view_bfs(root):
    """
    Return the rightmost value at each depth.

    Time:  O(n), Space: O(w).
    """
    if root is None:
        return []

    result = []
    queue = deque([root])
    while queue:
        level_size = len(queue)
        for i in range(level_size):
            node = queue.popleft()
            if i == level_size - 1:                # rightmost in this level
                result.append(node.val)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
    return result


# -------- B) DFS, right-first: first visit at each depth --------

def right_side_view(root):
    """
    DFS preferring right, appending when we reach a new max depth.

    Time:  O(n), Space: O(h).
    """
    result = []

    def walk(node, depth):
        if node is None:
            return
        if depth == len(result):
            # First node we're seeing at this depth from the right side
            result.append(node.val)
        walk(node.right, depth + 1)
        walk(node.left, depth + 1)

    walk(root, 0)
    return result


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    cases = [
        ([], []),
        ([1], [1]),
        ([1, 2], [1, 2]),
        ([1, 2, 3, None, 5, None, 4], [1, 3, 4]),            # LC #199 example
        ([1, None, 3], [1, 3]),
        ([1, 2, 3, 4], [1, 3, 4]),
        # Left-only chain: rightmost = the chain itself
        ([1, 2, None, 3, None, 4], [1, 2, 3, 4]),
        # Right-only chain
        ([1, None, 2, None, 3, None, 4], [1, 2, 3, 4]),
        # Tricky: left subtree deeper than right — its leftmost-visible
        #         becomes part of the view at lower depths
        ([1, 2, 3, 4], [1, 3, 4]),
        ([1, 2, 3, 4, 5, None, None, None, None, 6, 7], [1, 3, 5, 7]),
    ]

    for vals, expected in cases:
        tree = tree_from_list(vals)
        assert right_side_view(tree) == expected, f"DFS mismatch on {vals}"
        assert right_side_view_bfs(tree) == expected, f"BFS mismatch on {vals}"

    # Randomized cross-check
    import random
    random.seed(42)
    for _ in range(200):
        n = random.randint(0, 50)
        vals = [random.randint(0, 100) if random.random() < 0.85 else None for _ in range(n)]
        if vals and vals[0] is None:
            vals[0] = 0
        tree = tree_from_list(vals)
        assert right_side_view(tree) == right_side_view_bfs(tree)

    print("All tests passed!")
