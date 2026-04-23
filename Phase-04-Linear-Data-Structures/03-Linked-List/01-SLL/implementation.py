"""
implementation.py – Singly Linked List (from scratch)

A minimal SinglyLinkedList class implementing the standard operations
you'd expect from any linked-list container. Used as the substrate
for all the problems in this module.

Maintains:
    - `head`   — the first node (or None for empty list)
    - `tail`   — the last node (or None for empty list) — so append is O(1)
    - `size`   — the current number of nodes — so len() is O(1)

All three state variables must stay in sync after every operation.
Every mutating method must ask: "did this change head, tail, or size?"

---------------------------------------------------
Operation Complexity:

    append(x)       O(1)   (thanks to tail pointer)
    prepend(x)      O(1)
    pop()           O(n)   — need to find the node BEFORE the tail
    popleft()       O(1)
    insert(i, x)    O(n)   — walk to position i
    remove(x)       O(n)   — walk to find x
    __getitem__(i)  O(n)   — no random access on an SLL
    __contains__(x) O(n)
    len             O(1)

For O(1) pop from the right, use a doubly-linked list (02-DLL/).
"""


# =========================================================================
# Node
# =========================================================================

class Node:
    """A single node in a singly-linked list."""

    __slots__ = ("value", "next")                # save memory — skip __dict__

    def __init__(self, value, next=None):
        self.value = value
        self.next = next

    def __repr__(self):
        return f"Node({self.value!r})"


# =========================================================================
# Singly Linked List
# =========================================================================

class SinglyLinkedList:
    """
    A singly linked list with head/tail pointers and size counter.

    Empty list: head == tail == None, size == 0.
    Single-element list: head == tail, head.next == None, size == 1.
    """

    def __init__(self, iterable=None):
        self.head = None
        self.tail = None
        self.size = 0

        if iterable is not None:
            for x in iterable:
                self.append(x)

    # ------------------------------------------------------------------
    # Size queries
    # ------------------------------------------------------------------

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    # ------------------------------------------------------------------
    # Insertion — O(1) for the ends, O(n) for arbitrary positions
    # ------------------------------------------------------------------

    def append(self, value):
        """Add `value` at the TAIL. O(1) thanks to the tail pointer."""
        node = Node(value)
        if self.tail is None:
            # empty list → new node is both head and tail
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1

    def prepend(self, value):
        """Add `value` at the HEAD. O(1)."""
        self.head = Node(value, next=self.head)
        if self.tail is None:
            self.tail = self.head
        self.size += 1

    def insert(self, index, value):
        """
        Insert `value` at position `index`. 0-indexed.
        Shifts subsequent elements right.

        Time: O(n) in general; O(1) at head/tail.
        """
        if not 0 <= index <= self.size:
            raise IndexError(f"index out of range: {index}")

        if index == 0:
            self.prepend(value)
            return
        if index == self.size:
            self.append(value)
            return

        # Walk to the node BEFORE the insertion point
        prev = self.head
        for _ in range(index - 1):
            prev = prev.next

        prev.next = Node(value, next=prev.next)
        self.size += 1

    # ------------------------------------------------------------------
    # Deletion
    # ------------------------------------------------------------------

    def popleft(self):
        """Remove and return the HEAD. O(1). Raises IndexError on empty."""
        if self.head is None:
            raise IndexError("popleft from empty SinglyLinkedList")

        value = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None                      # list became empty
        self.size -= 1
        return value

    def pop(self):
        """
        Remove and return the TAIL. O(n) because we need to find the
        node BEFORE the tail on a singly-linked list.

        For O(1) pop from the tail, use a doubly-linked list.
        """
        if self.head is None:
            raise IndexError("pop from empty SinglyLinkedList")

        if self.head is self.tail:
            # single-element list
            value = self.head.value
            self.head = self.tail = None
            self.size = 0
            return value

        # walk to the second-to-last node
        prev = self.head
        while prev.next is not self.tail:
            prev = prev.next

        value = self.tail.value
        prev.next = None
        self.tail = prev
        self.size -= 1
        return value

    def remove(self, value):
        """
        Remove the FIRST node with the given value.
        Raises ValueError if not found. O(n).

        Uses the DUMMY-HEAD pattern for uniform handling of head deletion.
        """
        dummy = Node(None, next=self.head)
        prev = dummy

        while prev.next is not None:
            if prev.next.value == value:
                # splice out prev.next
                to_remove = prev.next
                prev.next = to_remove.next
                if to_remove is self.tail:
                    self.tail = prev if prev is not dummy else None
                self.head = dummy.next            # may have removed the head
                self.size -= 1
                return

            prev = prev.next

        raise ValueError(f"value not in list: {value!r}")

    def clear(self):
        """Empty the list. O(1) (thanks to Python's GC)."""
        self.head = self.tail = None
        self.size = 0

    # ------------------------------------------------------------------
    # Access — NOT O(1); this is a linked list
    # ------------------------------------------------------------------

    def __getitem__(self, index):
        """O(n) access by index."""
        if not 0 <= index < self.size:
            raise IndexError(f"index out of range: {index}")

        node = self.head
        for _ in range(index):
            node = node.next
        return node.value

    def __contains__(self, value):
        """`value in list` — O(n)."""
        node = self.head
        while node is not None:
            if node.value == value:
                return True
            node = node.next
        return False

    def index(self, value):
        """Return the 0-index of the first occurrence. Raises ValueError if absent."""
        node = self.head
        i = 0
        while node is not None:
            if node.value == value:
                return i
            node = node.next
            i += 1
        raise ValueError(f"value not in list: {value!r}")

    # ------------------------------------------------------------------
    # Iteration and representation
    # ------------------------------------------------------------------

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node.value
            node = node.next

    def __repr__(self):
        return "SinglyLinkedList([" + " → ".join(repr(v) for v in self) + "])"

    def to_list(self):
        """Materialize as a Python list. O(n)."""
        return list(self)


