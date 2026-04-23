"""
Problem: LRU Cache

Difficulty: Medium (LeetCode #146)

---------------------------------------------------
Problem Statement:

Implement an LRU (Least Recently Used) Cache with these operations,
both **O(1) average time**:

    get(key):       return value or -1 if not present; mark as most recently used
    put(key, val):  insert/update; if cache is full, evict the LEAST recently used entry

Every `get` or `put` counts as an "access" — the key becomes the most
recently used.

---------------------------------------------------
Why LRU Cache Is the Canonical DLL Problem:

LRU cache is the single best real-world example of **combining a
hash map with a doubly-linked list**:

    - The HASH MAP gives O(1) lookup by key.
    - The DOUBLY-LINKED LIST gives O(1) insert/delete GIVEN A NODE.
    - Together: O(1) get, O(1) put, O(1) eviction.

Specifically:

    - HEAD of the DLL = most recently used.
    - TAIL of the DLL = least recently used.
    - The hash map `key → DLL node` lets us find a node in O(1) and
      then `remove_node` / `move_to_front` in O(1).

Without the DLL, "mark as most recently used" would be O(n) (you'd
have to find the entry in some ordered structure and move it). The
DLL's "remove given a node in O(1)" is what makes the whole thing work.

Without the hash map, "find an entry by key" would be O(n). Together
they compose beautifully.

---------------------------------------------------
The Data Structures:

    class Node:
        key, value, prev, next

    class LRUCache:
        capacity : int
        cache    : Dict[key, Node]       # for O(1) lookup
        head, tail : Node                # sentinels

Sentinels eliminate head/tail special cases (same pattern as
../implementation.py).

---------------------------------------------------
The Operations:

    get(key):
        if key not in cache: return -1
        node = cache[key]
        move_to_front(node)
        return node.value

    put(key, value):
        if key in cache:
            node = cache[key]
            node.value = value
            move_to_front(node)
        else:
            if len(cache) == capacity:
                evict the tail node — remove from DLL and from cache
            new_node = Node(key, value)
            insert at head
            cache[key] = new_node

Every operation: O(1) dict op + O(1) DLL op = O(1) total.

---------------------------------------------------
"""


# =========================================================================
# Node (for the DLL inside the cache)
# =========================================================================

class _Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key=None, value=None, prev=None, next=None):
        self.key = key
        self.value = value
        self.prev = prev
        self.next = next


# =========================================================================
# LRU Cache — O(1) get, O(1) put
# =========================================================================

