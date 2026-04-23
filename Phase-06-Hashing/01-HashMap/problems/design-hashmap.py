"""
Problem: Design HashMap

Difficulty: Easy (LeetCode #706)

---------------------------------------------------
Problem Statement:

Design a HashMap without using any built-in hash-table libraries.
Implement the MyHashMap class:

    MyHashMap()              — initialize the object with an empty map
    put(key, value)          — insert (key, value). Overwrite if key exists.
    get(key) -> int          — return value for key, or -1 if absent.
    remove(key)              — remove the mapping if key exists.

Constraints:
    0 <= key, value <= 10^6
    At most 10^4 calls total.
    Must run well under a second.

---------------------------------------------------
Why This Problem Matters:

This is the "interview version" of what you just built in `chaining.py`.
The LC constraints are friendly (keys are small non-negative ints),
so a TRIVIAL fixed-size bucket array would pass — but that's boring.

Here we present three progressively better solutions:

    1. Naïve fixed-size array (passes LC, doesn't scale)
    2. Separate chaining with dynamic resize
    3. Open addressing with linear probing

All three are ~40 lines each. The distinctions we learned in the
module (load factor, tombstones, probe chains) all appear.

---------------------------------------------------
Complexity (all three):

    Average: O(1)  put / get / remove
    Worst:   O(n)  (colliding keys)
"""


# =========================================================================
# Solution 1: Fixed-Size Bucket Array (the "cheat" LC accepts)
# =========================================================================

