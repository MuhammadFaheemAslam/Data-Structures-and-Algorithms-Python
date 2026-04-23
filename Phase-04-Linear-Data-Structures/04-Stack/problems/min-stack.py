"""
Problem: Min Stack

Difficulty: Medium (LeetCode #155)

---------------------------------------------------
Problem Statement:

Design a stack that supports push, pop, peek, AND retrieving the
MINIMUM element, all in **O(1)** time.

    push(x)
    pop()
    top()
    get_min()   ← the interesting one

---------------------------------------------------
The Trick: A Second Stack of Minima

Naive approach: scan the stack for min on every `get_min()`. That's
O(n). Unacceptable.

Smart approach: keep a PARALLEL STACK of "the minimum up to here."

    main stack:  [5, 3, 7, 2, 6]
    min stack:   [5, 3, 3, 2, 2]

After every push(x):
    new_min = min(x, current min_stack top)
    push new_min onto min_stack

After every pop:
    also pop from min_stack

After every get_min():
    just return min_stack[-1]

All four operations: O(1). Space: O(n) — one extra int per element.

---------------------------------------------------
Optimization: Store Only When the Min Changes

A subtle improvement: the min stack only needs an entry when a NEW
minimum is pushed. On pop, we only pop from the min stack if the
popped value EQUALS the current min.

    main stack:  [5, 3, 7, 2, 6]
    min stack:   [5, 3, 2]           # only unique minima

Same Big-O, better constant factor when values are mostly non-decreasing.

We implement both versions.

---------------------------------------------------
"""


# =========================================================================
# Solution 1: Twin-Stack Implementation (Simplest)
# =========================================================================

class MinStackTwinStacks:
    """
    Min-Stack via two parallel stacks.

    Every push puts the running min onto the min_stack, so each pop
    can also pop from min_stack. All ops O(1); space O(n).
    """

    def __init__(self):
        self._data = []
        self._mins = []

    def push(self, x):
        self._data.append(x)
        self._mins.append(x if not self._mins else min(x, self._mins[-1]))

    def pop(self):
        if not self._data:
            raise IndexError("pop from empty stack")
        self._mins.pop()
        return self._data.pop()

    def top(self):
        if not self._data:
            raise IndexError("top on empty stack")
        return self._data[-1]

    def get_min(self):
        if not self._mins:
            raise IndexError("get_min on empty stack")
        return self._mins[-1]

    def __len__(self):
        return len(self._data)


# =========================================================================
# Solution 2: Optimized — Store Min Only When It Changes
# =========================================================================

class MinStackOptimized:
    """
    Min-Stack where the min_stack only records a value when the
    current push becomes the new minimum.

    Saves memory when values are mostly non-decreasing. Same Big-O.
    """

    def __init__(self):
        self._data = []
        self._mins = []                           # only UNIQUE minima in descending order (deepest first)

    def push(self, x):
        self._data.append(x)
        if not self._mins or x <= self._mins[-1]:
            self._mins.append(x)                   # new (tied) minimum

    def pop(self):
        if not self._data:
            raise IndexError("pop from empty stack")
        x = self._data.pop()
        if x == self._mins[-1]:
            self._mins.pop()
        return x

    def top(self):
        if not self._data:
            raise IndexError("top on empty stack")
        return self._data[-1]

    def get_min(self):
        if not self._mins:
            raise IndexError("get_min on empty stack")
        return self._mins[-1]

    def __len__(self):
        return len(self._data)


# =========================================================================
# Solution 3: Single-Stack with Delta Encoding — O(1) Space Overhead Per Op
# =========================================================================

