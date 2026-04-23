# Array — Theory

## Introduction

The **array** is the foundational data structure. Every other structure
in this phase either stores its elements in an array (strings, stacks,
queues with array backing) or was designed specifically to AVOID using
one (linked lists).

An array is:

> *A contiguous block of memory that holds n elements of the same
> (logical) size, accessed by integer index.*

Two words matter: **contiguous** (no gaps between slots) and **same
size** (so the address of slot `i` is `base + i * size`). Those two
properties give arrays their defining feature: **O(1) random access**.

---

## Static vs Dynamic Arrays

Arrays come in two flavours, differing in whether their size can change:

### Static Arrays

- **Fixed capacity** set at creation time.
- Can't grow. Can't shrink. Trying either requires allocating a new array.
- Languages that expose raw memory (C, C++) have these natively.
- Python has them via the `array` module or `numpy`, but you rarely
  use them directly.

### Dynamic Arrays (Python's `list`)

- **Grow as needed.** When capacity is exceeded, allocate a new
  larger block (usually ~2x), copy everything over, and free the old one.
- Internally have two sizes:
    - `size` — the number of elements actually stored.
    - `capacity` — the allocated block's size (≥ size).
- When `size < capacity`, append is O(1). When `size == capacity`,
  the next append triggers a resize (O(n)). But resizes happen
  infrequently enough that the **amortized** cost of append is O(1).

Python's built-in `list` is a dynamic array. So is `std::vector` in
C++, `ArrayList` in Java, `Vec` in Rust. They all use the
"over-allocate and occasionally resize" strategy.

---

## Time Complexity (The Table to Memorize)

| Operation                | Static Array | Dynamic Array         |
|--------------------------|--------------|------------------------|
| **Index access** `a[i]`  | O(1)         | O(1)                   |
| **Assign** `a[i] = x`    | O(1)         | O(1)                   |
| **Length** `len(a)`      | O(1)         | O(1)                   |
| **Append**               | n/a (fixed)  | **O(1) amortized**     |
| **Prepend** (insert at 0)| n/a          | O(n) (shift everything)|
| **Insert at index i**    | n/a          | O(n - i)               |
| **Delete from end** `pop()` | n/a       | O(1)                   |
| **Delete from start** `pop(0)` | n/a    | O(n)                   |
| **Delete at index i**    | n/a          | O(n - i)               |
| **Search (unsorted)** `x in a` | O(n)   | O(n)                   |
| **Search (sorted)**      | O(log n)     | O(log n) with `bisect` |
| **Concatenation** `a + b`| n/a          | O(n + m)               |
| **Slicing** `a[i:j]`     | O(k)         | O(k) where k = j - i   |
| **Iteration**            | O(n)         | O(n)                   |

**Key insights:**

- **The ends are cheap, the middle is expensive.** Dynamic arrays
  love `append` and `pop` (from the end). They hate `insert(0, x)`
  and `pop(0)` — those force an O(n) shift of all the later elements.
- **Random access is free.** Any arr[i] is one pointer arithmetic
  op plus one memory load. That's why sorting problems can afford
  their O(n log n) bound — the per-element work is O(1).

---

## Amortized Analysis (Why Append is "Amortized O(1)")

