"""
circular-queue.py – Fixed-Capacity Circular Queue (Ring Buffer)

A queue with a HARD CAPACITY limit. When full, enqueue either:
    (a) rejects the new element (strict mode), or
    (b) OVERWRITES the oldest element (ring-buffer mode).

Both variants are O(1) enqueue and dequeue. Both use a fixed-size
array with front/rear pointers that wrap modulo capacity.

---------------------------------------------------
Why Fixed Capacity?

Real-world use cases require it:

    - **Audio/video buffers.** A ring buffer smooths jitter — you
      know exactly how many samples fit, and old samples get
      overwritten when new ones arrive faster than consumers read.
    - **Log retention.** "Keep the last N log lines" is a ring buffer.
    - **Networking.** Packet receive queues are fixed-size to bound
      memory.
    - **Embedded systems.** Dynamic allocation is often forbidden.
    - **Rate-limited producer/consumer.** Fixed capacity provides
      backpressure.

The strict "reject on full" variant is LeetCode #622 (Design Circular
Queue). The overwrite variant is standard in systems programming.

---------------------------------------------------
Representation:

    Array of fixed size N.
    `front`: index of the oldest element.
    `rear`:  index where the NEXT enqueue will write.
    `size`:  current element count (disambiguates front == rear
             between empty and full).

    Empty:   size == 0
    Full:    size == N (strict mode: reject; overwrite mode: advance front)

    enqueue(x):  data[rear] = x; rear = (rear + 1) % N; size += 1
    dequeue():   v = data[front]; front = (front + 1) % N; size -= 1
"""


# =========================================================================
# Strict CircularQueue — Rejects on Full (LC #622)
# =========================================================================

class CircularQueue:
    """
    Fixed-capacity FIFO queue. enqueue on a full queue returns False
    (without inserting).

    Matches the LeetCode #622 interface.
    """

    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("capacity must be positive")

        self._capacity = capacity
        self._data = [None] * capacity
        self._front = 0
        self._size = 0

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def is_full(self):
        return self._size == self._capacity

    def capacity(self):
        return self._capacity

    # ------------------------------------------------------------------
    # Operations
    # ------------------------------------------------------------------

    def enqueue(self, value):
        """Add `value`. Returns True on success, False if queue is full."""
        if self.is_full():
            return False
        rear = (self._front + self._size) % self._capacity
        self._data[rear] = value
        self._size += 1
        return True

    def dequeue(self):
        """Remove and return the front. Returns None if empty (LC #622 convention)."""
        if self.is_empty():
            return None
        value = self._data[self._front]
        self._data[self._front] = None                # allow GC
        self._front = (self._front + 1) % self._capacity
        self._size -= 1
        return value

    def peek(self):
        """Return the front without removing. None if empty."""
        if self.is_empty():
            return None
        return self._data[self._front]

    def rear(self):
        """Return the back element. None if empty (LC #622 asks for this)."""
        if self.is_empty():
            return None
        return self._data[(self._front + self._size - 1) % self._capacity]

    # ------------------------------------------------------------------
    # Iteration and display
    # ------------------------------------------------------------------

    def __iter__(self):
        for i in range(self._size):
            yield self._data[(self._front + i) % self._capacity]

    def __repr__(self):
        return ("CircularQueue(cap="
                f"{self._capacity}, size={self._size}, "
                "front → [" + ", ".join(repr(x) for x in self) + "] ← rear)")


# =========================================================================
# Overwriting Ring Buffer — Newest Entries Overwrite Oldest
# =========================================================================

