# 🗺️ Master Python DSA — Roadmap

This document outlines the **13-phase learning journey** from DSA beginner to competitive-level programmer. Each phase builds on the previous one.

Legend: ✅ Complete · 🚧 In Progress · 📋 Planned

---

## 📊 Progress Overview

| Phase | Title | Status | Python | Markdown |
|-------|-------|--------|--------|----------|
| 01 | Foundations | ✅ Complete | 17 | 14 |
| 02 | Problem-Solving Foundations | ✅ Complete | 56 | 22 |
| 03 | Searching & Sorting | ✅ Complete | 38 | 10 |
| 04 | Linear Data Structures | ✅ Complete | 38 | 13 |
| 05 | Recursion & Backtracking | ✅ Complete | 27 | 5 |
| 06 | Hashing | ✅ Complete | 14 | 4 |
| 07 | Trees & Heaps | ✅ Complete | 45 | 7 |
| 08 | Graphs | ✅ Complete | 25 | 6 |
| 09 | Dynamic Programming | ✅ Complete | 24 | 7 |
| 10 | String Algorithms | 📋 Planned | — | — |
| 11 | Advanced Data Structures | 📋 Planned | — | — |
| 12 | Greedy & Math | 📋 Planned | — | — |
| 13 | Competitive Level | 📋 Planned | — | — |

**Totals so far**: 9 phases · 284 Python files · 88 Markdown files. Every Python file in completed phases ships with stress tests against either a brute-force reference, a Python built-in, or a cross-checked alternate implementation.

---

## 🏗️ Phase-by-Phase Breakdown

### Phase 01 — Foundations 🚧
Build the base: **what DSA is, how to measure efficiency, and how Python's built-ins work.**

- 🧠 Introduction to DSA (theory, why it matters, how to learn, glossary)
- ⏱️ Time & Space Complexity (Big O, amortized, recursion complexity)
- 🐍 Python Built-In DSA (List, Tuple, Dict, Set, String, Collections)

**Outcome:** You can pick the right built-in structure and predict its cost.

---

### Phase 02 — Problem-Solving Foundations 📋
Learn to **recognize problem patterns** and apply the right algorithmic strategy.

- 🧩 Algorithm Paradigms — Brute Force, Divide & Conquer, Greedy, DP, Backtracking, Branch & Bound
- ⚙️ Algorithmic Techniques — Two Pointers, Sliding Window, Prefix Sum, Difference Array, Binary Search on Answer, Fast/Slow Pointers, Hashing, Frequency Counting, Monotonic Stack, Meet in the Middle, Bit Manipulation, Merge Intervals

**Outcome:** You can classify any problem into a known pattern and reach for the right template.

---

### Phase 03 — Searching & Sorting 📋
Master the classic algorithms every interview expects.

- 🔍 Searching — Linear, Binary (+ variations), Jump, Exponential, Ternary
- 🫧 Basic Sorting — Bubble, Selection, Insertion
- ⚡ Efficient Sorting — Merge, Quick, Heap
- 📦 Non-Comparison Sorting — Counting, Radix, Bucket

**Outcome:** You know when each algorithm wins, and why.

---

### Phase 04 — Linear Data Structures 📋
Implement the fundamental containers from scratch.

- Array (static & dynamic)
- String
- Linked List (Singly, Doubly, Circular, Cycle Detection)
- Stack (array + linked, applications)
- Queue (array, linked, circular)
- Deque

**Outcome:** You understand memory layout and operation costs for every linear structure.

---

### Phase 05 — Recursion & Backtracking 📋
Think recursively and explore solution spaces systematically.

- 🔁 Recursion — Tail, Head, Tree, Indirect recursion; recursion trees
- 🔙 Backtracking — Subsets, Permutations, Combinations, N-Queens, Sudoku, Word Search, Graph Backtracking

**Outcome:** You can frame any exploratory problem as a recursive search with pruning.

---

### Phase 06 — Hashing 📋
Trade space for time — the single most powerful optimization in interviews.

- HashMap (chaining, open addressing, built-in `dict`)
- HashSet (from scratch + built-in `set`)
- Frequency techniques (`Counter`, frequency maps)
- Classic problems (Two Sum, Group Anagrams, LRU, Top-K)

**Outcome:** You reflexively reach for hashing when you see "find/count/group."