class MinStackSingleStack:
    """
    Clever O(n) extra space, single stack: instead of storing values
    directly, store the DIFFERENCE between the pushed value and the
    current min. That difference is negative exactly when the new
    value is a new min.

    Complicated to get right, interesting to see. Use the twin-stack
    version in any interview; this one is more of a puzzle.
    """

    def __init__(self):
        self._stack = []                          # stores "x - current_min" diffs
        self._min = None

    def push(self, x):
        if not self._stack:
            self._stack.append(0)
            self._min = x
        else:
            diff = x - self._min
            self._stack.append(diff)
            if diff < 0:
                self._min = x                     # new min

    def pop(self):
        if not self._stack:
            raise IndexError("pop from empty stack")
        diff = self._stack.pop()
        if diff < 0:
            # the element being popped WAS the min; the old min is
            # min - diff (reversing the push-time relation)
            result = self._min
            self._min = self._min - diff          # restore old min
            return result
        else:
            # the element being popped was NOT the min; its value is
            # min + diff
            return self._min + diff

    def top(self):
        if not self._stack:
            raise IndexError("top on empty stack")
        diff = self._stack[-1]
        return self._min if diff < 0 else self._min + diff

    def get_min(self):
        if not self._stack:
            raise IndexError("get_min on empty stack")
        return self._min

    def __len__(self):
        return len(self._stack)


# =========================================================================
# Test the Implementations
# =========================================================================

if __name__ == "__main__":
    # LC #155 canonical example
    print("LC #155 example — all three implementations:")
    for cls in (MinStackTwinStacks, MinStackOptimized, MinStackSingleStack):
        s = cls()
        s.push(-2)
        s.push(0)
        s.push(-3)
        assert s.get_min() == -3
        assert s.pop() == -3
        assert s.top() == 0
        assert s.get_min() == -2
        print(f"   {cls.__name__}: passed")
    print()

    # More scenarios
    scenarios = [
        # Pattern: all equal
        [(1, "p"), (1, "p"), (1, "p"), ("min", 1), ("pop", 1), ("min", 1), ("pop", 1), ("min", 1)],
        # Pattern: strictly decreasing
        [(5, "p"), (4, "p"), (3, "p"), (2, "p"), (1, "p"), ("min", 1), ("pop", 1), ("min", 2), ("pop", 2), ("min", 3)],
        # Pattern: strictly increasing
        [(1, "p"), (2, "p"), (3, "p"), ("min", 1), ("pop", 3), ("min", 1), ("pop", 2), ("min", 1)],
        # Pattern: mixed
        [(3, "p"), (1, "p"), (2, "p"), ("min", 1), ("pop", 2), ("min", 1), ("pop", 1), ("min", 3)],
    ]

    for i, ops in enumerate(scenarios):
        for cls in (MinStackTwinStacks, MinStackOptimized, MinStackSingleStack):
            s = cls()
            for op in ops:
                if op[1] == "p":
                    s.push(op[0])
                elif op[0] == "pop":
                    assert s.pop() == op[1]
                elif op[0] == "min":
                    assert s.get_min() == op[1]
        print(f"Scenario {i+1} passed on all three implementations")
    print()

    # Stress test — compare all three against a reference (brute force)
    import random
    random.seed(42)

    class ReferenceMinStack:
        """Brute-force reference: scan for min on each call."""
        def __init__(self):
            self.data = []
        def push(self, x):
            self.data.append(x)
        def pop(self):
            if not self.data:
                raise IndexError
            return self.data.pop()
        def top(self):
            if not self.data:
                raise IndexError
            return self.data[-1]
        def get_min(self):
            if not self.data:
                raise IndexError
            return min(self.data)
        def __len__(self):
            return len(self.data)

    for trial in range(100):
        ref = ReferenceMinStack()
        a = MinStackTwinStacks()
        b = MinStackOptimized()
        c = MinStackSingleStack()

        for _ in range(500):
            op = random.choice(["push", "pop", "top", "min"])
            if op == "push":
                v = random.randint(-100, 100)
                ref.push(v); a.push(v); b.push(v); c.push(v)
            elif op == "pop":
                if not ref.data:
                    continue
                r = ref.pop()
                assert a.pop() == r == b.pop() == c.pop()
            elif op == "top":
                if not ref.data:
                    continue
                assert a.top() == ref.top() == b.top() == c.top()
            elif op == "min":
                if not ref.data:
                    continue
                assert a.get_min() == ref.get_min() == b.get_min() == c.get_min()

            assert len(ref) == len(a) == len(b) == len(c)

    print("Stress test: 100 trials × 500 ops — all three implementations agree with reference")

    print("\nAll tests passed!")
