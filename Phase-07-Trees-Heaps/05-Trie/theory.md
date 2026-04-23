# Trie — Theory

A **trie** (pronounced "try", from reTRIEval) is a tree keyed by
STRING PREFIXES. Every path from root to a marked node spells out one
stored word. Shared prefixes share tree branches, which makes the
trie extremely space-efficient for dictionary-like workloads.

```
Insert: "car", "cat", "cart", "cat", "dog"

        (root)
        /    \
       c      d
       |      |
       a      o
      / \     |
     r   t    g ✓
    /|   ✓
   t ✓
   ✓
```

(A `✓` marks the END of a stored word.)

---

## The structure — a node has two things

Each trie node stores:

1. **children**: a map from character → child node.
2. **is_end**: a bool indicating "a word ends here".

That's it. Values aren't stored — the SEQUENCE OF EDGES down to the
`is_end` flag IS the word.

```python
class TrieNode:
    children: dict[str, TrieNode]
    is_end: bool
```

A fixed-size array (e.g. `children = [None] * 26` for lowercase English)
is the alternative. It's faster but wastes memory for sparse character
sets (Unicode, domain names, etc.). Use a dict for general keys; use
an array for hot-path ASCII workloads.

---

## Core operations

| Operation         | What it does                                      | Time                    |
|-------------------|---------------------------------------------------|-------------------------|
| `insert(word)`    | Walk down, creating nodes as needed; mark `is_end`. | O(L), L = word length |
| `search(word)`    | Walk down; return true iff we land on `is_end`.     | O(L)                    |
| `starts_with(p)`  | Walk down; return true iff the path existed.        | O(L)                    |
| `delete(word)`    | Unmark `is_end`; optionally prune dead branches.    | O(L)                    |

All four are O(L), independent of how many words are stored. Compare
to a hash set: `"abc" in set` is O(L) too (to hash + compare the key),
so a trie's theoretical search is no faster. The trie's REAL
advantages are:

- **`starts_with`** (prefix match) in O(L) — a hash set can't do this.
- **Space sharing**: `"car"`, `"card"`, `"cargo"` share 3 chars of
  storage.
- **Enumerate words with prefix** in O(k + output size) — crucial for
  autocomplete.
- **Iterate in sorted order** — if children are ordered (sorted dict
  or 26-slot array), a pre-order DFS yields the stored words sorted.

---

## Where tries beat hashing

The two killer use-cases:

### 1. Prefix queries
"Does any stored word start with `"app"`?" is O(L) for a trie,
O(n · L) for a hash set (scan everything).

### 2. Words matching a pattern
"Find all words matching `"c_t"` (one wildcard)." A trie's tree
structure lets you fork the search at the wildcard. A hash set
has no structure to fork on.

Both come up in:

- **Autocomplete / typeahead** — every modern search box.
- **Spell-check / suggest** — Levenshtein-constrained DFS on a trie.
- **IP-routing tables** — longest-prefix match on bit-level tries
  (radix tries).
- **Word-search puzzles** — LC #212 (see `problems/word-search-ii.py`).
- **Boggle / Scrabble validators** — check many candidate words
  against one big dictionary.

---

## Space complexity

Worst case: O(Σ |words|) — one node per character. In practice, the
sharing is dramatic on natural-language dictionaries (many common
prefixes), and tries outperform hash sets on space for the typical
English-dictionary workload. For random strings, no sharing → no
advantage.

**Radix tree / patricia trie**: a compressed trie where edges with no
branches are MERGED into a single edge labelled with a string. This
collapses long uni-branch chains into single edges. Same Big-O; much
better constants on sparse data. Used in routing tables, Rust's
`BTreeMap` alternatives, and Linux kernel.

---

## Trie vs hash set vs sorted list

| Operation                     | Hash set | Sorted list (bisect) | Trie       |
|-------------------------------|----------|----------------------|------------|
| `insert("abc")`               | O(L)     | O(n)                 | O(L)       |
| `search("abc")`               | O(L)     | O(L log n)           | O(L)       |
| `starts_with("ab")`           | **O(n·L)** | O(L log n) + binary-search scan | **O(L)** |
| `all_with_prefix("ab")`       | O(n·L)   | O(L log n + k)       | O(L + k)   |
| Enumerate sorted              | O(n log n) | O(n)               | O(n)       |
| Memory (English dictionary)   | worse    | worse                | best       |

For "do I have this word?" alone, a hash set wins on constants. The
moment prefix queries enter, a trie is uniquely positioned.

---

## What's in this module

- [implementation.py](implementation.py) — `Trie` class (insert / search / starts_with / delete).
- [problems/insert-search.py](problems/insert-search.py) — LC #208, the minimum-viable trie.
- [problems/word-break.py](problems/word-break.py) — LC #139, DP + trie lookup.
- [problems/word-search-ii.py](problems/word-search-ii.py) — LC #212, trie-guided DFS on a board.
- [problems/autocomplete.py](problems/autocomplete.py) — LC #642 style, top-k suggestions from prefix.
