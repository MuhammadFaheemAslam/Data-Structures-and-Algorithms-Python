"""
priority-queue.py — Priority Queue With Updatable Priorities

A PRIORITY QUEUE is an abstract queue where each element has a
"priority"; the next element served is the highest-priority one.
Implemented on top of a min-heap.

---------------------------------------------------
Why We Build Our Own (Instead Of Just Using `heapq`):

Python's `heapq` is a heap of VALUES — it doesn't natively support:

    1. Stable ordering (ties broken by insertion order).
    2. UPDATING a priority after push (Dijkstra / A* need this).
    3. DELETING an arbitrary item.

The canonical trick for (2) and (3): a "lazy deletion" pattern.
Keep a hash map `entry_finder: id → [priority, seq, id, deleted?]`.
When you want to change priority, mark the old entry as DELETED
and push a fresh one. `pop()` skips deleted entries. The heap may
temporarily hold garbage, but each garbage entry is cleared when
it bubbles to the top, so amortized O(log n) per op.

---------------------------------------------------
API:

    pq = PriorityQueue()
    pq.push(id="task-1", priority=5)
    pq.update("task-1", priority=1)     # lower priority = higher urgency
    pq.pop() → "task-1"
    pq.remove("task-2")                 # lazy delete
    pq.peek() → id
    len(pq)
"""

import heapq
import itertools


_DELETED = "<DELETED>"


class PriorityQueue:
    """Min-first priority queue with updatable priorities. Items are opaque ids (must be hashable)."""

    def __init__(self):
        self._heap = []                            # list of [priority, seq, id]
        self._entry_finder = {}                    # id -> entry (same list object)
        self._counter = itertools.count()          # tie-breaker — guarantees stable FIFO

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def __len__(self):
        return len(self._entry_finder)

    def __bool__(self):
        return bool(self._entry_finder)

    def __contains__(self, item):
        return item in self._entry_finder

    # ------------------------------------------------------------------
    # Core ops
    # ------------------------------------------------------------------

    def push(self, item, priority):
        """
        Insert or UPDATE `item` with given priority. O(log n).

        If `item` already exists, its old entry is lazily removed and
        a new one is pushed.
        """
        if item in self._entry_finder:
            self._remove_entry(item)
        entry = [priority, next(self._counter), item]
        self._entry_finder[item] = entry
        heapq.heappush(self._heap, entry)

    update = push                                  # alias — update is just push

    def remove(self, item):
        """O(1) amortized. Mark `item` as deleted. Raises KeyError if absent."""
        if item not in self._entry_finder:
            raise KeyError(item)
        self._remove_entry(item)

    def _remove_entry(self, item):
        entry = self._entry_finder.pop(item)
        entry[2] = _DELETED                        # tombstone the item slot

    def peek(self):
        """O(log n) amortized. Return the lowest-priority id without removing."""
        self._drop_deleted()
        if not self._heap:
            raise IndexError("peek from empty queue")
        return self._heap[0][2]

    def peek_priority(self):
        """Return (priority, id) of the min entry."""
        self._drop_deleted()
        if not self._heap:
            raise IndexError("peek from empty queue")
        return (self._heap[0][0], self._heap[0][2])

    def pop(self):
        """O(log n) amortized. Remove and return the min-priority id."""
        self._drop_deleted()
        if not self._heap:
            raise IndexError("pop from empty queue")
        _prio, _seq, item = heapq.heappop(self._heap)
        del self._entry_finder[item]
        return item

    def _drop_deleted(self):
        """Remove deleted entries from the top so peek/pop see a live one."""
        while self._heap and self._heap[0][2] is _DELETED:
            heapq.heappop(self._heap)


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Basic push/pop by priority
    pq = PriorityQueue()
    pq.push("task-A", 3)
    pq.push("task-B", 1)
    pq.push("task-C", 2)
    assert pq.pop() == "task-B"
    assert pq.pop() == "task-C"
    assert pq.pop() == "task-A"
    assert len(pq) == 0

    # Stable order on ties (FIFO)
    pq = PriorityQueue()
    for name in ["x", "y", "z"]:
        pq.push(name, 5)
    assert pq.pop() == "x"
    assert pq.pop() == "y"
    assert pq.pop() == "z"

    # Update priority
    pq = PriorityQueue()
    pq.push("a", 10)
    pq.push("b", 5)
    pq.push("c", 1)
    pq.update("a", 0)                              # now the most urgent
    assert pq.pop() == "a"
    assert pq.pop() == "c"
    assert pq.pop() == "b"

    # Remove arbitrary + membership
    pq = PriorityQueue()
    pq.push("a", 1)
    pq.push("b", 2)
    pq.push("c", 3)
    assert "b" in pq
    pq.remove("b")
    assert "b" not in pq
    assert pq.pop() == "a"
    assert pq.pop() == "c"

    # Missing remove → KeyError
    try:
        pq.remove("nope")
    except KeyError:
        pass
    else:
        raise AssertionError("expected KeyError")

    # Stress: simulate a Dijkstra-style workload
    import random
    random.seed(42)
    pq = PriorityQueue()
    pending = {}
    for _ in range(2000):
        item = f"n{random.randint(0, 200)}"
        new_prio = random.randint(0, 1000)
        if item in pending and new_prio < pending[item]:
            pq.push(item, new_prio)
            pending[item] = new_prio
        elif item not in pending:
            pq.push(item, new_prio)
            pending[item] = new_prio

    # Now pop everything — priorities should come out monotonically non-decreasing
    # (ties broken by FIFO insertion order, NOT by id string).
    priorities = []
    while pq:
        item = pq.pop()
        priorities.append(pending[item])

    assert priorities == sorted(priorities), "pq didn't pop in priority order"
    print(f"Stress test: {len(priorities)} items popped in correct priority order")
    print("All tests passed!")
