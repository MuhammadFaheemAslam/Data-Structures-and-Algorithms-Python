"""
Problem: Linked List Cycle

Difficulty: Easy (LeetCode #141)

---------------------------------------------------
Problem Statement:

Given the head of a linked list, return True iff the list contains
a cycle — i.e., some node can be reached again by walking forward
through `next` pointers.

Follow-up: can you do it in O(1) extra space?

---------------------------------------------------
Two Approaches:

    1. Floyd's Tortoise and Hare   O(n) time, O(1) space   ← the intended answer
    2. Hash set of visited nodes   O(n) time, O(n) space

Floyd's is the required follow-up answer. The hash-set version is
simpler to reason about; use it when O(n) space is acceptable.

---------------------------------------------------
"""


# =========================================================================
# Minimal ListNode
# =========================================================================

class ListNode:
    __slots__ = ("val", "next")

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build_list(values, cycle_index=-1):
    """Build a list, with an optional cycle at `values[cycle_index]`."""
    if not values:
        return None
    nodes = [ListNode(v) for v in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    if cycle_index >= 0:
        nodes[-1].next = nodes[cycle_index]
    return nodes[0]


# =========================================================================
# Solution 1: Floyd's — O(n) Time, O(1) Space
# =========================================================================

def has_cycle(head):
    """
    Floyd's Tortoise and Hare.

    Time:  O(n)
    Space: O(1)
    """
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


# =========================================================================
# Solution 2: Hash Set of Visited Nodes — O(n) Time, O(n) Space
# =========================================================================

def has_cycle_hashset(head):
    """
    Walk the list; if we see a node twice, there's a cycle.

    Time:  O(n)
    Space: O(n)
    """
    seen = set()
    node = head
    while node is not None:
        if id(node) in seen:                      # id() uniquely identifies the node
            return True
        seen.add(id(node))
        node = node.next
    return False


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Test cases
    print("Has cycle?")

    # No cycle
    for values in [[], [1], [1, 2], [1, 2, 3, 4, 5]]:
        head = build_list(values, cycle_index=-1)
        assert has_cycle(head) is False
        assert has_cycle_hashset(head) is False
        print(f"   build_list({values}, no cycle) → False")

    # Cycle at various positions
    cycle_cases = [
        ([1, 2, 3, 4, 5],  0),
        ([1, 2, 3, 4, 5],  2),
        ([1, 2, 3, 4, 5],  4),                    # self-loop at tail
        ([1],              0),                    # single-node self-loop
        ([1, 2],           0),
        ([1, 2],           1),                    # tail self-loops to itself
    ]
    for values, cycle_idx in cycle_cases:
        head = build_list(values, cycle_index=cycle_idx)
        assert has_cycle(head) is True
        assert has_cycle_hashset(head) is True
        print(f"   build_list({values}, cycle at index {cycle_idx}) → True")

    # Stress test
    import random
    random.seed(42)
    for _ in range(500):
        n = random.randint(0, 30)
        values = list(range(n))
        # 50% chance of a cycle
        if n > 0 and random.random() < 0.5:
            cycle_idx = random.randint(0, n - 1)
        else:
            cycle_idx = -1

        head = build_list(values, cycle_index=cycle_idx)
        assert has_cycle(head) == has_cycle_hashset(head)

    print("\nStress test: 500 random lists — Floyd's matches hash set")
    print("\nAll tests passed!")
