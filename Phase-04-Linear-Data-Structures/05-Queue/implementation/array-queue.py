"""
array-queue.py – Array-Backed Queue (Two-Pointer Wraparound)

A resizable array-backed queue where `front` and `rear` pointers wrap
around the array. Enqueue at rear, dequeue at front — both O(1)
amortized, no shifting.

---------------------------------------------------
Why Not Just Use `list.pop(0)`?

The naïve "use a list, append to enqueue, pop(0) to dequeue" is the
classic Python performance trap:

    q = []
    q.append(x)           # O(1)
    q.pop(0)              # O(n) — shifts everything left

`pop(0)` is O(n) because every subsequent element must shift one slot
to the left. Over many dequeues, total work is O(n²). Benchmark:

    n = 100_000   queue-as-list with pop(0):   ~seconds
    n = 100_000   this implementation:         ~milliseconds

The right approach: use two pointers and wrap them modulo capacity.

---------------------------------------------------
The Wraparound Logic:

    capacity: 8 slots
    front: index of the front element
    rear:  index where the NEXT enqueue will go (one past the last element)

Empty queue:  front == rear AND size == 0.
Full queue:   front == rear AND size == capacity.
(Note the ambiguity — we track `size` explicitly to disambiguate.)

    enqueue(x):  data[rear] = x; rear = (rear + 1) % capacity; size += 1
    dequeue():   v = data[front]; front = (front + 1) % capacity; size -= 1

When `size` reaches `capacity`, we RESIZE — double the underlying
array, copy elements over in proper order (starting from front).

---------------------------------------------------
Operation Complexity:

    enqueue(x)     O(1) amortized
    dequeue()      O(1)
    peek()         O(1)
    __len__        O(1)

Resize is O(n) but happens rarely (once per doubling), so amortized
away to O(1) per operation — same analysis as dynamic arrays in
Phase-04 / 01-Array.
"""


# =========================================================================
# ArrayQueue
# =========================================================================

class ArrayQueue:
    """
    FIFO queue backed by a dynamically-resized array with
    two wraparound pointers.

    Invariants:
        - 0 ≤ front < capacity
        - 0 ≤ rear  < capacity
        - size is the count of valid elements
        - When `size == 0`: no valid elements (front and rear may point anywhere)
        - When `size == capacity`: the queue is full and must resize before next enqueue
    """

    INITIAL_CAPACITY = 8

    def __init__(self, iterable=None):
        self._capacity = ArrayQueue.INITIAL_CAPACITY
        self._data = [None] * self._capacity
        self._front = 0
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
        return self._size == 0

    def __bool__(self):
        return self._size != 0

    # ------------------------------------------------------------------
    # Core operations
    # ------------------------------------------------------------------

    def enqueue(self, value):
        """Add `value` to the back. O(1) amortized."""
        if self._size == self._capacity:
            self._resize(2 * self._capacity)

        # rear is (front + size) mod capacity
        rear = (self._front + self._size) % self._capacity
        self._data[rear] = value
        self._size += 1

    def dequeue(self):
        """Remove and return the front. O(1). Raises IndexError on empty."""
        if self._size == 0:
            raise IndexError("dequeue from empty ArrayQueue")

        value = self._data[self._front]
        self._data[self._front] = None                # allow GC
        self._front = (self._front + 1) % self._capacity
        self._size -= 1

        # Optional: shrink if we're using ≤ 1/4 of capacity
        if 0 < self._size <= self._capacity // 4 and self._capacity > ArrayQueue.INITIAL_CAPACITY:
            self._resize(max(ArrayQueue.INITIAL_CAPACITY, self._capacity // 2))

        return value

    def peek(self):
        """Return the front without removing. O(1)."""
        if self._size == 0:
            raise IndexError("peek on empty ArrayQueue")
        return self._data[self._front]

    # ------------------------------------------------------------------
    # Resize
    # ------------------------------------------------------------------

    def _resize(self, new_capacity):
        """Allocate a new array of the given capacity and copy elements in proper order."""
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[(self._front + i) % self._capacity]

        self._data = new_data
        self._front = 0
        self._capacity = new_capacity

    # ------------------------------------------------------------------
    # Iteration and display
    # ------------------------------------------------------------------

    def __iter__(self):
        """Iterate front to back."""
        for i in range(self._size):
            yield self._data[(self._front + i) % self._capacity]

    def __repr__(self):
        return "ArrayQueue(front → [" + ", ".join(repr(x) for x in self) + "] ← back)"


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    q = ArrayQueue()
    assert q.is_empty()

    for x in [1, 2, 3, 4, 5]:
        q.enqueue(x)
    print(f"After 5 enqueues: {q}")
    assert list(q) == [1, 2, 3, 4, 5]
    assert q.peek() == 1
    assert len(q) == 5

    assert q.dequeue() == 1
    assert q.dequeue() == 2
    assert list(q) == [3, 4, 5]
    print(f"After 2 dequeues: {q}")

    # Wraparound — enqueue enough to cross the end
    q.enqueue(6); q.enqueue(7); q.enqueue(8); q.enqueue(9); q.enqueue(10)
    # capacity is 8; front=2, rear wraps; list should iterate front-to-back
    assert list(q) == [3, 4, 5, 6, 7, 8, 9, 10]
    print(f"After wraparound enqueues: {q}")

    # Trigger a resize
    for x in range(100, 110):
        q.enqueue(x)
    assert len(q) == 18
    print(f"After more enqueues (triggered resize), capacity={q._capacity}")

    # Drain
    while not q.is_empty():
        q.dequeue()
    assert q.is_empty()
    print(f"After draining: {q}")

    # Edge cases
    try:
        q.dequeue()
    except IndexError as e:
        print(f"\ndequeue empty: {e}")
    try:
        q.peek()
    except IndexError as e:
        print(f"peek empty: {e}")

    # Stress test against collections.deque
    from collections import deque
    import random

    random.seed(42)

    q = ArrayQueue()
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

    # Timing vs the NAÏVE list-pop(0) approach — demonstrates the O(n²) trap
    import time

    n = 10_000

    # Correct implementation
    q = ArrayQueue()
    t0 = time.time()
    for i in range(n):
        q.enqueue(i)
    for _ in range(n):
        q.dequeue()
    t_correct = time.time() - t0

    # Naïve (don't do this!)
    lst = []
    t0 = time.time()
    for i in range(n):
        lst.append(i)
    for _ in range(n):
        lst.pop(0)
    t_naive = time.time() - t0

    print(f"\nn={n} enqueues then dequeues:")
    print(f"   ArrayQueue (correct):      {t_correct:.4f}s")
    print(f"   list + pop(0) (wrong):     {t_naive:.4f}s")
    print(f"   slowdown ratio:            {t_naive / max(t_correct, 1e-6):.1f}×")

    print("\nAll tests passed!")
