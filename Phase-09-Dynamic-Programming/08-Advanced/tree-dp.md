# Tree DP — Theory

**Tree DP** is DP where the state is a tree node and its "mode" —
computing values bottom-up via post-order traversal. The structure
of a tree (every node has a unique parent; no cycles) gives you
**optimal substructure for free**: the optimal value at a node
depends only on its children's optimal values.

This makes tree DP one of the cleanest kinds of DP to write — once
you see the pattern, problems solve in 10-20 lines.

---

## The shape

```python
def solve(node):
    if node is None:
        return base_case           # identity element (0, inf, etc.)

    left  = solve(node.left)
    right = solve(node.right)
    return combine(node.val, left, right)
```

The state is implicitly `(node, mode)` where "mode" is one of a small
fixed set of states (rob-or-not, include-or-not, on-path-or-not).
Most tree DP problems return TUPLES — one value per mode — so the
parent can pick the max/min/sum across modes.

---

## The canonical example — House Robber III (LC #337)

Given a binary tree where each node has a value, rob a subset of
nodes such that no two CONNECTED (parent-child) nodes are both
robbed. Maximize total.

**State**: `(robbed_this_node, skipped_this_node)` = (int, int)

At each node:
```python
def rob(node):
    if node is None:
        return (0, 0)                    # (robbed, skipped) = (0, 0)

    left_rob, left_skip   = rob(node.left)
    right_rob, right_skip = rob(node.right)

    # If we rob this node, children MUST be skipped
    robbed  = node.val + left_skip + right_skip

    # If we skip this node, children can be either — pick the better
    skipped = max(left_rob, left_skip) + max(right_rob, right_skip)

    return (robbed, skipped)

answer = max(rob(root))
```

O(n) time, O(h) recursion depth. Classic tree DP in a dozen lines.

---

## Another example — Tree Diameter (Phase 07 already did this)

The longest path between two nodes in a tree (weighted or unweighted).

**State**: best downward path length ending at this node.

```python
best_diameter = 0

def dfs(node):
    nonlocal best_diameter
    if node is None:
        return 0
    left  = dfs(node.left)
    right = dfs(node.right)

    # Path THROUGH this node
    best_diameter = max(best_diameter, left + right)

    # Return best DOWNWARD extension for the parent
    return 1 + max(left, right)

dfs(root)
```

Pattern: return "best I can contribute UPWARD to my parent"; update
a closure variable with "best THROUGH me that ends locally". Same
dual-purpose recursion as LC #124 max path sum (Phase 07).

---

## Patterns

### 1. "Rob or skip" — boolean mode

Every node has two futures; pick the better one. Signals:
"constraints on adjacent nodes". Examples: LC #337 (tree robber),
LC #968 (camera placement), LC #1377 (frog position probabilities
under branching).

### 2. "Include me in the path" — two modes

The path from any subtree to its parent either "ends at me" or
"doesn't touch me". Return the best of each. Examples: LC #124,
tree diameter, longest path in a tree.

### 3. "Pass up aggregates" — numeric aggregation

Sum, product, count, min, max of a subtree. Just post-order DFS with
combine. Examples: "sum of nodes ≥ k", "count subtrees with property
X", "find median node".

### 4. Rerooting — compute for EVERY root in O(n)

Some problems ask "what's the answer if vertex V were the root?"
for all V. Naïvely O(n²); rerooting DP does it in O(n) by reusing
partial answers from a DFS and one more traversal that "moves" the
root by 1 edge at a time.

Rerooting is an advanced technique. Out of scope for this phase;
covered in Phase 11 (advanced trees).

---

## Tree DP vs graph DP

Tree DP is EASIER than DP on general graphs because:

1. **No cycles** — no need for `visited` sets, no back-edges to
   handle.
2. **Unique parent** — every node has exactly one "caller".
3. **Natural topological order** — post-order traversal IS the
   correct DP fill order.

When the problem is on a DAG instead of a tree, you still get (3)
via topological sort — that's "DP on a DAG", covered implicitly in
Phase 08 (shortest path in a DAG by topo-order relaxation).

---

## Complexity

Tree DP is almost always O(n · k) where n is the number of nodes
and k is the number of modes in the state. For LC #337, k = 2.
For LC #968 (camera placement), k = 3 (has-camera / covered /
uncovered). Even for tree DP with 10 modes per node, n = 10^5 is
fine — 10^6 total ops.

The recursion depth bound matters too. Python caps recursion at
1000 by default, so a LINEAR tree with > 1000 nodes crashes a
recursive tree DP. Either raise the limit (`sys.setrecursionlimit`)
or convert to an iterative post-order traversal.

---

## When NOT to reach for tree DP

- Problem involves PAIRS of nodes from the SAME subtree with no
  constraint → often still tree DP, just a 2-mode state.
- Problem is actually a GRAPH (has cycles) → this is graph DP,
  usually needing `visited`.
- Problem involves QUERIES over subtrees → segment/Fenwick tree
  over Euler tour (Phase 11), not plain tree DP.
- Problem involves ranges on the TREE ITSELF (e.g. "sum of values
  on path u → v") → LCA + prefix sums (Phase 11).

---

## Cross-references

This phase touched tree DP indirectly in:

- [Phase 07 / 01-Binary-Tree / properties / diameter.py](../../Phase-07-Trees-Heaps/01-Binary-Tree/properties/diameter.py) — tree diameter.
- [Phase 07 / 01-Binary-Tree / problems / max-path-sum.py](../../Phase-07-Trees-Heaps/01-Binary-Tree/problems/max-path-sum.py) — LC #124.
- [Phase 07 / 01-Binary-Tree / properties / balanced.py](../../Phase-07-Trees-Heaps/01-Binary-Tree/properties/balanced.py) — short-circuit height.

All of those are tree DP in disguise. Recognize the pattern, adapt
the state, and you can write them without looking up the solution.
