"""
implementation.py – Circular Linked List (Singly and Doubly)

A circular linked list is an SLL (or DLL) where the LAST node's `next`
points back to the HEAD instead of None. Traversal never hits a
terminal — you loop until you come back to where you started.

    SLL:  head → A → B → C → D → head (wraps)
    DLL:  head ↔ A ↔ B ↔ C ↔ D ↔ head (both directions wrap)

---------------------------------------------------
When Is This Useful?

    - **Round-robin scheduling.** Next task = current.next; naturally
      wraps to the first once you've gone around.
    - **Cyclic buffers.** Audio/video ring buffers, TCP send queues.
    - **Game turn order.** After the last player, it's the first
      player's turn again — exactly the SLL semantics.
    - **Josephus problem** (people in a circle eliminating every kth)
      — a classic use of circular linked lists.

In production, most of these are implemented as arrays with modular
indexing (`i = (i + 1) % n`) — simpler, cache-friendly. But on the
theoretical side, circular linked lists are the "correct" abstraction.

---------------------------------------------------
Key Implementation Trick:

For the SLL version, we keep ONLY a `tail` pointer (not `head`).
That's because on a circular list:

    - `tail` gives O(1) access to the head (it's `tail.next`).
    - `tail` gives O(1) append (the new node becomes tail).
    - `tail` gives O(1) prepend (set new node's next to current head;
      `tail.next = new node` — done, no head update).

This is the elegant "single pointer for a circular structure" trick.

---------------------------------------------------
"""


# =========================================================================
# Circular SLL — Single Tail Pointer
# =========================================================================

class Node:
    """Node for a circular singly-linked list."""
    __slots__ = ("value", "next")

    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class CircularSLL:
    """
    Circular singly-linked list using only a `tail` pointer.

    Invariants:
        - If `size == 0`: `tail is None`.
        - Else: `tail` points to the last node, and `tail.next`
          points to the first node (the head).
    """

    def __init__(self, iterable=None):
        self._tail = None
        self._size = 0

        if iterable is not None:
            for x in iterable:
                self.append(x)

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    @property
    def head(self):
        """Return the first node (or None if empty)."""
        return self._tail.next if self._tail else None

    @property
    def tail(self):
        return self._tail

    # ------------------------------------------------------------------
    # Insertion — all O(1)
    # ------------------------------------------------------------------

    def append(self, value):
        """Insert at the tail. O(1)."""
        node = Node(value)
        if self._tail is None:
            # empty list: node points to itself
            node.next = node
        else:
            node.next = self._tail.next
            self._tail.next = node
        self._tail = node
        self._size += 1

    def prepend(self, value):
        """Insert at the head. O(1) — we don't move `tail`, just splice."""
        node = Node(value)
        if self._tail is None:
            node.next = node
            self._tail = node
        else:
            node.next = self._tail.next           # new head's next = old head
            self._tail.next = node                # tail's next = new head
        self._size += 1

    # ------------------------------------------------------------------
    # Removal — O(1) at head, O(n) at tail (need to find its predecessor)
    # ------------------------------------------------------------------

    def popleft(self):
        """Remove and return the head value. O(1)."""
        if self._tail is None:
            raise IndexError("popleft from empty CircularSLL")

        head = self._tail.next
        value = head.value

        if self._size == 1:
            self._tail = None
        else:
            self._tail.next = head.next

        self._size -= 1
        return value

    def pop(self):
        """
        Remove and return the tail value. O(n) — we must walk to find
        the node BEFORE the tail. Same limitation as a non-circular SLL.
        """
        if self._tail is None:
            raise IndexError("pop from empty CircularSLL")

        if self._size == 1:
            value = self._tail.value
            self._tail = None
            self._size = 0
            return value

        # walk to the second-to-last node
        prev = self._tail.next                    # start at head
        while prev.next is not self._tail:
            prev = prev.next

        value = self._tail.value
        prev.next = self._tail.next               # close the circle without tail
        self._tail = prev
        self._size -= 1
        return value

    def remove(self, value):
        """Remove the FIRST node with the given value. O(n)."""
        if self._tail is None:
            raise ValueError(f"value not in list: {value!r}")

        prev = self._tail
        curr = prev.next                          # start at head
        for _ in range(self._size):
            if curr.value == value:
                # splice it out
                prev.next = curr.next
                if curr is self._tail:
                    self._tail = prev if self._size > 1 else None
                self._size -= 1
                return
            prev = curr
            curr = curr.next

        raise ValueError(f"value not in list: {value!r}")

    # ------------------------------------------------------------------
    # Iteration
    # ------------------------------------------------------------------

    def __iter__(self):
        """Yield each element once (stops after a full loop)."""
        if self._tail is None:
            return
        node = self._tail.next                    # start at head
        for _ in range(self._size):
            yield node.value
            node = node.next

    def rotate(self, k):
        """
        Rotate the list so that the k-th-from-head element becomes the head.

        In a circular list, "rotation" is free — we just advance the
        `tail` pointer by k steps. O(k mod n).
        """
        if self._tail is None or self._size == 1:
            return
        k = k % self._size
        for _ in range(k):
            self._tail = self._tail.next

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def __repr__(self):
        if self._tail is None:
            return "CircularSLL([])"
        return "CircularSLL([" + " → ".join(repr(v) for v in self) + " → ↩])"


