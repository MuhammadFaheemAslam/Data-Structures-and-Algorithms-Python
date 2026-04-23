"""
array-stack.py – Stack Backed by a Python list (Array)

A stack implemented on top of a Python `list`. The END of the list
is the TOP of the stack:

    push(x)  →  self._data.append(x)       O(1) amortized
    pop()    →  self._data.pop()           O(1)
    peek()   →  self._data[-1]             O(1)

Simplest possible stack implementation. In production Python, you'd
usually just use a `list` directly — this class exists to make the
stack INTERFACE explicit (so callers can't accidentally use non-stack
operations like random-access or insert-in-middle).

---------------------------------------------------
Complexity:

    All operations O(1) amortized (due to `list`'s dynamic-array growth).
"""


class ArrayStack:
    """
    LIFO stack backed by a Python `list`.

    Behaves like `list` if you only use `.append()` and `.pop()` —
    but adds error messages for empty-pop and hides anything that
    would violate the stack discipline.
    """

    def __init__(self, iterable=None):
        self._data = []
        if iterable is not None:
            for x in iterable:
                self._data.append(x)

    # ------------------------------------------------------------------
    # Core stack operations
    # ------------------------------------------------------------------

    def push(self, value):
        """Add `value` to the top. O(1) amortized."""
        self._data.append(value)

    def pop(self):
        """Remove and return the top. O(1). Raises IndexError on empty."""
        if not self._data:
            raise IndexError("pop from empty ArrayStack")
        return self._data.pop()

    def peek(self):
        """Return the top without removing. O(1). Raises IndexError on empty."""
        if not self._data:
            raise IndexError("peek at empty ArrayStack")
        return self._data[-1]

    # ------------------------------------------------------------------
    # Size queries
    # ------------------------------------------------------------------

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return len(self._data) == 0

    def __bool__(self):
        """`if stack:` → True iff non-empty."""
        return len(self._data) != 0

    # ------------------------------------------------------------------
    # Iteration, display, and safety
    # ------------------------------------------------------------------

    def __iter__(self):
        """
        Iterate from TOP to bottom.

        Note: iteration order matches what you'd see if you popped
        the stack one by one. If you want bottom-to-top, use
        `iter(stack._data)` or reverse the output.
        """
        return reversed(self._data)

    def __repr__(self):
        return "ArrayStack([" + ", ".join(repr(x) for x in self._data) + "] <- top)"

    def __contains__(self, value):
        """`x in stack` — O(n). Shouldn't normally be needed on a stack."""
        return value in self._data


# =========================================================================
# Test the Stack
# =========================================================================

if __name__ == "__main__":
    s = ArrayStack()
    assert s.is_empty()
    assert len(s) == 0

    # Push
    for x in [1, 2, 3]:
        s.push(x)
    print(f"After pushing 1, 2, 3: {s}")
    assert len(s) == 3
    assert s.peek() == 3

    # Pop
    assert s.pop() == 3
    assert s.pop() == 2
    assert s.peek() == 1
    assert len(s) == 1
    print(f"After two pops: {s}")

    # Push more
    s.push(10)
    s.push(20)
    print(f"After pushing 10, 20: {s}")
    assert list(s) == [20, 10, 1]                 # iteration is top→bottom

    # Edge cases
    s2 = ArrayStack()
    try:
        s2.pop()
    except IndexError as e:
        print(f"\npop empty: {e}")
    try:
        s2.peek()
    except IndexError as e:
        print(f"peek empty: {e}")

    # Truthiness
    assert not ArrayStack()
    assert ArrayStack([1])

    # Construction from iterable
    s = ArrayStack([1, 2, 3, 4, 5])
    assert len(s) == 5
    assert s.peek() == 5                          # last pushed is on top

    # Stress test against Python's list
    import random
    random.seed(42)

    stack = ArrayStack()
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

    print("\nStress test: 2000 random ops — matches Python's list")
    print("\nAll tests passed!")
