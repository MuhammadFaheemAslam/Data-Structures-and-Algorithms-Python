"""
open-addressing.py – HashMap via Open Addressing (Linear Probing)

In open addressing, EVERY key lives in the main bucket array — no
auxiliary linked lists. On a collision, we search for the NEXT
empty slot using a PROBING SEQUENCE.

This is what CPython's `dict` uses (with a more sophisticated
probing scheme than what we implement here).

---------------------------------------------------
The Three Probing Schemes:

    Linear probing:       probe h, h+1, h+2, h+3, ...
    Quadratic probing:    probe h, h+1², h+2², h+3², ...
    Double hashing:       probe h, h + h'(k), h + 2h'(k), ...

We implement LINEAR PROBING in the main class (simplest, most
cache-friendly) and sketch the quadratic variant at the end.

---------------------------------------------------
The Tombstone Problem:

Open addressing has one major complication: DELETION.

If you just set a deleted slot to empty, LOOKUP breaks: imagine you
insert `A` at slot 3, `B` at slot 4 (because 3 was full). If you
delete A by setting slot 3 to empty, then looking up B sees "empty
at probe position, so B must not exist" — and returns not-found,
even though B is at slot 4.

Solution: mark deleted slots with a TOMBSTONE (a sentinel marker
meaning "used to be here — keep probing"). Tombstones are treated
as EMPTY for insertion but as FULL for lookup.

This means deletions don't physically free slots; over time,
tombstones accumulate and degrade performance. A good implementation
rehashes periodically to eliminate them.

---------------------------------------------------
Complexity:

    Average case:  O(1) per op (with good hash + low load factor)
    Worst case:    O(n)
    Max recommended load factor: 0.5 — 0.75
                   (lower than chaining because probe chains degrade)

---------------------------------------------------
"""


# Sentinels for slot state
_EMPTY = object()                                 # never been used
_TOMBSTONE = object()                             # was used, then deleted


class HashMapOpenAddressing:
    """
    Hash map with LINEAR PROBING and tombstone-based deletion.

    Slot values:
        _EMPTY      — never used; lookup stops here
        _TOMBSTONE  — was used, now deleted; lookup continues past
        (key, val)  — active entry
    """

    INITIAL_CAPACITY = 8
    LOAD_FACTOR_THRESHOLD = 0.5                   # lower than chaining's 0.75

    def __init__(self):
        self._capacity = HashMapOpenAddressing.INITIAL_CAPACITY
        self._slots = [_EMPTY] * self._capacity
        self._size = 0                             # active entries
        self._tombstones = 0                       # deleted slots

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def load_factor(self):
        """Load factor counts active + tombstone slots, since both block probing."""
        return (self._size + self._tombstones) / self._capacity

    def capacity(self):
        return self._capacity

    # ------------------------------------------------------------------
    # Probing
    # ------------------------------------------------------------------

    def _hash(self, key):
        return hash(key) % self._capacity

    def _find_slot(self, key):
        """
        Linear-probe to find either:
            (a) a slot containing `key` (for lookup/remove), or
            (b) the first EMPTY/TOMBSTONE slot (for insert).

        Returns (slot_index, found_existing):
            found_existing = True  if the slot contains `key`
                             False if the slot is EMPTY or a tombstone
                                    (meaning `key` is not in the table,
                                     and this is where it'd be inserted)
        """
        idx = self._hash(key)
        first_tombstone = -1                       # remember first tombstone for insertion

        while True:
            slot = self._slots[idx]

            if slot is _EMPTY:
                # End of probe chain — key not found
                return (first_tombstone if first_tombstone != -1 else idx, False)

            if slot is _TOMBSTONE:
                if first_tombstone == -1:
                    first_tombstone = idx
            elif slot[0] == key:
                # Found
                return (idx, True)

            idx = (idx + 1) % self._capacity       # linear probing

    # ------------------------------------------------------------------
    # Core operations
    # ------------------------------------------------------------------

    def put(self, key, value):
        """Insert or update. Amortized O(1). Triggers resize near load-factor threshold."""
        slot_idx, found = self._find_slot(key)

        if found:
            # Update in place
            self._slots[slot_idx] = (key, value)
            return

        # New insertion
        was_tombstone = self._slots[slot_idx] is _TOMBSTONE
        self._slots[slot_idx] = (key, value)

        if was_tombstone:
            self._tombstones -= 1
        self._size += 1

        if self.load_factor() > HashMapOpenAddressing.LOAD_FACTOR_THRESHOLD:
            self._resize(self._capacity * 2)

    def get(self, key, default=None):
        """Return the value for `key`, or `default` if absent. O(1) average."""
        slot_idx, found = self._find_slot(key)
        if found:
            return self._slots[slot_idx][1]
        return default

    def contains(self, key):
        _slot_idx, found = self._find_slot(key)
        return found

    def remove(self, key):
        """Remove `key`. Raises KeyError if absent. O(1) average."""
        slot_idx, found = self._find_slot(key)
        if not found:
            raise KeyError(key)

        self._slots[slot_idx] = _TOMBSTONE
        self._size -= 1
        self._tombstones += 1

        # If tombstones accumulate too much, rehash without resizing up
        if self._tombstones > self._capacity // 4:
            self._resize(self._capacity)          # same size — just clears tombstones

    # ------------------------------------------------------------------
    # Resize
    # ------------------------------------------------------------------

    def _resize(self, new_capacity):
        """Rehash all active entries into a fresh slot array."""
        old_slots = self._slots
        self._capacity = new_capacity
        self._slots = [_EMPTY] * new_capacity
        self._size = 0
        self._tombstones = 0

        for slot in old_slots:
            if slot is _EMPTY or slot is _TOMBSTONE:
                continue
            key, value = slot
            self.put(key, value)

    # ------------------------------------------------------------------
    # Python dict-ish interface
    # ------------------------------------------------------------------

    def __getitem__(self, key):
        slot_idx, found = self._find_slot(key)
        if not found:
            raise KeyError(key)
        return self._slots[slot_idx][1]

    def __setitem__(self, key, value):
        self.put(key, value)

    def __delitem__(self, key):
        self.remove(key)

    def __contains__(self, key):
        return self.contains(key)

    def __iter__(self):
        for slot in self._slots:
            if slot is _EMPTY or slot is _TOMBSTONE:
                continue
            yield slot[0]

    def keys(self):
        return list(iter(self))

    def values(self):
        return [slot[1] for slot in self._slots if slot is not _EMPTY and slot is not _TOMBSTONE]

    def items(self):
        return [slot for slot in self._slots if slot is not _EMPTY and slot is not _TOMBSTONE]

    def __repr__(self):
        items_str = ", ".join(f"{k!r}: {v!r}" for k, v in self.items())
        return f"HashMapOpenAddressing({{{items_str}}})"


