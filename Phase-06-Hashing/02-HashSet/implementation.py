"""
implementation.py – HashSet via Separate Chaining

A HashSet is a HashMap without the values: each bucket holds a list of
ELEMENTS instead of (key, value) pairs. We could cheat and wrap our
HashMap (storing each element twice, once as key once as value), but
a standalone implementation is ~20% smaller AND lets us implement the
interesting set-theoretic operations (union, intersection, difference)
in a natural way.

---------------------------------------------------
Complexity:

    add, remove, contains:  O(1) average, O(n) worst
    union, intersection, difference: O(|a| + |b|) average

Resizes when load factor exceeds 0.75 — same threshold as our chained
HashMap.
"""


class HashSet:
    """
    Hash-based set with separate chaining.

    Buckets are plain Python lists. Since duplicates are not allowed,
    each bucket has at most a few elements once load factor is bounded.
    """

    INITIAL_CAPACITY = 8
    LOAD_FACTOR_THRESHOLD = 0.75

    def __init__(self, iterable=None):
        self._capacity = HashSet.INITIAL_CAPACITY
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0
        if iterable is not None:
            for x in iterable:
                self.add(x)

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
    # Core operations
    # ------------------------------------------------------------------

    def _bucket_index(self, x):
        return hash(x) % self._capacity

    def add(self, x):
        """Insert `x`. No-op if already present. Amortized O(1)."""
        bucket = self._buckets[self._bucket_index(x)]
        for existing in bucket:
            if existing == x:
                return                             # already present
        bucket.append(x)
        self._size += 1
        if self.load_factor() > HashSet.LOAD_FACTOR_THRESHOLD:
            self._resize(self._capacity * 2)

    def remove(self, x):
        """Remove `x`. Raises KeyError if absent. O(1) average."""
        bucket = self._buckets[self._bucket_index(x)]
        for i, existing in enumerate(bucket):
            if existing == x:
                del bucket[i]
                self._size -= 1
                return
        raise KeyError(x)

    def discard(self, x):
        """Remove `x` if present; otherwise do nothing (like Python's set.discard)."""
        bucket = self._buckets[self._bucket_index(x)]
        for i, existing in enumerate(bucket):
            if existing == x:
                del bucket[i]
                self._size -= 1
                return

    def contains(self, x):
        bucket = self._buckets[self._bucket_index(x)]
        for existing in bucket:
            if existing == x:
                return True
        return False

    # ------------------------------------------------------------------
    # Resize
    # ------------------------------------------------------------------

    def _resize(self, new_capacity):
        old_buckets = self._buckets
        self._capacity = new_capacity
        self._buckets = [[] for _ in range(new_capacity)]
        self._size = 0
        for bucket in old_buckets:
            for x in bucket:
                self.add(x)

    # ------------------------------------------------------------------
    # Python set-ish interface
    # ------------------------------------------------------------------

    def __contains__(self, x):
        return self.contains(x)

    def __iter__(self):
        for bucket in self._buckets:
            for x in bucket:
                yield x

    def __repr__(self):
        return "HashSet({" + ", ".join(repr(x) for x in self) + "})"

    def __eq__(self, other):
        if not isinstance(other, HashSet):
            return NotImplemented
        if len(self) != len(other):
            return False
        return all(x in other for x in self)

    # ------------------------------------------------------------------
    # Set-theoretic operations
    # ------------------------------------------------------------------
    #
    # The recipes are simple, but each has a subtle optimization:
    #   union         — iterate through whichever is smaller for the SECOND pass,
    #                   but we just scan both into the result
    #   intersection  — iterate through the SMALLER set, probe the larger
    #   difference    — iterate through self, probe other

    def union(self, other):
        """Return a new HashSet containing every element in self OR other."""
        result = HashSet()
        for x in self:
            result.add(x)
        for x in other:
            result.add(x)
        return result

    def intersection(self, other):
        """Return a new HashSet containing elements in BOTH self and other."""
        # Iterate the smaller set for fewer lookups
        small, large = (self, other) if len(self) <= len(other) else (other, self)
        result = HashSet()
        for x in small:
            if x in large:
                result.add(x)
        return result

    def difference(self, other):
        """Return a new HashSet of elements in self but NOT in other."""
        result = HashSet()
        for x in self:
            if x not in other:
                result.add(x)
        return result

    def symmetric_difference(self, other):
        """Return a new HashSet of elements in EXACTLY ONE of self / other."""
        result = HashSet()
        for x in self:
            if x not in other:
                result.add(x)
        for x in other:
            if x not in self:
                result.add(x)
        return result

    # Operator overloads for the set-theoretic ops
    def __or__(self, other):  return self.union(other)
    def __and__(self, other): return self.intersection(other)
    def __sub__(self, other): return self.difference(other)
    def __xor__(self, other): return self.symmetric_difference(other)


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Basic add / contains / remove
    s = HashSet()
    assert s.is_empty()
    assert 42 not in s

    s.add(1)
    s.add(2)
    s.add(3)
    s.add(2)                                       # duplicate, no-op
    assert len(s) == 3
    assert 1 in s and 2 in s and 3 in s
    assert 4 not in s

    # discard vs remove
    s.discard(99)                                  # no-op
    s.remove(2)
    assert 2 not in s
    try:
        s.remove(2)
    except KeyError:
        pass
    else:
        raise AssertionError("expected KeyError on double-remove")

    # Construction from iterable
    s = HashSet([1, 2, 3, 2, 1])
    assert len(s) == 3

    # Iteration
    assert set(s) == {1, 2, 3}

    # Equality
    assert HashSet([1, 2, 3]) == HashSet([3, 2, 1])
    assert HashSet([1, 2, 3]) != HashSet([1, 2])

    # Set operations
    a = HashSet([1, 2, 3, 4])
    b = HashSet([3, 4, 5, 6])
    assert set(a | b) == {1, 2, 3, 4, 5, 6}
    assert set(a & b) == {3, 4}
    assert set(a - b) == {1, 2}
    assert set(b - a) == {5, 6}
    assert set(a ^ b) == {1, 2, 5, 6}

    # Resize under load
    s = HashSet()
    initial_capacity = s.capacity()
    for i in range(100):
        s.add(i)
    assert len(s) == 100
    assert s.capacity() > initial_capacity
    print(f"After 100 adds: size={len(s)}, capacity={s.capacity()}, lf={s.load_factor():.2f}")

    # Adding existing elements does NOT resize
    for i in range(100):
        s.add(i)
    assert len(s) == 100

    # Stress test against Python's set
    import random
    random.seed(42)
    mine = HashSet()
    py = set()

    for _ in range(5_000):
        op = random.choice(["add", "discard", "contains"])
        x = random.randint(0, 200)
        if op == "add":
            mine.add(x)
            py.add(x)
        elif op == "discard":
            mine.discard(x)
            py.discard(x)
        else:
            assert (x in mine) == (x in py)
        assert len(mine) == len(py)

    assert set(mine) == py

    # Set ops against Python set
    a_py = {random.randint(0, 100) for _ in range(50)}
    b_py = {random.randint(0, 100) for _ in range(50)}
    a_hs = HashSet(a_py)
    b_hs = HashSet(b_py)
    assert set(a_hs | b_hs) == (a_py | b_py)
    assert set(a_hs & b_hs) == (a_py & b_py)
    assert set(a_hs - b_hs) == (a_py - b_py)
    assert set(a_hs ^ b_hs) == (a_py ^ b_py)

    print(f"\nStress test: 5000 random ops — matches Python set exactly")
    print(f"   final size: {len(mine)}, capacity: {mine.capacity()}")
    print(f"   set ops (|, &, -, ^) match Python semantics")

    print("\nAll tests passed!")
