# 🧠 Solutions Explanation – Easy Problems (Dictionary)

This file explains the logic behind each easy problem step‑by‑step,
with a focus on the dict‑specific ideas each problem is teaching.

The three problems together cover the three core dict patterns you will
reuse for the rest of your career:

1. **Counting** — `d[k] = d.get(k, 0) + 1`
2. **Complement lookup** — "has X's partner already been seen?"
3. **Grouping by signature** — `groups.setdefault(key, []).append(item)`

---

# ✅ Problem 01 – Word Frequency Count

## 🔹 Problem Recap

Given a sentence, return a dict mapping each word to how many times it
appears. Also return the most frequent word.

Example:
```
Input:  "the quick brown fox jumps over the lazy dog the"
Output: {'the': 3, 'quick': 1, 'brown': 1, 'fox': 1,
         'jumps': 1, 'over': 1, 'lazy': 1, 'dog': 1}
         most frequent = 'the'
```

---

## 🔹 Approach 1 – Manual Loop with `.get()` (Interview Friendly)

```python
counts = {}
for word in sentence.split():
    counts[word] = counts.get(word, 0) + 1
```

### Step‑by‑step logic:

1. Start with an empty dict.
2. For each word:
   - `counts.get(word, 0)` returns the current count (or 0 if new).
   - Add 1 and write it back.
3. Return `counts`.

Time Complexity: O(n)  
Space Complexity: O(k) where k = number of distinct words.

This is the single most important dict pattern in Python. Memorize it.

---

## 🔹 Approach 2 – `setdefault()`

```python
counts[word] = counts.setdefault(word, 0) + 1
```

Equivalent but slightly awkward for counting. `setdefault` is most useful
when the default is a **mutable container** — see Problem 03's grouping idiom.

---

## 🔹 Approach 3 – `collections.Counter` (One-Liner)

```python
from collections import Counter
counts = Counter(sentence.split())
```

`Counter` is a `dict` subclass built for exactly this problem. It even has
a `.most_common(n)` helper that returns the top-N `(word, count)` pairs.

If you're allowed stdlib, use `Counter`. If the problem asks you to
"implement it", use Approach 1.

---

## 🔹 Finding the Most Frequent Word

```python
max(counts, key=counts.get)
```

### How it works:

- `max(counts, ...)` iterates the dict's **keys**.
- `key=counts.get` makes `max` compare by the dict's VALUE, not by the key.
- Ties are broken by first-seen order (`max` keeps the first winner).

This "find the key with the largest value" pattern shows up constantly:
top scorer, most recent timestamp, highest-paid employee, longest string.

---

# ✅ Problem 02 – Two Sum

## 🔹 Problem Recap

Given `nums` and `target`, return indices `(i, j)` with `i < j` such that
`nums[i] + nums[j] == target`.

Example:
```
nums   = [2, 7, 11, 15]
target = 9
Output = (0, 1)    # 2 + 7 == 9
```

---

## 🔹 Approach 1 – Hash Map, Single Pass (The Answer)

```python
seen = {}                        # value -> index
for i, x in enumerate(nums):
    complement = target - x
    if complement in seen:
        return (seen[complement], i)
    seen[x] = i
```

### Step‑by‑step logic:

1. For each element `x` at index `i`:
   - Compute `complement = target - x`. This is the value we'd need to see
     to complete the pair.
   - If `complement` is already in `seen`, we found the answer — it was at
     `seen[complement]`, and `x` is at `i`.
   - Otherwise, record `seen[x] = i` so a future element can find us.
2. If the loop finishes, no pair exists.

Time Complexity: **O(n)** — one pass, O(1) dict ops.  
Space Complexity: **O(n)** — `seen` can hold up to n entries.

### Why This Is the Canonical Dict Problem

The insight is: *"I don't need to search the rest of the list for the
partner — I only need to know whether the partner has already appeared."*

A dict answers that in O(1). A list would answer it in O(n), giving
O(n²) total. This single trick shows up in:

- **Two Sum** (this problem)
- **Four Sum**, **Subarray Sum Equals K**
- **Longest Substring Without Repeating Characters**
- **First Unique Character**
- **Continuous Subarray Sum** (modular arithmetic + hash map)
- **Happy Number** (cycle detection)

Any time you find yourself thinking "for each element I need to check all
the others," ask: *can I precompute something into a dict that answers my
question in O(1)?*

---

## 🔹 Approach 2 – Brute Force

```python
for i in range(n):
    for j in range(i + 1, n):
        if nums[i] + nums[j] == target:
            return (i, j)
```

O(n²). For n = 10,000, that's ~50M comparisons vs ~10K dict ops. Do not
ship this.

