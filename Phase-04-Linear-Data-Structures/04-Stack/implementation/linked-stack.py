"""
linked-stack.py – Stack Backed by a Singly-Linked List

Same ADT as `array-stack.py`, but storage is a singly-linked list
whose HEAD is the TOP of the stack. The head pointer gives O(1)
push and pop with no hidden resize cost.

---------------------------------------------------
Push / Pop — Both O(1):

    push(x):
        new_node = Node(x, next=head)
        head = new_node

    pop():
        value = head.value
        head = head.next
        return value

---------------------------------------------------
Array-Stack vs Linked-Stack:

    | Metric           | Array-backed        | Linked-backed            |
    |------------------|---------------------|--------------------------|
    | push / pop       | O(1) amortized*     | O(1) (true)              |
    | memory per elem  | ~1 pointer          | 2 pointers + obj overhead |
    | cache behaviour  | Good                | Poor                     |
    | Resize cost      | O(n) rare           | None                     |
    | Implementation   | Trivial             | A few more lines         |

    * amortized because of dynamic-array growth (see 01-Array/theory.md).

Use array-backed unless you have a specific reason (e.g., forbidden
resize pauses in a real-time system). For education: implementing both
makes the ADT/storage distinction concrete.
"""


class _Node:
    """A node in the linked stack — private to this module."""
    __slots__ = ("value", "next")

    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class LinkedStack:
    """
    Stack backed by a singly-linked list. HEAD is TOP.

    Invariants:
        - `_head is None` iff the stack is empty.
        - `_size` is always the count of nodes.
    """

    def __init__(self, iterable=None):
        self._head = None
        self._size = 0
        if iterable is not None:
            for x in iterable:
                self.push(x)

    # ------------------------------------------------------------------
    # Core stack operations — all O(1)
    # ------------------------------------------------------------------

    def push(self, value):
        """Add `value` to the top. O(1)."""
        self._head = _Node(value, next=self._head)
        self._size += 1

    def pop(self):
        """Remove and return the top. O(1). Raises IndexError on empty."""
        if self._head is None:
            raise IndexError("pop from empty LinkedStack")

        value = self._head.value
        self._head = self._head.next
        self._size -= 1
        return value

    def peek(self):
        """Return the top without removing. O(1)."""
        if self._head is None:
            raise IndexError("peek at empty LinkedStack")
        return self._head.value

    # ------------------------------------------------------------------
    # Size queries
    # ------------------------------------------------------------------

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._head is None

    def __bool__(self):
        return self._head is not None

    # ------------------------------------------------------------------
    # Iteration and display
    # ------------------------------------------------------------------

    def __iter__(self):
        """Iterate from TOP to bottom."""
        node = self._head
        while node is not None:
            yield node.value
            node = node.next

    def __repr__(self):
        return "LinkedStack([" + ", ".join(repr(x) for x in self) + "] <- top)"

    def __contains__(self, value):
        """`x in stack` — O(n)."""
        for v in self:
            if v == value:
                return True
        return False


# =========================================================================
# Test the Stack
# =========================================================================

if __name__ == "__main__":
    s = LinkedStack()
    assert s.is_empty()
    assert len(s) == 0
    assert not s                                   # __bool__ on empty → False

    for x in [1, 2, 3]:
        s.push(x)
    print(f"After pushing 1, 2, 3: {s}")
    assert len(s) == 3
    assert s.peek() == 3

    assert s.pop() == 3
    assert s.pop() == 2
    assert s.peek() == 1
    print(f"After two pops: {s}")

    s.push(100)
    s.push(200)
    print(f"After pushing 100, 200: {s}")
    # Iteration is top→bottom, so 200 first
    assert list(s) == [200, 100, 1]

    # Edge cases
    s2 = LinkedStack()
    try:
        s2.pop()
    except IndexError as e:
        print(f"\npop empty: {e}")
    try:
        s2.peek()
    except IndexError as e:
        print(f"peek empty: {e}")

    # Construction from iterable
    s = LinkedStack([1, 2, 3, 4, 5])
    assert len(s) == 5
    assert s.peek() == 5

    # Stress test vs Python list
    import random
    random.seed(42)

    stack = LinkedStack()
    py = []

    for _ in range(2_000):
        op = random.choice(["push", "pop", "peek"])
        if op == "push":
            v = random.randint(0, 100)
            stack.push(v)
            py.append(v)
        elif op == "pop":
            if not py:
                continue
            assert stack.pop() == py.pop()
        elif op == "peek":
            if not py:
                continue
            assert stack.peek() == py[-1]

        assert len(stack) == len(py)
        assert list(stack) == list(reversed(py))

    print("\nStress test: 2000 random ops — matches Python list")
    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Array vs Linked — Which to Pick?
    #
    #   In Python, array-backed is almost always the right choice:
    #     - Simpler.
    #     - Faster in practice (cache locality, fewer indirections).
    #     - `list.append` and `list.pop` are written in C.
    #
    #   Linked-stack's niche:
    #     - You're on a platform where memory resizes are expensive
    #       or forbidden (real-time, embedded).
    #     - You need to SHARE tail-structure between stacks (persistent
    #       data structures — unusual in Python but common in Haskell).
    #
    # For learning: implementing both makes the "ADT vs implementation"
    # distinction crisp. For production Python: just use list.
    # ---------------------------------------------------------------
