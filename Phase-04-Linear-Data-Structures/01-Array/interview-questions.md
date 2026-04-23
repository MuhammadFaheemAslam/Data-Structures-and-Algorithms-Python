# Array — Interview Questions

A cheatsheet of the conceptual questions that come up alongside the
coding problems. If you can answer every question below confidently,
you're ready for any array-focused interview.

---

## 🧠 Conceptual Questions

### 1. What is the difference between a static and a dynamic array?

**Static:** fixed capacity at creation. Can't grow or shrink. Typically
allocated as a contiguous block of raw memory (C's `int arr[100]`).

**Dynamic:** grows automatically on append by allocating a new larger
block and copying. Python's `list`, C++'s `vector`, Java's `ArrayList`.

Both give O(1) random access. Dynamic trades a small memory overhead
(unused capacity) for the convenience of amortized-O(1) appending.

---

### 2. Why is append O(1) amortized instead of O(n)?

Because dynamic arrays grow by a CONSTANT FACTOR (typically 2× or
1.5×). When the array fills, we allocate `2n` slots and copy — that's
O(n). But we've "earned" n O(1) appends before the next resize.

Amortized over any sequence of n appends:

- n "cheap" appends = O(n) total work
- Resizes: 1 + 2 + 4 + 8 + … + n = O(n) total work
- Total: O(n) for n operations = **O(1) per op on average**.

The geometric series is the magic. Linear growth (resize by adding
a constant) would give O(n²) amortized — much worse.

---

### 3. Why is insert(0, x) O(n)?

Inserting at the FRONT shifts every existing element one slot to the
right to make room. That's n − 1 writes = O(n).

Inserting in the MIDDLE is the same pattern: everything AFTER the
insertion point must shift right. So `insert(i, x)` is O(n − i).

If you need fast front-inserts, use `collections.deque` (O(1) at
both ends) — not `list`.

---

### 4. How does Python's `list` compare to C++'s `vector` and Java's `ArrayList`?

All three are dynamic arrays. Differences:

| Property           | Python `list`           | C++ `vector`    | Java `ArrayList`   |
|--------------------|-------------------------|-----------------|--------------------|
| Stores             | references (`PyObject*`) | values or ptrs | references         |
| Growth factor      | ~1.125×                 | typically 2×    | 1.5×               |
| Memory layout      | array of pointers       | array of values | array of pointers  |
| Cache efficiency   | Moderate                | **Excellent**   | Moderate           |

C++ `vector<int>` stores 32-bit ints BACK-TO-BACK. Python `list[int]`
stores pointers back-to-back; the actual ints live elsewhere. That's
why NumPy arrays (which DO store values contiguously) are so much
faster than lists for numeric work.

---

### 5. When should I NOT use a list?

- **Many prepends / pop-fronts.** → `collections.deque`
- **Key → value lookups.** → `dict`
- **Membership tests.** → `set`
- **Maintain sorted order on insert.** → `sortedcontainers.SortedList`
- **Large numeric arrays.** → `numpy.ndarray`
- **Fixed-size, tight memory.** → `array.array`

---

### 6. Is it safe to modify a list while iterating over it?

**Generally no.** Results are undefined. Examples of bugs:

```python
nums = [1, 2, 3, 4]
for x in nums:
    if x == 2:
        nums.remove(x)    # DANGER
```

Python's iterator walks the list by index; removing an element shifts
later elements left, so the iterator skips one.

**Safe alternatives:**

- Iterate a COPY: `for x in nums[:]: ...`
- Build a new list via comprehension: `nums = [x for x in nums if x != 2]`
- Walk by index DOWNWARD: `for i in range(len(nums) - 1, -1, -1): ...`

---

### 7. What's the complexity of `arr[i:j]`?

**O(j − i)** — it allocates a new list and copies the references.

Slicing is not free. If you're repeatedly slicing in a hot loop,
use indexing instead or preallocate.

---

### 8. What's the difference between `arr.sort()` and `sorted(arr)`?

| Call           | In place | Returns               |
|----------------|----------|------------------------|
| `arr.sort()`   | Yes      | `None`                |
| `sorted(arr)`  | No       | a NEW sorted list     |

Both are O(n log n) using Timsort. `sorted` works on any iterable
(generators, sets, dict views); `arr.sort()` only works on lists.

Pick `sort` when you don't need the original; `sorted` otherwise.

---

### 9. How does `arr.copy()` differ from `arr[:]`?

Both produce a SHALLOW copy — same Big-O, same result. `arr.copy()`
is more explicit; `arr[:]` is older Python idiom. Use whichever fits
your team's style.

For a DEEP copy (when the list contains nested mutable objects),
use `copy.deepcopy(arr)`.

---

## 💼 Common Coding Questions

All of these have implementations in `problems/` or in earlier phases —
cross-references below.

### Easy

- **Find max / min** — `problems/easy/01-max-min.py`
- **Reverse in place** — `problems/easy/02-reverse.py`
- **Contains duplicate** — Phase-02 / 02 / 07-Hashing-Technique
- **Two Sum (unsorted)** — Phase-02 / 02 / 07-Hashing-Technique
- **Move zeros to end** — two-pointer swap (in-place variant of reverse)
- **Remove duplicates from sorted array** — Phase-02 / 02 / 01-Two-Pointers

### Medium

- **Rotate array** — `problems/medium/01-rotate.py`
- **Maximum subarray (Kadane)** — `problems/medium/02-subarray-sum.py`
- **Subarray sum equals K** — Phase-02 / 02 / 03-Prefix-Sum
- **Product of array except self** — two passes, prefix + suffix
- **3Sum** — Phase-02 / 02 / 01-Two-Pointers
- **Container with most water** — Phase-02 / 02 / 01-Two-Pointers
- **Sort colors (Dutch National Flag)** — Phase-03 / 02 / 02-Quick-Sort
- **Find duplicate number** — Phase-02 / 02 / 06-Fast-Slow-Pointers
- **Majority element (Boyer-Moore)** — Phase-02 / 02 / 08-Frequency-Counting
- **Longest consecutive sequence** — use a set, walk each "start"

### Hard

- **Median of two sorted arrays** — `problems/hard/01-median-two-arrays.py`
- **Trapping rain water** — two-pointer or monotonic stack
  (Phase-02 / 02 / 09-Monotonic-Stack)
- **First missing positive** — hash set O(n) or in-place O(n)
- **Largest rectangle in histogram** — Phase-02 / 02 / 09-Monotonic-Stack
- **Maximal rectangle** — DP + histogram on each row

---

## 🎯 Things to Ask Before Answering

Before diving into any array problem, these clarifications save you
from producing the wrong answer:

1. **Can the array contain duplicates?** Often changes the approach.
2. **Is it sorted?** Enables binary search, two pointers, merge.
3. **Are values bounded?** Opens up counting sort, radix, bitmask.
4. **Do I need in-place / O(1) extra space?** Rules out some techniques.
5. **Can the array have negatives / zeros?** Affects product / sum tricks.
6. **What's the expected size?** n = 100 vs n = 10⁶ → wildly different choices.
7. **Is the array immutable?** Affects whether you can sort or swap in place.

---

## 🧠 Mental Models Worth Keeping

### "Scan once with running state"

Kadane's, best-stock-to-buy, Boyer-Moore, longest streak of 1s — all
share the pattern:
```
state = initial
for x in arr:
    state = update(state, x)
    best  = max(best, state)
```

### "Two pointers converging or same-direction"

Reverse, palindrome, Two Sum on sorted, container with most water,
remove duplicates, sort colors.

### "Prefix / suffix arrays"

Range sum queries (Phase-02 / 02 / 03), product-except-self,
trapping rain water (with two-pointer variant).

### "Sort, then exploit the order"

Most "seemingly hard" array problems become easy after sorting:
Three Sum, merge intervals, bucket-based optimizations, median-of-medians.

### "Hash map to turn O(n²) into O(n)"

Two Sum, subarray sum K, contains duplicate, longest consecutive.
Whenever you see a nested loop doing the same check repeatedly,
consider replacing the inner loop with a dict lookup.

---

## ⚡ Speed Round: One-Line Answers

- **Reverse in place?** → two-pointer swap.
- **Rotate by k?** → three reverses.
- **Max subarray?** → Kadane (`current = max(x, current + x)`).
- **Find duplicate in [1..n]?** → Floyd's (treat array as cycle).
- **Two Sum unsorted?** → hash map of `value → index`.
- **Two Sum sorted?** → two pointers.
- **Contains duplicate?** → `len(set(arr)) != len(arr)`.
- **Median of stream?** → two heaps (Phase 07 territory).
- **Kth largest?** → heap of size k, or quickselect.
- **Merge intervals?** → sort by start, sweep.

---

## Next Up

You're done with Array. Next is **02-String** — essentially a specialized
array of characters with a few quirks (immutability, Python-specific
APIs). Many of the patterns you learned here (two-pointer, sliding
window, prefix sum) carry over directly.
