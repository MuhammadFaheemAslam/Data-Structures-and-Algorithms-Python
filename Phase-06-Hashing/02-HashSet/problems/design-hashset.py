"""
Problem: Design HashSet

Difficulty: Easy (LeetCode #705)

---------------------------------------------------
Problem Statement:

Design a HashSet without using any built-in hash table libraries.
Implement the MyHashSet class:

    MyHashSet()              — initialize the object
    add(key)                 — insert key
    remove(key)              — remove key if present
    contains(key) -> bool    — true iff key is present

Constraints:
    0 <= key <= 10^6
    At most 10^4 calls total

---------------------------------------------------
Strategy:

Three tiers, same as Design HashMap:

    1. Bit array — exploits LC's small key domain
    2. Separate chaining with dynamic resize (general-purpose)
    3. Open addressing with tombstones (best cache locality)

The bit array is interesting here because, unlike HashMap, we don't
store a value — just a "present" flag. So one BIT per potential key
suffices: 10^6 keys fit in 125 KB, and add/remove/contains are each
a single bit operation.

---------------------------------------------------
Complexity:

    Bit array:          O(1) everything, O(max_key) space
    Chaining:           O(1) average, O(n) worst, O(n) space
    Open addressing:    same as chaining, better cache locality
"""


# =========================================================================
# Solution 1: Bit Array (exploits key domain 0..10^6)
# =========================================================================

class MyHashSetBitArray:
    """
    One bit per possible key. Simple, dense, and O(1) worst-case.

    Only works when keys are non-negative integers in a known small range.
    """

    MAX_KEY = 10 ** 6

    def __init__(self):
        # bytearray of ceil((MAX_KEY + 1) / 8) bytes, each bit = one key
        self._bits = bytearray((MyHashSetBitArray.MAX_KEY // 8) + 1)

    def add(self, key):
        self._bits[key >> 3] |= (1 << (key & 7))

    def remove(self, key):
        self._bits[key >> 3] &= ~(1 << (key & 7))

    def contains(self, key):
        return bool(self._bits[key >> 3] & (1 << (key & 7)))


# =========================================================================
# Solution 2: Separate Chaining With Resize
# =========================================================================

class MyHashSetChaining:
    """
    General-purpose chained HashSet. Works for any hashable key.
    Resizes when load factor exceeds 0.75.
    """

    INITIAL_CAPACITY = 16
    LOAD_FACTOR_THRESHOLD = 0.75

    def __init__(self):
        self._cap = MyHashSetChaining.INITIAL_CAPACITY
        self._buckets = [[] for _ in range(self._cap)]
        self._size = 0

    def _idx(self, key):
        return hash(key) % self._cap

    def add(self, key):
        bucket = self._buckets[self._idx(key)]
        if key in bucket:
            return
        bucket.append(key)
        self._size += 1
        if self._size / self._cap > MyHashSetChaining.LOAD_FACTOR_THRESHOLD:
            self._resize()

    def remove(self, key):
        bucket = self._buckets[self._idx(key)]
        if key in bucket:
            bucket.remove(key)
            self._size -= 1

    def contains(self, key):
        return key in self._buckets[self._idx(key)]

    def _resize(self):
        old = self._buckets
        self._cap *= 2
        self._buckets = [[] for _ in range(self._cap)]
        self._size = 0
        for bucket in old:
            for key in bucket:
                self.add(key)


# =========================================================================
# Solution 3: Open Addressing With Tombstones
# =========================================================================

_EMPTY = object()
_TOMBSTONE = object()


class MyHashSetOpenAddress:
    """
    Linear probing + tombstones. Cache-friendly: one flat array of slots.
    """

    INITIAL_CAPACITY = 16
    LOAD_FACTOR_THRESHOLD = 0.5

    def __init__(self):
        self._cap = MyHashSetOpenAddress.INITIAL_CAPACITY
        self._slots = [_EMPTY] * self._cap
        self._size = 0
        self._tombstones = 0

    def _find(self, key):
        """Return (idx, found). idx is where to INSERT if not found."""
        idx = hash(key) % self._cap
        first_tomb = -1
        while True:
            slot = self._slots[idx]
            if slot is _EMPTY:
                return (first_tomb if first_tomb != -1 else idx, False)
            if slot is _TOMBSTONE:
                if first_tomb == -1:
                    first_tomb = idx
            elif slot == key:
                return (idx, True)
            idx = (idx + 1) % self._cap

    def add(self, key):
        idx, found = self._find(key)
        if found:
            return
        was_tomb = self._slots[idx] is _TOMBSTONE
        self._slots[idx] = key
        if was_tomb:
            self._tombstones -= 1
        self._size += 1
        if (self._size + self._tombstones) / self._cap > MyHashSetOpenAddress.LOAD_FACTOR_THRESHOLD:
            self._resize(self._cap * 2)

    def remove(self, key):
        idx, found = self._find(key)
        if not found:
            return
        self._slots[idx] = _TOMBSTONE
        self._size -= 1
        self._tombstones += 1

    def contains(self, key):
        _idx, found = self._find(key)
        return found

    def _resize(self, new_cap):
        old = self._slots
        self._cap = new_cap
        self._slots = [_EMPTY] * new_cap
        self._size = 0
        self._tombstones = 0
        for slot in old:
            if slot is _EMPTY or slot is _TOMBSTONE:
                continue
            self.add(slot)


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    for cls in (MyHashSetBitArray, MyHashSetChaining, MyHashSetOpenAddress):
        print(f"\n=== {cls.__name__} ===")
        s = cls()

        # LC #705 example
        s.add(1)
        s.add(2)
        assert s.contains(1)
        assert not s.contains(3)
        s.add(2)                                   # no-op
        assert s.contains(2)
        s.remove(2)
        assert not s.contains(2)

        # Idempotent remove
        s.remove(2)                                # no error
        s.remove(999)

        # Stress test against Python set — start fresh
        import random
        random.seed(42)
        mine = cls()
        py = set()
        for _ in range(5_000):
            op = random.choice(["add", "remove", "contains"])
            k = random.randint(0, 200)
            if op == "add":
                mine.add(k)
                py.add(k)
            elif op == "remove":
                mine.remove(k)
                py.discard(k)
            else:
                assert mine.contains(k) == (k in py)

        for k in py:
            assert mine.contains(k)
        print(f"   Stress test: 5000 random ops passed")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Bit array vs general hashing:
    #
    #   The bit-array solution ONLY works because the LC constraint
    #   says 0 <= key <= 10^6. For any real-world API, you'd write
    #   MyHashSetChaining (or wrap your HashMap). Still — noticing
    #   that the constraint allows a direct-indexed solution is
    #   the kind of thing that impresses interviewers.
    # ---------------------------------------------------------------
