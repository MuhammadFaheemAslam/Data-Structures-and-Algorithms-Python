```markdown
# Python List – Theory

## Introduction

The Python `list` is one of the most versatile and frequently used built‑in data structures. 
It is an ordered, mutable collection that can hold elements of different data types. 
Lists are implemented as **dynamic arrays** under the hood, which gives them excellent performance 
for indexing and appending, but makes insertions and deletions in the middle costly.

In this document, we’ll explore how lists work, their time complexities, memory behavior, 
and best practices for using them effectively in your algorithms.

---

## Underlying Implementation

Python lists are not linked lists; they are **contiguous arrays of pointers** (in CPython, the reference implementation). 
Each element stored in a list is actually a pointer to the Python object. The array itself is allocated in a contiguous block 
of memory, which enables **O(1) random access** via indexing.

### Dynamic Resizing

When a list is created, it has a certain **capacity** (the total allocated space) and a **size** (the number of elements actually stored). 
If you append an element and the size equals the capacity, the list must resize:

1. Allocate a new, larger array (typically ~1.125× or 2× the old size, depending on the Python version).
2. Copy all existing pointers to the new array.
3. Free the old array.

This resizing operation takes **O(n)** time, but it happens infrequently. As a result, the **amortized cost** of appending is **O(1)**. 
(You already studied amortized analysis in Phase‑02.)

> **Note:** Since lists store pointers, the actual elements (especially large objects) are stored elsewhere in memory; 
the list only holds references. This means resizing a list does not move the objects themselves – only the pointer array is copied.

---

## Key Characteristics

| Property       | Description                                                               |
|----------------|---------------------------------------------------------------------------|
| **Ordered**    | Elements maintain the insertion order.                                   |
| **Mutable**    | You can change, add, or remove elements after creation.                  |
| **Heterogeneous** | Can contain elements of different types (including other lists).       |
| **Allows duplicates** | Same value can appear multiple times.                                |
| **Indexable**  | Access any element in O(1) time via `lst[i]`.                            |
| **Iterable**   | Supports iteration, comprehension, and many functional operations.       |

---

## Common Operations and Their Complexities

The following table summarises the time complexity of typical list operations. A detailed analysis with examples is available 
in [`time-complexity.md`](time-complexity.md).

| Operation                 | Time Complexity | Notes                                                                 |
|---------------------------|-----------------|-----------------------------------------------------------------------|
| Indexing (`lst[i]`)       | O(1)            | Direct access to the underlying array.                               |
| Assignment (`lst[i] = x`) | O(1)            |                                                         |
| Append (`lst.append(x)`)  | Amortized O(1)  | May trigger a resize, but averages O(1).                             |
| Pop last (`lst.pop()`)    | O(1)            | Removes the last element; no resizing (capacity may shrink in some implementations). |
| Pop intermediate (`lst.pop(i)`) | O(n)      | Shifts all subsequent elements left.                                 |
| Insert (`lst.insert(i, x)`) | O(n)         | Shifts elements right to make space.                                 |
| Delete (`del lst[i]`)     | O(n)            | Same shifting cost as pop.                                           |
| Contains (`x in lst`)     | O(n)            | Linear scan until element found.                                     |
| Slice (`lst[i:j]`)        | O(k)            | Creates a new list with k = j‑i elements; copies references.         |
| Concatenation (`lst1 + lst2`) | O(n + m)    | Creates a new list; copies both input lists.                         |
| Extend (`lst.extend(iterable)`) | O(k)      | Appends each element of iterable; may trigger resizes.               |
| Sort (`lst.sort()`)       | O(n log n)      | Uses TimSort (stable, hybrid algorithm).                             |
| Reverse (`lst.reverse()`) | O(n)            | Reverses in place.                                                   |
| Copy (`lst.copy()` or `lst[:]`) | O(n)      | Shallow copy of the list.                                            |
| Length (`len(lst)`)       | O(1)            | Size is stored as an attribute.                                      |

---

## Memory Usage

- Each list object has a small overhead (e.g., reference count, type, size, capacity).
- The underlying array stores `capacity` pointers; each pointer is 8 bytes on 64‑bit systems.
- The list itself does not account for the memory of the objects it references – those objects live elsewhere.

When elements are removed, the list’s size decreases, but the capacity usually does not shrink automatically. To free unused memory, 
you can create a slice copy (`lst = lst[:]`) or use `lst.clear()` (which frees the array in CPython).

---

## When to Use (and Not Use) Lists

✅ **Good use cases:**

- You need an ordered sequence that you will frequently access by index.
- You primarily add or remove elements **at the end** (stack behavior).
- You need a mutable, heterogeneous collection.
- You are performing operations like sorting, reversing, or iterating.

❌ **Avoid when:**

- You need frequent **insertions or deletions at arbitrary positions** – consider `collections.deque` for ends,
or a balanced tree / linked list for interior operations.
- You need **fast membership testing** – use a `set` or `dict` if order is not important.
- You are working with **large, fixed‑size homogeneous data** – consider `array.array` or NumPy arrays 
for better memory efficiency and performance.

---

## Code Example (Quick Overview)

```python
# Creating lists
empty = []
numbers = [1, 2, 3, 4]
mixed = [1, "hello", 3.14, [5, 6]]

# Indexing
print(numbers[0])      # 1
numbers[-1] = 10       # assign to last element

# Appending and extending
numbers.append(5)
numbers.extend([6, 7])

# Inserting and deleting
numbers.insert(2, 99)
popped = numbers.pop()    # removes last
del numbers[0]             # remove first

# Slicing
first_two = numbers[:2]
copy = numbers[:]

# Membership
if 3 in numbers:
    print("found")

# Sorting and reversing
numbers.sort()
numbers.reverse()
```

For a more thorough demonstration of each operation, see [`operations.py`](operations.py).