class LRUCache:
    """
    Fixed-capacity LRU cache.

    Internally: hash map {key → DLL node}, plus a doubly-linked list
    with sentinel head (most recent) and sentinel tail (least recent).
    """

    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("capacity must be positive")

        self.capacity = capacity
        self._cache = {}                          # key → Node

        # Sentinels
        self._head = _Node()
        self._tail = _Node()
        self._head.next = self._tail
        self._tail.prev = self._head

    # ------------------------------------------------------------------
    # DLL primitives (O(1) each)
    # ------------------------------------------------------------------

    def _remove_node(self, node):
        """Unlink `node` from the list."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_at_head(self, node):
        """Insert `node` immediately after the sentinel head."""
        node.prev = self._head
        node.next = self._head.next
        self._head.next.prev = node
        self._head.next = node

    def _move_to_head(self, node):
        """Remove `node` from its current position and put it at the head."""
        self._remove_node(node)
        self._insert_at_head(node)

    # ------------------------------------------------------------------
    # Public operations
    # ------------------------------------------------------------------

    def get(self, key):
        """
        Return the value for `key`, or -1 if missing.
        Marks `key` as the most recently used.
        """
        if key not in self._cache:
            return -1
        node = self._cache[key]
        self._move_to_head(node)
        return node.value

    def put(self, key, value):
        """
        Insert or update the value for `key`. If inserting exceeds
        capacity, evict the least-recently-used entry.
        """
        if key in self._cache:
            node = self._cache[key]
            node.value = value
            self._move_to_head(node)
            return

        # Inserting new entry
        if len(self._cache) == self.capacity:
            # Evict the LRU = the node just before the sentinel tail
            lru = self._tail.prev
            self._remove_node(lru)
            del self._cache[lru.key]

        new_node = _Node(key=key, value=value)
        self._cache[key] = new_node
        self._insert_at_head(new_node)

    # ------------------------------------------------------------------
    # Introspection helpers (for tests)
    # ------------------------------------------------------------------

    def __len__(self):
        return len(self._cache)

    def keys_mru_to_lru(self):
        """Return keys ordered from most to least recently used."""
        out = []
        node = self._head.next
        while node is not self._tail:
            out.append(node.key)
            node = node.next
        return out


# =========================================================================
# Test the LRU Cache
# =========================================================================

if __name__ == "__main__":
    # LC #146 canonical example
    print("LC #146 canonical example:")
    cache = LRUCache(2)
    cache.put(1, 1)              # cache = {1=1}
    cache.put(2, 2)              # cache = {1=1, 2=2}
    assert cache.get(1) == 1     # returns 1; marks 1 as MRU → {2=2, 1=1}
    cache.put(3, 3)              # evicts key 2; cache = {1=1, 3=3}
    assert cache.get(2) == -1    # returns -1 (evicted)
    cache.put(4, 4)              # evicts key 1; cache = {3=3, 4=4}
    assert cache.get(1) == -1    # returns -1 (evicted)
    assert cache.get(3) == 3     # returns 3
    assert cache.get(4) == 4     # returns 4
    print(f"   final cache MRU→LRU: {cache.keys_mru_to_lru()}")
    assert cache.keys_mru_to_lru() == [4, 3]
    print("   passed\n")

    # Edge: single-capacity cache
    print("Single-capacity:")
    cache = LRUCache(1)
    cache.put(1, 100)
    assert cache.get(1) == 100
    cache.put(2, 200)
    assert cache.get(1) == -1
    assert cache.get(2) == 200
    print("   passed\n")

    # Edge: update existing key (shouldn't evict)
    print("Update existing key doesn't evict:")
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(1, 100)            # update, not insert
    assert cache.get(1) == 100
    assert cache.get(2) == 2     # still present
    print("   passed\n")

    # Stress test — compare against OrderedDict-based reference
    from collections import OrderedDict
    import random

    class ReferenceLRU:
        """OrderedDict-based LRU cache for cross-validation."""
        def __init__(self, capacity):
            self.capacity = capacity
            self.d = OrderedDict()

        def get(self, key):
            if key not in self.d:
                return -1
            self.d.move_to_end(key, last=False)   # most recent at FRONT
            return self.d[key]

        def put(self, key, value):
            if key in self.d:
                self.d.move_to_end(key, last=False)
                self.d[key] = value
                return
            if len(self.d) == self.capacity:
                self.d.popitem(last=True)          # evict LRU (at back)
            self.d[key] = value
            self.d.move_to_end(key, last=False)

    random.seed(42)
    for trial in range(100):
        capacity = random.randint(1, 10)
        my = LRUCache(capacity)
        ref = ReferenceLRU(capacity)

        for _ in range(500):
            op = random.choice(["get", "put"])
            key = random.randint(0, 15)

            if op == "get":
                a = my.get(key)
                b = ref.get(key)
                assert a == b, f"get({key}): my={a}, ref={b}"
            else:
                val = random.randint(0, 100)
                my.put(key, val)
                ref.put(key, val)

            # MRU→LRU order should match
            assert my.keys_mru_to_lru() == list(ref.d.keys()), (
                f"order mismatch: mine={my.keys_mru_to_lru()}, ref={list(ref.d.keys())}"
            )

    print("Stress test: 100 trials × 500 ops — matches OrderedDict reference")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Why You Should Know This Cold:
    #
    #   LRU cache is THE classic interview question for demonstrating
    #   that you understand when to combine data structures. It comes
    #   up so often it deserves to be muscle memory:
    #
    #     - dict for key lookup
    #     - DLL for ordering (MRU at head, LRU at tail)
    #     - Sentinel nodes to simplify edge cases
    #     - Every operation is O(1)
    #
    #   In real Python code, `collections.OrderedDict` with
    #   `move_to_end(key, last=False)` already implements LRU order —
    #   Python's own `functools.lru_cache` decorator is built on
    #   roughly this same idea.
    # ---------------------------------------------------------------
