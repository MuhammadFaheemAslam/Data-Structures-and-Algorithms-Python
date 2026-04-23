"""
implementation.py – Deque (from scratch, via Doubly-Linked List)

A deque supporting O(1) add/remove at both ends, backed by a
sentinel-headed doubly-linked list — very similar to
Phase-04 / 03-Linked-List / 02-DLL/implementation.py, but exposing
only the six-operation deque interface.

---------------------------------------------------
Interface (matches Python's `collections.deque` where sensible):

    append(x)       — add at BACK         O(1)
    appendleft(x)   — add at FRONT        O(1)
    pop()           — remove from BACK    O(1)
    popleft()       — remove from FRONT   O(1)
    peek_back()     — look at BACK        O(1)
    peek_front()    — look at FRONT       O(1)
    clear()                               O(n) — for GC's sake
    __len__, __iter__, __reversed__, __bool__, __repr__, __contains__

---------------------------------------------------
Sentinel-Node Trick (Reused from DLL):

Instead of `head = None` / `tail = None` for empty state, we use
TWO sentinel nodes flanking the real data. Every real node always
has both `prev` and `next` pointing at SOMETHING — so insert/remove
logic has no special cases.

    _head ↔ [A] ↔ [B] ↔ [C] ↔ _tail      (non-empty)
    _head ↔ _tail                         (empty)
"""


class _Node:
    __slots__ = ("value", "prev", "next")

    def __init__(self, value, prev=None, next=None):
        self.value = value
        self.prev = prev
        self.next = next


