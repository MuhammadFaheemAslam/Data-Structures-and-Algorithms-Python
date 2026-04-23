"""
Problem: Implement Stack using Queues

Difficulty: Easy (LeetCode #225)

---------------------------------------------------
Problem Statement:

Implement a LIFO stack using ONLY standard queue operations
(push to back, pop from front, size, is_empty).

    push(x)   – add to top
    pop()     – remove and return top
    top()     – peek at top
    empty()   – is stack empty

---------------------------------------------------
The Puzzle:

Queues are FIFO (first in, first out). Stacks are LIFO (last in,
first out). They're OPPOSITE disciplines — so building one from the
other requires some cleverness.

There are two common solutions:

    1. **Two queues, O(n) on PUSH**:
           On push(x), dequeue everything from q1 into q2, enqueue x
           into q1, then dequeue everything from q2 back into q1.
           Now q1 has x at the FRONT (first to dequeue), matching
           stack semantics.

    2. **Two queues, O(n) on POP**:
           Push straight into q1. On pop, move all-but-last from q1
           into q2, dequeue the last from q1 (= the "top"), swap q1 and q2.

We'll implement Version 1 (expensive push, cheap pop) since it's the
common interview expectation. LeetCode #225 accepts either.

    3. **One queue, O(n) on PUSH**: After pushing x, rotate the queue
       n-1 times (dequeue and re-enqueue) to bring x to the front.
       Same complexity; uses only one queue. We implement this too.

---------------------------------------------------
Complexity Summary:

    push:   O(n)   amortized — we rotate the queue
    pop:    O(1)
    top:    O(1)
    empty:  O(1)

(The push-cost/pop-cost tradeoff — O(n) push and O(1) pop — is the
opposite of the "queue using two stacks" problem where push is O(1)
and pop is amortized O(1).)

---------------------------------------------------
"""

from collections import deque


# =========================================================================
# Solution 1: Two Queues, O(n) Push, O(1) Pop
# =========================================================================

class MyStackTwoQueues:
    """
    Stack built from two queues. Push rearranges so the new element
    is always at the FRONT of the main queue.

    push:  O(n)  — rearrange on every push
    pop:   O(1)
    top:   O(1)
    """

    def __init__(self):
        self._q1 = deque()
        self._q2 = deque()

    def push(self, x):
        # Put x at the front of q1 by:
        #   1. Enqueue x into the (empty) q2.
        #   2. Move everything from q1 to q2 after x.
        #   3. Swap q1 and q2.
        self._q2.append(x)
        while self._q1:
            self._q2.append(self._q1.popleft())
        self._q1, self._q2 = self._q2, self._q1

    def pop(self):
        if not self._q1:
            raise IndexError("pop from empty stack")
        return self._q1.popleft()

    def top(self):
        if not self._q1:
            raise IndexError("top on empty stack")
        return self._q1[0]

    def empty(self):
        return not self._q1

    def __len__(self):
        return len(self._q1)


# =========================================================================
# Solution 2: One Queue, O(n) Push, O(1) Pop — Cleaner
# =========================================================================

class MyStackOneQueue:
    """
    Same semantics as MyStackTwoQueues, but uses a single queue.

    On push, ROTATE the queue so that the newly-added element ends up
    at the front.

        push(x):
            enqueue x                     (x goes to the back)
            rotate n - 1 times            (bring x to the front)

    This is the cleaner one-queue solution. Same Big-O as the two-queue
    version.
    """

    def __init__(self):
        self._q = deque()

    def push(self, x):
        self._q.append(x)
        # rotate everything except the newly-appended element
        for _ in range(len(self._q) - 1):
            self._q.append(self._q.popleft())

    def pop(self):
        if not self._q:
            raise IndexError("pop from empty stack")
        return self._q.popleft()

    def top(self):
        if not self._q:
            raise IndexError("top on empty stack")
        return self._q[0]

    def empty(self):
        return not self._q

    def __len__(self):
        return len(self._q)


# =========================================================================
# Solution 3: Two Queues, O(1) Push, O(n) Pop
# =========================================================================

class MyStackLazyPop:
    """
    Lazy version: push is O(1); pop is O(n).

    On pop, move all-but-one element from q1 to q2, then dequeue the
    last from q1 (which is the "top"). Swap queue roles.

    Useful when your workload has many pushes but few pops.
    """

    def __init__(self):
        self._q1 = deque()
        self._q2 = deque()

    def push(self, x):
        self._q1.append(x)

    def pop(self):
        if not self._q1:
            raise IndexError("pop from empty stack")

        # Move all but the last to q2
        while len(self._q1) > 1:
            self._q2.append(self._q1.popleft())

        top = self._q1.popleft()

        # Swap
        self._q1, self._q2 = self._q2, self._q1
        return top

    def top(self):
        if not self._q1:
            raise IndexError("top on empty stack")
        # same as pop but re-enqueue the extracted value
        while len(self._q1) > 1:
            self._q2.append(self._q1.popleft())
        top = self._q1[0]                             # peek; don't pop yet
        self._q2.append(self._q1.popleft())
        self._q1, self._q2 = self._q2, self._q1
        return top

    def empty(self):
        return not self._q1

    def __len__(self):
        return len(self._q1)


# =========================================================================
# Test All Three Implementations
# =========================================================================

if __name__ == "__main__":
    # LeetCode #225 example
    print("LC #225 example — all three implementations:")
    for cls in (MyStackTwoQueues, MyStackOneQueue, MyStackLazyPop):
        s = cls()
        s.push(1)
        s.push(2)
        assert s.top() == 2
        assert s.pop() == 2
        assert s.empty() is False
        assert s.top() == 1
        assert s.pop() == 1
        assert s.empty() is True
        print(f"   {cls.__name__}: passed")
    print()

    # Stress test against Python's list (which IS a stack)
    import random
    random.seed(42)

    for cls in (MyStackTwoQueues, MyStackOneQueue, MyStackLazyPop):
        my = cls()
        ref = []

        for _ in range(2_000):
            op = random.choice(["push", "pop", "top"])
            if op == "push":
                v = random.randint(0, 100)
                my.push(v)
                ref.append(v)
            elif op == "pop":
                if not ref:
                    continue
                assert my.pop() == ref.pop()
            elif op == "top":
                if not ref:
                    continue
                assert my.top() == ref[-1]

            assert len(my) == len(ref)

        print(f"   {cls.__name__} stress test: 2000 ops — passed")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Dual Problem: Queue Using Two Stacks
    #
    # Symmetric elegance: implement a queue using only stacks. The
    # standard solution uses TWO stacks:
    #
    #     stack_in:  enqueue goes here          O(1)
    #     stack_out: dequeue comes from here    O(1) amortized
    #
    #     dequeue():
    #         if stack_out is empty:
    #             while stack_in is non-empty:
    #                 stack_out.push(stack_in.pop())   # transfer
    #         return stack_out.pop()
    #
    # The lazy transfer gives amortized O(1) dequeue. (Every element
    # is pushed onto stack_in once and moved to stack_out once — two
    # ops per element over its lifetime.)
    # ---------------------------------------------------------------
