"""
linked-queue.py – Linked-List-Backed Queue

FIFO queue implemented as a singly-linked list with both `front`
(for dequeue) and `rear` (for enqueue) pointers. Both operations
O(1) with no resize cost, no capacity limit.

---------------------------------------------------
Two-Pointer Linked List:

    front → [A] → [B] → [C] → [D] ← rear

    enqueue(E):
        new_node = Node(E)
        rear.next = new_node
        rear = new_node                 O(1)

    dequeue():
        v = front.value
        front = front.next              O(1)
        if front is None: rear = None   (list now empty)
        return v

Compared to array-backed: no amortized resize cost, no capacity
concept, but ~2× memory per element (each node has its own object
overhead + `next` pointer). In Python, use `collections.deque` for
production code — it gets the best of both worlds.
"""


# =========================================================================
# Node
# =========================================================================

class _Node:
    __slots__ = ("value", "next")

    def __init__(self, value, next=None):
        self.value = value
        self.next = next


# =========================================================================
# LinkedQueue
# =========================================================================

class LinkedQueue:
    """
    FIFO queue backed by a singly-linked list.

    Invariants:
        - `front is None` iff empty.
        - If non-empty, `front` is the oldest, `rear` is the newest.
        - `rear.next is None` always.
    """

    def __init__(self, iterable=None):
        self._front = None
        self._rear = None
        self._size = 0

        if iterable is not None:
            for x in iterable:
                self.enqueue(x)

    # ------------------------------------------------------------------
    # Size queries
    # ------------------------------------------------------------------

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._front is None

    def __bool__(self):
        return self._front is not None

    # ------------------------------------------------------------------
    # Core operations
    # ------------------------------------------------------------------

    def enqueue(self, value):
        """Add `value` at the back. O(1)."""
        node = _Node(value)
        if self._rear is None:
            # Empty queue → new node is both front and rear
            self._front = node
            self._rear = node
        else:
            self._rear.next = node
            self._rear = node
        self._size += 1

    def dequeue(self):
        """Remove and return the front. O(1). Raises IndexError on empty."""
        if self._front is None:
            raise IndexError("dequeue from empty LinkedQueue")

        value = self._front.value
        self._front = self._front.next
        if self._front is None:
            # Queue became empty — reset rear too
            self._rear = None
        self._size -= 1
        return value

    def peek(self):
        """Return the front without removing. O(1)."""
        if self._front is None:
            raise IndexError("peek on empty LinkedQueue")
        return self._front.value

    # ------------------------------------------------------------------
    # Iteration and display
    # ------------------------------------------------------------------

    def __iter__(self):
        """Iterate front to back."""
        node = self._front
        while node is not None:
            yield node.value
            node = node.next

    def __repr__(self):
        return "LinkedQueue(front → [" + ", ".join(repr(x) for x in self) + "] ← back)"


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    q = LinkedQueue()
    assert q.is_empty()

    for x in [1, 2, 3, 4, 5]:
        q.enqueue(x)
    print(f"After 5 enqueues: {q}")
    assert list(q) == [1, 2, 3, 4, 5]
    assert q.peek() == 1

    assert q.dequeue() == 1
    assert q.dequeue() == 2
    assert list(q) == [3, 4, 5]
    print(f"After 2 dequeues: {q}")

    # Invariant: after emptying, rear should be None too
    while not q.is_empty():
        q.dequeue()
    assert q._rear is None and q._front is None
    print(f"After draining: {q}")

    # Can re-enqueue after empty
    q.enqueue(99)
    assert q.peek() == 99
    print(f"After re-enqueue: {q}")

    # Edge cases
    empty = LinkedQueue()
    try:
        empty.dequeue()
    except IndexError as e:
        print(f"\ndequeue empty: {e}")
    try:
        empty.peek()
    except IndexError as e:
        print(f"peek empty: {e}")

    # Single-element churn
    q = LinkedQueue()
    for _ in range(10):
        q.enqueue(1)
        assert q.dequeue() == 1
    assert q.is_empty()
    assert q._front is None and q._rear is None

    # Stress test against collections.deque
    from collections import deque
    import random

    random.seed(42)

    q = LinkedQueue()
    ref = deque()

    for _ in range(5_000):
        op = random.choice(["enq", "deq", "peek"])
        if op == "enq":
            v = random.randint(0, 100)
            q.enqueue(v)
            ref.append(v)
        elif op == "deq":
            if not ref:
                continue
            assert q.dequeue() == ref.popleft()
        elif op == "peek":
            if not ref:
                continue
            assert q.peek() == ref[0]

        assert len(q) == len(ref)
        assert list(q) == list(ref)

    print("\nStress test: 5000 random ops — matches collections.deque")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # LinkedQueue vs ArrayQueue — Which to Pick?
    #
    #                Array (wraparound)    Linked
    #   enqueue      O(1) amortized        O(1) (always)
    #   dequeue      O(1)                  O(1)
    #   memory       ~1 pointer per elem   ~2 pointers + obj overhead
    #   cache        Good (contiguous)     Poor (scattered)
    #   resize       Occasional O(n)       Never
    #
    # In Python: `collections.deque` beats both (blocks + deque gets
    # O(1) and cache-friendly). The two implementations here are for
    # teaching the ADT.
    # ---------------------------------------------------------------
