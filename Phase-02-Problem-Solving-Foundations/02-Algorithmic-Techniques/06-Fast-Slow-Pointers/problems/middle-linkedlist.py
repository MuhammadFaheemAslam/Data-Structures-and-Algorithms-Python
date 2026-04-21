"""
Problem: Middle of the Linked List

Technique: Fast & Slow Pointers
Difficulty: Easy (LeetCode #876)

---------------------------------------------------
Problem Statement:

Given the head of a singly linked list, return the MIDDLE NODE.

If the list has an even number of nodes, there are two middle nodes;
return the SECOND one.

Examples:
    [1,2,3,4,5]     → node with value 3        (single middle)
    [1,2,3,4,5,6]   → node with value 4        (second of two middles)

---------------------------------------------------
The Fast-Slow Lens:

Naive approach: walk the list once to get its length `n`, then walk
again `n // 2` steps. Two passes — O(n) time, O(1) space.

Fast-slow does it in ONE pass:

    slow moves 1 step at a time.
    fast moves 2 steps at a time.

When fast reaches the end (or just past it), slow is at the middle.
The symmetry is exact: if fast has taken 2k steps, slow has taken k.

For ODD length n: fast reaches the last node exactly when slow reaches
the middle. For EVEN length n: fast steps past the last node one step
after slow reaches the SECOND middle — which is what the problem asks
for.

    sequence of length 5:
        slow,fast at 0
        step 1: slow=1, fast=2
        step 2: slow=2, fast=4  ← fast.next is None → stop.  slow = middle.

    sequence of length 6:
        slow,fast at 0
        step 1: slow=1, fast=2
        step 2: slow=2, fast=4
        step 3: slow=3, fast=6  ← fast is past the end → stop.  slow = 2nd middle.

Termination condition: `while fast and fast.next`.

Time Complexity:  O(n)
Space Complexity: O(1)

---------------------------------------------------
Variant — Return the FIRST Middle:

If you want the first of two middles on even-length lists (i.e., index
(n-1)//2 instead of n//2), change the loop condition:

    while fast.next and fast.next.next:
        ...

This stops one step earlier on even-length inputs, landing slow at the
first middle rather than the second.

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
    if not values:
        return None, []
    nodes = [ListNode(v) for v in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    return nodes[0], nodes


# -------------------------------------------------
# Fast-Slow Solution — Returns the SECOND Middle on Even
# -------------------------------------------------

def middle_node(head):
    """
    Return the middle node (second middle if even length).

    Time Complexity:  O(n)
    Space Complexity: O(1)
    """
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow


# -------------------------------------------------
# Variant — Returns the FIRST Middle on Even
# -------------------------------------------------

def middle_node_first(head):
    """
    Return the middle node, preferring the FIRST middle on even-length lists.

    Time Complexity:  O(n)
    Space Complexity: O(1)
    """
    if not head:
        return None

    slow = fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    return slow


# -------------------------------------------------
# Two-Pass Reference (For Contrast)
# -------------------------------------------------

def middle_node_two_pass(head):
    """
    Count length first, then walk to the middle. Same big-O, but two
    passes instead of one.

    Included to show both approaches are equivalent — the fast-slow
    version just does both walks simultaneously.
    """
    if not head:
        return None

    n = 0
    cur = head
    while cur:
        n += 1
        cur = cur.next

    cur = head
    for _ in range(n // 2):
        cur = cur.next
    return cur


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    # Odd length
    head, nodes = build_list([1, 2, 3, 4, 5])
    mid = middle_node(head)
    mid_first = middle_node_first(head)
    mid_tp = middle_node_two_pass(head)
    assert mid is nodes[2] == mid_tp
    assert mid_first is nodes[2]
    print(f"Test 1 passed: [1,2,3,4,5] -> middle = node({mid.value})")

    # Even length — second middle
    head, nodes = build_list([1, 2, 3, 4, 5, 6])
    mid = middle_node(head)
    mid_first = middle_node_first(head)
    mid_tp = middle_node_two_pass(head)
    assert mid is nodes[3] == mid_tp         # second middle
    assert mid_first is nodes[2]             # first middle
    print(f"Test 2 passed: [1,2,3,4,5,6] -> second middle = node({mid.value}), first middle = node({mid_first.value})")

    # Single element
    head, nodes = build_list([42])
    mid = middle_node(head)
    assert mid is nodes[0]
    print(f"Test 3 passed: [42] -> middle = node({mid.value})")

    # Two elements — edge case for even
    head, nodes = build_list([1, 2])
    mid = middle_node(head)
    mid_first = middle_node_first(head)
    assert mid is nodes[1]                   # second middle
    assert mid_first is nodes[0]             # first middle
    print(f"Test 4 passed: [1,2] -> second={mid.value}, first={mid_first.value}")

    # Empty list
    assert middle_node(None) is None
    assert middle_node_first(None) is None
    assert middle_node_two_pass(None) is None
    print("Test 5 passed: empty list -> None")

    # Larger list
    head, nodes = build_list(list(range(100)))
    mid = middle_node(head)
    assert mid is nodes[50]                  # second of 50/49
    print(f"Test 6 passed: [0..99] -> second middle = node({mid.value})")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Why Middle-Finding Is Foundational:
    #
    #   "Find the middle" is rarely the final question — it's usually
    #   step 1 of a more interesting algorithm:
    #
    #     Palindrome Linked List (LC #234)
    #         find middle → reverse second half → compare both halves
    #
    #     Reorder List (LC #143)
    #         find middle → reverse second half → interleave halves
    #
    #     Sort List (LC #148)
    #         find middle → recurse on each half → merge (merge sort)
    #
    #   In all of these, O(1)-space midpoint-finding is what keeps the
    #   whole algorithm O(1)-space. That's the real value of the
    #   fast-slow trick here.
    # ---------------------------------------------------------------
