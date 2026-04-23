"""
min-heap.py — Binary Min-Heap (from scratch)

A min-heap keeps the smallest element at the root (= index 0).
Standard array layout:
    parent(i) = (i - 1) // 2
    left(i)   = 2*i + 1
    right(i)  = 2*i + 2

---------------------------------------------------
API (mirrors Python's heapq, but OO):

    h = MinHeap()               or MinHeap([4, 1, 3])   (O(n) build)
    h.push(5)                   # O(log n)
    h.peek()                    # O(1)  — smallest
    h.pop()                     # O(log n)  — remove smallest
    len(h), bool(h)
"""


class MinHeap:
    """Binary min-heap backed by a Python list."""

    def __init__(self, iterable=None):
        self._h = list(iterable) if iterable else []
        if self._h:
            self._heapify()

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def __len__(self):
        return len(self._h)

    def __bool__(self):
        return bool(self._h)

    def peek(self):
        """O(1). Return the smallest element without removing it."""
        if not self._h:
            raise IndexError("peek from empty heap")
        return self._h[0]

    # ------------------------------------------------------------------
    # Core operations
    # ------------------------------------------------------------------

    def push(self, x):
        """O(log n). Insert `x`."""
        self._h.append(x)
        self._sift_up(len(self._h) - 1)

    def pop(self):
        """O(log n). Remove and return the smallest element."""
        if not self._h:
            raise IndexError("pop from empty heap")
        smallest = self._h[0]
        last = self._h.pop()
        if self._h:                                # still non-empty
            self._h[0] = last
            self._sift_down(0)
        return smallest

    def pushpop(self, x):
        """
        O(log n). Push `x`, then pop min. Faster than push+pop.

        If `x` is already ≤ the smallest, we return it right away
        without touching the heap.
        """
        if self._h and self._h[0] < x:
            x, self._h[0] = self._h[0], x
            self._sift_down(0)
        return x

    def replace(self, x):
        """
        O(log n). Pop min AND push `x` as one operation. Faster than
        pop+push. Requires the heap to be non-empty.
        """
        if not self._h:
            raise IndexError("replace on empty heap")
        smallest = self._h[0]
        self._h[0] = x
        self._sift_down(0)
        return smallest

    # ------------------------------------------------------------------
    # Internal: sift up / sift down / heapify
    # ------------------------------------------------------------------

    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) >> 1
            if self._h[parent] > self._h[i]:
                self._h[parent], self._h[i] = self._h[i], self._h[parent]
                i = parent
            else:
                return

    def _sift_down(self, i):
        n = len(self._h)
        while True:
            left = 2 * i + 1
            if left >= n:
                return                             # no children
            right = left + 1
            smallest_child = left
            if right < n and self._h[right] < self._h[left]:
                smallest_child = right
            if self._h[i] <= self._h[smallest_child]:
                return                             # invariant satisfied
            self._h[i], self._h[smallest_child] = self._h[smallest_child], self._h[i]
            i = smallest_child

    def _heapify(self):
        """O(n). Bottom-up sift-down from the last non-leaf."""
        for i in range((len(self._h) - 2) >> 1, -1, -1):
            self._sift_down(i)

    # ------------------------------------------------------------------
    # Utilities for tests / debugging
    # ------------------------------------------------------------------

    def to_list(self):
        """Return the underlying array (for inspection)."""
        return list(self._h)

    def is_valid(self):
        """True iff the min-heap property holds everywhere."""
        n = len(self._h)
        for i in range(n):
            left, right = 2 * i + 1, 2 * i + 2
            if left < n and self._h[i] > self._h[left]:
                return False
            if right < n and self._h[i] > self._h[right]:
                return False
        return True

    def __repr__(self):
        return f"MinHeap({self._h})"


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    import heapq
    import random

    # Basic push / pop
    h = MinHeap()
    assert not h
    for x in [4, 1, 7, 3, 8, 2]:
        h.push(x)
    assert h.is_valid()
    assert h.peek() == 1
    assert len(h) == 6

    # Pop in order yields sorted
    out = [h.pop() for _ in range(len(h))]
    assert out == [1, 2, 3, 4, 7, 8]

    # O(n) build from iterable
    h = MinHeap([5, 3, 8, 1, 9, 2, 4])
    assert h.is_valid()
    assert h.peek() == 1

    # pushpop and replace edge cases
    h = MinHeap([2, 4, 6])
    assert h.pushpop(1) == 1                       # x < min → returned directly
    assert h.peek() == 2
    assert h.replace(5) == 2                       # pop-then-push
    assert sorted(h.to_list()) == [4, 5, 6]

    # Empty errors
    empty = MinHeap()
    for op in (empty.peek, empty.pop, lambda: empty.replace(1)):
        try:
            op()
        except IndexError:
            pass
        else:
            raise AssertionError("expected IndexError")

    # Stress: agree with Python's heapq on 10000 operations
    random.seed(42)
    mine = MinHeap()
    ref = []
    for _ in range(10_000):
        op = random.choice(["push", "pop"] if ref else ["push"])
        if op == "push":
            x = random.randint(-1000, 1000)
            mine.push(x)
            heapq.heappush(ref, x)
        else:
            assert mine.peek() == ref[0]
            assert mine.pop() == heapq.heappop(ref)
        assert len(mine) == len(ref)

    # Verify the heapify build yields a valid heap for many random inputs
    for _ in range(200):
        arr = [random.randint(-100, 100) for _ in range(random.randint(0, 50))]
        h = MinHeap(arr)
        assert h.is_valid()
        assert sorted([h.pop() for _ in range(len(h))]) == sorted(arr)

    print("All tests passed!")
