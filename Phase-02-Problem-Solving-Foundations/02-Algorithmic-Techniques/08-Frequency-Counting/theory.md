# Frequency Counting — Theory

## Introduction

**Frequency Counting** is a specialization of hashing: track how many
times each value appears, and use those counts to answer questions.

It's separated out from generic hashing because:

1. **It has its own idioms.** `collections.Counter`, `.most_common(k)`,
   Counter arithmetic (add / subtract / intersection) — none of these
   apply to general hashing, but all show up constantly in counting
   problems.
2. **It has specialized algorithms.** Boyer-Moore Voting solves
   "majority element" in O(1) space, beating the hash-based O(n)-space
   approach on memory. Character counts with a fixed alphabet use a
   26-slot array, not a dict.
3. **It composes beautifully with other techniques.** Frequency
   counting shows up *inside* sliding window (character counts within
   the window), prefix sum (running counts), and sorting (sort by
   frequency).

Where generic hashing says "record values for later lookup", frequency
counting says:

> *"For each distinct value, how many times did it occur?"*

---

## The Four Operations

Nearly every frequency-counting problem uses a subset of these four
operations. Master the four, and the problems become fill-in-the-blank.

### 1. Build the counter

The one-pass setup. O(n) time.

```python
# Idiomatic
from collections import Counter
counts = Counter(items)

# Manual (works on older Python or without imports)
counts = {}
for x in items:
    counts[x] = counts.get(x, 0) + 1
```

### 2. Query the counts

Four useful variants:

```python
counts[x]                   # how many x's?        (dict lookup, O(1))
max(counts, key=counts.get) # the most-frequent value (O(distinct))
counts.most_common(k)       # top k by frequency    (O(distinct * log k))
sum(counts.values())        # total count = len(items)
```

### 3. Compare two counters

Two multisets are equal iff their counts match — a one-line check:

```python
Counter(s) == Counter(t)    # anagram check, multiset equality
```

### 4. Arithmetic on counters

Counter supports +, -, &, | for element-wise combinations:

```python
a = Counter("aabbc")        # {'a': 2, 'b': 2, 'c': 1}
b = Counter("abc")          # {'a': 1, 'b': 1, 'c': 1}

a + b                       # {'a': 3, 'b': 3, 'c': 2}   pointwise add
a - b                       # {'a': 1, 'b': 1}           pointwise subtract, clipped at 0
a & b                       # {'a': 1, 'b': 1, 'c': 1}   multiset intersection
a | b                       # {'a': 2, 'b': 2, 'c': 1}   multiset union
```

Note that `Counter - Counter` **clips negative counts to zero** —
handy when you want "what's in A that isn't already covered by B."
For negatives, subtract with a dict manually.

---

## Two Representations: Counter vs Array-of-26

For strings over a **fixed small alphabet** (like lowercase a-z), a
26-slot array is often better than a Counter:

```python
# Counter approach
from collections import Counter
c = Counter(s)

# Array-of-26 approach
counts = [0] * 26
for ch in s:
    counts[ord(ch) - ord("a")] += 1
```

| Representation       | Advantages                                  | When to use                                 |
|----------------------|---------------------------------------------|---------------------------------------------|
| `Counter` / dict     | Works for arbitrary keys. Idiomatic.         | General items (ints, strings, tuples).     |
| Array of size k      | Faster (no hashing). O(1) per op, no dict lookup. | Fixed alphabet, k ≤ ~256.                |

The array version is also **hashable as a tuple** — which makes it
useful as a dict key when grouping anagrams by letter profile. See
Phase-02 / 02 / 07-Hashing-Technique / problems / anagram-groups.py.

---

## Canonical Problem Shapes

### 1. "Most common / top-k" — majority, mode, top words

Build Counter → `most_common(k)`. O(n + k log n) with a heap.