# =========================================================================
# Bonus: Quadratic Probing Variant
# =========================================================================

class HashMapQuadraticProbing(HashMapOpenAddressing):
    """
    Same as HashMapOpenAddressing but with QUADRATIC probing:
        probe h, h+1², h+2², h+3², ... (mod capacity)

    Advantages:
        - Avoids "primary clustering" (long runs of consecutive taken slots).
        - Better distribution on many adversarial inputs.

    Disadvantages:
        - Worse cache behaviour (jumps around).
        - Tricky math: to ensure we visit every slot, capacity should be a power of 2
          and we probe with triangular numbers (h, h+1, h+3, h+6, ...). We use the
          simpler (but imperfect) h+i² form below.
    """

    def _find_slot(self, key):
        base = self._hash(key)
        first_tombstone = -1

        for i in range(self._capacity):
            idx = (base + i * i) % self._capacity
            slot = self._slots[idx]

            if slot is _EMPTY:
                return (first_tombstone if first_tombstone != -1 else idx, False)

            if slot is _TOMBSTONE:
                if first_tombstone == -1:
                    first_tombstone = idx
            elif slot[0] == key:
                return (idx, True)

        # Every slot was FULL or a tombstone — shouldn't happen if we resize in time
        if first_tombstone != -1:
            return (first_tombstone, False)
        raise RuntimeError("HashMap full — resize didn't fire in time")


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    for cls in (HashMapOpenAddressing, HashMapQuadraticProbing):
        print(f"\n=== {cls.__name__} ===")

        m = cls()
        assert m.is_empty()

        m.put("alice", 30)
        m.put("bob", 25)
        m.put("carol", 40)
        assert m.get("alice") == 30
        assert m.get("bob") == 25
        assert m.get("missing") is None
        assert m.get("missing", "default") == "default"
        assert len(m) == 3

        # Update
        m.put("alice", 31)
        assert m.get("alice") == 31
        assert len(m) == 3

        # Remove → tombstone
        m.remove("bob")
        assert "bob" not in m
        assert len(m) == 2

        # After delete, we can still find other keys (tombstone doesn't break lookup)
        assert m.get("alice") == 31
        assert m.get("carol") == 40

        # Re-insert the removed key — should claim the tombstone slot
        m.put("bob", 26)
        assert m.get("bob") == 26

        # Stress test
        import random
        random.seed(42)

        my_map = cls()
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

        assert set(my_map.keys()) == set(py_dict.keys())
        for k in py_dict:
            assert my_map.get(k) == py_dict[k]

        print(f"   Stress test: 5000 random ops passed")
        print(f"   final size: {len(my_map)}, capacity: {my_map.capacity()}")
        print(f"   load factor: {my_map.load_factor():.2f}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Open Addressing vs Chaining — The Practical Choice:
    #
    #                   Chaining           Open Addressing
    #   Load factor:    up to ~10          up to ~0.7
    #   Cache:          poor (linked)       excellent (contiguous)
    #   Memory:         more (ptrs)         less (but unused slots)
    #   Deletion:       simple              needs tombstones
    #   Worst case:     O(n) chain           O(n) probe chain
    #   Used in:        Java HashMap         Python dict, Rust HashMap, Go map
    #
    # Open addressing wins for CACHE locality, which matters much
    # more on modern CPUs than the theoretical Big-O. That's why
    # CPython, Rust, and Go all use it.
    # ---------------------------------------------------------------
