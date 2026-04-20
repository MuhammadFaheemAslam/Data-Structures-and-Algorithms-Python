# 🧠 Solutions Explanation – Easy Problems (Set)

This file explains the logic behind each easy problem step‑by‑step,
with a focus on the set‑specific ideas the problem is teaching.

All three problems share the same headline lesson:

> **Any time you reach for "does X exist in this collection?",
> reach for a set first.** It turns O(n) lookups into O(1) and
> O(n²) brute force into O(n).

---

# ✅ Problem 01 – Remove Duplicates from a List

## 🔹 Problem Recap

Given a list, return a new list with duplicates removed.

Example:
```
Input:  [1, 2, 2, 3, 1, 4, 3, 5]
Output: [1, 2, 3, 4, 5]
```

---

## 🔹 Approach 1 – `set()` (Shortest, Order Lost)

```python
list(set(items))
```

Drop the list into a set. Duplicates vanish because a set only
holds unique elements.

Time Complexity: O(n)  
Space Complexity: O(n)

Downside: the order of elements in the output is **not guaranteed**.

---

## 🔹 Approach 2 – `seen` Set + Output List (Interview Friendly)

### Step‑by‑step logic:

1. Keep a `seen` set for O(1) membership lookups.
2. Keep a `result` list for the output order.
3. For each item:
   - If it's **not in** `seen`, add it to both `seen` and `result`.
   - If it **is in** `seen`, skip it.
4. Return `result`.

Time Complexity: O(n)  
Space Complexity: O(n)

This is the standard "dedupe while preserving first-appearance
order" pattern in Python. Same Big‑O as Approach 1, but preserves order.

---

## 🔹 Approach 3 – `dict.fromkeys()` (Cleanest One-Liner)

```python
list(dict.fromkeys(items))
```

Since Python 3.7, dicts preserve insertion order. Building a dict
from a list uses each item as a key — duplicates are dropped,
order is preserved.

Time Complexity: O(n)  
Space Complexity: O(n)

---

## 🔹 Approach 4 – Brute Force (Anti-Pattern)

```python
for item in items:
    if item not in result:     # O(n) linear scan of the list
        result.append(item)
```

Looks similar to Approach 2, but `x not in list` is **O(n)** instead of
O(1). That turns the whole thing into **O(n²)**.

This is the single most common "accidentally quadratic" bug in
real-world Python code.

---

## 🔹 Key Takeaway

`seen_set.add(x)` and `x in seen_set` are the two most useful
one-liners in all of Python. They turn membership checks from
O(n) into O(1), and they show up in almost every efficient
algorithm below the name "hash set".

---

# ✅ Problem 02 – Intersection and Union of Two Lists

## 🔹 Problem Recap

Given two lists, return:
- Their **intersection** — elements in both (unique)
- Their **union** — elements in either (unique)

Example:
```
a = [1, 2, 2, 3, 4]
b = [3, 4, 4, 5, 6]

intersection = [3, 4]
union        = [1, 2, 3, 4, 5, 6]
```

---

## 🔹 Approach 1 – Set Operators `&` and `|`

```python
intersection = set(a) & set(b)
union        = set(a) | set(b)
```

### Why this is the right answer

Sets support the mathematical operations directly. Python does
all the work in C, in one pass, and handles de-duplication
automatically.

Time Complexity:
- Intersection: O(n + m) to build the sets, then **O(min(n, m))** for
  the intersection itself.
- Union: O(n + m).

Space Complexity: O(n + m) for the two sets plus the result.

---

## 🔹 Approach 2 – Method Forms (Accept Any Iterable)

```python
set(a).intersection(b)   # `b` can be a list, tuple, generator, …
set(a).union(b)
```

The method form is strictly more flexible than the operator form.

The operator form requires **both** sides to be sets:
```python
set(a) & [3, 4]          # TypeError
```

Use whichever reads best. If you often work with iterables that
might not be sets yet, the method form saves a `set(...)` call.

---

## 🔹 Approach 3 – Brute Force (Anti-Pattern)

```python
for x in a:
    if x in b and x not in result:
        result.append(x)
```

Both `in b` and `in result` are O(n) linear scans of lists.
The whole function becomes **O(n · m)**.

On lists of a few thousand elements the difference is already
dramatic — the set-based version is orders of magnitude faster.

