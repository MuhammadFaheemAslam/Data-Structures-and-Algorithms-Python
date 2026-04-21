# Merge Intervals — Theory

## Introduction

**Merge Intervals** is the specialized technique for problems involving
**ranges, meetings, time windows, and overlaps** — anywhere the input
is a collection of `(start, end)` pairs and the answer depends on how
they relate.

The core insight:

> *Sort intervals by start time. Walk them in order. For each interval,
> either it overlaps with the running "merged" interval (extend it)
> or it doesn't (emit the old one and start fresh).*

That one sentence covers a whole family of problems:

- **Merge Intervals** — combine overlapping ranges into maximal
  non-overlapping ranges.
- **Insert Interval** — splice a new interval into a pre-sorted list.
- **Meeting Rooms I / II** — can we attend all meetings? How many
  rooms do we need?
- **Non-overlapping Intervals** — minimum removals to eliminate
  overlaps.
- **Interval Intersection** — common parts between two interval lists.

All of these reduce to "sort by start time, then sweep." The O(n log n)
sort is the bottleneck; the merge itself is O(n).

---

## The Core Algorithm

```
def merge(intervals):
    if not intervals:
        return []

    intervals.sort(key=lambda iv: iv[0])              # sort by START
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:                         # overlap
            merged[-1] = (last_start, max(last_end, end))
        else:                                         # disjoint
            merged.append((start, end))

    return merged
```

Two things to verify on your own examples:

1. **The sort is by start time, not end time.** After sorting by start,
   the only intervals that could overlap with the running tail are
   those with a start ≤ the tail's end.
2. **The "overlap" condition is `start <= last_end`** (not `<`).
   Touching intervals like `[1, 5]` and `[5, 8]` usually count as
   overlapping for "merge" purposes. Switch to `<` if the problem says
   they don't.

---

## Overlap Detection — The Three Tests

Given two intervals `A = [a1, a2]` and `B = [b1, b2]`:

| Relationship                     | Test                         |
|----------------------------------|------------------------------|
| A ends before B starts (disjoint, A left) | `a2 < b1`          |
| A starts after B ends (disjoint, A right) | `a1 > b2`          |
| A and B overlap                  | `a1 <= b2 AND b1 <= a2`      |
| A is fully inside B              | `b1 <= a1 AND a2 <= b2`      |

The "overlap" test — `a1 <= b2 AND b1 <= a2` — is the one you need
for detecting conflicts. It's the negation of either disjoint case.

The overlap's intersection (when it exists) is:

```
intersection = [max(a1, b1), min(a2, b2)]
```

Use when the problem asks for "the common part" of two intervals.

---

## When to Reach for Merge Intervals

Strong signals:

1. **The input is a list of `(start, end)` pairs.** This is the whole
   technique's signature.
2. **The question is about overlaps, conflicts, scheduling, or
   coverage.** Calendar, classrooms, time windows, IP ranges, date
   ranges.
3. **The output is also a list of intervals** (as in Merge Intervals
   or Insert Interval) — sort + sweep.

Indirect signals:

4. **"Maximum concurrent events at any time."** Convert to
   (start, +1) and (end, -1) events, sort by time, sweep with a
   running counter. This is the **sweep line** technique —
   Merge Intervals' more general cousin.
5. **"How many rooms do we need?"** Min heap of end times as you
   process intervals in start order. A slight twist on the merge
   skeleton.

---

## The Sweep Line Pattern

A generalization of merge intervals that handles more complex questions:

```
Convert each interval [start, end] into TWO events:
    (start, +1)     — a new interval begins
    (end,   -1)     — an interval ends

Sort all events by time.
Walk them, keeping a running counter of "currently active intervals".
The counter's value at any moment is the # of intervals covering that point.
```

Use when:

