"""
floyd-algorithm.py – Floyd's Tortoise and Hare

The canonical algorithm for detecting and locating CYCLES in any
sequence where "next" is a deterministic function — linked lists,
iterated integer sequences, function iterations.

Also covered (briefly) in Phase-02 / 02 / 06-Fast-Slow-Pointers,
but with a linked-list-specific spotlight here.

---------------------------------------------------
Complexity:

    Time:   O(n)
    Space:  O(1)

No other algorithm both detects cycles AND locates their start in
O(1) space. A hash set of seen nodes also works but uses O(n) space —
the hash-set approach is fine when memory is available, but fails on
the "do it in O(1) space" interview variant.

---------------------------------------------------
The Algorithm — Two Phases:

Let `head` be the first node of a (possibly cyclic) linked list.
Define the cycle's ENTRY as the first node that's visited TWICE if
you walk forever.

**Phase 1 — Detect a cycle:**

    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next           # one step at a time
        fast = fast.next.next      # two steps at a time
        if slow is fast:
            # they met → there's a cycle
            break
    else:
        # fast reached the end → no cycle
        return None (or False)

**Phase 2 — Find the cycle's entry:**

    slow = head
    while slow is not fast:
        slow = slow.next
        fast = fast.next           # both move at the SAME speed now
    return slow                     # they meet at the cycle entry

---------------------------------------------------
Why Phase 2 Works — The Math:

Let:
    L = distance from head to cycle entry
    C = cycle length
    d = distance from cycle entry to the meeting point (inside the cycle)

When slow and fast first meet:
    slow has traveled  L + d
    fast has traveled  2(L + d)   and also  L + d + k·C  for some integer k ≥ 1
                        (k full laps of the cycle in excess of slow)

Setting those equal:
    2(L + d) = L + d + k·C
    L + d    = k·C
    L        = k·C - d

Now starting from head and from the meeting point, moving both by 1:
    - After L steps from head → at the cycle entry.
    - After L steps from the meeting point → at position d + L = d + k·C - d
      = k·C, which wraps back to the cycle entry.

So they meet at the entry. Beautiful.

---------------------------------------------------
"""


# =========================================================================
# Minimal ListNode (for linked-list use)
# =========================================================================

class ListNode:
    __slots__ = ("val", "next")

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build_list_with_cycle(values, cycle_start_index=-1):
    """
    Build a linked list from `values`. If `cycle_start_index` is ≥ 0,
    the tail's .next points to the node at that index (creating a cycle).

    Returns the head.
    """
    if not values:
        return None

    nodes = [ListNode(v) for v in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]

    if cycle_start_index >= 0:
        nodes[-1].next = nodes[cycle_start_index]

    return nodes[0]


# =========================================================================
# Floyd's — Detect Cycle
# =========================================================================

def has_cycle(head):
    """
    Phase 1 only — return True iff the linked list contains a cycle.

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
# Floyd's — Locate Cycle Start
# =========================================================================

def cycle_start(head):
    """
    Phase 1 + Phase 2 — return the node where the cycle starts, or None.

    Time:  O(n)
    Space: O(1)
    """
    # Phase 1: find the meeting point
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            break
    else:
        # fast hit None → no cycle
        return None

    if fast is None or fast.next is None:
        return None

    # Phase 2: reset slow to head; advance both at speed 1
    slow = head
    while slow is not fast:
        slow = slow.next
        fast = fast.next
    return slow


# =========================================================================
# Hash-Set Alternative (O(n) Space)
# =========================================================================

def has_cycle_hashset(head):
    """
    Hash-set alternative — O(n) time, O(n) space.

    Simpler to reason about than Floyd's; use it when space isn't
    a constraint. Otherwise prefer Floyd's for O(1) space.
    """
    seen = set()
    node = head
    while node is not None:
        if id(node) in seen:
            return True
        seen.add(id(node))
        node = node.next
    return False


def cycle_start_hashset(head):
    """Hash-set version of `cycle_start`. O(n) time, O(n) space."""
    seen = set()
    node = head
    while node is not None:
        if id(node) in seen:
            return node
        seen.add(id(node))
        node = node.next
    return None


# =========================================================================
# Cycle Length (Bonus)
# =========================================================================

def cycle_length(head):
    """
    Return the length of the cycle, or 0 if no cycle exists.

    Time:  O(n)
    Space: O(1)

    After Phase 1 detects a cycle, walk slow around the cycle counting
    steps until it meets fast again.
    """
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            break
    else:
        return 0

    if fast is None or fast.next is None:
        return 0

    # Count around the cycle
    length = 1
    slow = slow.next
    while slow is not fast:
        slow = slow.next
        length += 1
    return length


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    # No cycle
    head = build_list_with_cycle([1, 2, 3, 4, 5])
    assert has_cycle(head) is False
    assert cycle_start(head) is None
    assert cycle_length(head) == 0
    print("No cycle:")
    print(f"   has_cycle:     {has_cycle(head)}")
    print(f"   cycle_start:   {cycle_start(head)}")
    print(f"   cycle_length:  {cycle_length(head)}")

    # Cycle in the middle
    head = build_list_with_cycle([1, 2, 3, 4, 5], cycle_start_index=1)
    assert has_cycle(head) is True
    start = cycle_start(head)
    assert start.val == 2
    assert cycle_length(head) == 4              # cycle: 2 → 3 → 4 → 5 → back to 2
    print("\nCycle from tail back to node[1] (value 2):")
    print(f"   has_cycle:     {has_cycle(head)}")
    print(f"   cycle_start.val: {start.val}")
    print(f"   cycle_length:  {cycle_length(head)}")

    # Self-loop (single node cycle)
    head = build_list_with_cycle([99], cycle_start_index=0)
    assert has_cycle(head) is True
    assert cycle_start(head) is head
    assert cycle_length(head) == 1
    print(f"\nSelf-loop: cycle_start.val = {cycle_start(head).val}, length = {cycle_length(head)}")

    # Empty list
    assert has_cycle(None) is False
    assert cycle_start(None) is None
    assert cycle_length(None) == 0

    # Cross-check hash-set alternative
    import random
    random.seed(42)
    for trial in range(200):
        n = random.randint(0, 30)
        values = list(range(n))
        cycle_idx = random.choice([-1, -1, -1] + list(range(n))) if n > 0 else -1

        head = build_list_with_cycle(values, cycle_idx)
        assert has_cycle(head) == has_cycle_hashset(head)

        a = cycle_start(head)
        b = cycle_start_hashset(head)
        assert (a is None) == (b is None)
        if a is not None:
            assert a is b

    print("\nStress test: 200 trials — Floyd's matches hash-set cycle detection")
    print("\nAll tests passed!")