---

## 🔹 Approach 3 – Sort + Two Pointers

O(n log n) if you can afford to lose the original indices (or you carry
them through explicitly). Still worse than the O(n) hash-map version for
this problem, but a useful technique for **3-Sum** and **Container With
Most Water** where sorting unlocks a simpler invariant.

---

# ✅ Problem 03 – Group Anagrams

## 🔹 Problem Recap

Given a list of strings, group the anagrams together.

Example:
```
Input:  ["eat", "tea", "tan", "ate", "nat", "bat"]
Output: [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
```

---

## 🔹 The Core Idea – Signature-Based Grouping

Two strings are anagrams iff they share the same **signature** — a
canonical form that ignores the order of characters.

We'll use a dict where:
- **Key** = the signature (same for all anagrams of a given word)
- **Value** = list of words that share that signature

The only question is: *what signature?*

---

## 🔹 Approach 1 – Sorted String as Key

```python
key = "".join(sorted(word))
groups.setdefault(key, []).append(word)
```

Two anagrams produce the same sorted string:
```
sorted("eat") == sorted("tea") == sorted("ate") == ['a', 'e', 't']
```

Time Complexity: O(n · k log k)  
Space Complexity: O(n · k)

Clean, short, works for any characters.

---

## 🔹 Approach 2 – Character-Count Tuple as Key

```python
counts = [0] * 26
for ch in word:
    counts[ord(ch) - ord("a")] += 1
key = tuple(counts)             # MUST be a tuple – lists aren't hashable
```

Counting is O(k); sorting is O(k log k). For long words this matters.

### ⚠️ Why `tuple(counts)` and not `counts`?

**Lists are not hashable.** A dict key must be hashable. If you tried
`groups[counts] = ...`, Python would raise `TypeError: unhashable type:
'list'`. Converting to a tuple makes it hashable — this is the same
reason tuples are the preferred type for record-shaped data.

Time Complexity: O(n · k)  
Space Complexity: O(n)

---

## 🔹 Approach 3 – `defaultdict(list)`

```python
from collections import defaultdict
groups = defaultdict(list)
for w in words:
    groups["".join(sorted(w))].append(w)
```

`defaultdict(list)` auto-creates an empty list the first time you access
a missing key, so you can skip the `setdefault(...)` boilerplate.

It's the most Pythonic version of this pattern — whenever you see
`setdefault(key, [])` or `setdefault(key, set())`, `defaultdict` can
replace it.

---

## 🔹 Approach 4 – Brute Force

Scan existing groups for each new word. O(n² · k log k). Mentioned only
as a reminder of what you're avoiding by using a dict.

---

## 🔹 The Grouping Pattern to Remember

```python
groups = {}
for item in items:
    key = signature(item)
    groups.setdefault(key, []).append(item)
```

Swap `signature()` for whatever collapses equivalent items:

| Problem                                           | Signature                            |
|---------------------------------------------------|--------------------------------------|
| Group anagrams                                    | sorted string / letter-count tuple   |
| Group people by birth year                        | `person.year`                        |
| Group files by extension                          | `path.rsplit(".", 1)[-1]`            |
| Group transactions by customer                    | `tx.customer_id`                     |
| Group shapes by number of sides                   | `len(shape.vertices)`                |
| Group points by quadrant                          | `(sign(x), sign(y))`                 |

Same five-line shape, different signature function.

---

# 🔥 Key Interview Takeaway

All three problems are instances of the same underlying observation:

> **A dict turns "search" into "lookup".**

| Question                                          | Without dict  | With dict      |
|---------------------------------------------------|---------------|----------------|
| "How many times does X appear?"                   | rescan each time | count[x] += 1 |
| "Has partner of X been seen?"                     | scan list — O(n) | `x in seen` — O(1) |
| "Which bucket does X belong to?"                  | scan groups   | `groups[signature(x)]` |

Whenever you see "for each element, check against all the others," the
fix is almost always: *build a dict, then look things up.*

---

# 🎯 Practice Questions

1. **First Unique Character** — given a string, return the index of the
   first character that appears exactly once (or -1).
2. **Contains Duplicate II** — given `nums` and `k`, return True if there
   exist `i ≠ j` with `nums[i] == nums[j]` and `abs(i - j) ≤ k`.
3. **Valid Anagram** — given two strings `s` and `t`, return True if `t`
   is an anagram of `s`.
4. **Subarray Sum Equals K** — count the number of contiguous subarrays
   whose sum equals `k` (prefix-sum + dict).
5. **Top K Frequent Words** — given words and an integer `k`, return the
   `k` most frequent words sorted by frequency (ties broken alphabetically).