---

### Phase 07 — Trees & Heaps 📋
Hierarchical data + priority-based retrieval.

- Binary Tree (traversals, properties, construction)
- Binary Search Tree (search, insert, delete, validate)
- AVL Tree (rotations, balancing)
- Heap (min/max, priority queue, heap sort, K-problems)
- Trie (prefix search, autocomplete)

**Outcome:** You can choose between tree types based on operation frequency.

---

### Phase 08 — Graphs 📋
Model and traverse relationships — the backbone of most hard problems.

- Representation (matrix, list, edge list, weighted)
- Traversal (BFS, DFS, Topological Sort, Cycle Detection)
- Shortest Path (Dijkstra, Bellman-Ford, Floyd-Warshall)
- Minimum Spanning Tree (Kruskal, Prim)
- Union-Find / DSU
- Advanced — SCC (Kosaraju, Tarjan), Articulation Points, Bridges, Eulerian Path

**Outcome:** Given any graph problem, you can pick the right algorithm in seconds.

---

### Phase 09 — Dynamic Programming 📋
Turn recursion with overlapping subproblems into efficient iterative solutions.

- 🧱 Foundations (memoization vs tabulation, optimal substructure)
- 1D DP, 2D DP
- Knapsack (0/1 and Unbounded)
- LCS family, LIS family
- Matrix Chain Multiplication
- DP on Trees, DP on Grids
- Bitmask DP, State Compression

**Outcome:** You can identify, formulate, and optimize any DP problem.

---

### Phase 10 — String Algorithms 📋
Go beyond substring matching.

- Naive matching & Rabin-Karp
- KMP (failure function)
- Z-algorithm
- Manacher's (palindromes)
- Suffix Array & LCP
- Trie applications (Aho-Corasick)

**Outcome:** String problems stop being scary.

---

### Phase 11 — Advanced Data Structures 📋
Tools that power competitive programming.

- Advanced Tries (compressed, suffix)
- Segment Tree (+ lazy propagation)
- Fenwick Tree (BIT)
- Sparse Table (RMQ)
- Sqrt Decomposition (+ Mo's algorithm)
- Ordered Statistics Tree

**Outcome:** Range queries and updates become routine.

---

### Phase 12 — Greedy & Math 📋
Sharpen mathematical intuition.

- 💰 Greedy classics (Activity Selection, Huffman, Platforms, Job Sequencing)
- 🔢 Number Theory (GCD, primes, sieves)
- 📐 Modular Arithmetic (exponentiation, inverse)
- 🎲 Combinatorics (factorials, nCr, Catalan)
- 🔣 Advanced Bit Manipulation (XOR tricks, subset generation)

**Outcome:** You can handle math-heavy problems with confidence.

---

### Phase 13 — Competitive Level 📋
Frontier topics for contests and harder interviews.

- Heavy-Light Decomposition
- Network Flow (Ford-Fulkerson, Edmonds-Karp, Dinic)
- Convex Hull (Graham Scan, Jarvis March)
- Mo's Algorithm
- Advanced Strings (Suffix Automaton, Suffix Tree)
- Advanced DP (Digit DP, Probability DP)

**Outcome:** You're prepared for competitive programming and FAANG-hard rounds.

---

## 🎯 Milestones

- 🥉 **After Phase 04:** You can solve most LeetCode Easy problems.
- 🥈 **After Phase 09:** You can solve most LeetCode Medium problems.
- 🥇 **After Phase 13:** You can tackle Hard problems and compete on Codeforces.

---

## 📚 Supporting Resources

Alongside the phases, the `resources/` folder contains:

- 📋 Cheatsheets (paradigms, techniques, complexity, data structures, Python)
- 🧰 Templates (binary search, sliding window, DP, backtracking, graphs, trees)
- 🎤 Interview prep (company-wise, behavioral, system design, mocks)
- 📖 Book notes (CTCI, EPI, Algorithm Design Manual)
- 🎥 Video playlists
- 🏋️ Practice tracks (LeetCode, Codeforces, HackerRank)

And `projects/` contains end-to-end applications of DSA at beginner / intermediate / advanced levels.

---

## 🚀 Contributing

Want to help complete this roadmap? See the [Contributing Guide](docs/contributing-guide.md).

---

*Last updated: 2026-04-20*