- **Counting concurrent events** at each point.
- **Meeting Rooms II** (max concurrent intervals = min rooms).
- **"Paint intervals" / "union of intervals length"** problems.
- **Skyline problem** (LC #218 — sweep line with a max heap).

Sweep line = sort events + scan. It's more flexible than merge
intervals but requires more bookkeeping.

---

## Canonical Applications

### 1. Merge Intervals — LeetCode #56

Given a list of intervals, return the list of merged (maximal
non-overlapping) intervals. The simplest form; see
[`problems/merge-intervals.py`](problems/merge-intervals.py).

### 2. Insert Interval — LeetCode #57

Given a SORTED list of non-overlapping intervals and a new interval,
insert it and re-merge. See
[`problems/insert-interval.py`](problems/insert-interval.py).

### 3. Meeting Rooms I — LeetCode #252

Given meeting times, return True iff a single person can attend them all.
Sort by start; return False if any interval's start is before the
previous one's end.

### 4. Meeting Rooms II — LeetCode #253

Same input, but return the MINIMUM NUMBER of rooms needed so that
every meeting can happen. Sort by start; use a min-heap of current
rooms' end times. Max heap size = answer.

### 5. Non-Overlapping Intervals — LeetCode #435

Return the minimum number of intervals to REMOVE so the rest don't
overlap. Greedy: sort by END time; pick the earliest-ending
compatible interval (this is the Activity Selection pattern from
03-Greedy — the problems are duals).

### 6. Interval List Intersections — LeetCode #986

Given two lists of non-overlapping intervals (both sorted), return
their intersection. Two-pointer walk through both lists.

### 7. Car Pooling — LeetCode #1094

Max concurrent passengers problem. Can be solved via sweep line OR
via a difference array (see Phase-02 / 02 / 04-Difference-Array) —
the two techniques overlap heavily on this class of problem.

---

## Merge Intervals vs Related Techniques

| Technique            | Shape                                           |
|----------------------|-------------------------------------------------|
| **Merge Intervals**  | Sort by start, sweep, merge/emit                |
| **Sweep Line**       | Convert each interval into two events; sort events |
| **Difference Array** | Record +1 at start and −1 at end+1; prefix sum counts |
| **Two Pointers**     | On two pre-sorted lists (Interval Intersection) |
| **Greedy**           | Activity Selection — sort by END, pick earliest-finishing |

The overlap between these is real:

- Merge Intervals IS a greedy algorithm (the local rule is "merge if
  possible, else emit").
- Sweep Line and Difference Array are two ways of answering the SAME
  question about concurrent intervals — pick whichever matches your
  memory layout.
- Interval Intersection on two sorted lists is a two-pointer walk.

The technique name "Merge Intervals" is a specific pattern in this
family. When the problem is clearly about intervals, recognizing which
of the related techniques applies is half the battle.

---

## Complexity

- **Sorting:** O(n log n). This dominates.
- **Sweep / merge pass:** O(n).
- **Space:** O(n) for the output (or O(1) if you merge in place).

The O(n log n) bound is inescapable for the general merge problem
— there's no known way to avoid sorting when the input is unsorted.

Exceptions:

- Insert Interval (LC #57) starts from a SORTED list, so the whole
  algorithm is O(n) — no sort needed.
- Pre-sorted interval lists (as in LC #986 intersections) use two
  pointers for O(n + m).

---

## Pitfalls

- **Sorting by end instead of start.** Works for Activity Selection
  (greedy), but for Merge Intervals you need to sort by START —
  otherwise the walk misses overlaps.
- **Off-by-one on the overlap condition.** Is `[1, 3]` overlapping
  `[3, 5]`? Depends on the problem's definition. "Touching counts"
  uses `<=`, "strict overlap" uses `<`.
- **Mutating input during iteration.** Python doesn't like that,
  and it's usually wrong anyway. Build a new `merged` list.
- **Missing the empty-input case.** Many of these solutions reference
  `merged[-1]` — crash on empty input. Handle it at the top.
- **Assuming intervals are `(start, end)` tuples.** LeetCode uses
  `[start, end]` lists. Both work for this technique, but don't
  conflate them in a single test suite.
- **Comparing intervals as 2-element lists with min/max.** `min([3,
  5], [1, 2])` compares lexicographically — `[1, 2]` wins. Usually
  what you want, but understand what's happening.

---

## Pseudocode Skeletons

### Merge

```
sorted_intervals = sort by start
merged = [sorted[0]]
for interval in sorted[1:]:
    if interval.start <= merged[-1].end:
        merged[-1] = (merged[-1].start, max(merged[-1].end, interval.end))
    else:
        merged.append(interval)
return merged
```

### Meeting Rooms II (Sweep / Heap)

```
sort by start
heap = []
for (start, end) in intervals:
    if heap and heap[0] <= start:
        heapq.heappop(heap)          # reuse a freed room
    heapq.heappush(heap, end)        # new (or reused) room's end time
return len(heap)
```

### Interval Intersection (Two Pointers)

```
i = j = 0
result = []
while i < len(A) and j < len(B):
    lo = max(A[i].start, B[j].start)
    hi = min(A[i].end,   B[j].end)
    if lo <= hi:
        result.append([lo, hi])
    if A[i].end < B[j].end:
        i += 1
    else:
        j += 1
return result
```

For concrete implementations of Merge and Insert, see
[`template.py`](template.py) and [`problems/`](problems/).

---

## Key Takeaways

1. **Sort by start, then sweep.** That's merge intervals in its
   simplest form.
2. **Overlap test:** `a1 <= b2 AND b1 <= a2`. Or: no gap between them.
3. **Touching vs overlapping** depends on the problem — `<` vs `<=`.
4. **Sweep line** generalizes merge intervals for "count concurrent"
   questions. Difference array is its array-based cousin.
5. **Complexity is O(n log n)** dominated by the sort. If the input
   is pre-sorted (Insert Interval, intersections), it's O(n).