- **Majority Element** (>n/2): hash or Boyer-Moore.
- **Top K Frequent Elements** (LC #347): heap on Counter.
- **Top K Frequent Words** (LC #692): heap with tiebreak.

### 2. "Does this equal that?" — multiset equality

`Counter(a) == Counter(b)`. O(n) in the string length.

- **Valid Anagram** (LC #242).
- **Find All Anagrams in a String** (LC #438).
- **Permutation in String** (LC #567).

### 3. "Which element breaks the pattern?" — parity / uniqueness

The "count mod 2 == 1" trick (or "count == 1") to pick out the odd
one out.

- **Single Number** (LC #136): XOR is the fastest solution, but
  Counter works too.
- **First Unique Character** (LC #387): Counter + single pass.

### 4. "Frequency inside a sliding window"

Maintain a Counter as the window slides — add the entering char,
remove the leaving char. See Phase-02 / 02 / 02-Sliding-Window.

### 5. "Count subarrays with some property based on running frequency"

Often combines prefix sum with frequency counting.

- **Subarray Sums Divisible by K** (LC #974).
- **Contiguous Array** (LC #525): count of 0s vs 1s.

---

## The Boyer-Moore Voting Algorithm

One of the elegant "why didn't I think of that?" algorithms — and a
frequency-counting problem that's solved BETTER without a counter.

**Problem:** Find the majority element in an array — the element
appearing more than n/2 times. Assume one exists.

**Counter-based approach:** O(n) time, O(n) space (the Counter).

**Boyer-Moore:** O(n) time, **O(1) space**.

```python
def majority_element(nums):
    candidate = None
    count = 0
    for x in nums:
        if count == 0:
            candidate = x
        count += 1 if x == candidate else -1
    return candidate
```

**The idea:** treat each element as a "vote for its value". Every time
you encounter a value *not* equal to the current candidate, "pair it
off" with a vote for the candidate — both cancel. If the majority
exists, its votes outnumber all others combined, so at the end the
candidate survives.

This works because the majority appears >n/2 times — any pairing-off
tournament against all other elements leaves surplus majority votes.

It doesn't work for "element appearing > n/3 times" without adaptation
(you need two candidates, two counters, and a second pass — LC #229
"Majority Element II"). The k-candidate generalization is a standard
follow-up.

Boyer-Moore is a reminder that a problem *looking* like a frequency
count sometimes has a cleverer O(1)-space solution. Always ask: "do
I really need to know the counts, or do I just need one specific
answer?"

---

## Frequency Counting vs Related Techniques

| Technique              | Use when…                                       |
|------------------------|-------------------------------------------------|
| **Generic Hashing**    | You need arbitrary value→index / membership lookups |
| **Frequency Counting** | You specifically need **counts of each value**  |
| **Sliding Window + Counter** | Counts INSIDE a moving window                |
| **Prefix Sum + Counter**| Running count of a property up to position i   |
| **Boyer-Moore Voting** | Finding the majority / plurality with O(1) space |

Frequency Counting is often used INSIDE one of the others. It rarely
stands alone as the outermost technique on harder problems.

---

## Complexity

For a Counter over `n` items from a universe of `k` distinct values:

- **Build:** O(n) time, O(k) space.
- **Query single value:** O(1) average.
- **Query top-k:** O(k log k) with `most_common()` (O(k) unordered
  heap + O(k log k) sort, or O(k log K) with a size-K heap).
- **Multiset equality:** O(k) — compares every key-value pair.
- **Counter arithmetic:** O(k).

For fixed small alphabets, replace O(k) with O(26) / O(128) / etc. —
effectively constant.

---

## Common Pitfalls

- **Confusing `Counter` with `dict`.** A Counter's `__getitem__`
  returns 0 for missing keys (instead of raising KeyError). This is
  usually what you want, but it silently masks bugs where you think
  you're checking "does key X exist?"
- **Using `Counter.subtract` when you meant `-`.** `subtract` is
  in-place and *allows* negative counts. `-` returns a new Counter
  with negatives clipped to zero. Very different — mix them up once
  and you'll remember.
- **Sorting by value in a dict.** `sorted(counts, key=counts.get)`
  gives ascending; add `reverse=True` for descending. `most_common(k)`
  is usually the cleaner choice.
- **Forgetting tie-break order.** `most_common(k)` returns ties in
  insertion order (Python 3.7+). For alphabetical tie-breaking or
  similar custom rules, sort explicitly.
- **Rebuilding Counter every loop iteration.** Frequently appears in
  naive sliding-window solutions. Build incrementally instead — add
  the entering element, remove the leaving element.

---

## Canonical Examples

### Majority Element — LeetCode #169

The Boyer-Moore showcase. O(n) time, O(1) space (beats hashing).

### Valid Anagram — LeetCode #242

Two Counters compared for equality. Two-liner.

### Top K Frequent Elements — LeetCode #347

Counter + heap. O(n + k log n).

### First Unique Character — LeetCode #387

Counter pass, then second pass to find the first index with count 1.

### Find All Anagrams in a String — LeetCode #438

Sliding window + character counter — the window's counter is compared
with the target's counter every step.

### Rearrange String K Distance Apart — LeetCode #358

Counter + max-heap + cooldown queue. One of the harder interview
problems built on frequency counting.

---

## Key Takeaways

1. **Frequency counting = dict of value → count.** That's the data
   structure; everything else is what you do with it.
2. **`collections.Counter` is the idiomatic tool.** Learn its four
   operations: build, query, compare, arithmetic.
3. **Array-of-26 beats dict when the alphabet is fixed.** It's faster
   and produces a hashable tuple you can use as a dict key for grouping.
4. **Boyer-Moore Voting** solves majority in O(1) space — remember
   this; it's the classic "you didn't need a counter" surprise.
5. **Frequency counting composes with other techniques.** The counter
   often lives inside a sliding window, a prefix-sum pass, or a heap.

For the template, see [`template.py`](template.py). For two worked
problems — one showcasing Boyer-Moore, one showcasing Counter
comparison — see [`problems/`](problems/).