---

## 🔹 Key Insight – Intersection is O(min(n, m))

Python's set intersection **iterates the smaller set** and checks
membership in the larger one. That's why intersecting a 10-element
set with a 10-million-element set runs in milliseconds.

Mental model:
> For any "what do these two collections share?" question,
> convert both to sets and use `&`.

---

# ✅ Problem 03 – Detect if a List Contains Any Duplicate

## 🔹 Problem Recap

Return `True` if any value appears at least twice in the list;
otherwise `False`.

Example:
```
[1, 2, 3, 1] -> True
[1, 2, 3, 4] -> False
```

---

## 🔹 Approach 1 – Compare Lengths with a Set (Shortest)

```python
len(nums) != len(set(nums))
```

If the set's length differs from the list's, some elements were
absorbed as duplicates.

Time Complexity: O(n)  
Space Complexity: O(n)

Downside: always builds the full set. If the first two elements
are duplicates, it still hashes the remaining n − 2 elements.

---

## 🔹 Approach 2 – Early-Exit Traversal (Interview Friendly)

### Step‑by‑step logic:

1. Start with an empty `seen` set.
2. For each element:
   - If it's already in `seen`, return `True` immediately.
   - Otherwise add it to `seen`.
3. If the loop finishes without hitting that branch, return `False`.

Time Complexity: O(n) worst case, early exit on "duplicate near the
start" inputs.  
Space Complexity: O(n) worst case.

This is the interview version. Same big‑O as Approach 1, but with a
meaningful constant-factor speedup on realistic inputs. It also
generalizes — the same pattern is the inner loop of Two Sum,
Happy Number, and Contains Duplicate II.

---

## 🔹 Approach 3 – Brute Force (Anti-Pattern)

Two nested loops → **O(n²)**.

For `n = 10_000`:
- Brute force:  ~50,000,000 comparisons
- Set version:  ~10,000 hash operations

The difference is the whole point of this problem.

---

## 🔹 Approach 4 – Sort, Then Check Adjacent Pairs

```python
for i in range(1, len(sorted_nums)):
    if sorted_nums[i] == sorted_nums[i - 1]:
        return True
```

Time Complexity: O(n log n) — dominated by sorting.  
Space Complexity: O(n) — `sorted()` returns a new list.

Worse than the set versions, but useful when:
- The elements aren't hashable but are comparable.
- You're already going to sort anyway (e.g., merging a file).

---

## 🔹 The Set Pattern to Remember

```python
seen = set()
for x in iterable:
    if x in seen:
        ...     # duplicate logic
    seen.add(x)
```

This five-line pattern, with minor variations, solves:

- "Does the collection contain duplicates?"         (this problem)
- "Find the first duplicate."                       (early exit on hit)
- "Find a pair that sums to k."                     (store `k - x` in `seen`)
- "Find the longest substring without repeats."     (set + sliding window)
- "Is there a cycle in this linked list?"           (set of visited nodes)
- "Does any permutation of X equal Y?"              (`set(X) == set(Y)`)

Once you have this pattern in your hands, a whole class of
problems collapses from O(n²) to O(n).

---

# 🔥 Key Interview Takeaway

Across all three problems the win is the same:

| Question                             | List approach | Set approach |
|--------------------------------------|---------------|--------------|
| "Have I seen X before?"              | O(n)          | **O(1) avg** |
| "Remove duplicates from a list"      | O(n²)         | **O(n)**     |
| "What do two collections share?"     | O(n·m)        | **O(n + m)** |
| "Does this list contain a duplicate?"| O(n²)         | **O(n)**     |

A set is not "a list without duplicates." It is a different
data structure with a different purpose: **constant-time
presence testing.** The moment your problem has the word
"unique", "seen", "shared", "contains", or "duplicate" in
it, you should be reaching for a set.

---

# 🎯 Practice Questions

1. Given two strings, check if one is a permutation of the other.
2. Find the first non-repeating character in a string.
3. Given a list of emails, return the unique domains (`@example.com`).
4. Given a list of integers, find the longest streak of consecutive
   numbers (e.g., `[100, 4, 200, 1, 3, 2]` → 4 for `[1, 2, 3, 4]`).
5. Given two lists, return elements that appear in exactly one of
   them (symmetric difference).
