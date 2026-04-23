"""
implementation.py – Doubly Linked List (from scratch)

A doubly linked list where each node has both `prev` and `next` pointers.
This unlocks:

    - O(1) insert/delete at either end
    - O(1) insert/delete given a NODE reference (no predecessor walk)
    - O(1) reverse iteration

The cost: one extra pointer per node, and more bookkeeping on edits.

---------------------------------------------------
The Sentinel-Node Trick (Used Here):

Instead of `head = None` / `tail = None` for an empty list, we use
two SENTINEL nodes — `_head` and `_tail` — that always exist and
flank the real data:

    _head ↔ [A] ↔ [B] ↔ [C] ↔ _tail

Empty list:  _head ↔ _tail

This eliminates almost all "is this the first/last node?" edge cases.
Every real node always has a prev and a next (sentinel or real).

It's the DLL equivalent of the dummy-head pattern on SLLs, pushed to
both ends.

---------------------------------------------------
Complexity:

    append(x), appendleft(x)     O(1)
    pop(), popleft()             O(1)
    insert_before(node, x)       O(1)     — given a node reference
    insert_after(node, x)        O(1)     — given a node reference
    remove(node)                 O(1)     — given a node reference
    get_at(i), insert_at(i, x)   O(n)     — must walk to position i
    __contains__(x), index(x)    O(n)
    __len__                      O(1)
    iteration forward / reverse  O(n)

The O(1) removal given just a node reference is what the LRU cache
depends on (see problems/lru-cache.py).
"""


# =========================================================================
# Node
# =========================================================================

class DNode:
    """A node in a doubly linked list."""

    __slots__ = ("value", "prev", "next")

    def __init__(self, value, prev=None, next=None):
        self.value = value
        self.prev = prev
        self.next = next

    def __repr__(self):
        return f"DNode({self.value!r})"


# =========================================================================
# Doubly Linked List
# =========================================================================

class DoublyLinkedList:
    """
    A doubly linked list with sentinel head and tail nodes.

    The sentinels mean every "real" node always has both prev and
    next pointers pointing at SOMETHING — eliminating the special
    cases you'd need with None pointers at the boundaries.
    """

    def __init__(self, iterable=None):
        # Sentinel nodes. _head.next is the first real node; _tail.prev
        # is the last real node. _head's prev and _tail's next are always None.
        self._head = DNode(None)
        self._tail = DNode(None)
        self._head.next = self._tail
        self._tail.prev = self._head
        self._size = 0

        if iterable is not None:
            for x in iterable:
                self.append(x)

    # ------------------------------------------------------------------
    # Size queries
    # ------------------------------------------------------------------

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    # ------------------------------------------------------------------
    # Core primitive: splice in / splice out a node — O(1) each
    # ------------------------------------------------------------------

    def _insert_between(self, value, left, right):
        """Insert a new node between `left` and `right`. O(1)."""
        node = DNode(value, prev=left, next=right)
        left.next = node
        right.prev = node
        self._size += 1
        return node

    def _remove_node(self, node):
        """Unlink `node` from the list. O(1). Node must be non-sentinel."""
        assert node is not self._head and node is not self._tail
        node.prev.next = node.next
        node.next.prev = node.prev
        node.prev = node.next = None               # detach the removed node entirely
        self._size -= 1

    # ------------------------------------------------------------------
    # Insertion at the ends — O(1)
    # ------------------------------------------------------------------

    def append(self, value):
        """Add `value` at the TAIL. O(1)."""
        return self._insert_between(value, self._tail.prev, self._tail)

    def appendleft(self, value):
        """Add `value` at the HEAD. O(1)."""
        return self._insert_between(value, self._head, self._head.next)

    # ------------------------------------------------------------------
    # Removal at the ends — O(1)
    # ------------------------------------------------------------------

    def pop(self):
        """Remove and return the tail value. O(1). Raises IndexError on empty."""
        if self.is_empty():
            raise IndexError("pop from empty DoublyLinkedList")
        node = self._tail.prev
        value = node.value
        self._remove_node(node)
        return value

    def popleft(self):
        """Remove and return the head value. O(1). Raises IndexError on empty."""
        if self.is_empty():
            raise IndexError("popleft from empty DoublyLinkedList")
        node = self._head.next
        value = node.value
        self._remove_node(node)
        return value

    # ------------------------------------------------------------------
    # Insert / remove given a NODE reference — O(1)
    # This is what makes DLLs powerful for LRU cache and similar.
    # ------------------------------------------------------------------

    def insert_before(self, node, value):
        """Insert a new node BEFORE the given reference node. O(1)."""
        if node is self._head:
            raise ValueError("cannot insert before the sentinel head")
        return self._insert_between(value, node.prev, node)

    def insert_after(self, node, value):
        """Insert a new node AFTER the given reference node. O(1)."""
        if node is self._tail:
            raise ValueError("cannot insert after the sentinel tail")
        return self._insert_between(value, node, node.next)

    def remove_node(self, node):
        """Remove the given node. O(1)."""
        self._remove_node(node)

    def move_to_front(self, node):
        """
        Unlink `node` and re-insert at the head. O(1). Used heavily in LRU caches.
        """
        self._remove_node(node)
        self._size += 1                             # remove dec'd it; we'll re-insert
        # Splice between head and old head.next
        node.prev = self._head
        node.next = self._head.next
        self._head.next.prev = node
        self._head.next = node

    # ------------------------------------------------------------------
    # Indexed operations — O(n)
    # ------------------------------------------------------------------

    def insert_at(self, index, value):
        """Insert at position `index`. O(n) to walk to the position."""
        if not 0 <= index <= self._size:
            raise IndexError(f"index out of range: {index}")

        # Decide which direction to walk from
        if index <= self._size // 2:
            left = self._head
            for _ in range(index):
                left = left.next
        else:
            left = self._tail
            for _ in range(self._size - index):
                left = left.prev
            left = left.prev

        return self._insert_between(value, left, left.next)

    def __getitem__(self, index):
        """Access by index. O(n)."""
        if not 0 <= index < self._size:
            raise IndexError(f"index out of range: {index}")

        # walk from whichever end is closer
        if index < self._size // 2:
            node = self._head.next
            for _ in range(index):
                node = node.next
        else:
            node = self._tail.prev
            for _ in range(self._size - 1 - index):
                node = node.prev

        return node.value

    def remove(self, value):
        """Remove the first node with the given value. O(n). Raises ValueError if absent."""
        node = self._head.next
        while node is not self._tail:
            if node.value == value:
                self._remove_node(node)
                return
            node = node.next
        raise ValueError(f"value not in list: {value!r}")

    # ------------------------------------------------------------------
    # Iteration (forward and reverse)
    # ------------------------------------------------------------------

    def __iter__(self):
        node = self._head.next
        while node is not self._tail:
            yield node.value
            node = node.next

    def __reversed__(self):
        node = self._tail.prev
        while node is not self._head:
            yield node.value
            node = node.prev

    def __contains__(self, value):
        return any(v == value for v in self)

    # ------------------------------------------------------------------
    # Repr and equality
    # ------------------------------------------------------------------

    def __repr__(self):
        return "DLL([" + " ↔ ".join(repr(v) for v in self) + "])"

    def __eq__(self, other):
        if isinstance(other, DoublyLinkedList):
            return list(self) == list(other)
        if isinstance(other, list):
            return list(self) == other
        return NotImplemented


