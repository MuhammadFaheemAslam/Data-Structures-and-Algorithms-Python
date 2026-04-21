"""
template.py – Fast & Slow Pointers Reference Template

This file demonstrates the three core patterns:

    1. has_cycle(head)          — detect a cycle in a linked list
    2. cycle_start(head)        — find the node where the cycle begins
    3. find_middle(head)        — find the middle of a linked list

All three use O(1) extra space — the defining advantage of the
fast-slow technique.

A minimal ListNode class is defined here so the file is self-contained
and runnable.

Run this file to see each template's output.
"""


# =========================================================================
# Minimal Linked List Definition
# =========================================================================

class ListNode:
    """Single-linked node."""

    def __init__(self, value, next=None):
        self.value = value
        self.next = next

    def __repr__(self):
        return f"ListNode({self.value})"


def build_list(values):
    """
    Build a linked list from an iterable of values.
    Returns (head, [nodes]) so tests can attach cycles at specific nodes.
    """
    if not values:
        return None, []

    nodes = [ListNode(v) for v in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    return nodes[0], nodes


# =========================================================================
# Template 1: Detect a Cycle
# =========================================================================

def has_cycle(head):
    """
    Return True if the linked list starting at `head` contains a cycle.

    Time Complexity:  O(n)
    Space Complexity: O(1)

    Phase 1 of Floyd's. If fast ever reaches None, no cycle. If slow
    catches up to fast, cycle detected.
    """
    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True

    return False


# =========================================================================
# Template 2: Find the Start of a Cycle
# =========================================================================

def cycle_start(head):
    """
    Return the node where the cycle begins, or None if there's no cycle.

    Time Complexity:  O(n)
    Space Complexity: O(1)

    Phases 1 + 2 of Floyd's. See theory.md for why Phase 2 converges
    exactly at the cycle's start.
    """
    # Phase 1 — detect
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            break
    else:
        return None                           # fast reached end → no cycle

    if not fast or not fast.next:
        return None                           # edge case — empty or 1-node

    # Phase 2 — find start by resetting one pointer to head
    slow = head
    while slow is not fast:
        slow = slow.next
        fast = fast.next

    return slow


# =========================================================================
# Template 3: Find the Middle of the List
# =========================================================================

def find_middle(head):
    """
    Return the middle node of the list. For even length, returns the
    SECOND of the two middle nodes (index n/2).

    Time Complexity:  O(n)
    Space Complexity: O(1)
    """
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow


# =========================================================================
# Bonus: Happy Number — Floyd's on a Function Iteration
# =========================================================================

def is_happy(n):
    """
    LeetCode #202. Returns True if repeatedly replacing n with the sum
    of squares of its digits eventually reaches 1. Otherwise the
    sequence enters a non-1 cycle and we return False.

    Same fast-slow technique, but the "list" is implicit — the transition
    function is `sum_of_digit_squares`.

    Time Complexity:  O(log n) per step (number of digits), cycle-length steps
    Space Complexity: O(1)
    """
    def next_val(x):
        total = 0
        while x:
            d = x % 10
            total += d * d
            x //= 10
        return total

    slow = n
    fast = next_val(n)
    while fast != 1 and slow != fast:
        slow = next_val(slow)
        fast = next_val(next_val(fast))

    return fast == 1


# =========================================================================
# Demonstration
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Template 1 — Cycle Detection")
    print("=" * 60)

    # No cycle
    head, nodes = build_list([1, 2, 3, 4, 5])
    assert has_cycle(head) is False
    print(f"   [1,2,3,4,5], no cycle      -> has_cycle = {has_cycle(head)}")

    # Cycle: tail points back to node[1]
    head, nodes = build_list([3, 2, 0, -4])
    nodes[3].next = nodes[1]
    assert has_cycle(head) is True
    print(f"   [3,2,0,-4] tail→node[1]    -> has_cycle = {has_cycle(head)}")

    # Self-loop
    head, nodes = build_list([1])
    nodes[0].next = nodes[0]
    assert has_cycle(head) is True
    print(f"   single-node self-loop      -> has_cycle = {has_cycle(head)}")

    # Empty list
    assert has_cycle(None) is False
    print(f"   empty list                 -> has_cycle = {has_cycle(None)}")
    print()

    print("=" * 60)
    print("Template 2 — Cycle Start")
    print("=" * 60)

    # Cycle at node index 1
    head, nodes = build_list([3, 2, 0, -4])
    nodes[3].next = nodes[1]
    cs = cycle_start(head)
    assert cs is nodes[1]
    print(f"   cycle starts at node with value {cs.value}  (expected {nodes[1].value})")

    # No cycle
    head, nodes = build_list([1, 2, 3])
    assert cycle_start(head) is None
    print(f"   no cycle                   -> cycle_start = {cycle_start(head)}")

    # Full cycle
    head, nodes = build_list([1, 2])
    nodes[1].next = nodes[0]
    cs = cycle_start(head)
    assert cs is nodes[0]
    print(f"   full cycle                 -> cycle_start = node({cs.value})")
    print()

    print("=" * 60)
    print("Template 3 — Find the Middle")
    print("=" * 60)

    # Odd length
    head, nodes = build_list([1, 2, 3, 4, 5])
    mid = find_middle(head)
    assert mid is nodes[2]
    print(f"   [1,2,3,4,5]  -> middle = node({mid.value})")

    # Even length — returns SECOND middle
    head, nodes = build_list([1, 2, 3, 4, 5, 6])
    mid = find_middle(head)
    assert mid is nodes[3]
    print(f"   [1,2,3,4,5,6] -> middle = node({mid.value})  (second of two middles)")

    # Single element
    head, nodes = build_list([42])
    assert find_middle(head) is nodes[0]
    print(f"   [42]         -> middle = node(42)")
    print()

    print("=" * 60)
    print("Bonus — Happy Number (Floyd's on function iteration)")
    print("=" * 60)
    cases = [(1, True), (7, True), (19, True), (2, False), (4, False), (20, False)]
    for n, expected in cases:
        got = is_happy(n)
        assert got == expected
        print(f"   is_happy({n:3}) = {got}")

    print("\nAll tests passed!")