# =========================================================================
# Test the Implementation
# =========================================================================

if __name__ == "__main__":
    # Basic usage
    sll = SinglyLinkedList()
    assert sll.is_empty()
    assert len(sll) == 0

    for x in [1, 2, 3, 4, 5]:
        sll.append(x)
    print(f"After 5 appends: {sll}")
    assert list(sll) == [1, 2, 3, 4, 5]
    assert len(sll) == 5

    # prepend
    sll.prepend(0)
    print(f"After prepend(0): {sll}")
    assert list(sll) == [0, 1, 2, 3, 4, 5]

    # insert
    sll.insert(3, 99)
    print(f"After insert(3, 99): {sll}")
    assert list(sll) == [0, 1, 2, 99, 3, 4, 5]

    # pop from head
    assert sll.popleft() == 0
    assert sll.popleft() == 1
    print(f"After two popleft(): {sll}")
    assert list(sll) == [2, 99, 3, 4, 5]

    # pop from tail
    assert sll.pop() == 5
    print(f"After pop() from tail: {sll}")
    assert list(sll) == [2, 99, 3, 4]

    # remove by value
    sll.remove(99)
    print(f"After remove(99): {sll}")
    assert list(sll) == [2, 3, 4]

    # index / contains
    assert 3 in sll
    assert 100 not in sll
    assert sll.index(3) == 1

    # __getitem__
    assert sll[0] == 2
    assert sll[2] == 4

    # Edge cases: empty operations
    sll.clear()
    assert sll.is_empty()
    try:
        sll.popleft()
    except IndexError:
        pass
    try:
        sll.pop()
    except IndexError:
        pass
    try:
        sll.remove(1)
    except ValueError:
        pass
    try:
        _ = sll[0]
    except IndexError:
        pass

    # Construction from iterable
    sll = SinglyLinkedList(range(5))
    assert list(sll) == [0, 1, 2, 3, 4]
    assert sll.head.value == 0
    assert sll.tail.value == 4

    # Tail correctness after mixed operations
    sll = SinglyLinkedList([1, 2, 3])
    sll.pop()
    assert sll.tail.value == 2
    sll.append(99)
    assert sll.tail.value == 99
    sll.remove(99)
    assert sll.tail.value == 2

    # Stress test against Python's list
    import random
    random.seed(42)

    sll = SinglyLinkedList()
    py = []

    for _ in range(2_000):
        op = random.choice(["append", "prepend", "popleft", "pop",
                            "insert", "remove", "index"])
        if op == "append":
            v = random.randint(0, 100)
            sll.append(v)
            py.append(v)
        elif op == "prepend":
            v = random.randint(0, 100)
            sll.prepend(v)
            py.insert(0, v)
        elif op == "popleft":
            if sll.is_empty():
                continue
            assert sll.popleft() == py.pop(0)
        elif op == "pop":
            if sll.is_empty():
                continue
            assert sll.pop() == py.pop()
        elif op == "insert":
            idx = random.randint(0, len(sll))
            v = random.randint(0, 100)
            sll.insert(idx, v)
            py.insert(idx, v)
        elif op == "remove":
            if not py:
                continue
            v = random.choice(py)
            sll.remove(v)
            py.remove(v)

        # Invariants
        assert list(sll) == py, f"mismatch after {op}: sll={list(sll)} py={py}"
        assert len(sll) == len(py)
        if py:
            assert sll.head.value == py[0]
            assert sll.tail.value == py[-1]
        else:
            assert sll.head is None and sll.tail is None

    print("\nStress test: 2000 random operations — matches Python list exactly")
    print("\nAll tests passed!")