# =========================================================================
# Test the Implementation
# =========================================================================

if __name__ == "__main__":
    # Basic
    dll = DoublyLinkedList()
    assert dll.is_empty()
    assert len(dll) == 0

    dll.append(1)
    dll.append(2)
    dll.append(3)
    print(f"After appends: {dll}")
    assert list(dll) == [1, 2, 3]

    dll.appendleft(0)
    print(f"After appendleft(0): {dll}")
    assert list(dll) == [0, 1, 2, 3]

    assert dll.pop() == 3
    assert dll.popleft() == 0
    print(f"After pop + popleft: {dll}")
    assert list(dll) == [1, 2]

    # insert_at
    dll.insert_at(0, 99)
    assert list(dll) == [99, 1, 2]
    dll.insert_at(3, 100)
    assert list(dll) == [99, 1, 2, 100]
    dll.insert_at(2, 50)
    assert list(dll) == [99, 1, 50, 2, 100]
    print(f"After inserts at various positions: {dll}")

    # Access
    assert dll[0] == 99
    assert dll[2] == 50
    assert dll[-1 + len(dll)] == 100                # last element

    # Reverse iteration
    assert list(reversed(dll)) == [100, 2, 50, 1, 99]
    print(f"Reversed: {list(reversed(dll))}")

    # Remove by value
    dll.remove(50)
    assert list(dll) == [99, 1, 2, 100]

    # O(1) operations given a node reference
    dll.clear = None                                # don't need it; just a lint-style check
    dll = DoublyLinkedList([1, 2, 3, 4, 5])
    # Get a reference to a specific node
    ref_node = dll._head.next.next                  # the "2" node
    assert ref_node.value == 2

    dll.remove_node(ref_node)
    print(f"After remove_node(the '2'): {dll}")
    assert list(dll) == [1, 3, 4, 5]

    # Move-to-front (the LRU-cache primitive)
    dll = DoublyLinkedList([1, 2, 3, 4, 5])
    target = dll._head.next.next.next               # the "3" node
    dll.move_to_front(target)
    assert list(dll) == [3, 1, 2, 4, 5]
    print(f"After move_to_front('3'): {dll}")

    # Edge cases
    empty = DoublyLinkedList()
    try:
        empty.pop()
    except IndexError as e:
        print(f"\nempty.pop(): {e}")
    try:
        empty.popleft()
    except IndexError as e:
        print(f"empty.popleft(): {e}")

    # Stress test
    import random
    random.seed(42)

    dll = DoublyLinkedList()
    py = []

    for _ in range(2_000):
        op = random.choice(["append", "appendleft", "pop", "popleft", "insert", "remove"])
        if op == "append":
            v = random.randint(0, 100)
            dll.append(v)
            py.append(v)
        elif op == "appendleft":
            v = random.randint(0, 100)
            dll.appendleft(v)
            py.insert(0, v)
        elif op == "pop":
            if not py:
                continue
            assert dll.pop() == py.pop()
        elif op == "popleft":
            if not py:
                continue
            assert dll.popleft() == py.pop(0)
        elif op == "insert":
            idx = random.randint(0, len(dll))
            v = random.randint(0, 100)
            dll.insert_at(idx, v)
            py.insert(idx, v)
        elif op == "remove":
            if not py:
                continue
            v = random.choice(py)
            dll.remove(v)
            py.remove(v)

        assert list(dll) == py
        assert list(reversed(dll)) == list(reversed(py))
        assert len(dll) == len(py)

    print("\nStress test: 2000 random operations — matches Python list (fwd + reverse)")
    print("\nAll tests passed!")
