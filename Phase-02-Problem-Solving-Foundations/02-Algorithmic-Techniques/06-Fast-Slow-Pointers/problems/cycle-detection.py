"""
Problem: Linked List Cycle Detection (Parts I & II)

Technique: Fast & Slow Pointers (Floyd's Tortoise and Hare)
Difficulty: Easy (LC #141) / Medium (LC #142)

---------------------------------------------------
Problem Statement:

Part I (LeetCode #141):
    Given the head of a linked list, return True if it contains a cycle
    (some node's `next` pointer revisits an earlier node), otherwise False.

Part II (LeetCode #142):
    Return the node where the cycle begins (the first node that is
    visited twice when walking from the head). Return None if there
    is no cycle.

---------------------------------------------------
The Fast-Slow Lens:

A cycle in a linked list means some node's `next` pointer loops back
to an earlier node. There's no "end" (no None) along the cyclic part
of the list.

We can detect this with a **hash set** of visited nodes in O(n) time,
O(n) space. But we can do better:

    O(n) time, O(1) space via Floyd's Tortoise and Hare.

Two pointers walk the list:
    - slow: one step at a time
    - fast: two steps at a time

If there's no cycle, `fast` eventually reaches None.
If there IS a cycle, `fast` catches up to `slow` inside the cycle — the
1-step-per-iteration gap closure guarantees this within `cycle_length`
steps once both pointers are inside the cycle.

Part II goes one step further: after the meeting, reset one pointer
to head. Now move both 1 step at a time — they meet exactly at the
cycle's entrance. See theory.md for the proof.

---------------------------------------------------
Why Part II Works (The L = kC - x Trick):

Let:
    L = distance from head to cycle entrance
    C = cycle length
    x = distance from entrance to the first meeting point

When slow and fast first meet:
    slow has walked L + x.
    fast has walked 2*(L + x), which also equals L + x + k*C
    (some number of full laps).

Equating:
    2(L + x) = L + x + k*C
    L + x    = k*C
    L        = k*C - x
              ≡ (k-1)*C + (C - x)

That's "distance from head to entrance" = "distance from meeting point
to entrance, going around". So moving both pointers one step at a time
from head and from the meeting point, they converge exactly at the entrance.

---------------------------------------------------
"""

# -------------------------------------------------
# Minimal Linked List Definition (Self-Contained)
# -------------------------------------------------

class ListNode:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

    def __repr__(self):
        return f"ListNode({self.value})"


def build_list(values):
    """Build a linked list from values, returning (head, [nodes])."""
    if not values:
        return None, []
    nodes = [ListNode(v) for v in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    return nodes[0], nodes


# -------------------------------------------------
# Part I: Does the List Have a Cycle?
# -------------------------------------------------

def has_cycle(head):
    """
    Return True if the list starting at `head` contains a cycle.

    Time Complexity:  O(n)
    Space Complexity: O(1)
    """
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


# -------------------------------------------------
# Part II: Find the Node Where the Cycle Begins
# -------------------------------------------------

def detect_cycle(head):
    """
    Return the first node of the cycle, or None if no cycle exists.

    Time Complexity:  O(n)
    Space Complexity: O(1)

    Uses the full two-phase Floyd's algorithm.
    """
    # Phase 1: detect meeting point inside the cycle
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            break
    else:
        return None                            # fast hit None → no cycle

    if not fast or not fast.next:
        return None                            # cover short-list edge case

    # Phase 2: reset one pointer to head, advance both by 1 — they meet at entrance
    slow = head
    while slow is not fast:
        slow = slow.next
        fast = fast.next

    return slow


# -------------------------------------------------
# Hash-Set Alternative (For Contrast)
# -------------------------------------------------

def detect_cycle_hashset(head):
    """
    Simpler alternative using O(n) space.

    Walk the list, recording each node. If you revisit one, that's the
    cycle's start.

    Time Complexity:  O(n)
    Space Complexity: O(n)

    Correct and arguably easier to read; but use Floyd's when O(1)
    space is required (interviews often ask for it).
    """
    seen = set()
    while head:
        if head in seen:
            return head
        seen.add(head)
        head = head.next
    return None


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    # Case 1: No cycle
    head, nodes = build_list([1, 2, 3, 4, 5])
    assert has_cycle(head) is False
    assert detect_cycle(head) is None
    assert detect_cycle_hashset(head) is None
    print("Test 1 passed: [1,2,3,4,5], no cycle")

    # Case 2: Cycle starting at index 1  (3 → 2 → 0 → -4 → [back to 2])
    head, nodes = build_list([3, 2, 0, -4])
    nodes[3].next = nodes[1]
    assert has_cycle(head) is True
    assert detect_cycle(head) is nodes[1]
    assert detect_cycle_hashset(head) is nodes[1]
    print(f"Test 2 passed: cycle starts at node({nodes[1].value})")

    # Case 3: Cycle starting at head (full-list loop)
    head, nodes = build_list([1, 2])
    nodes[1].next = nodes[0]
    assert has_cycle(head) is True
    assert detect_cycle(head) is nodes[0]
    print(f"Test 3 passed: full cycle; entrance = node({nodes[0].value})")

    # Case 4: Single-node self-loop
    head, nodes = build_list([42])
    nodes[0].next = nodes[0]
    assert has_cycle(head) is True
    assert detect_cycle(head) is nodes[0]
    print("Test 4 passed: self-loop on single node")

    # Case 5: Empty list
    assert has_cycle(None) is False
    assert detect_cycle(None) is None
    print("Test 5 passed: empty list")

    # Case 6: Single node, no cycle
    head, nodes = build_list([7])
    assert has_cycle(head) is False
    assert detect_cycle(head) is None
    print("Test 6 passed: single node, no cycle")

    # Case 7: Cycle further into the list
    head, nodes = build_list([1, 2, 3, 4, 5, 6, 7])
    nodes[6].next = nodes[4]
    assert detect_cycle(head) is nodes[4]
    print(f"Test 7 passed: cycle entrance at node({nodes[4].value})")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Technique Map:
    #
    #   Cycle in any SEQUENCE WITH DETERMINISTIC next():
    #     - Linked list            →  Floyd's directly
    #     - Happy Number           →  next(x) = sum_of_digit_squares(x)
    #     - Find the Duplicate     →  nums treated as a function graph
    #     - Sequence convergence   →  any iterated function
    #
    # Any time your "walk" is next(x) = f(x) for a single-valued f,
    # and you want to detect a cycle, fast-slow is the right tool.
    # ---------------------------------------------------------------
