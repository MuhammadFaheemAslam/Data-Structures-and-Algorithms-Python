# Binary Tree — Theory

A **binary tree** is either empty, or a NODE holding a value plus two
sub-trees: a `left` child and a `right` child. The recursive definition
is also the reason almost every binary-tree algorithm is recursive.

```
        A
       / \
      B   C
     / \   \
    D   E   F
```

Terminology we'll use throughout:

| Term        | Meaning                                                          |
|-------------|------------------------------------------------------------------|
| root        | The top node. The only node with no parent.                      |
| leaf        | A node with no children.                                         |
| internal    | A node with at least one child.                                  |
| depth       | Edges from root to this node. Root has depth 0.                  |
| height      | Edges from this node to its deepest leaf. Leaves have height 0.  |
| height of tree | Height of the root node (max depth over all leaves).          |
| subtree     | A node plus all its descendants, viewed as a tree on its own.    |

The edge count doubles per level if the tree is full, so a tree of
height `h` has at most `2^(h+1) - 1` nodes. Flipped: a tree with `n`
nodes has height at least `⌈log2(n+1)⌉ - 1` (balanced) and at most
`n - 1` (a degenerate chain).

---

## Why binary (vs. n-ary)?

N-ary trees (each node may have many children) exist and are useful —
the DOM, filesystem, XML. But for *search / sort / compare* problems,
binary trees are the right abstraction:

- A binary decision ("left or right?") naturally encodes a comparison.
- Expression trees, decision trees, Huffman codes, syntax trees — all
  naturally binary after arity normalization.
- Balanced binary trees give O(log n) for the operations that matter.

When you meet a general tree (filesystem traversal, for example), a
common trick is the **left-child / right-sibling** encoding: any
n-ary tree can be represented as a binary tree where a node's `left`
is its first child and `right` is its next sibling.

---

## Kinds of binary trees

| Name           | Definition                                                         |
|----------------|--------------------------------------------------------------------|
| **Full**       | Every node has 0 OR 2 children. No one-child internal nodes.       |
| **Complete**   | Every level is fully filled, except possibly the last, which fills left-to-right. |
| **Perfect**    | Every internal node has 2 children AND every leaf is at the same depth. |
| **Balanced**   | For every node, `|height(left) - height(right)|` ≤ some constant.  |
| **Degenerate** | Every node has at most one child — shape is a linked list.         |

Useful facts:

- Perfect ⊆ Complete ⊆ Balanced.
- A complete tree's shape lets you store it in an array (Phase 04's
  heap does exactly this).
- A balanced tree is what AVL, Red-Black, and B-trees are all built to
  preserve — because only balanced trees guarantee O(log n).

---

## The `TreeNode` we'll use

Throughout this module (and the BST / AVL modules), nodes look like:

```python
class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

`__slots__` saves memory and forbids typo-bugs ("node.value = x"
silently creating a new attribute). This is the same shape LeetCode
uses (minus the slots), so solutions copy-paste cleanly.

---

## The four traversals

A traversal is a *rule* for ordering the nodes. The four canonical
ones:

| Order         | Rule (relative to current node)  | When you'd use it                     |
|---------------|----------------------------------|---------------------------------------|
| **Pre-order** | visit, recurse left, recurse right | serialization, tree copying           |
| **In-order**  | recurse left, visit, recurse right | BST → sorted sequence                 |
| **Post-order**| recurse left, recurse right, visit | delete tree, evaluate expression tree |
| **Level-order** | BFS: root, then all at depth 1, etc. | problems about "closest to root"     |

All four visit each node exactly once, so they're O(n) time and
O(h) space for the recursive versions (O(w) for level-order, where w
is the max width). In-order and pre-order also have clever iterative
formulations — see the `traversals/` subdir for each.

Morris traversal is a specialty: in-order in O(n) time and **O(1)**
space by temporarily mutating the tree.

---

## Common properties

Every binary-tree property can be computed in a single DFS by choosing
the right aggregation function. The properties/ directory implements
the classics:

- **Height** — `1 + max(height(left), height(right))`, leaves 0.
- **Diameter** — longest path between any two nodes (may pass through
  any node, not necessarily the root).
- **Balanced?** — check `|height(left) - height(right)| ≤ 1` at every
  node; return height in the same pass to keep it O(n).
- **Symmetric?** — mirror self-comparison.

These are the canonical "you must handle return value AND side-effect"
recursive patterns. Get fluent in this style — they underlie a LOT of
LeetCode tree problems.

---

## Construction

Two given traversals are usually enough to reconstruct a unique binary
tree — but not any two. Inorder + (preorder OR postorder) works.
Preorder + postorder alone does not (ambiguous on one-child nodes).

`construction/from-in-pre.py` and `from-in-post.py` cover the two cases.
`serialize-deserialize.py` shows the LC #297 approach: a pre-order walk
with `"null"` markers for missing children — O(n) time, O(n) output.

---

## The big mental model

For ~80% of binary-tree problems, the algorithm is:

1. **Recurse** on left and right.
2. **Combine** their results with the current node's value.
3. **Return** the combined result up to your parent.

This is essentially "divide and conquer on a tree". Once you see the
recursion pattern, problems like "max path sum" or "lowest common
ancestor" fall out of a careful choice of what to return.

The other ~20% need a second pass, a global variable, or an iterative
formulation (Morris, level-order with queue). We'll meet those too.
