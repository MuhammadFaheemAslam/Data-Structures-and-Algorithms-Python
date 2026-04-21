# 02 — Algorithmic Techniques

The first half of Phase 02 taught you six **paradigms** — the high-level
strategies for attacking a problem. This second half teaches **techniques**
— the reusable micro-patterns you execute inside a paradigm.

If a paradigm is the architecture of your solution, a technique is the
move you make to implement one step of it. A Divide & Conquer merge
sort uses **two pointers** inside its merge step. A Dynamic Programming
subarray-sum problem uses a **prefix-sum** preprocessing. Greedy
interval scheduling uses **merge intervals** to count overlaps.

Most "clever" algorithmic solutions in interviews and competitive
programming are some combination of 2–3 of the twelve techniques below.
Master them and the unknown problem starts to feel like the known ones.

---

## The Twelve Techniques

| # | Technique                 | When you reach for it                                |
|---|---------------------------|------------------------------------------------------|
| 1  | **Two Pointers**         | Sorted arrays, pair-finding, in-place partitioning.  |
| 2  | **Sliding Window**       | Contiguous subarray / substring problems.            |
| 3  | **Prefix Sum**           | Fast range sums on an immutable array.               |
| 4  | **Difference Array**     | Fast range updates.                                  |
| 5  | **Binary Search on Answer** | Minimize / maximize over a monotonic predicate.   |
| 6  | **Fast & Slow Pointers** | Cycle detection and middle-finding on sequences.     |
| 7  | **Hashing**              | Turn O(n²) search into O(n) lookup.                  |
| 8  | **Frequency Counting**   | Count occurrences, find majorities, compare multisets. |
| 9  | **Monotonic Stack**      | Next-greater / next-smaller element problems.        |
| 10 | **Meet in the Middle**   | Split an exponential search in half.                 |
| 11 | **Bit Manipulation**     | Subsets, parity, set operations on small ints.       |
| 12 | **Merge Intervals**      | Overlap and scheduling problems.                     |

---

## Technique vs Paradigm — Read This Once

This is the most common source of confusion. Commit it to memory:

| Paradigm            | Technique                              |
|---------------------|----------------------------------------|
| **A strategy.**     | **A move inside a strategy.**          |
| "We will solve this with Divide & Conquer." | "…and inside the merge step we'll use two pointers." |
| Broad, architectural.| Narrow, tactical.                      |

Paradigms answer "*how do we approach this problem?*" Techniques answer
"*how do we make this step efficient?*"

---

## How Techniques Relate to Each Other

Techniques are not disjoint. Several of them share machinery:

- **Two Pointers** is the skeleton of **Sliding Window** — a sliding
  window is just two pointers where one always stays behind the other.
- **Fast & Slow Pointers** is also a two-pointer pattern, specialized to
  detect cycles by speed difference.
- **Prefix Sum** and **Difference Array** are duals of each other:
  prefix sum is for *queries*, difference array is for *updates*.
- **Hashing** and **Frequency Counting** both use dicts/sets; the
  distinction is whether you're tracking "seen X?" or "how many of X?"
- **Meet in the Middle** is a generalized divide-and-conquer trick —
  helpful when n is small enough that 2^(n/2) is feasible but 2^n isn't.

Recognizing these relationships lets you use one technique to compose
another.

---

## How to Work Through This Section

Two reasonable orders:

**Sequential (recommended for first pass):** go 01 → 12. Earlier
techniques keep appearing in later ones — knowing Two Pointers first
makes Sliding Window read like a specialization.

**By frequency (after first pass):** most interview problems hit the
first five techniques (Two Pointers, Sliding Window, Prefix Sum, Binary
Search on Answer, Hashing). Master those; the rest as needed.

---

## Folder Shape

Every module follows the same pattern:

```
NN-Technique-Name/
├── theory.md            ← what it is, when to reach for it
├── template.py          ← the reusable skeleton
└── problems/            ← worked examples, each runnable with tests
    └── …
```

A few modules have variations where they split the template or add
extra files (e.g., Sliding Window splits into `fixed-window.py` and
`variable-window.py`; Bit Manipulation has a dedicated `bit-operations.py`
reference). Those splits reflect the technique's natural structure.

---

## Outcome

By the end of this section you should be able to:

- Look at a new problem and within a minute recognize which 1–2
  techniques apply.
- Pull the matching `template.py` from memory and adapt it — rather
  than rebuilding the pattern from scratch every time.
- Compose techniques: a problem might need Prefix Sum + Hashing, or
  Two Pointers + Binary Search on Answer.

That is the difference between "I've seen this problem before" and
**"I recognize the machinery"**.
