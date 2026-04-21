# Fast & Slow Pointers — Theory

## Introduction

**Fast & Slow Pointers** (also known as **Floyd's Tortoise and Hare**)
is a specialization of the Two Pointers technique where the two
pointers advance at **different speeds**.

Classically:

- **Slow** moves one step at a time.
- **Fast** moves two steps at a time.

The speed difference is what unlocks the technique. It lets you answer
two kinds of questions with O(1) extra space — questions that would
otherwise need O(n) space with a hash set:

> *"Does this sequence have a cycle?"*  and
> *"Where is the middle of this sequence?"*

Both show up constantly on linked lists and sequence-of-transitions
problems. The speed difference is a trick you'll re-encounter under
different names for the rest of your career.

---

## The Two Core Ideas

### 1. Cycle Detection — The Speed Gap Catches Up

If a sequence has a cycle, the fast pointer (moving 2x) and the slow
pointer (moving 1x) MUST meet inside the cycle. Here's why:

- Once both pointers are inside the cycle, the gap between them
  closes by exactly 1 step every iteration (fast gains 2, slow gains 1).
- If the cycle length is `C`, the gap closes completely within at
  most `C` steps.

If the sequence has NO cycle, the fast pointer eventually reaches the
end (None for linked lists). That's the termination condition.

```
Sequence with no cycle:

    node → node → node → None
    s↑        f↑   (fast reaches None — no cycle)

Sequence with a cycle:

    node → node → node → node → node
                          ↑             ↓
                          └─────────────┘
    eventually: s↑ and f↑ end up at the SAME node.
```

**Key property:** this is done with O(1) extra memory, unlike the
"hash set of visited nodes" approach which costs O(n).

### 2. Middle Finding — Fast Reaches End When Slow Is Halfway

If fast advances twice as fast as slow, then when fast reaches the
end of a sequence of length `n`, slow has taken `n/2` steps — so
slow is at the middle.

```
sequence of length 5:

    step 0:  s=0, f=0
    step 1:  s=1, f=2
    step 2:  s=2, f=4  (fast reached end)
             → slow is at index 2 (the middle of a 5-length sequence)

sequence of length 6:

    step 0:  s=0, f=0
    step 1:  s=1, f=2
    step 2:  s=2, f=4
    step 3:  s=3, f=6  (fast at end)
             → slow at index 3 (the SECOND middle for even length)
```

For even-length sequences, the "middle" is ambiguous. By convention,
fast-slow finding lands on the SECOND of the two middle elements
(index n/2 for a 0-indexed array of length n). If you want the first
middle, tweak the termination condition.

---

## Floyd's Cycle-Finding Algorithm — The Full Version

Beyond "does a cycle exist?", the algorithm can also find the **start
of the cycle** — the node where the cycle begins. This is the "full"
Floyd's algorithm, used in LeetCode #142 Linked List Cycle II.

**Phase 1 — Detect:**

Walk with slow (1 step) and fast (2 steps) until they meet. If fast
hits None first, no cycle — done.

**Phase 2 — Find the start:**

Once they meet, reset one pointer (say slow) to the head. Now advance
BOTH slow and fast ONE step at a time. They meet exactly at the cycle's
starting node.

### Why does this work?

Let:
- `L` = distance from head to cycle entrance.
- `C` = cycle length.
- `x` = distance from cycle entrance to the meeting point.

When slow and fast first meet:
- Slow has walked `L + x` steps.
- Fast has walked `2(L + x)` steps.
- Fast has also completed some number `k` of full cycle laps, so
  `2(L + x) = L + x + k·C`, giving `L + x = k·C`.

Rearranging: `L = k·C - x = (k-1)·C + (C - x)`.

In words: starting from head and walking `L` steps lands you at the
cycle entrance; starting from the meeting point and walking `L` steps
ALSO lands you at the cycle entrance (because L ≡ -x (mod C)).

So in Phase 2, both pointers walk exactly `L` steps and meet at the
cycle's starting node. Beautiful.

---

## When to Reach for Fast & Slow

Strong signals:

1. **The input is a linked list** (or any iterator of single-link
   "next" transitions).
2. You need to detect a **cycle** or the **middle** of the sequence.
3. You need **O(1) space** — a hash set would also work, but uses O(n).
4. You need to **reverse / compare** the second half (finding middle
   is the prerequisite).

Indirect signals — these look like different problems but reduce to
cycle detection:

5. **Sequences of transitions** where `next(x) = f(x)` is deterministic.
   If the sequence eventually repeats, it has a cycle — detectable
   by this technique. Examples: Happy Number (digit-square iteration),
   "find duplicate number" via index-value chaining (LC #287).
6. **Functional graphs** — any `x → f(x)` graph. Every node has
   out-degree 1, so following `f` from any start must eventually cycle.

---

## Classic Applications

### 1. Linked List Cycle — LeetCode #141

Return True if the list has a cycle. Use Phase 1 of Floyd's.

### 2. Linked List Cycle II — LeetCode #142

Return the node where the cycle begins. Use Phase 1 + Phase 2.

### 3. Middle of the Linked List — LeetCode #876

Return the middle node. Standard fast-slow walk until fast reaches end.

### 4. Happy Number — LeetCode #202

Repeatedly replace n with the sum of squares of its digits. Return True
if it eventually reaches 1, False if it enters a non-1 cycle. Classic
Floyd's on a function-iteration "sequence".

### 5. Find the Duplicate Number — LeetCode #287

Given nums[] containing n+1 integers in [1..n], find the one duplicate.
Treat nums as a functional graph: next(i) = nums[i]. The duplicate
creates a cycle. Apply Phase 1 + 2 of Floyd's to find the cycle start,
which is the duplicate.

### 6. Palindrome Linked List — LeetCode #234

Find the middle (fast-slow), reverse the second half, compare with the
first. All in O(1) space.

---

## Fast & Slow vs Related Techniques

| Technique              | Shape                                     | Typical use                       |
|------------------------|-------------------------------------------|-----------------------------------|
| **Two Pointers**       | Both move same speed                      | Pair search, sorted-array problems |
| **Sliding Window**     | Two pointers, both rightward, variable gap | Contiguous subarrays              |
| **Fast & Slow**        | Two pointers, DIFFERENT speeds            | Cycle detection, midpoint         |
| **Hash Set of Visited**| Track every node seen                     | Also detects cycles — but O(n) space |

The hash-set approach is a perfectly valid alternative for cycle
detection. It's simpler to reason about and has the same time
complexity. The ONLY reason to prefer fast-slow is when O(1) space
is required (which is often, in interviews).

---

## Complexity

- **Time:** O(n) — both pointers together take at most 2n steps.
- **Space:** O(1) — two pointers, period. No auxiliary structures.

---

## Pitfalls

- **Forgetting the null-safety on fast.** You must check both `fast`
  AND `fast.next` before `fast.next.next`. If fast is None or
  fast.next is None, you're at or past the end.
- **Confusing first-middle and second-middle.** For even-length
  sequences, the "canonical" middle found by fast-slow is the second
  of the two (i.e., index n/2 for 0-indexed). If you want the first,
  change the loop condition: `while fast.next and fast.next.next`.
- **Not resetting properly for Phase 2.** You must reset exactly one
  pointer to head before Phase 2. Resetting both or neither gives the
  wrong answer.
- **Assuming the input has a cycle.** Always check fast/fast.next for
  None at each iteration. Many interview bugs come from assuming the
  cycle exists.
- **Using slow/fast on something without a deterministic next.** The
  technique needs `next(x)` to be a single function. If branches are
  possible, you need a different algorithm (DFS/BFS).

---

## Pseudocode Skeletons

### Cycle Detection (Phase 1 only)

```
slow = head
fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow == fast:
        return True             # cycle detected
return False                    # fast reached end → no cycle
```

### Cycle Start (Phases 1 + 2)

```
# Phase 1
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow == fast:
        break
else:
    return None                 # no cycle

# Phase 2
slow = head
while slow != fast:
    slow = slow.next
    fast = fast.next
return slow                     # cycle start
```

### Find the Middle

```
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
return slow                     # middle for odd length; second middle for even
```

For concrete implementations + worked linked-list problems, see
[`template.py`](template.py) and [`problems/`](problems/).

---

## Key Takeaways

1. **Two pointers at different speeds unlock two O(1)-space tricks:**
   cycle detection and middle-finding.
2. **The speed gap is the engine.** Slow moves 1, fast moves 2 — the
   1-step gap per iteration is why they catch up in cycles and why
   slow lands at the halfway point.
3. **Floyd's full algorithm** uses two phases: detect (slow + 2x-fast),
   then find start (reset one to head, both 1x).
4. **Applies to any functional graph**, not just linked lists — Happy
   Number and Find Duplicate are cycle problems in disguise.
5. **Prefer over hash-set** when O(1) space is needed. Otherwise,
   hash-set is simpler and equally fast.

For the template see [`template.py`](template.py). For worked problems,
see [`problems/cycle-detection.py`](problems/cycle-detection.py) and
[`problems/middle-linkedlist.py`](problems/middle-linkedlist.py).
