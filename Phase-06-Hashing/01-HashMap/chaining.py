"""
chaining.py – HashMap via Separate Chaining

The simplest collision-resolution strategy: each bucket stores a
LINKED LIST (or array) of `(key, value)` pairs. On a collision,
the new pair is appended to the bucket's list.

---------------------------------------------------
Structure:

    buckets: list of buckets, where bucket[i] is a list of (key, value) pairs

    hash(key) → bucket_index
    buckets[bucket_index] = [(k1, v1), (k2, v2), ...]

---------------------------------------------------
Operations:

    put(key, value):
        idx = hash(key) % num_buckets
        for pair in buckets[idx]:
            if pair.key == key:
                pair.value = value       # update existing
                return
        buckets[idx].append((key, value))
        size += 1
        if load_factor > threshold:
            resize()

    get(key):
        idx = hash(key) % num_buckets
        for pair in buckets[idx]:
            if pair.key == key:
                return pair.value
        return None

    remove(key):
        idx = hash(key) % num_buckets
        for i, pair in enumerate(buckets[idx]):
            if pair.key == key:
                del buckets[idx][i]
                size -= 1
                return

---------------------------------------------------
Complexity:

    Average case:  O(1) per op (with good hash + low load factor)
    Worst case:    O(n)    (all keys collide into one bucket)

Load factor (= size / num_buckets) determines behaviour:
    - low load factor    → short chains, fast
    - high load factor   → long chains, slow

Chaining can TOLERATE load factors above 1 (e.g., 5-10 per bucket),
at the cost of slower per-operation constants.

---------------------------------------------------
"""


# Sentinel for pop()'s "no default provided" case
_MISSING = object()


