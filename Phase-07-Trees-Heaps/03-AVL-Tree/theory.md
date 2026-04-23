# AVL Tree — Theory

An **AVL tree** is a BST that keeps itself BALANCED. After every
insert or delete, the height of each node's two subtrees differs by
AT MOST 1. This invariant guarantees `h = O(log n)` always — even on
the pathological sorted-insertion input that turns a plain BST into
a chain.

Named after Adelson-Velsky and Landis, who published it in 1962 —
the first self-balancing BST ever invented.

---

## The invariant

For every node `N`:

```
|height(N.left) - height(N.right)| ≤ 1
```

We call `height(N.left) - height(N.right)` the **balance factor** of
N. It must always be in `{-1, 0, +1}`. If any operation (insert or
delete) tips it outside that range, we ROTATE to restore balance.

Height is typically stored in each node and updated bottom-up after
every structural change, so we never have to recompute it. The extra
field costs O(1) per node (just an integer).

---

## Why balance matters — the numbers

A plain BST's height is `O(n)` in the worst case. AVL guarantees
`O(log n)`. Concretely:

| Operation        | Plain BST (adversarial) | AVL tree   |
|------------------|-------------------------|------------|
| search           | O(n)                    | O(log n)   |
| insert           | O(n)                    | O(log n)   |
| delete           | O(n)                    | O(log n)   |
| in-order scan    | O(n)                    | O(n)       |

For `n = 10^6`, `log₂ n ≈ 20`. An O(n) search on a degenerate chain
is 50,000× slower than O(log n) on an AVL. Balance is not a micro-
optimization — it's the difference between working and timing out.

---

## Rotations — the mechanical trick

There are four imbalance cases, resolved by four rotation patterns:

```
LL (left-left):  left subtree is too tall, and the grandchild is on the left
                 → one RIGHT ROTATION at the unbalanced node.

RR (right-right): mirror of LL
                 → one LEFT ROTATION.

LR (left-right):  left subtree is too tall, but grandchild is on the right
                 → LEFT rotation on the child, then RIGHT on the node.

RL (right-left):  mirror of LR
                 → RIGHT rotation on the child, then LEFT on the node.
```

Each rotation is O(1) — constant pointer rewiring. See
[rotations.py](rotations.py) for standalone diagrams and code.

After an insert, at MOST one rotation (or one double rotation) is
needed to restore balance everywhere. Deletes can cascade — up to
O(log n) rotations along the path to the root. Both still O(log n)
total work.

---

## The single invariant that makes rotations safe

A rotation preserves the BST ordering property because it only
rearranges pointers *within a triple* that was already BST-ordered.
You never need to re-check ordering after rotating — only the height
and balance.

That's the whole elegance: "if the subtree was a valid BST before,
the rotation keeps it valid."

---

## AVL vs Red-Black vs B-tree

| Tree           | Balance guarantee                   | Where it shines                |
|----------------|-------------------------------------|--------------------------------|
| **AVL**        | `|bf| ≤ 1` — *very* tight            | Read-heavy; precise latency    |
| **Red-Black**  | Path from root to leaf: ≤ 2× shortest | Mixed workloads; less rotation on insert |
| **B-tree**     | Same per-leaf bound + high fanout    | DISK-backed (databases, filesystems) |

Rough rule: AVL gives slightly faster LOOKUPS (tighter balance), but
does more work on INSERT/DELETE (more rotations). Red-black is the
usual "general-purpose in-memory balanced BST" choice, which is why
`std::map` (C++), `TreeMap` (Java), and most Rust/Go map libraries
pick it.

Python's `dict` uses hashing (Phase 06), not a balanced BST. For a
sorted container, pip install `sortedcontainers` — which uses a
completely different data structure (skip-list-like) but exposes the
same API.

---

## When you'd reach for AVL

- You're implementing an in-memory index with **latency SLAs**: "99%
  of lookups in under X µs" demands tight `h`.
- You need **range queries** (O(log n + k)) — order-preserving
  structure required.
- You want to implement **order statistics** (kth element in log n)
  by augmenting each node with a subtree-size count.
- You're in an **interview** and asked "design a data structure with
  worst-case O(log n) insert, delete, search, AND in-order iteration" —
  this is the answer. Hash tables don't give you order; heaps don't
  give you search.

The raw number of production systems that use AVL specifically (vs.
red-black or B-tree) is small. The concept of "self-balancing via
rotations" is universal.

---

## What's next in this module

- [implementation.py](implementation.py) — the AVL class with insert, delete, and search.
- [rotations.py](rotations.py) — the 4 rotation cases as standalone functions with ASCII diagrams.
- [applications.md](applications.md) — a short tour of where self-balancing BSTs show up in production.