# =========================================================================
# The Josephus Problem (Classic Circular-LL Application)
# =========================================================================

def josephus(n, k):
    """
    n people stand in a circle, numbered 1 to n. Starting from person 1,
    we count k people and eliminate the kth. Then we continue from the
    next person. Return the position of the last survivor.

    Example: n=5, k=2
        Eliminate 2, 4, 1, 5 → survivor = 3

    Time:  O(n * k)
    Space: O(n)

    The classical linked-list solution. A closed-form mathematical
    solution exists (O(n) without the linked list), but this version
    showcases the data structure.
    """
    if n <= 0 or k <= 0:
        raise ValueError("n and k must be positive")

    people = CircularSLL(range(1, n + 1))

    # Start at the head; advance (k - 1) times, remove.
    # We need a pointer to "the person BEFORE the one we're about to remove"
    # so we can splice efficiently. The CircularSLL.remove helper does this
    # at O(n), but for n rounds the total is O(n²). For n rounds with explicit
    # pointer tracking, we can get O(n * k).
    current = people._tail                        # predecessor of head
    while people._size > 1:
        # Step k - 1 to reach the predecessor of the next victim
        for _ in range(k - 1):
            current = current.next
        # Victim is current.next
        victim = current.next
        current.next = victim.next
        # Adjust tail if we removed it
        if victim is people._tail:
            people._tail = current
        people._size -= 1

    return people.head.value


# =========================================================================
# Test the Implementation
# =========================================================================

if __name__ == "__main__":
    # Basic
    cll = CircularSLL()
    assert cll.is_empty()
    for x in [1, 2, 3, 4, 5]:
        cll.append(x)
    print(f"After appends: {cll}")
    assert list(cll) == [1, 2, 3, 4, 5]
    assert cll.head.value == 1
    assert cll.tail.value == 5
    assert cll.tail.next is cll.head               # the circle closes

    # Prepend
    cll.prepend(0)
    print(f"After prepend(0): {cll}")
    assert list(cll) == [0, 1, 2, 3, 4, 5]
    assert cll.head.value == 0
    assert cll.tail.next is cll.head

    # popleft / pop
    assert cll.popleft() == 0
    assert list(cll) == [1, 2, 3, 4, 5]
    assert cll.pop() == 5
    assert list(cll) == [1, 2, 3, 4]
    print(f"After popleft + pop: {cll}")

    # remove by value
    cll.remove(2)
    assert list(cll) == [1, 3, 4]

    # Rotate: shifts the "start" forward by k. After rotate(k), the
    # element originally at index k becomes the new head.
    cll = CircularSLL([1, 2, 3, 4, 5])
    cll.rotate(2)                                  # head moves from index 0 to index 2
    print(f"After rotate(2): {cll}")
    assert list(cll) == [3, 4, 5, 1, 2]
    cll.rotate(8)                                  # 8 mod 5 = 3; head moves from 0 to 3 of current list
    assert list(cll) == [1, 2, 3, 4, 5]             # back to original (2 + 3 = 5 ≡ 0 mod 5)

    # Empty-list edge cases
    empty = CircularSLL()
    try:
        empty.popleft()
    except IndexError as e:
        print(f"\nempty.popleft(): {e}")
    try:
        empty.pop()
    except IndexError as e:
        print(f"empty.pop(): {e}")
    try:
        empty.remove(5)
    except ValueError as e:
        print(f"empty.remove(5): {e}")

    # Single-element edge cases
    one = CircularSLL([42])
    assert one.head is one.tail
    assert one.tail.next is one.tail               # single node points at itself
    assert one.pop() == 42
    assert one.is_empty()

    # Circularity check — iterate `size` times without infinite loop
    cll = CircularSLL([1, 2, 3])
    node = cll.head
    seen = []
    for _ in range(3 * 5):                         # loop 5 full rounds
        seen.append(node.value)
        node = node.next
    assert seen == [1, 2, 3] * 5
    print(f"\n5 full rounds: {seen}")

    # Josephus
    print("\nJosephus problem:")
    josephus_cases = [
        (5,  2,  3),                               # classic: n=5, k=2 → survivor 3
        (7,  3,  4),
        (1,  1,  1),
        (10, 1,  10),                              # k=1 → every person eliminated in order
        (6,  5,  1),
    ]
    for n, k, expected in josephus_cases:
        got = josephus(n, k)
        assert got == expected, f"josephus({n}, {k}) = {got}, expected {expected}"
        print(f"   josephus(n={n}, k={k}) = {got}")

    # Stress test — compare against a Python-list-based reference
    import random
    random.seed(42)

    def josephus_list(n, k):
        """Reference implementation using a Python list."""
        people = list(range(1, n + 1))
        idx = 0
        while len(people) > 1:
            idx = (idx + k - 1) % len(people)
            people.pop(idx)
        return people[0]

    for _ in range(50):
        n = random.randint(1, 20)
        k = random.randint(1, 15)
        assert josephus(n, k) == josephus_list(n, k), f"josephus({n}, {k}) mismatch"

    print("\nStress test: 50 random Josephus configs — matches list reference")
    print("\nAll tests passed!")
