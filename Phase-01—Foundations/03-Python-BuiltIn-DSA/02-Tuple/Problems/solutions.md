# 🧠 Solutions Explanation – Easy Problems (Tuple)

This file explains the logic behind each easy problem step-by-step,
with a focus on the tuple-specific ideas the problem is teaching.

---

# ✅ Problem 01 – Swap Two Values Using a Tuple

## 🔹 Problem Recap

Given two values `a` and `b`, return them swapped as `(b, a)`.

Example:
a = 1, b = 2

Output:
(2, 1)

---

## 🔹 Approach 1 – Return a New Tuple

Just construct `(b, a)` directly.

Time Complexity: O(1)  
Space Complexity: O(1)

---

## 🔹 Approach 2 – Pythonic Tuple Swap (Most Important)

```python
a, b = b, a
```

### Step-by-step logic:

1. The right-hand side `b, a` first builds a temporary tuple `(b, a)`.
2. Python then **unpacks** that tuple into the two names on the left.
3. No explicit temp variable is needed — the tuple IS the temp.

This is the idiomatic Python way to swap. Most other languages require
a `temp` variable; Python's tuple packing/unpacking makes it a one-liner.

---

## 🔹 Approach 3 – Temp Variable (Classical)

Shown only for contrast. Works, but verbose compared to the tuple swap.

---

## 🔹 Why This Problem Is Important

This problem teaches:

- **Packing** multiple values into a tuple
- **Unpacking** a tuple into named variables
- The Pythonic swap idiom — shows up in sorting, two-pointer problems,
  and anywhere you need to exchange two values

---

# ✅ Problem 02 – Find the Pair with the Maximum Sum

## 🔹 Problem Recap

Given a list of `(a, b)` tuples, return the pair with the largest sum.

Example:
[(1, 2), (3, 4), (5, 1), (2, 8)]

Output:
(2, 8)     # 2 + 8 = 10

---

## 🔹 Why Tuples Here?

Each pair is a **fixed record** of exactly two values. That is the
textbook use case for a tuple:
- Ordered
- Fixed size
- Immutable — nobody downstream can accidentally lengthen a "pair"

Using tuples also makes iteration cleaner:
```python
for a, b in pairs:
    ...
```
Unpacking directly in the `for` clause gives each field a name.

---

## 🔹 Approach 1 – `max()` with a Key Function

```python
max(pairs, key=sum)
```

Python's `max()` accepts a `key` function. We pass `sum`, which,
when called on a tuple, returns `a + b`. The tuple with the largest
key wins.

Time Complexity: O(n)  
Space Complexity: O(1)

---

## 🔹 Approach 2 – Manual Traversal (Interview Friendly)

### Step-by-step logic:

1. Assume the first pair is the best so far.
2. Walk through the remaining pairs, unpacking each as `a, b`.
3. If `a + b` beats the running best, update.
4. Return the best pair.

This is the version to write in an interview — it shows you understand
the algorithm, not just the library.

---

## 🔹 Approach 3 – Sort by Sum, Pick the Last

```python
sorted(pairs, key=sum)[-1]
```

Clean, but O(n log n) — strictly worse than the one-pass solutions.
Included to highlight the tradeoff: sometimes the "elegant" version
does more work than it needs to.

---

## 🔹 Key Takeaway

For a single "maximum by some criterion" question, one pass in O(n)
is always enough. Reach for `max(..., key=...)` first; fall back to
a manual loop if the criterion is complex.

---

# ✅ Problem 03 – Count Unique Coordinates

## 🔹 Problem Recap

Given a list of `(x, y)` coordinate tuples (possibly with duplicates):
1. Count how many are unique.
2. Return the unique ones in order of first appearance.

Example:
[(1, 2), (3, 4), (1, 2), (5, 6), (3, 4)]

Output:
unique_count = 3
unique_points = [(1, 2), (3, 4), (5, 6)]

---

## 🔹 Why This Problem Exists

This is the headline feature of tuples:

> **Tuples are hashable (if their elements are).**

That single property lets them live inside sets and act as dict keys.
Lists **cannot** do this — a list inside a set raises `TypeError`.

This problem could not be solved as cleanly with lists-of-lists. The
choice of tuple here is not stylistic; it's what makes `set()` and
`dict` lookups legal in the first place.

---

## 🔹 Approach 1 – `set()`

```python
len(set(points))
```

Drop the whole list into a set. Duplicates disappear automatically.

Time Complexity: O(n) average  
Space Complexity: O(n)

Downside: sets are unordered, so this answers the *count* question
but loses the order of first appearance.

---

## 🔹 Approach 2 – Preserve First-Appearance Order

### Step-by-step logic:

1. Keep a `seen` set for O(1) lookups.
2. Keep a `result` list for order.
3. For each point:
   - If it's NOT in `seen`, add it to both.
   - If it IS in `seen`, skip it.
4. Return `result`.

This is the standard "dedupe while preserving order" pattern in Python.

Time Complexity: O(n)  
Space Complexity: O(n)

---

## 🔹 Approach 3 – Count Occurrences

Use a dict: `{ point: how_many_times_it_appeared }`.

Again, only possible because tuples are valid dict keys.

Time Complexity: O(n)  
Space Complexity: O(n)

---

## 🔹 Why This Would Fail With Lists

```python
set([[1, 2], [3, 4]])   # TypeError: unhashable type: 'list'
{ [1, 2]: "origin" }    # TypeError: unhashable type: 'list'
```

Whenever you need a small fixed record as a set element or dict key,
reach for a tuple.

---

# 🔥 Key Interview Takeaway

Tuples are not "lists with parentheses." They solve a different problem:

| Use a list when...                     | Use a tuple when...                         |
|----------------------------------------|---------------------------------------------|
| The collection will grow or shrink     | The record has a fixed shape                |
| Elements are homogeneous (all ints)    | Elements are a heterogeneous record         |
| You don't need it as a dict key        | You DO need it as a dict key / set member   |
| You plan to sort / reverse in place    | The data should never change after creation |

Picking the right one makes your code clearer AND unlocks data
structures (sets / dict keys) that lists can't participate in.

---

# 🎯 Practice Questions

1. Swap three values in a cycle: `(a, b, c) -> (c, a, b)`.
2. Given a list of `(name, score)` tuples, return the name with the
   highest score.
3. Given a list of `(x, y)` points, return the point closest to the origin.
4. Given a list of `(city, country)` tuples, group them into a dict
   mapping country -> list of cities.
5. Count how many times each `(word, length)` pair appears in a text.
