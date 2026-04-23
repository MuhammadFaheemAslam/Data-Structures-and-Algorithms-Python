"""
operations.py – Common Singly-Linked-List Operations (Standalone Functions)

A collection of stand-alone functions that operate on a linked list
given ONLY its head node — no container class, no tail pointer, no
size counter. These are the operations you'd write in an interview
where you're handed a `head: ListNode`.

All functions use a minimal `ListNode` class (defined below) that
matches the LeetCode signature.

---------------------------------------------------
What's Here:

    1. length(head)                     — count nodes
    2. get_at(head, i)                  — access by index
    3. find(head, value)                — search for a value
    4. insert_at(head, i, value)        — insert at position i
    5. delete_at(head, i)               — remove at position i
    6. reverse(head)                    — reverse (iterative)
    7. reverse_recursive(head)          — reverse (recursive)
    8. middle_node(head)                — find the middle (fast/slow)
    9. merge_sorted(a, b)               — merge two sorted lists
   10. remove_duplicates_sorted(head)   — in place, sorted input
"""


# =========================================================================
# Minimal ListNode (LeetCode-compatible)
# =========================================================================

class ListNode:
    """The minimal linked-list node used by almost every LC problem."""

    __slots__ = ("val", "next")

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        return f"ListNode({self.val})"


def build_list(values):
    """Build a linked list from an iterable. Returns head (or None if empty)."""
    dummy = ListNode()
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def list_to_python(head):
    """Convert a linked list back to a Python list (for easy inspection)."""
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


# =========================================================================
# 1. Length
# =========================================================================

def length(head):
    """
    Return the number of nodes. O(n).
    """
    n = 0
    while head:
        n += 1
        head = head.next
    return n


# =========================================================================
# 2. Access by Index (Note: O(n) — no random access)
# =========================================================================

def get_at(head, i):
    """
    Return the value at 0-based index `i`. Raises IndexError on out of range.

    Time: O(n)
    """
    node = head
    pos = 0
    while node is not None and pos < i:
        node = node.next
        pos += 1
    if node is None:
        raise IndexError(f"index out of range: {i}")
    return node.val


# =========================================================================
# 3. Find a Value (Linear Search)
# =========================================================================

def find(head, value):
    """Return the first index at which `value` appears, or -1 if absent."""
    node = head
    i = 0
    while node is not None:
        if node.val == value:
            return i
        node = node.next
        i += 1
    return -1


# =========================================================================
# 4. Insert at a Given Position
# =========================================================================

def insert_at(head, i, value):
    """
    Insert a new node with `value` at position `i`. Returns the new head.

    Uses the DUMMY HEAD pattern to avoid a special case for i == 0.

    Time: O(n)
    """
    if i < 0:
        raise IndexError(f"negative index: {i}")

    dummy = ListNode(0, next=head)
    prev = dummy
    for _ in range(i):
        if prev.next is None:
            raise IndexError(f"index out of range: {i}")
        prev = prev.next

    prev.next = ListNode(value, next=prev.next)
    return dummy.next


# =========================================================================
# 5. Delete at a Given Position
# =========================================================================

def delete_at(head, i):
    """
    Remove the node at position `i`. Returns the new head.

    Time: O(n)
    """
    if i < 0:
        raise IndexError(f"negative index: {i}")

    dummy = ListNode(0, next=head)
    prev = dummy
    for _ in range(i):
        if prev.next is None:
            raise IndexError(f"index out of range: {i}")
        prev = prev.next

    if prev.next is None:
        raise IndexError(f"index out of range: {i}")

    prev.next = prev.next.next
    return dummy.next


# =========================================================================
# 6. Reverse (Iterative, O(1) Space)
# =========================================================================

def reverse(head):
    """
    Reverse the list in place via a three-pointer walk. Returns the
    new head.

    Time:  O(n)
    Space: O(1)

    The canonical linked-list primitive. Internalize this.
    """
    prev = None
    curr = head
    while curr is not None:
        nxt = curr.next                           # save the next node
        curr.next = prev                          # flip the current link
        prev = curr                               # advance prev
        curr = nxt                                # advance curr
    return prev


# =========================================================================
# 7. Reverse (Recursive)
# =========================================================================

def reverse_recursive(head):
    """
    Recursive reverse — returns the new head.

    Time:  O(n)
    Space: O(n) for the recursion stack

    For any list of practical size, prefer the iterative version.
    """
    if head is None or head.next is None:
        return head

    new_head = reverse_recursive(head.next)
    head.next.next = head
    head.next = None
    return new_head


# =========================================================================
# 8. Find the Middle Node (Fast / Slow Pointers)
# =========================================================================

def middle_node(head):
    """
    Return the middle node. For even-length lists, returns the SECOND
    of the two middles (standard LC #876 convention).

    Technique: fast pointer moves 2 per step; slow moves 1. When
    fast hits the end, slow is at the middle.

    Time:  O(n)
    Space: O(1)
    """
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    return slow