class Deque:
    """
    Double-ended queue backed by a sentinel-headed DLL.

    All six end operations are O(1). Iteration is O(n).
    """

    def __init__(self, iterable=None):
        self._head = _Node(None)                  # sentinel — just before the front
        self._tail = _Node(None)                  # sentinel — just after the back
        self._head.next = self._tail
        self._tail.prev = self._head
        self._size = 0

        if iterable is not None:
            for x in iterable:
                self.append(x)

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def __bool__(self):
        return self._size != 0

    # ------------------------------------------------------------------
    # Private splice primitive — O(1)
    # ------------------------------------------------------------------

    def _insert_between(self, value, left, right):
        """Insert a new node with `value` between `left` and `right`."""
        node = _Node(value, prev=left, next=right)
        left.next = node
        right.prev = node
        self._size += 1
        return node

    def _unlink(self, node):
        """Remove `node` from the list and return its value. O(1)."""
        assert node is not self._head and node is not self._tail
        node.prev.next = node.next
        node.next.prev = node.prev
        value = node.value
        # Detach entirely so the GC can reclaim
        node.prev = node.next = None
        self._size -= 1
        return value

    # ------------------------------------------------------------------
    # Public add / remove at both ends — O(1)
    # ------------------------------------------------------------------

    def append(self, value):
        """Add at BACK. O(1)."""
        self._insert_between(value, self._tail.prev, self._tail)

    def appendleft(self, value):
        """Add at FRONT. O(1)."""
        self._insert_between(value, self._head, self._head.next)

    def pop(self):
        """Remove and return BACK. O(1). Raises IndexError on empty."""
        if self._size == 0:
            raise IndexError("pop from empty Deque")
        return self._unlink(self._tail.prev)

    def popleft(self):
        """Remove and return FRONT. O(1). Raises IndexError on empty."""
        if self._size == 0:
            raise IndexError("popleft from empty Deque")
        return self._unlink(self._head.next)

    # ------------------------------------------------------------------
    # Peek — O(1)
    # ------------------------------------------------------------------

    def peek_back(self):
        """Return back without removing. O(1)."""
        if self._size == 0:
            raise IndexError("peek_back on empty Deque")
        return self._tail.prev.value

    def peek_front(self):
        """Return front without removing. O(1)."""
        if self._size == 0:
            raise IndexError("peek_front on empty Deque")
        return self._head.next.value

    # ------------------------------------------------------------------
    # Bulk operations
    # ------------------------------------------------------------------

    def clear(self):
        """Remove everything. O(n) due to detaching each node for GC."""
        node = self._head.next
        while node is not self._tail:
            nxt = node.next
            node.prev = node.next = None
            node = nxt
        self._head.next = self._tail
        self._tail.prev = self._head
        self._size = 0

    def extend(self, iterable):
        """Append every element of `iterable`. O(k)."""
        for x in iterable:
            self.append(x)

    def extendleft(self, iterable):
        """
        Prepend every element of `iterable` — so the final order in the
        deque is the iterable REVERSED (each element is prepended in turn).

        Matches `collections.deque.extendleft` semantics.
        """
        for x in iterable:
            self.appendleft(x)

    # ------------------------------------------------------------------
    # Iteration and display
    # ------------------------------------------------------------------

    def __iter__(self):
        """Iterate FRONT → BACK."""
        node = self._head.next
        while node is not self._tail:
            yield node.value
            node = node.next

    def __reversed__(self):
        """Iterate BACK → FRONT."""
        node = self._tail.prev
        while node is not self._head:
            yield node.value
            node = node.prev

    def __contains__(self, value):
        """`x in deque` — O(n)."""
        return any(v == value for v in self)

    def __repr__(self):
        return "Deque([" + ", ".join(repr(x) for x in self) + "])"

    def __eq__(self, other):
        if isinstance(other, Deque):
            return list(self) == list(other)
        if isinstance(other, list):
            return list(self) == other
        return NotImplemented


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    d = Deque()
    assert d.is_empty()

    d.append(1)
    d.append(2)
    d.appendleft(0)
    d.appendleft(-1)
    print(f"After append(1, 2) + appendleft(0, -1): {d}")
    assert list(d) == [-1, 0, 1, 2]
    assert d.peek_front() == -1
    assert d.peek_back() == 2
    assert len(d) == 4

    assert d.pop() == 2
    assert d.popleft() == -1
    print(f"After pop and popleft: {d}")
    assert list(d) == [0, 1]

    # Reverse iteration
    assert list(reversed(d)) == [1, 0]

    # Edge cases
    empty = Deque()
    for op in ("pop", "popleft", "peek_front", "peek_back"):
        try:
            getattr(empty, op)()
        except IndexError as e:
            print(f"empty.{op}(): {e}")
    print()

    # Extend / extendleft
    d = Deque([1, 2, 3])
    d.extend([4, 5])
    assert list(d) == [1, 2, 3, 4, 5]
    d.extendleft([0, -1, -2])                  # each prepended in turn
    assert list(d) == [-2, -1, 0, 1, 2, 3, 4, 5]
    print(f"After extend + extendleft: {d}")

    # Clear
    d.clear()
    assert d.is_empty()
    print(f"After clear: {d}")

    # Stress test — compare against collections.deque
    from collections import deque as stddeque
    import random

    random.seed(42)

    my = Deque()
    ref = stddeque()

    for _ in range(5_000):
        op = random.choice([
            "append", "appendleft", "pop", "popleft",
            "peek_front", "peek_back",
        ])

        if op == "append":
            v = random.randint(0, 100)
            my.append(v)
            ref.append(v)
        elif op == "appendleft":
            v = random.randint(0, 100)
            my.appendleft(v)
            ref.appendleft(v)
        elif op == "pop":
            if not ref:
                continue
            assert my.pop() == ref.pop()
        elif op == "popleft":
            if not ref:
                continue
            assert my.popleft() == ref.popleft()
        elif op == "peek_front":
            if not ref:
                continue
            assert my.peek_front() == ref[0]
        elif op == "peek_back":
            if not ref:
                continue
            assert my.peek_back() == ref[-1]

        assert len(my) == len(ref)
        assert list(my) == list(ref)
        assert list(reversed(my)) == list(reversed(ref))

    print("\nStress test: 5000 random ops — matches collections.deque (front + back + iter + reversed)")

    # Equality
    assert Deque([1, 2, 3]) == [1, 2, 3]
    assert Deque() == []
    assert Deque([1, 2]) != [1, 2, 3]

    print("\nAll tests passed!")
