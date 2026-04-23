"""
max-heap.py — Binary Max-Heap

A max-heap keeps the LARGEST element at the root. The structure is
identical to a min-heap with all comparisons flipped.

---------------------------------------------------
Two Ways To Build One In Python:

    A) Dedicated class (below) — flipped comparators throughout.
    B) Negate-and-use-min-heap — push -x, pop -(-x) = x.

(B) is what Python users typically do since `heapq` is min-only.
It's a 5-character change per push/pop, but it breaks for non-numeric
values (strings, tuples) — there's no "negate a string". For those
cases, use (A) or wrap values with a reversing comparator class.

We implement (A) here.
"""


class MaxHeap:
    """Binary max-heap backed by a Python list."""

    def __init__(self, iterable=None):
        self._h = list(iterable) if iterable else []
        if self._h:
            self._heapify()

    def __len__(self):
        return len(self._h)

    def __bool__(self):
        return bool(self._h)

    def peek(self):
        """O(1). Return the largest element."""
        if not self._h:
            raise IndexError("peek from empty heap")
        return self._h[0]

    def push(self, x):
        """O(log n)."""
        self._h.append(x)
        self._sift_up(len(self._h) - 1)

    def pop(self):
        """O(log n). Remove and return the largest element."""
        if not self._h:
            raise IndexError("pop from empty heap")
        largest = self._h[0]
        last = self._h.pop()
        if self._h:
            self._h[0] = last
            self._sift_down(0)
        return largest

    def pushpop(self, x):
        """O(log n). Push then pop max as one op."""
        if self._h and self._h[0] > x:
            x, self._h[0] = self._h[0], x
            self._sift_down(0)
        return x

    def replace(self, x):
        """O(log n). Pop max + push x. Heap must be non-empty."""
        if not self._h:
            raise IndexError("replace on empty heap")
        largest = self._h[0]
        self._h[0] = x
        self._sift_down(0)
        return largest

    # ------------------------------------------------------------------
    # Internals — symmetric to MinHeap, all comparators flipped
    # ------------------------------------------------------------------

    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) >> 1
            if self._h[parent] < self._h[i]:
                self._h[parent], self._h[i] = self._h[i], self._h[parent]
                i = parent
            else:
                return

    def _sift_down(self, i):
        n = len(self._h)
        while True:
            left = 2 * i + 1
            if left >= n:
                return
            right = left + 1
            largest_child = left
            if right < n and self._h[right] > self._h[left]:
                largest_child = right
            if self._h[i] >= self._h[largest_child]:
                return
            self._h[i], self._h[largest_child] = self._h[largest_child], self._h[i]
            i = largest_child

    def _heapify(self):
        for i in range((len(self._h) - 2) >> 1, -1, -1):
            self._sift_down(i)

    def to_list(self):
        return list(self._h)

    def is_valid(self):
        n = len(self._h)
        for i in range(n):
            left, right = 2 * i + 1, 2 * i + 2
            if left < n and self._h[i] < self._h[left]:
                return False
            if right < n and self._h[i] < self._h[right]:
                return False
        return True

    def __repr__(self):
        return f"MaxHeap({self._h})"


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    import heapq
    import random

    # Basic: push + pop
    h = MaxHeap()
    for x in [4, 1, 7, 3, 8, 2]:
        h.push(x)
    assert h.is_valid()
    assert h.peek() == 8
    out = [h.pop() for _ in range(len(h))]
    assert out == [8, 7, 4, 3, 2, 1]

    # Build from iterable
    h = MaxHeap([5, 3, 8, 1, 9, 2, 4])
    assert h.is_valid()
    assert h.peek() == 9

    # Works on non-numeric types (strings) — proves the "no-negate" advantage
    h = MaxHeap(["banana", "apple", "cherry", "date"])
    assert h.peek() == "date"                      # lexicographic max
    assert h.pop() == "date"
    assert h.pop() == "cherry"

    # Empty errors
    empty = MaxHeap()
    for op in (empty.peek, empty.pop, lambda: empty.replace(1)):
        try:
            op()
        except IndexError:
            pass
        else:
            raise AssertionError("expected IndexError")

    # Stress against heapq with negation
    random.seed(42)
    mine = MaxHeap()
    ref = []                                       # min-heap of negatives
    for _ in range(10_000):
        op = random.choice(["push", "pop"] if ref else ["push"])
        if op == "push":
            x = random.randint(-1000, 1000)
            mine.push(x)
            heapq.heappush(ref, -x)
        else:
            assert mine.peek() == -ref[0]
            assert mine.pop() == -heapq.heappop(ref)
        assert len(mine) == len(ref)

    print("All tests passed!")