class MyHashMapFixed:
    """
    Exploits LC's tiny key range. With 10^6 possible keys and 10^4 calls,
    a direct-index array of size ~1000 keeps chains at ~10 elements.

    This is NOT a general-purpose hash map — it breaks if keys are large,
    or non-integer. But it illustrates why domain knowledge matters when
    choosing data structures.
    """

    NUM_BUCKETS = 1009                             # prime, ~sqrt(10^6)

    def __init__(self):
        self._buckets = [[] for _ in range(MyHashMapFixed.NUM_BUCKETS)]

    def _idx(self, key):
        return key % MyHashMapFixed.NUM_BUCKETS

    def put(self, key, value):
        bucket = self._buckets[self._idx(key)]
        for i, (k, _v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))

    def get(self, key):
        for k, v in self._buckets[self._idx(key)]:
            if k == key:
                return v
        return -1

    def remove(self, key):
        bucket = self._buckets[self._idx(key)]
        for i, (k, _v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return


# =========================================================================
# Solution 2: Separate Chaining With Resize (general-purpose)
# =========================================================================

class MyHashMapChaining:
    """
    General-purpose chained hash map that works for any hashable keys.
    Resizes when load factor exceeds 0.75.

    Essentially a stripped-down version of `chaining.py` matching the
    LC interface (get returns -1 instead of None, remove is silent).
    """

    INITIAL_CAPACITY = 16
    LOAD_FACTOR_THRESHOLD = 0.75

    def __init__(self):
        self._capacity = MyHashMapChaining.INITIAL_CAPACITY
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0

    def _idx(self, key):
        return hash(key) % self._capacity

    def put(self, key, value):
        bucket = self._buckets[self._idx(key)]
        for i, (k, _v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1
        if self._size / self._capacity > MyHashMapChaining.LOAD_FACTOR_THRESHOLD:
            self._resize()

    def get(self, key):
        for k, v in self._buckets[self._idx(key)]:
            if k == key:
                return v
        return -1

    def remove(self, key):
        bucket = self._buckets[self._idx(key)]
        for i, (k, _v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self._size -= 1
                return

    def _resize(self):
        old = self._buckets
        self._capacity *= 2
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0
        for bucket in old:
            for k, v in bucket:
                self.put(k, v)


# =========================================================================
# Solution 3: Open Addressing With Linear Probing + Tombstones
# =========================================================================

_EMPTY = object()
_TOMBSTONE = object()


class MyHashMapOpenAddress:
    """
    Open-addressing variant: flat array of slots, linear probing on
    collision, tombstones on delete.

    Faster in cache-locality terms than chaining; this is the shape
    CPython's own `dict` uses internally.
    """

    INITIAL_CAPACITY = 16
    LOAD_FACTOR_THRESHOLD = 0.5

    def __init__(self):
        self._capacity = MyHashMapOpenAddress.INITIAL_CAPACITY
        self._slots = [_EMPTY] * self._capacity
        self._size = 0
        self._tombstones = 0

    def _find(self, key):
        idx = hash(key) % self._capacity
        first_tomb = -1
        while True:
            slot = self._slots[idx]
            if slot is _EMPTY:
                return (first_tomb if first_tomb != -1 else idx, False)
            if slot is _TOMBSTONE:
                if first_tomb == -1:
                    first_tomb = idx
            elif slot[0] == key:
                return (idx, True)
            idx = (idx + 1) % self._capacity

    def put(self, key, value):
        idx, found = self._find(key)
        if found:
            self._slots[idx] = (key, value)
            return
        was_tomb = self._slots[idx] is _TOMBSTONE
        self._slots[idx] = (key, value)
        if was_tomb:
            self._tombstones -= 1
        self._size += 1
        if (self._size + self._tombstones) / self._capacity > MyHashMapOpenAddress.LOAD_FACTOR_THRESHOLD:
            self._resize(self._capacity * 2)

    def get(self, key):
        idx, found = self._find(key)
        return self._slots[idx][1] if found else -1

    def remove(self, key):
        idx, found = self._find(key)
        if not found:
            return
        self._slots[idx] = _TOMBSTONE
        self._size -= 1
        self._tombstones += 1

    def _resize(self, new_cap):
        old = self._slots
        self._capacity = new_cap
        self._slots = [_EMPTY] * new_cap
        self._size = 0
        self._tombstones = 0
        for slot in old:
            if slot is _EMPTY or slot is _TOMBSTONE:
                continue
            self.put(slot[0], slot[1])


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    for cls in (MyHashMapFixed, MyHashMapChaining, MyHashMapOpenAddress):
        print(f"\n=== {cls.__name__} ===")
        m = cls()

        # LC #706 example
        m.put(1, 1)
        m.put(2, 2)
        assert m.get(1) == 1
        assert m.get(3) == -1
        m.put(2, 1)                                # update
        assert m.get(2) == 1
        m.remove(2)
        assert m.get(2) == -1

        # Remove of a missing key should be a no-op
        m.remove(999)                              # no error

        # Stress test against Python dict — start from a fresh instance
        import random
        random.seed(42)
        m2 = cls()
        py = {}
        for _ in range(5_000):
            op = random.choice(["put", "get", "remove"])
            k = random.randint(0, 200)
            if op == "put":
                v = random.randint(0, 10 ** 6)
                m2.put(k, v)
                py[k] = v
            elif op == "get":
                expected = py.get(k, -1)
                assert m2.get(k) == expected
            else:
                m2.remove(k)
                py.pop(k, None)

        for k, v in py.items():
            assert m2.get(k) == v
        print(f"   Stress test: 5000 random ops passed")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Which Solution Would You Use in an Interview?
    #
    #   - MyHashMapFixed is DANGEROUS to present: the moment the
    #     interviewer asks "what if keys are strings?" or "what if
    #     keys can be 10^18?", you're rewriting from scratch.
    #
    #   - MyHashMapChaining is the SAFE choice: 40 lines, works for
    #     any hashable key, and you can explain load factor & resize
    #     trade-offs clearly.
    #
    #   - MyHashMapOpenAddress impresses, but be ready to explain
    #     tombstones. Most interviewers will follow up with "why
    #     not just clear the slot?" — nail that and you've shown
    #     real depth.
    # ---------------------------------------------------------------
