"""
Problem: Nth Node From End

Difficulty: Easy → Medium (LeetCode #19 Remove Nth From End)

---------------------------------------------------
Covered in this file:

    1. nth_from_end(head, n)                   — return the nth-from-end node
    2. remove_nth_from_end(head, n)            — LC #19: remove that node
    3. nth_from_end_two_pass(head, n)          — the naive O(2n) reference

---------------------------------------------------
The Two-Pointer Trick:

On a singly-linked list you can't index from the end — you can only
walk forward. But the **two-pointer gap trick** lets you find the
nth-from-end in ONE PASS with O(1) space:

    1. Advance the `fast` pointer n steps ahead.
    2. Now move `fast` and `slow` together, one step at a time.
    3. When `fast` reaches the end, `slow` is n steps BEHIND the end —
       i.e., it's at the nth-from-end node.

Both pointers are always a fixed gap of n apart, so when the faster
one finishes, the slower one is exactly where we want it.

Time:  O(n) — a single pass.
Space: O(1) — two pointers.

---------------------------------------------------
The Two-Pass Approach (For Comparison):

    1. Walk once to compute the length L.
    2. Walk again to the (L - n)th node.

O(n) time, O(1) space — same Big-O. But TWO passes through the list.
On data that doesn't fit in cache or comes from a stream, the
single-pass version strictly wins.

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
# 1. Two-Pointer, Single-Pass
# =========================================================================

def nth_from_end(head, n):
    """
    Return the value of the nth-from-end node (1-indexed).

    Raises ValueError if n exceeds the list length.

    Time:  O(n)
    Space: O(1)
    """
    if n <= 0:
        raise ValueError("n must be at least 1")

    # Advance `fast` n steps
    fast = head
    for _ in range(n):
        if fast is None:
            raise ValueError(f"n={n} exceeds list length")
        fast = fast.next

    # Now move both until `fast` runs off the end
    slow = head
    while fast is not None:
        slow = slow.next
        fast = fast.next

    return slow.val


# =========================================================================
# 2. Remove Nth From End (LC #19)
# =========================================================================

def remove_nth_from_end(head, n):
    """
    Remove the nth-from-end node. Returns the new head.

    Time:  O(n)
    Space: O(1)

    Uses a DUMMY HEAD so that removing the first node is not a special
    case. The trick: we want `slow` to end up pointing at the node
    BEFORE the one to remove, so we start slow at dummy (one step
    before head) and advance fast n+1 steps.
    """
    if n <= 0:
        raise ValueError("n must be at least 1")

    dummy = ListNode(0, next=head)

    fast = dummy
    for _ in range(n + 1):
        if fast is None:
            raise ValueError(f"n={n} exceeds list length")
        fast = fast.next

    slow = dummy
    while fast is not None:
        slow = slow.next
        fast = fast.next

    # slow is one step BEFORE the node to remove
    slow.next = slow.next.next

    return dummy.next


# =========================================================================
# 3. Two-Pass Reference Implementation
# =========================================================================

def nth_from_end_two_pass(head, n):
    """
    Reference two-pass implementation — walk to compute length,
    then walk again to position (length - n).

    Time:  O(n)
    Space: O(1)

    Same asymptotic cost as the single-pass version, but takes 2n
    operations in practice. Used to validate the single-pass version.
    """
    # First pass: compute length
    length = 0
    node = head
    while node is not None:
        length += 1
        node = node.next

    if n > length:
        raise ValueError(f"n={n} exceeds list length {length}")

    # Second pass: walk to (length - n)
    target_index = length - n
    node = head
    for _ in range(target_index):
        node = node.next

    return node.val


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    # 1. nth_from_end basic
    print("1. nth_from_end:")
    head = build_list([1, 2, 3, 4, 5])
    for n in range(1, 6):
        got = nth_from_end(head, n)
        expected = [1, 2, 3, 4, 5][-n]
        assert got == expected, f"nth_from_end(n={n}) = {got}, expected {expected}"
        print(f"   nth_from_end([1,2,3,4,5], n={n}) = {got}")
    print()

    # Edge cases
    try:
        nth_from_end(build_list([1, 2]), 5)
    except ValueError as e:
        print(f"   ValueError (n > length): {e}")

    try:
        nth_from_end(build_list([1, 2, 3]), 0)
    except ValueError as e:
        print(f"   ValueError (n <= 0):     {e}")
    print()

    # 2. remove_nth_from_end (LC #19)
    print("2. remove_nth_from_end (LC #19):")
    remove_cases = [
        ([1, 2, 3, 4, 5],  2,  [1, 2, 3, 5]),
        ([1],              1,  []),
        ([1, 2],           1,  [1]),
        ([1, 2],           2,  [2]),
        ([1, 2, 3, 4, 5],  1,  [1, 2, 3, 4]),
        ([1, 2, 3, 4, 5],  5,  [2, 3, 4, 5]),       # remove head
    ]
    for values, n, expected in remove_cases:
        head = build_list(values)
        result = remove_nth_from_end(head, n)
        got = list_to_python(result)
        assert got == expected, f"remove({values}, n={n}) = {got}, expected {expected}"
        print(f"   remove_nth_from_end({values}, n={n}) = {got}")
    print()

    # 3. Single-pass and two-pass agree
    print("3. Single-pass and two-pass implementations agree:")
    import random
    random.seed(42)
    for _ in range(200):
        length = random.randint(1, 50)
        values = [random.randint(-100, 100) for _ in range(length)]
        n = random.randint(1, length)

        single = nth_from_end(build_list(values), n)
        two = nth_from_end_two_pass(build_list(values), n)
        assert single == two, f"values={values}, n={n}: single={single}, two={two}"

    print("   200 random lists — both approaches agree")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Why This Problem Matters:
    #
    #   The two-pointer gap trick is a recurring pattern on linked
    #   lists. It also solves:
    #
    #     - Middle of the Linked List (speed 2 vs 1; see operations.py)
    #     - Linked List Cycle (Floyd's; see ../../04-Cycle-Detection/)
    #     - Reorder List (find middle, reverse second half, interleave)
    #     - Palindrome Linked List (find middle, reverse, compare)
    #
    #   The common theme: two pointers on the same list, at different
    #   speeds or with a fixed gap, let us solve many "index from the
    #   end" / "cycle / middle" problems in one pass, O(1) space.
    # ---------------------------------------------------------------