class HashMapChaining:
    """
    Hash map using separate chaining with Python lists as buckets.

    Uses Python's built-in `hash()` (SipHash with randomization) for
    the hash function. Resizes when the load factor exceeds 0.75.
    """

    INITIAL_CAPACITY = 8
    LOAD_FACTOR_THRESHOLD = 0.75

    def __init__(self):
        self._capacity = HashMapChaining.INITIAL_CAPACITY
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def load_factor(self):
        return self._size / self._capacity

    def capacity(self):
        return self._capacity

    # ------------------------------------------------------------------
    # Hash: map any key to a bucket index
    # ------------------------------------------------------------------

    def _bucket_index(self, key):
        return hash(key) % self._capacity

    # ------------------------------------------------------------------
    # Core operations
    # ------------------------------------------------------------------

    def put(self, key, value):
        """
        Insert or update (key, value). Amortized O(1); may trigger resize.
        """
        idx = self._bucket_index(key)
        bucket = self._buckets[idx]

        # Check if the key already exists in this bucket — update in place
        for i, (k, _v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        # Key doesn't exist — append
        bucket.append((key, value))
        self._size += 1

        # Resize if load factor exceeds threshold
        if self.load_factor() > HashMapChaining.LOAD_FACTOR_THRESHOLD:
            self._resize(self._capacity * 2)

    def get(self, key, default=None):
        """Return the value for `key`, or `default` if absent. O(1) average."""
        idx = self._bucket_index(key)
        for k, v in self._buckets[idx]:
            if k == key:
                return v
        return default

    def contains(self, key):
        """True iff `key` is present. O(1) average."""
        idx = self._bucket_index(key)
        for k, _v in self._buckets[idx]:
            if k == key:
                return True
        return False

    def remove(self, key):
        """
        Remove `key` from the map. Raises KeyError if absent.
        O(1) average.
        """
        idx = self._bucket_index(key)
        bucket = self._buckets[idx]
        for i, (k, _v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self._size -= 1
                return
        raise KeyError(key)

    def pop(self, key, default=_MISSING):
        """
        Remove and return the value for `key`. Return `default` if absent.
        If no default is provided, raise KeyError.
        """
        idx = self._bucket_index(key)
        bucket = self._buckets[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self._size -= 1
                return v
        if default is _MISSING:
            raise KeyError(key)
        return default

    # ------------------------------------------------------------------
    # Resize
    # ------------------------------------------------------------------

    def _resize(self, new_capacity):
        """
        Allocate a bigger bucket array and rehash every entry.

        Time: O(n) — every entry visits a new bucket.
        Space: O(n) during resize.
        """
        old_buckets = self._buckets
        self._capacity = new_capacity
        self._buckets = [[] for _ in range(new_capacity)]
        self._size = 0                            # put() will increment back

        for bucket in old_buckets:
            for key, value in bucket:
                self.put(key, value)

    # ------------------------------------------------------------------
    # Python dict-ish interface (__getitem__, __setitem__, etc.)
    # ------------------------------------------------------------------

    def __getitem__(self, key):
        """`map[key]` — O(1) average; raises KeyError if absent."""
        idx = self._bucket_index(key)
        for k, v in self._buckets[idx]:
            if k == key:
                return v
        raise KeyError(key)

    def __setitem__(self, key, value):
        self.put(key, value)

    def __delitem__(self, key):
        self.remove(key)

    def __contains__(self, key):
        return self.contains(key)

    def __iter__(self):
        """Iterate over KEYS (matching dict semantics)."""
        for bucket in self._buckets:
            for k, _v in bucket:
                yield k

    def keys(self):
        return list(iter(self))

    def values(self):
        return [v for bucket in self._buckets for (_k, v) in bucket]

    def items(self):
        return [(k, v) for bucket in self._buckets for (k, v) in bucket]

    def __repr__(self):
        items_str = ", ".join(f"{k!r}: {v!r}" for k, v in self.items())
        return f"HashMapChaining({{{items_str}}})"


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    m = HashMapChaining()
    assert m.is_empty()
    assert m.get("x") is None
    assert "x" not in m

    # Basic insert / get
    m.put("alice", 30)
    m.put("bob", 25)
    m.put("carol", 40)
    assert m.get("alice") == 30
    assert m.get("bob") == 25
    assert m.get("carol") == 40
    assert m.get("missing") is None
    assert m.get("missing", "default") == "default"
    assert len(m) == 3
    print(f"After 3 inserts: {m}")
    print(f"   load factor: {m.load_factor():.2f}")
    print(f"   capacity:    {m.capacity()}")

    # Update existing key
    m.put("alice", 31)
    assert m.get("alice") == 31
    assert len(m) == 3                            # count unchanged

    # Contains / __contains__
    assert m.contains("bob")
    assert "bob" in m
    assert "missing" not in m

    # Remove
    m.remove("bob")
    assert "bob" not in m
    assert len(m) == 2
    try:
        m.remove("bob")
    except KeyError:
        pass
    else:
        raise AssertionError("expected KeyError on double remove")

    # Pop
    v = m.pop("alice")
    assert v == 31
    assert "alice" not in m
    assert m.pop("missing", -1) == -1
    try:
        m.pop("missing")
    except KeyError:
        pass

    # Test resize: insert many keys, verify load factor triggers resize
    m = HashMapChaining()
    initial_capacity = m.capacity()
    for i in range(100):
        m.put(f"key{i}", i)
    assert len(m) == 100
    assert m.capacity() > initial_capacity       # should have resized
    print(f"\nAfter 100 inserts:")
    print(f"   size:        {len(m)}")
    print(f"   capacity:    {m.capacity()}")
    print(f"   load factor: {m.load_factor():.2f}")

    # Every key is still reachable
    for i in range(100):
        assert m.get(f"key{i}") == i

    # Iteration
    keys = set(m)
    assert keys == {f"key{i}" for i in range(100)}

    # Values and items
    assert set(m.values()) == set(range(100))
    assert set(m.items()) == {(f"key{i}", i) for i in range(100)}

    # __setitem__ / __getitem__ / __delitem__
    m["new_key"] = "new_value"
    assert m["new_key"] == "new_value"
    del m["new_key"]
    assert "new_key" not in m

    # KeyError for missing keys
    try:
        _ = m["missing"]
    except KeyError:
        pass
    else:
        raise AssertionError("expected KeyError")

    # Stress test against Python's dict
    import random
    random.seed(42)

    my_map = HashMapChaining()
    py_dict = {}

    for _ in range(5_000):
        op = random.choice(["put", "get", "remove", "contains"])
        key = f"key{random.randint(0, 200)}"

        if op == "put":
            value = random.randint(0, 100)
            my_map.put(key, value)
            py_dict[key] = value
        elif op == "get":
            assert my_map.get(key) == py_dict.get(key)
        elif op == "remove":
            if key in py_dict:
                my_map.remove(key)
                del py_dict[key]
        elif op == "contains":
            assert (key in my_map) == (key in py_dict)

        assert len(my_map) == len(py_dict)

    # Final state matches
    assert set(my_map.keys()) == set(py_dict.keys())
    for k in py_dict:
        assert my_map.get(k) == py_dict[k]

    print("\nStress test: 5000 random ops — matches Python dict exactly")
    print(f"   final size: {len(my_map)}, capacity: {my_map.capacity()}")
    print(f"   load factor: {my_map.load_factor():.2f}")

    print("\nAll tests passed!")
