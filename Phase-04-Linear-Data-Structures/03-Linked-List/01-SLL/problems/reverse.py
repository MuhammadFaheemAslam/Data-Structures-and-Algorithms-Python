"""
Problem: Reverse a Linked List

Difficulty: Easy → Medium (LeetCode #206 easy, #92 medium variant)

---------------------------------------------------
Covered in this file:

    1. reverse(head)                 — iterative, O(1) space (LC #206)
    2. reverse_recursive(head)       — recursive, O(n) stack
    3. reverse_between(head, m, n)   — reverse a SUBLIST [m..n] (LC #92)
    4. reverse_k_group(head, k)      — reverse every k consecutive nodes (LC #25)

These four form a natural ladder:
    - Reverse the whole list  ← the primitive.
    - Reverse a range         ← generalize with bookkeeping.
    - Reverse in groups of k  ← apply the range reverse repeatedly.

If you can do #1 fluently, the others are mechanical extensions.

---------------------------------------------------
The Iterative Reverse Algorithm:

    prev = None
    curr = head
    while curr:
        nxt = curr.next      # save where we were going
        curr.next = prev     # FLIP the link
        prev = curr          # advance prev
        curr = nxt           # advance curr
    return prev              # prev is the new head

Four lines, O(n) time, O(1) space. The canonical linked-list primitive.
"""


# =========================================================================
# Minimal ListNode
# =========================================================================