Individual appends to a dynamic array sometimes cost O(n) (when they
trigger a resize) and sometimes O(1) (when they don't). How do we
give the operation a single cost?

Suppose the array doubles whenever it fills up. Starting from capacity
1, after n appends:

    Regular ops:      n - (number of doublings)
    Resize ops:       1 + 2 + 4 + 8 + ... + capacity_just_before_n
                    = 2·n - 1
                    = O(n)

Total work: O(n) across n appends → **O(1) per append on average**.

The resizes get exponentially more expensive but exponentially less
frequent. They exactly balance each other.

This is why you don't need to worry about `list.append()` in real Python
code — it's O(1) amortized, full stop.

---

## Memory Layout and Cache Behaviour

Arrays are **the cache's best friend**. When you access `a[0]`, the CPU
loads not just `a[0]` but a chunk of adjacent memory (a "cache line",
typically 64 bytes, holding ~16 int pointers or 8 doubles). Subsequent
accesses to `a[1]`, `a[2]`, ... are almost free — they hit the cache.

This is why arrays are often **10× faster than linked lists in practice**,
despite the same O(n) traversal cost on paper. Linked lists scatter their
nodes across memory; every hop is a cache miss.

Two consequences:

1. **Prefer arrays to linked lists when you can.** The O(1) middle-insert
   of a linked list is rarely worth the cache penalty.
2. **Locality matters for algorithm choice.** Why merge sort on an
   array runs faster than on a linked list of the same length: the
   array version accesses memory sequentially.

---

## Common Array Operations in Python

```python
# Creation
arr = [1, 2, 3]                     # literal
arr = list(range(10))               # from iterable
arr = [0] * 100                     # pre-allocated with 100 zeros

# Access and modification
arr[0]                              # first element
arr[-1]                             # last element
arr[2] = 10                         # assignment
len(arr)                            # length

# Adding elements
arr.append(4)                       # O(1) amortized — END
arr.extend([5, 6, 7])               # O(k) — append many
arr.insert(0, 0)                    # O(n) — prepend (SLOW, use deque)
arr.insert(2, 99)                   # O(n - 2) — middle insert

# Removing
arr.pop()                           # O(1) — END
arr.pop(0)                          # O(n) — START (SLOW)
arr.pop(i)                          # O(n - i)
arr.remove(value)                   # O(n) — by value
del arr[i]                          # same as pop(i)
arr.clear()                         # O(n) — empty the list

# Slicing (creates new list)
arr[i:j]                            # O(j - i)
arr[:]                              # O(n) shallow copy
arr[::-1]                           # O(n) reversed copy
arr[::2]                            # O(n/2) every other element

# Searching
3 in arr                            # O(n)
arr.index(3)                        # O(n); raises ValueError if absent
arr.count(3)                        # O(n)

# Sorting (in place, Timsort)
arr.sort()                          # O(n log n)
sorted(arr)                         # O(n log n) — returns NEW list

# Reversing
arr.reverse()                       # O(n) — in place
arr[::-1]                           # O(n) — new list

# Iteration
for x in arr: ...
for i, x in enumerate(arr): ...
```

---

## When to Use an Array

✅ **Default choice for ordered sequences.**

- You need random access by index.
- You mostly append or pop from the END.
- Your data is fixed-size or grows in bulk.
- You need fast iteration and good cache behaviour.

❌ **When an array is the wrong choice:**

- You need fast **prepend** or **pop from front** → use `collections.deque`.
- You need fast **insertion in the middle** → use a linked list.
- You need **fast membership testing** → use a `set`.
- You need **fast lookup by key** → use a `dict`.
- You need **unique elements** → use a `set`.
- You need **sorted order maintained on insert** → use `SortedList` from
  `sortedcontainers`, or a tree.

---

## The Most Important Lesson

> **"Array vs Linked List" is the first and most important data-structure
> tradeoff in all of computer science.**

The short version:

- **Array**: fast access, slow insert/delete in the middle.
- **Linked List**: slow access, fast insert/delete in the middle.

Any time you pick a linear data structure, you're picking a side of
this tradeoff. Every more-sophisticated structure (trees, heaps,
hash tables) is either:
- an array with cleverer indexing (heap, hash table), or
- a linked structure with cleverer pointers (tree, graph).

Internalize this dichotomy and the rest of data structures feels
like variations on a theme.

---

## Key Takeaways

1. **Arrays store elements contiguously.** That's what gives them
   O(1) random access.
2. **Dynamic arrays grow by doubling.** Append is O(1) amortized;
   the occasional O(n) resize averages out.
3. **The ends are cheap; the middle is expensive.** Append/pop at the
   end are O(1); prepend/pop at the start or insert/delete in the middle
   are O(n).
4. **Cache behaviour wins.** Arrays are often 10× faster than "equivalent"
   linked structures in practice due to memory locality.
5. **`list` is a dynamic array.** Python's built-in is what most
   other languages call a vector / ArrayList.

For implementations — a static array from scratch and a dynamic one
matching Python's `list` semantics — see [`implementation.py`](implementation.py)
and [`dynamic-array.py`](dynamic-array.py). For practice problems,
see [`problems/`](problems/) tiered into easy / medium / hard.
