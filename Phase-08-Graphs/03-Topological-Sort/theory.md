# Topological Sort — Theory

A **topological sort** (or "topo sort") is a LINEAR ORDERING of the
vertices of a **DIRECTED ACYCLIC GRAPH** (DAG) such that for every
edge `u → v`, `u` comes BEFORE `v`.

```
       A → B → D
       ↓   ↓
       C → E

    Valid topo orders:   [A, B, C, E, D]
                         [A, C, B, D, E]
                         [A, B, D, C, E]   ✓ (all consistent with → )

    INVALID:             [B, A, ...]       ✗ (A → B broken)
```

---

## Why it matters

Topo sort is the algorithmic way to answer "in what order can I
process these with-dependencies things?". Concrete cases:

- **Course schedule** — course X requires course Y; what's the
  enrolment order?
- **Build systems** — file A depends on file B; compile B first.
  `make`, Ninja, Bazel, Cargo, every package manager.
- **Spreadsheet recalculation** — cell X uses cell Y; compute Y first.
- **Database query planning** — resolve sub-queries in dependency order.
- **Dead-code / unused-import detection** — in a post-order walk,
  a symbol with no consumers surfaces at the top of the reverse topo
  order.

Whenever the question is "process these in a **valid dependency
order**", the answer is topo sort.

---

## The two standard algorithms

### 1. Kahn's algorithm (BFS-based)

Maintain the IN-DEGREE of each vertex. Repeatedly pick a vertex with
in-degree 0 (nothing pointing at it → ready to process); emit it; for
each outgoing edge `v → w`, decrement w's in-degree. Stop when every
vertex is emitted.

```
queue ← all vertices with in-degree 0
while queue:
    u = queue.popleft()
    emit u
    for each v in neighbours(u):
        indeg[v] -= 1
        if indeg[v] == 0:
            queue.append(v)
```

If the loop finishes with fewer emitted vertices than V, there's a
**cycle** — a topo sort is impossible. Same algorithm, same code,
detects cycles for free.

**Time**: O(V + E). **Space**: O(V).

### 2. DFS-based algorithm

Run DFS. As each vertex **finishes** (all its descendants visited),
push it onto a stack. The REVERSE of the finish order is a valid
topo order.

```
post_order = []
visited = set()
def dfs(u):
    visited.add(u)
    for v in neighbours(u):
        if v not in visited:
            dfs(v)
    post_order.append(u)
for each u in vertices:
    if u not in visited:
        dfs(u)

topo_order = reversed(post_order)
```

Cycle detection needs a **three-color** scheme: WHITE (unvisited),
GRAY (on the current DFS path), BLACK (finished). Seeing a GRAY
vertex during traversal means a back-edge → cycle.

**Time**: O(V + E). **Space**: O(V).

---

## When to pick which

| Aspect                   | Kahn's (BFS)              | DFS-based                  |
|--------------------------|---------------------------|----------------------------|
| Iterative by default     | ✓                         | ✗ (or use iterative DFS)    |
| Natural fit for problems giving you in-degrees | ✓ | ✗                          |
| Lexicographic smallest topo order | ✓ (use a min-heap instead of FIFO) | tricky                     |
| Cycle detection          | "did I emit everyone?"     | three-color scheme          |
| Single-call "also finds SCCs" | ✗                 | ✓ (Tarjan / Kosaraju — 06-Advanced) |

Default: **Kahn's**. Clean, iterative, natural cycle test. Reach for
DFS-based when the problem REQUIRES post-order info for other
reasons (DP on DAG, SCC, longest path), or when you already have a
DFS traversal written.

---

## Properties worth knowing

1. **Uniqueness** — A topo order is unique iff the DAG is a HAMILTONIAN PATH
   (every pair of consecutive vertices in the order is directly connected).
   Otherwise there can be many. Most problems accept any valid order.

2. **DAG-ness is the only precondition** — topo sort is defined only
   on DAGs. A cyclic graph has no valid order. Every topo-sort algorithm
   must have a cycle check.

3. **First / last-layer semantics** — In Kahn's, the first vertex
   emitted is one with no prerequisites ("can start immediately"); the
   last emitted has no dependents. The ORDER of same-layer emissions
   is determined by queue discipline (FIFO = insertion order;
   min-heap = lexicographic; etc.).

4. **DP on DAG** — Many DP problems on DAGs can be solved by
   processing vertices in topo order:
   - Longest path in a DAG
   - Counting paths from s to t
   - Shortest path in a DAG with negative weights (topo-order
     relaxation — O(V + E) instead of Bellman-Ford's O(V·E))

---

## What's in this module

- [kahn-bfs.py](kahn-bfs.py) — Kahn's algorithm with cycle detection.
- [dfs-based.py](dfs-based.py) — DFS three-color algorithm.
- [problems/course-schedule.py](problems/course-schedule.py) — LC #207 (can-finish) + #210 (order).
- [problems/alien-dictionary.py](problems/alien-dictionary.py) — LC #269, deriving an alphabet from sorted words.
