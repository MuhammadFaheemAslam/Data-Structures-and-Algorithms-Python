"""
Problem: LRU Cache

Difficulty: Medium (LeetCode #146)

---------------------------------------------------
Problem Statement:

Design a data structure that follows the LEAST RECENTLY USED (LRU)
eviction policy with capacity `cap`:

    LRUCache(cap)            — initialize with max capacity `cap`
    get(key) -> int          — return value for key, or -1 if absent;
                                ALSO marks the entry as most-recently-used.
    put(key, value)          — insert or update. If the cache is at
                                capacity, evict the least-recently-used
                                entry BEFORE inserting.

Every operation must be O(1) average.

---------------------------------------------------
The Classic Design: HashMap + Doubly-Linked List

To get O(1) `get`, O(1) `put`, AND O(1) eviction of the oldest, we
combine two data structures:

    Doubly-linked list:   stores entries in USAGE ORDER
                          (most recent at head, oldest at tail).
                          Any node can be moved to head in O(1)
                          because we have prev/next pointers.

    Hash map:             key → node, so we can LOCATE a node by
                          key in O(1).

On `get(key)`:
    node = hashmap[key]
    move node to head of DLL          (mark as most-recent)
    return node.value

On `put(key, value)`:
    if key in hashmap:
        update node.value; move to head
    else:
        if size == cap:
            remove tail node from DLL; delete its key from hashmap
        create new node at head; insert key → node in hashmap

---------------------------------------------------
Why This Problem Is a Classic:

It combines TWO data structures to achieve a complexity that neither
could achieve alone:

    - DLL alone: O(1) reorder, but O(n) key lookup
    - Dict alone: O(1) key lookup, but no ordering

Together: O(1) everything. This kind of structural COMBINATION is
the heart of advanced data-structure design (see LFU, Timeline,
DataStream with top-k, etc.).

---------------------------------------------------
Two Implementations Below:

    1. Manual DLL + our HashMapChaining (the from-scratch version)
    2. Python's collections.OrderedDict (the one-liner for prod)
"""

import os
import sys

# Import our HashMap from the sibling directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from chaining import HashMapChaining


# =========================================================================
# Solution 1: Manual DLL + Our HashMap
# =========================================================================

class _Node:
    """Doubly-linked list node holding (key, value)."""
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    """
    O(1) LRU cache built from scratch on our HashMapChaining + a DLL.

    DLL has sentinel head and tail nodes to simplify edge cases:
        head <-> [most recent] <-> ... <-> [oldest] <-> tail
    """

    def __init__(self, capacity):
        self.capacity = capacity
        self._map = HashMapChaining()              # key -> _Node
        self._head = _Node(None, None)             # sentinel (most-recent side)
        self._tail = _Node(None, None)             # sentinel (least-recent side)
        self._head.next = self._tail
        self._tail.prev = self._head

    # ---- DLL helpers (all O(1)) ----

    def _remove(self, node):
        """Unlink `node` from the DLL."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_front(self, node):
        """Insert `node` right after the head sentinel (most-recent position)."""
        node.prev = self._head
        node.next = self._head.next
        self._head.next.prev = node
        self._head.next = node

    def _move_to_front(self, node):
        self._remove(node)
        self._add_to_front(node)

    # ---- Public API ----

    def get(self, key):
        """O(1). Return value or -1. Touching a key marks it most-recent."""
        if key not in self._map:
            return -1
        node = self._map[key]
        self._move_to_front(node)
        return node.value

    def put(self, key, value):
        """O(1). Insert/update. Evict LRU if we'd exceed capacity."""
        if key in self._map:
            node = self._map[key]
            node.value = value
            self._move_to_front(node)
            return

        if len(self._map) == self.capacity:
            lru = self._tail.prev                  # node just before tail sentinel
            self._remove(lru)
            self._map.remove(lru.key)

        node = _Node(key, value)
        self._add_to_front(node)
        self._map.put(key, node)

    def __len__(self):
        return len(self._map)

    def __repr__(self):
        """Show entries from most- to least-recent."""
        items = []
        cur = self._head.next
        while cur is not self._tail:
            items.append(f"{cur.key}:{cur.value}")
            cur = cur.next
        return f"LRUCache([{', '.join(items)}])"


# =========================================================================
# Solution 2: The One-Liner (OrderedDict)
# =========================================================================

from collections import OrderedDict


class LRUCacheOrdered:
    """
    Python's `OrderedDict` already tracks insertion order AND supports
    O(1) move-to-end and O(1) pop-from-front. So the whole problem
    collapses to ~10 lines.

    In production, this IS the right answer. The manual version above
    is for when you're asked to implement it in a language without
    such a data structure, or in an interview.
    """

    def __init__(self, capacity):
        self.capacity = capacity
        self._d = OrderedDict()

    def get(self, key):
        if key not in self._d:
            return -1
        self._d.move_to_end(key)
        return self._d[key]

    def put(self, key, value):
        if key in self._d:
            self._d.move_to_end(key)
        elif len(self._d) == self.capacity:
            self._d.popitem(last=False)            # pop oldest (front)
        self._d[key] = value

    def __len__(self):
        return len(self._d)


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    for cls in (LRUCache, LRUCacheOrdered):
        print(f"\n=== {cls.__name__} ===")

        # LC #146 example
        cache = cls(2)
        cache.put(1, 1)
        cache.put(2, 2)
        assert cache.get(1) == 1                   # {2=2, 1=1}  (1 now MRU)
        cache.put(3, 3)                            # evicts key 2
        assert cache.get(2) == -1
        cache.put(4, 4)                            # evicts key 1
        assert cache.get(1) == -1
        assert cache.get(3) == 3
        assert cache.get(4) == 4

        # Update an existing key: value replaced, MRU refreshed, no eviction
        cache = cls(2)
        cache.put(1, 10)
        cache.put(2, 20)
        cache.put(1, 100)                          # update, not evict
        assert len(cache) == 2
        assert cache.get(1) == 100
        cache.put(3, 30)                           # evicts 2 (LRU)
        assert cache.get(2) == -1
        assert cache.get(1) == 100
        assert cache.get(3) == 30

        # Capacity 1
        cache = cls(1)
        cache.put("a", 1)
        cache.put("b", 2)                          # evicts "a"
        assert cache.get("a") == -1
        assert cache.get("b") == 2

        # Stress test: compare both implementations side-by-side
        import random
        random.seed(42)

        a = LRUCache(50)
        b = LRUCacheOrdered(50)

        for _ in range(5_000):
            op = random.choice(["put", "get"])
            key = random.randint(0, 100)
            if op == "put":
                v = random.randint(0, 1000)
                a.put(key, v)
                b.put(key, v)
            else:
                assert a.get(key) == b.get(key)

        print(f"   Stress test: 5000 ops — matches OrderedDict LRU exactly")
        print(f"   final size:  {len(a)}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Follow-up — LFU Cache (LC #460):
    #
    #   LFU (Least Frequently Used) is a noticeably harder variant.
    #   When items have equal frequency, ties break by LRU — which
    #   means you need:
    #
    #       freq -> DLL of (key, value) at that freq (for LRU order)
    #       key  -> (node, freq)
    #       min_freq tracker
    #
    #   Same ideas, one more level of indirection. Try it next!
    # ---------------------------------------------------------------
