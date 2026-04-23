"""
Problem: Linked List Cycle II — Find the Cycle Start

Difficulty: Medium (LeetCode #142)

---------------------------------------------------
Problem Statement:

Given the head of a linked list, return the node where the cycle
BEGINS, or None if there is no cycle.

Follow-up: O(1) extra space.

---------------------------------------------------
The Full Floyd's Algorithm — Phases 1 + 2:

**Phase 1** (detect the cycle):

    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            break                    # cycle detected; meeting point is `slow`
    else:
        return None                  # no cycle

**Phase 2** (find the cycle start):

    slow = head                      # reset slow to the head
    while slow is not fast:
        slow = slow.next
        fast = fast.next             # fast now moves at speed 1
    return slow                       # they meet at the cycle entrance

---------------------------------------------------
Why the Math Works:

Let:
    L = distance from head to the cycle entrance.
    C = cycle length.
    d = distance inside the cycle from the entrance to the meeting point.

At the meeting point:
    slow has walked L + d.
    fast has walked L + d + k·C (for some positive k, because it lapped slow).

Also, fast walks twice as fast as slow, so:
    2·(L + d) = L + d + k·C
    L + d = k·C
    L = k·C − d

This says: L ≡ −d (mod C). In English: if you start at the head and
move L steps, AND simultaneously if you start at the meeting point
and move L steps, you BOTH end up at the cycle entrance. Hence the
Phase 2 walk works.

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
    if not values:
        return None, None
    nodes = [ListNode(v) for v in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    expected_start = None
    if cycle_index >= 0:
        nodes[-1].next = nodes[cycle_index]
        expected_start = nodes[cycle_index]
    return nodes[0], expected_start


# =========================================================================
# Solution 1: Floyd's — O(n) Time, O(1) Space
# =========================================================================

def detect_cycle_start(head):
    """
    Return the node where the cycle starts, or None.

    Time:  O(n)
    Space: O(1)
    """
    # Phase 1: detect
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            break
    else:
        return None

    if fast is None or fast.next is None:
        return None

    # Phase 2: find the entrance
    slow = head
    while slow is not fast:
        slow = slow.next
        fast = fast.next
    return slow


# =========================================================================
# Solution 2: Hash Set — O(n) Time, O(n) Space
# =========================================================================

def detect_cycle_start_hashset(head):
    """
    Walk the list; the first repeat is the cycle start.

    Time:  O(n)
    Space: O(n)
    """
    seen = set()
    node = head
    while node is not None:
        if id(node) in seen:
            return node
        seen.add(id(node))
        node = node.next
    return None


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # No cycle
    for values in [[], [1], [1, 2, 3]]:
        head, expected = build_list(values, -1)
        assert detect_cycle_start(head) is None
        assert detect_cycle_start_hashset(head) is None
        print(f"build_list({values}, no cycle) → None")

    # Cycle cases
    print()
    cycle_cases = [
        ([3, 2, 0, -4], 1),                        # LC #142 example 1 → node with value 2
        ([1, 2], 0),                               # cycle back to head
        ([1], 0),                                  # self-loop
        ([1, 2, 3, 4, 5], 3),                      # cycle to node[3] (value 4)
    ]
    for values, cycle_idx in cycle_cases:
        head, expected = build_list(values, cycle_idx)
        got = detect_cycle_start(head)
        got_hs = detect_cycle_start_hashset(head)
        assert got is expected, f"floyd's mismatch for {values}, idx={cycle_idx}"
        assert got_hs is expected, f"hashset mismatch for {values}, idx={cycle_idx}"
        print(f"build_list({values}, cycle→idx {cycle_idx}) → node.val = {got.val}")

    # Stress test
    import random
    random.seed(42)
    for _ in range(500):
        n = random.randint(0, 30)
        values = list(range(n))
        if n > 0 and random.random() < 0.5:
            cycle_idx = random.randint(0, n - 1)
        else:
            cycle_idx = -1

        head, expected = build_list(values, cycle_idx)
        got1 = detect_cycle_start(head)
        got2 = detect_cycle_start_hashset(head)
        assert got1 is expected
        assert got2 is expected

    print("\nStress test: 500 random lists — Floyd's matches hash set (with known expected)")
    print("\nAll tests passed!")
