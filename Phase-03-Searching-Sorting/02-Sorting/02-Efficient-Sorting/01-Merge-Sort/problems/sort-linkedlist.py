"""
Problem: Sort a Linked List

Technique: Merge Sort on a linked list
Difficulty: Medium (LeetCode #148)

---------------------------------------------------
Problem Statement:

Given the head of a singly linked list, sort the list in ascending
order and return the new head.

Must be done in O(n log n) time. LC #148 additionally asks for O(1)
extra space (not counting the recursion stack) — which merge sort
can't quite do (the recursion stack is O(log n)), but top-down merge
sort on a linked list is the standard answer.

---------------------------------------------------
Why Merge Sort Is THE Algorithm for Linked Lists:

On arrays, quick sort is usually faster than merge sort in practice.
On LINKED LISTS, merge sort beats every other comparison-based sort:

    1. **Splitting is O(n/2)** via fast-slow pointers — no arithmetic,
       no random access needed.
    2. **Merging is O(1)-space per step** — splice nodes rather than
       copy values. This is what lets linked-list merge sort achieve
       the goal that array merge sort can't: O(1) auxiliary memory
       (up to recursion stack).
    3. **No random access** — linked lists can't do quicksort's
       partition step efficiently. Merge sort doesn't need random
       access.

So: arrays → prefer quick sort. Linked lists → use merge sort. This
is one of the clearest cases where the data structure dictates the
algorithm.

---------------------------------------------------
The Algorithm:

    1. Split: use fast-slow pointers to find the middle; split into
       two halves.
    2. Recurse: sort each half.
    3. Merge: splice two sorted linked lists by walking both with
       a dummy head.

---------------------------------------------------
Example:

    Input:  4 -> 2 -> 1 -> 3
    Output: 1 -> 2 -> 3 -> 4

---------------------------------------------------
"""

# =========================================================================
# Linked List Node and Builders
# =========================================================================

class ListNode:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

    def __repr__(self):
        return f"ListNode({self.value})"


def build_list(values):
    """Build a singly linked list from an iterable; return head."""
    if not values:
        return None
    head = ListNode(values[0])
    current = head
    for v in values[1:]:
        current.next = ListNode(v)
        current = current.next
    return head


def list_to_python(head):
    """Convert a linked list to a Python list for easy inspection."""
    result = []
    while head:
        result.append(head.value)
        head = head.next
    return result


# =========================================================================
# Merge Sort on a Linked List
# =========================================================================

def sort_list(head):
    """
    Sort a singly linked list via merge sort.

    Time:   O(n log n)
    Space:  O(log n) for the recursion stack; O(1) beyond that.
    Stable: Yes
    """
    if head is None or head.next is None:
        return head                               # 0 or 1 element

    # 1. Split in half using fast-slow pointers
    mid = _split_middle(head)

    # 2. Recursively sort each half
    left = sort_list(head)
    right = sort_list(mid)

    # 3. Merge the two sorted halves
    return _merge_sorted_lists(left, right)


def _split_middle(head):
    """
    Walk fast/slow pointers to split the list in half. Returns the head
    of the SECOND half; the first half ends at `slow_prev.next = None`.

    For even n, the second half is one longer than the first. That's
    standard for this problem.
    """
    slow = head
    fast = head.next                              # start fast ahead of slow

    # when fast hits the end, slow is just BEFORE the midpoint
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # slow.next is the start of the second half
    second_half = slow.next
    slow.next = None                              # terminate first half
    return second_half


def _merge_sorted_lists(a, b):
    """
    Merge two sorted linked lists in place.

    Uses a dummy head to simplify the "first node to attach" case.

    Time:   O(len(a) + len(b))
    Space:  O(1) — rearranges existing nodes, no new nodes allocated
    """
    dummy = ListNode(0)
    tail = dummy

    while a and b:
        if a.value <= b.value:                    # <= for stability
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next

    # attach the remaining non-null list
    tail.next = a if a else b

    return dummy.next


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    # Classic example
    head = build_list([4, 2, 1, 3])
    sorted_head = sort_list(head)
    print(f"Input:  [4, 2, 1, 3]")
    print(f"Sorted: {list_to_python(sorted_head)}")
    print()

    # Test cases
    test_cases = [
        [4, 2, 1, 3],
        [],
        [5],
        [1, 2, 3, 4, 5],                          # already sorted
        [5, 4, 3, 2, 1],                          # reverse sorted
        [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5],
        [0, -1, 2, -3, 4, -5],
        [7, 7, 7, 7, 7],
        [1, 1, 2, 2, 3, 3],                       # duplicates
    ]

    for i, data in enumerate(test_cases):
        head = build_list(data)
        sorted_head = sort_list(head)
        got = list_to_python(sorted_head)
        expected = sorted(data)
        assert got == expected, (
            f"Test {i+1} failed: expected {expected}, got {got}"
        )
        print(f"Test {i+1} passed: {data} -> {got}")

    # Stability check — sort tuples' by first element
    pairs = [(1, "a"), (2, "b"), (1, "c"), (2, "d"), (1, "e")]

    def sort_list_pairs(head):
        if head is None or head.next is None:
            return head

        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        second = slow.next
        slow.next = None

        left = sort_list_pairs(head)
        right = sort_list_pairs(second)

        dummy = ListNode(None)
        tail = dummy
        while left and right:
            if left.value[0] <= right.value[0]:
                tail.next = left
                left = left.next
            else:
                tail.next = right
                right = right.next
            tail = tail.next
        tail.next = left or right
        return dummy.next

    head = build_list(pairs)
    sorted_head = sort_list_pairs(head)
    sorted_pairs = list_to_python(sorted_head)
    assert sorted_pairs == [(1, "a"), (1, "c"), (1, "e"), (2, "b"), (2, "d")]
    print(f"\nStability check passed: {sorted_pairs}")

    # Stress test
    import random
    random.seed(13)
    for _ in range(100):
        n = random.randint(0, 50)
        data = [random.randint(-100, 100) for _ in range(n)]
        head = build_list(data)
        sorted_head = sort_list(head)
        assert list_to_python(sorted_head) == sorted(data)

    print("\nStress test: 100 random linked lists matched sorted()")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Why Merge Sort on a Linked List Is Cleaner:
    #
    #   - Split is a single fast-slow walk (O(n/2) nodes touched).
    #   - Merge is node-level splicing; no copying, no buffer.
    #   - Total auxiliary space: just the recursion stack (O(log n)).
    #
    #   Contrast with quicksort on a linked list:
    #     - Partition needs a pivot pick (O(1)), but walk is O(n).
    #     - Partitioning is clumsier: need to relink nodes into two
    #       sublists, handle pointers carefully.
    #     - Worst case O(n²) lurks (random pivot helps, but the
    #       bookkeeping is painful).
    #
    # On linked lists, the costs favor merge sort by a clear margin.
    # ---------------------------------------------------------------