class ListNode:
    __slots__ = ("val", "next")

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build_list(values):
    dummy = ListNode()
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def list_to_python(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


# =========================================================================
# 1. Reverse (Iterative) — LC #206
# =========================================================================

def reverse(head):
    """
    Iteratively reverse the linked list in place.

    Time:  O(n)
    Space: O(1)
    """
    prev = None
    curr = head
    while curr is not None:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev


# =========================================================================
# 2. Reverse (Recursive) — LC #206
# =========================================================================

def reverse_recursive(head):
    """
    Recursively reverse the linked list.

    Time:  O(n)
    Space: O(n) — recursion stack

    Less practical than iterative (same Big-O, more overhead, risk of
    stack overflow). Shown for the recursion intuition.

    The trick: after `reverse_recursive(head.next)`, the sublist
    `head.next → head.next.next → …` has been reversed, with the
    original `head.next` now at the tail of that sublist. All we
    need to do is append `head` to that tail.

        head.next.next = head    # append `head` after the old 2nd node
        head.next = None         # the old head is now the new tail
    """
    if head is None or head.next is None:
        return head

    new_head = reverse_recursive(head.next)
    head.next.next = head
    head.next = None
    return new_head


# =========================================================================
# 3. Reverse Sublist [m..n] (LC #92)
# =========================================================================

def reverse_between(head, left, right):
    """
    Reverse the sublist from position `left` to `right` (1-indexed, INCLUSIVE).
    Positions outside [left, right] are unchanged.

    Example:  1 → 2 → 3 → 4 → 5,  left=2, right=4
         →    1 → 4 → 3 → 2 → 5

    Time:  O(n)
    Space: O(1)

    Technique: dummy head + walk to position left-1, then splice in the
    reversed segment.
    """
    if head is None or left == right:
        return head

    dummy = ListNode(0, next=head)
    prev = dummy

    # Walk `prev` to the node BEFORE position `left`
    for _ in range(left - 1):
        prev = prev.next

    # `curr` will be reversed in place; `prev.next` is where the reversed
    # segment starts (and where it will end after reversal).
    curr = prev.next
    for _ in range(right - left):
        # "front insertion" trick: move curr.next to the front of the reversed segment
        next_node = curr.next
        curr.next = next_node.next
        next_node.next = prev.next
        prev.next = next_node

    return dummy.next


# =========================================================================
# 4. Reverse Every K Consecutive Nodes (LC #25)
# =========================================================================

def reverse_k_group(head, k):
    """
    Reverse every k consecutive nodes. Any tail group smaller than k
    is left as is.

    Example:  1 → 2 → 3 → 4 → 5,  k=2  →  2 → 1 → 4 → 3 → 5
              1 → 2 → 3 → 4 → 5,  k=3  →  3 → 2 → 1 → 4 → 5

    Time:  O(n)
    Space: O(1)

    Technique: dummy head + repeatedly find the next k-group, reverse
    it in place, and splice it back into the main list.
    """
    if k <= 1 or head is None:
        return head

    dummy = ListNode(0, next=head)
    group_prev = dummy

    while True:
        # Check if there are k more nodes ahead
        kth = group_prev
        for _ in range(k):
            kth = kth.next
            if kth is None:
                return dummy.next                 # fewer than k left — leave it

        # Reverse the k-node segment between group_prev and kth.next (exclusive)
        group_next = kth.next
        prev = group_next
        curr = group_prev.next
        for _ in range(k):
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt

        # Splice: the old first node of the group is now the tail; patch
        # group_prev to point at the reversed group's new head (kth)
        tmp = group_prev.next
        group_prev.next = kth
        group_prev = tmp


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    # 1. reverse (iterative)
    for values in [[], [1], [1, 2], [1, 2, 3, 4, 5]]:
        head = build_list(values)
        assert list_to_python(reverse(head)) == list(reversed(values))
    print("1. reverse (iterative) — passed")

    # 2. reverse_recursive
    for values in [[], [1], [1, 2], [1, 2, 3, 4, 5]]:
        head = build_list(values)
        assert list_to_python(reverse_recursive(head)) == list(reversed(values))
    print("2. reverse_recursive — passed")

    # 3. reverse_between
    print("3. reverse_between:")
    cases3 = [
        ([1, 2, 3, 4, 5],     2, 4,  [1, 4, 3, 2, 5]),
        ([5],                 1, 1,  [5]),
        ([1, 2],              1, 2,  [2, 1]),
        ([1, 2, 3, 4, 5],     1, 5,  [5, 4, 3, 2, 1]),
        ([1, 2, 3, 4, 5],     2, 2,  [1, 2, 3, 4, 5]),      # left == right → no change
    ]
    for values, left, right, expected in cases3:
        head = build_list(values)
        result = reverse_between(head, left, right)
        got = list_to_python(result)
        assert got == expected, f"reverse_between({values}, {left}, {right}) = {got}, expected {expected}"
        print(f"   {values}  left={left}, right={right}  →  {got}")
    print()

    # 4. reverse_k_group
    print("4. reverse_k_group:")
    cases4 = [
        ([1, 2, 3, 4, 5],   2,  [2, 1, 4, 3, 5]),
        ([1, 2, 3, 4, 5],   3,  [3, 2, 1, 4, 5]),
        ([1, 2, 3, 4, 5],   5,  [5, 4, 3, 2, 1]),
        ([1, 2, 3, 4, 5],   6,  [1, 2, 3, 4, 5]),              # k > n — no change
        ([1, 2, 3, 4, 5],   1,  [1, 2, 3, 4, 5]),              # k = 1 — no change
        ([],                3,  []),
        ([1, 2, 3, 4, 5, 6, 7, 8],  3,  [3, 2, 1, 6, 5, 4, 7, 8]),
    ]
    for values, k, expected in cases4:
        head = build_list(values)
        result = reverse_k_group(head, k)
        got = list_to_python(result)
        assert got == expected, f"reverse_k_group({values}, {k}) = {got}, expected {expected}"
        print(f"   {values}  k={k}  →  {got}")
    print()

    # Stress test — double-reverse should be identity
    import random
    random.seed(42)
    for _ in range(200):
        n = random.randint(0, 30)
        values = [random.randint(-100, 100) for _ in range(n)]
        head = reverse(reverse(build_list(values)))
        assert list_to_python(head) == values

    print("Stress test: 200 lists — double reverse is identity")

    print("\nAll tests passed!")
