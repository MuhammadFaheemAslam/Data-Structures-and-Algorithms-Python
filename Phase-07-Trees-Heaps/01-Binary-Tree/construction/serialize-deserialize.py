"""
Serialize and Deserialize Binary Tree

LeetCode #297 (Hard)

---------------------------------------------------
The Problem:

Define two functions that are inverses of each other:

    serialize(root) -> str
    deserialize(s) -> TreeNode

The string format is up to you; it just has to round-trip losslessly.

---------------------------------------------------
Approaches:

    A) PREORDER with "null" markers
       Write each node's value; write "null" for every missing child.
       Deserialize by consuming values in preorder, recursively.
       O(n) time, O(n) output length.

    B) LEVEL-ORDER (BFS) with "null" markers
       Like LC's own tree-literal format. Slightly shorter output
       because trailing nulls are trimmed. More natural to show users,
       but the parsing code is trickier.

    C) BRACKET notation "val(left)(right)"
       Compact but parsing is essentially writing a mini-parser.

We implement (A) because it's the canonical interview answer. The
recursion is trivial and it generalizes to serializing a BST with
less information (see LC #449).

---------------------------------------------------
Complexity:

    serialize:   O(n) time, O(n) string length.
    deserialize: O(n) time, O(h) recursion.
"""

import os
import sys
from collections import deque

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from implementation import TreeNode, tree_from_list, trees_equal, tree_to_list


NULL_MARKER = "#"
SEP = ","


# -------- Approach A: preorder with null markers --------

def serialize(root):
    """
    Preorder DFS; emit '#' for None. Values joined by commas.

    Time:  O(n). Space: O(n).
    """
    parts = []

    def walk(node):
        if node is None:
            parts.append(NULL_MARKER)
            return
        parts.append(str(node.val))
        walk(node.left)
        walk(node.right)

    walk(root)
    return SEP.join(parts)


def deserialize(data):
    """
    Reconstruct tree from preorder-with-nulls string.

    Time:  O(n). Space: O(h).
    """
    if not data:
        return None

    tokens = iter(data.split(SEP))

    def build():
        tok = next(tokens)
        if tok == NULL_MARKER:
            return None
        node = TreeNode(int(tok))
        node.left = build()
        node.right = build()
        return node

    return build()


# -------- Approach B: level-order (BFS) for reference --------

def serialize_bfs(root):
    """BFS serialize. Output matches LC's tree-literal format (with trimmed trailing nulls)."""
    if root is None:
        return ""

    out = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append(NULL_MARKER)
        else:
            out.append(str(node.val))
            queue.append(node.left)
            queue.append(node.right)

    # Trim trailing nulls for a canonical form
    while out and out[-1] == NULL_MARKER:
        out.pop()
    return SEP.join(out)


def deserialize_bfs(data):
    """Parse LC tree-literal format."""
    if not data:
        return None
    tokens = data.split(SEP)
    root = TreeNode(int(tokens[0]))
    queue = deque([root])
    i = 1
    n = len(tokens)

    while queue and i < n:
        node = queue.popleft()
        if i < n and tokens[i] != NULL_MARKER:
            node.left = TreeNode(int(tokens[i]))
            queue.append(node.left)
        i += 1
        if i < n and tokens[i] != NULL_MARKER:
            node.right = TreeNode(int(tokens[i]))
            queue.append(node.right)
        i += 1

    return root


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    cases = [
        [],
        [1],
        [1, 2, 3],
        [1, None, 2, 3],
        [3, 9, 20, None, None, 15, 7],
        [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1],
        [1, 2, 2, 3, 4, 4, 3],
    ]

    # Round-trip both formats
    for vals in cases:
        tree = tree_from_list(vals)

        # Preorder+null format
        s1 = serialize(tree)
        rebuilt1 = deserialize(s1)
        assert trees_equal(tree, rebuilt1), f"preorder round-trip failed on {vals}: {s1}"

        # BFS format
        s2 = serialize_bfs(tree)
        rebuilt2 = deserialize_bfs(s2)
        assert trees_equal(tree, rebuilt2), f"BFS round-trip failed on {vals}: {s2}"

    # Examine the serialized forms for one example
    tree = tree_from_list([1, 2, 3, None, None, 4, 5])
    print("Tree [1, 2, 3, None, None, 4, 5]:")
    print(f"   preorder-null: {serialize(tree)}")
    print(f"   bfs:           {serialize_bfs(tree)}")

    # Randomized
    import random
    random.seed(42)
    for _ in range(200):
        n = random.randint(0, 50)
        vals = [random.randint(-100, 100) if random.random() < 0.85 else None for _ in range(n)]
        if vals and vals[0] is None:
            vals[0] = 0
        tree = tree_from_list(vals)
        assert trees_equal(tree, deserialize(serialize(tree)))
        assert trees_equal(tree, deserialize_bfs(serialize_bfs(tree)))

    print("\nAll tests passed!")