class RingBuffer:
    """
    Fixed-capacity queue. enqueue on a full buffer OVERWRITES the oldest
    element (the front).

    This is the classic "ring buffer" used in audio, logging, and
    network packet buffers.

    All operations O(1).
    """

    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("capacity must be positive")

        self._capacity = capacity
        self._data = [None] * capacity
        self._front = 0
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def is_full(self):
        return self._size == self._capacity

    def capacity(self):
        return self._capacity

    def enqueue(self, value):
        """
        Add `value` at the back. If full, the OLDEST value is
        overwritten silently (front advances by 1).
        """
        if self.is_full():
            # Overwrite: advance front, size stays at capacity
            rear = self._front                      # slot currently holding the oldest
            self._data[rear] = value
            self._front = (self._front + 1) % self._capacity
        else:
            rear = (self._front + self._size) % self._capacity
            self._data[rear] = value
            self._size += 1

    def dequeue(self):
        """Remove and return the front. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("dequeue from empty RingBuffer")
        value = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % self._capacity
        self._size -= 1
        return value

    def peek(self):
        """Return front without removing."""
        if self.is_empty():
            raise IndexError("peek on empty RingBuffer")
        return self._data[self._front]

    def __iter__(self):
        for i in range(self._size):
            yield self._data[(self._front + i) % self._capacity]

    def __repr__(self):
        return ("RingBuffer(cap="
                f"{self._capacity}, size={self._size}, "
                "front → [" + ", ".join(repr(x) for x in self) + "] ← rear)")


# =========================================================================
# Test the Implementations
# =========================================================================

if __name__ == "__main__":
    # --- CircularQueue (strict, LC #622) ---
    print("CircularQueue (strict — reject on full):")
    q = CircularQueue(3)
    assert q.enqueue(1) is True
    assert q.enqueue(2) is True
    assert q.enqueue(3) is True
    assert q.enqueue(4) is False                   # queue is full — reject
    assert q.is_full()
    assert q.peek() == 1
    assert q.rear() == 3
    print(f"   {q}")

    assert q.dequeue() == 1
    assert q.dequeue() == 2
    # now can enqueue again
    assert q.enqueue(10) is True
    assert q.enqueue(20) is True
    assert q.is_full()
    assert list(q) == [3, 10, 20]
    print(f"   after churn: {q}")

    # Drain
    while not q.is_empty():
        q.dequeue()
    assert q.dequeue() is None                     # empty → None
    assert q.peek() is None
    print(f"   after drain: {q}")

    # --- RingBuffer (overwriting) ---
    print()
    print("RingBuffer (overwrite on full):")
    r = RingBuffer(3)
    r.enqueue(1); r.enqueue(2); r.enqueue(3)
    assert list(r) == [1, 2, 3]
    print(f"   after 3 enqueues: {r}")

    r.enqueue(4)                                    # overwrites oldest (1)
    assert list(r) == [2, 3, 4]
    r.enqueue(5)                                    # overwrites 2
    assert list(r) == [3, 4, 5]
    print(f"   after 2 overwrites: {r}")

    assert r.dequeue() == 3
    assert list(r) == [4, 5]
    print(f"   after dequeue: {r}")

    # Edge cases
    try:
        CircularQueue(0)
    except ValueError as e:
        print(f"\ncapacity=0: {e}")

    # Stress test for CircularQueue vs a reference using deque
    from collections import deque
    import random
    random.seed(42)

    q = CircularQueue(50)
    ref = deque(maxlen=None)                       # unbounded for comparison

    total_ops = 0
    rejected = 0
    for _ in range(5_000):
        op = random.choice(["enq", "deq"])
        if op == "enq":
            v = random.randint(0, 100)
            if q.enqueue(v):
                ref.append(v)
            else:
                rejected += 1
                assert len(ref) == 50              # reference would also be at capacity
        else:
            my = q.dequeue()
            theirs = ref.popleft() if ref else None
            assert my == theirs
        assert list(q) == list(ref)
        total_ops += 1

    print(f"\nStress test (CircularQueue): {total_ops} ops, {rejected} rejected due to full queue")

    # Stress test for RingBuffer — should never reject, always overwrites
    r = RingBuffer(5)
    ref = deque(maxlen=5)

    for _ in range(5_000):
        op = random.choice(["enq", "deq"])
        if op == "enq":
            v = random.randint(0, 100)
            r.enqueue(v)
            ref.append(v)                          # deque(maxlen=5) auto-drops oldest
        else:
            if not ref:
                continue
            assert r.dequeue() == ref.popleft()
        assert list(r) == list(ref)

    print("Stress test (RingBuffer): 5000 ops — matches deque(maxlen=5)")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Two Modes, Two Use Cases:
    #
    #   CircularQueue (strict):
    #     - LeetCode #622's exact semantics.
    #     - Any system where dropped data is an error (reject + notify).
    #
    #   RingBuffer (overwrite):
    #     - Audio/video: old samples don't matter; always get the most recent.
    #     - Logging: keep the last N lines, drop older ones.
    #     - Debugging trace buffers.
    #
    # Both give O(1) operations. The difference is just "what happens
    # when we'd lose data anyway."
    # ---------------------------------------------------------------
