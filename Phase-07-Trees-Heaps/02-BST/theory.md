# Binary Search Tree — Theory

A **Binary Search Tree (BST)** is a binary tree where every node's
value is greater than ALL values in its left subtree AND less than
ALL values in its right subtree. This single invariant makes search
O(h) instead of O(n).

```
        8
       / \
      3   10
     / \    \
    1   6    14
       / \   /
      4   7 13
```

For every node, `left.val < node.val < right.val`, recursively.

---

## The invariant — stated precisely

Different textbooks disagree on what to do with equal keys. Three
common conventions:

| Variant             | Duplicate handling                                  |
|---------------------|-----------------------------------------------------|
| **No duplicates**   | `insert` of an existing key is a no-op (what we use). |
| **Left ≤, right >** | Duplicates always go LEFT. In-order traversal still sorted. |
| **Counter per node**| Each node stores a count; `insert(x)` increments if found. |

Our implementation uses "no duplicates, insert is a no-op". This matches
`set`-style semantics (LC problems almost always assume this).

---

## Why it works — the height bound

Search, insert, and delete all walk a single root-to-leaf path. The
length of that path is the tree's HEIGHT `h`. So operations are O(h).

The kicker: `h` depends on INSERTION ORDER, not just on `n`:

- Random / balanced insertions → `h ≈ log n` — all ops O(log n).
- Sorted insertions → `h = n - 1` — tree is a chain, all ops O(n).
  `insert(1); insert(2); insert(3); ...` is the classic pitfall.

Unbalanced trees are a genuine performance foot-gun. The whole point of
**self-balancing BSTs** (AVL, red-black, B-tree) is to transparently
keep `h = O(log n)` no matter the insertion order. Module 03-AVL-Tree
implements one from scratch.

---

## In-order traversal → sorted sequence

The most important consequence of the BST invariant: an in-order
traversal visits values in **sorted ascending order**. This is the
secret behind:

- **LC #230 Kth Smallest** — in-order walk, stop at the k-th visit.
- **LC #98 Validate BST** — in-order should be strictly ascending.
- **LC #108 Sorted Array → BST** — any balanced assignment of the
  sorted sequence works; pick mid as root recursively.
- **LC #109 Sorted List → BST** — same pattern via simulated in-order.
- **LC #173 BST Iterator** — in-order traversal, paused and resumed.

If you're stuck on a BST problem, your first thought should be
"is in-order helpful here?"

---

## The four core operations

| Operation    | Algorithm (high level)                                | Time |
|--------------|-------------------------------------------------------|------|
| **search(x)**   | Walk down: left if x < node, right if x > node.     | O(h) |
| **insert(x)**   | Search; if we fall off the tree, attach x there.    | O(h) |
| **delete(x)**   | Find x, handle three cases (see delete.py).         | O(h) |
| **validate**    | Range-pass DFS: each subtree's values must be in a specific (lo, hi). | O(n) |

The `operations/` subdir has each as its own file with both recursive
and iterative forms where useful.

---

## Delete is the tricky one

Deletion has three cases:

```
Case 1 — leaf:            just remove it
Case 2 — one child:       replace node with its child
Case 3 — two children:    replace node's VALUE with its in-order
                          SUCCESSOR (smallest in right subtree);
                          then delete the successor recursively
                          (which, by construction, has ≤ 1 child).
```

Case 3 is where most implementations have bugs — in particular, it's
easy to use the predecessor on one side and the successor on the other
and end up with an unbalanced tree, or to forget to delete the
successor itself after copying its value.

We implement it in [operations/delete.py](operations/delete.py).

---

## Adjacency queries — floor / ceil / predecessor / successor

Beyond search, a BST answers "what's the closest key to x?" in O(h):

- **floor(x)**     — largest key ≤ x
- **ceil(x)**      — smallest key ≥ x
- **predecessor**  — largest key < given node
- **successor**    — smallest key > given node

These reduce to "walk down and remember the best candidate on the
correct side". See [problems/floor-ceil.py](problems/floor-ceil.py).

---

## When to use a BST (vs. hash set)

| Question                             | Hash set | BST      |
|--------------------------------------|----------|----------|
| `x in S`                             | O(1)     | O(log n) |
| Iterate in sorted order              | ❌ (need external sort) | O(n) natural |
| Find floor / ceil / successor of x   | ❌        | O(log n) |
| Range query "give me all 50 ≤ x ≤ 100" | ❌     | O(log n + k) |
| Kth smallest                         | ❌        | O(log n) (augmented) |
| Guaranteed worst case                | O(n) (adversarial) | O(log n) (if balanced) |

Short rule: **use a BST when the keys have an ORDER you care about**.
Phone directories, leaderboards, database indexes — all BSTs (or
B-trees, their on-disk cousin). For "have I seen X?" with no order
structure, hash sets win.

---

## What's not in this module

- **Red-black trees, B-trees, 2-3-4 trees** — Phase 11 (advanced trees).
- **Python's `bisect`** — a sorted-list alternative to a BST with the
  same Big-O on search but O(n) inserts. Covered in Phase 04.
- **`SortedDict` / `SortedList`** (sortedcontainers) — in practice, the
  right tool in Python when you'd reach for a BST. We don't use it here
  because we're *building* the data structure.
