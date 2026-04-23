"""
Zigzag Level-Order Traversal

Difficulty: Medium (LeetCode #103)

---------------------------------------------------
Problem:

Same as level-order, except alternate levels are reversed:

        3
       / \
      9   20
         /  \
        15   7

    → [[3], [20, 9], [15, 7]]

---------------------------------------------------
Two Natural Implementations:

    1. BFS + per-level reverse  (O(n) time, O(w) space)
       Do standard level-order BFS; reverse every other level before
       appending.

    2. Two stacks                (O(n) time, O(w) space)
       Stack A (L→R order) feeds stack B (push left then right);
       stack B (R→L order) feeds stack A (push right then left).
       Cleaner asymptotically — never builds-then-reverses — but
       more state.

In Python, approach (1) is shorter and just as fast. Approach (2) is
the textbook solution from CLRS-style presentations.

Both are below.
"""

import os
import sys
from collections import deque

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from implementation import TreeNode, tree_from_list


# -------- Approach 1: BFS + reverse alternate levels --------

def zigzag_level_order(root):
    """
    BFS, reversing every second level's output before appending.

    Time:  O(n).
    Space: O(w).
    """
    if root is None:
        return []

    result = []
    queue = deque([root])
    left_to_right = True

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

        if not left_to_right:
            level.reverse()
        result.append(level)
        left_to_right = not left_to_right

    return result


# -------- Approach 2: Two stacks --------

def zigzag_two_stacks(root):
    """
    Ping-pong between two stacks. The stack that pushes children
    determines the ordering of the NEXT level.

    Left-to-right level: pop from stack A, push LEFT then RIGHT onto B
                         → next level's B is in L→R order (because LIFO
                         pops in reverse). Wait — let's be careful.

    The key rules:
        - When reading stack A (L→R next level's goal): push children
          LEFT-then-RIGHT, so popping B later gives RIGHT-then-LEFT
          which IS reversed from L→R → that's R→L, what we want for
          the next (reversed) level.
        - When reading stack B (R→L): push RIGHT-then-LEFT so popping
          A later gives LEFT-then-RIGHT = L→R for the following level.

    Result: each level comes out in the right order without an
    explicit reverse pass.

    Time:  O(n).
    Space: O(w).
    """
    if root is None:
        return []

    result = []
    current = [root]                               # reading: L→R
    next_level = []
    left_to_right = True

    while current:
        level_vals = []
        while current:
            node = current.pop()
            level_vals.append(node.val)
            if left_to_right:
                # Next level will be read R→L, so push L, R (child pops right-most first)
                if node.left is not None:  next_level.append(node.left)
                if node.right is not None: next_level.append(node.right)
            else:
                # Next level will be read L→R — push R, L
                if node.right is not None: next_level.append(node.right)
                if node.left is not None:  next_level.append(node.left)

        result.append(level_vals)
        current, next_level = next_level, []
        left_to_right = not left_to_right

    return result


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    cases = [
        ([], []),
        ([1], [[1]]),
        ([3, 9, 20, None, None, 15, 7], [[3], [20, 9], [15, 7]]),
        ([1, 2, 3, 4, 5, 6, 7], [[1], [3, 2], [4, 5, 6, 7]]),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
         [[1], [3, 2], [4, 5, 6, 7], [15, 14, 13, 12, 11, 10, 9, 8]]),
    ]

    for vals, expected in cases:
        tree = tree_from_list(vals)
        assert zigzag_level_order(tree) == expected, f"zigzag_level_order mismatch on {vals}"
        assert zigzag_two_stacks(tree) == expected, f"zigzag_two_stacks mismatch on {vals}"

    # Cross-check on random inputs
    import random
    random.seed(42)
    for _ in range(200):
        n = random.randint(0, 50)
        vals = [random.randint(0, 100) if random.random() < 0.85 else None for _ in range(n)]
        if vals and vals[0] is None:
            vals[0] = 0
        tree = tree_from_list(vals)
        assert zigzag_level_order(tree) == zigzag_two_stacks(tree)

    print("All tests passed!")