# =========================================================================
# 9. Merge Two Sorted Lists
# =========================================================================

def merge_sorted(a, b):
    """
    Merge two sorted linked lists. Returns the head of the merged list.

    Same algorithm as the merge step of merge sort on arrays, but using
    node splicing instead of value copying. O(1) auxiliary space.

    Time:  O(len(a) + len(b))
    Space: O(1)
    """
    dummy = ListNode()
    tail = dummy

    while a is not None and b is not None:
        if a.val <= b.val:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next

    # attach whatever remains
    tail.next = a if a is not None else b
    return dummy.next


# =========================================================================
# 10. Remove Duplicates from a SORTED List (LC #83)
# =========================================================================

def remove_duplicates_sorted(head):
    """
    In a sorted list, remove nodes with duplicate values, keeping the
    first occurrence.

        1 → 1 → 2 → 3 → 3  →  1 → 2 → 3

    Time:  O(n)
    Space: O(1)
    """
    curr = head
    while curr is not None and curr.next is not None:
        if curr.val == curr.next.val:
            curr.next = curr.next.next            # skip the duplicate
            # don't advance curr — the new next might also be a duplicate
        else:
            curr = curr.next
    return head


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    # 1. length
    assert length(build_list([])) == 0
    assert length(build_list([1])) == 1
    assert length(build_list([1, 2, 3, 4, 5])) == 5
    print("1. length — passed")

    # 2. get_at / find
    head = build_list([10, 20, 30, 40, 50])
    assert get_at(head, 0) == 10
    assert get_at(head, 4) == 50
    try:
        get_at(head, 10)
    except IndexError:
        pass

    assert find(head, 30) == 2
    assert find(head, 99) == -1
    print("2. get_at / find — passed")

    # 3. insert_at / delete_at
    head = build_list([1, 2, 3])
    head = insert_at(head, 0, 0)                    # prepend
    assert list_to_python(head) == [0, 1, 2, 3]
    head = insert_at(head, 2, 99)                   # middle
    assert list_to_python(head) == [0, 1, 99, 2, 3]
    head = insert_at(head, 5, 100)                  # tail
    assert list_to_python(head) == [0, 1, 99, 2, 3, 100]

    head = delete_at(head, 2)                       # remove 99
    assert list_to_python(head) == [0, 1, 2, 3, 100]
    head = delete_at(head, 0)                       # remove head
    assert list_to_python(head) == [1, 2, 3, 100]
    head = delete_at(head, 3)                       # remove tail
    assert list_to_python(head) == [1, 2, 3]
    print("3. insert_at / delete_at — passed")

    # 4. reverse (both versions)
    for values in [[], [1], [1, 2], [1, 2, 3, 4, 5]]:
        head = build_list(values)
        rev = reverse(head)
        assert list_to_python(rev) == list(reversed(values))

        head = build_list(values)
        rev = reverse_recursive(head)
        assert list_to_python(rev) == list(reversed(values))

    print("4. reverse / reverse_recursive — passed on several inputs")

    # 5. middle_node
    assert middle_node(build_list([1, 2, 3, 4, 5])).val == 3
    assert middle_node(build_list([1, 2, 3, 4, 5, 6])).val == 4     # second middle
    assert middle_node(build_list([1])).val == 1
    assert middle_node(build_list([])) is None
    print("5. middle_node — passed")

    # 6. merge_sorted
    a = build_list([1, 3, 5])
    b = build_list([2, 4, 6])
    merged = merge_sorted(a, b)
    assert list_to_python(merged) == [1, 2, 3, 4, 5, 6]

    a = build_list([])
    b = build_list([1, 2, 3])
    merged = merge_sorted(a, b)
    assert list_to_python(merged) == [1, 2, 3]
    print("6. merge_sorted — passed")

    # 7. remove_duplicates_sorted
    assert list_to_python(remove_duplicates_sorted(build_list([1, 1, 2, 3, 3]))) == [1, 2, 3]
    assert list_to_python(remove_duplicates_sorted(build_list([]))) == []
    assert list_to_python(remove_duplicates_sorted(build_list([1, 1, 1]))) == [1]
    assert list_to_python(remove_duplicates_sorted(build_list([1, 2, 3]))) == [1, 2, 3]
    print("7. remove_duplicates_sorted — passed")

    # Stress test — reverse composes correctly
    import random
    random.seed(42)
    for _ in range(100):
        n = random.randint(0, 50)
        values = [random.randint(-100, 100) for _ in range(n)]
        head = build_list(values)
        reversed_once = list_to_python(reverse(build_list(values)))
        assert reversed_once == list(reversed(values))
        # Double-reverse should return the original
        head2 = reverse(reverse(build_list(values)))
        assert list_to_python(head2) == values

    print("\nStress test: 100 random lists — reverse is its own inverse")
    print("\nAll tests passed!")
