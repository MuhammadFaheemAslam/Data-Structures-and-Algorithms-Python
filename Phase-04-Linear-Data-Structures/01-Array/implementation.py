"""
implementation.py – Static Array (Fixed-Size) from Scratch

Python doesn't have a "static array" type — `list` is always dynamic.
To really understand arrays, we implement one with FIXED capacity,
using Python's `ctypes` to allocate a raw C-level array of Python
objects.

This gives us an array that:
    - Has O(1) random access.
    - Rejects out-of-bounds writes (even to empty slots).
    - CAN'T grow — once full, you get an IndexError, not a resize.
    - Has no `insert` or `remove` — those would require shifting,
      which defeats the point of a static array.

This mirrors what a C-style array looks like under the hood. Later,
`dynamic-array.py` builds a dynamic array ON TOP of this static one,
showing how `list` is implemented.

---------------------------------------------------
Why ctypes?

Python's `list` hides the concept of "raw memory" behind a dynamic
interface. To build a true static array, we need to allocate memory
directly. `ctypes.py_object * n` gives us a fixed-size C array of
`n` Python object references — exactly what CPython uses internally.

---------------------------------------------------
"""

import ctypes


class StaticArray:
    """
    A fixed-capacity array of Python objects.

    Capacity is set at creation and cannot change. All operations
    raise IndexError for out-of-range access (both read and write).
    """

    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("capacity must be positive")

        self._capacity = capacity
        self._size = 0
        # Allocate a raw C-level array of `capacity` Python object slots.
        # All slots start uninitialized — we track "valid" slots via self._size.
        self._data = (capacity * ctypes.py_object)()

    # ------------------------------------------------------------------
    # Size queries
    # ------------------------------------------------------------------

    def __len__(self):
        """Current number of VALID elements. O(1)."""
        return self._size

    def capacity(self):
        """Total allocated slots (not the same as len). O(1)."""
        return self._capacity

    def is_full(self):
        return self._size == self._capacity

    def is_empty(self):
        return self._size == 0

    # ------------------------------------------------------------------
    # Access and mutation — O(1)
    # ------------------------------------------------------------------

    def __getitem__(self, index):
        """
        Return arr[index]. Supports negative indexing.

        Time Complexity: O(1)
        """
        index = self._normalize_index(index)
        return self._data[index]

    def __setitem__(self, index, value):
        """
        Set arr[index] = value. Supports negative indexing. Must be
        within [0, size) — you can't "set" an uninitialized slot.

        Time Complexity: O(1)
        """
        index = self._normalize_index(index)
        self._data[index] = value

    # ------------------------------------------------------------------
    # Add at the end — O(1)
    # ------------------------------------------------------------------

    def append(self, value):
        """
        Add `value` to the end. Raises IndexError if full — a static
        array can't grow.

        Time Complexity: O(1)
        """
        if self.is_full():
            raise IndexError("StaticArray is full (capacity reached)")
        self._data[self._size] = value
        self._size += 1

    def pop(self):
        """
        Remove and return the last element.

        Time Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("pop from empty StaticArray")
        self._size -= 1
        value = self._data[self._size]
        # Optional: clear the slot to allow the garbage collector to
        # free the object. Important for arrays of large objects.
        self._data[self._size] = None
        return value

    # ------------------------------------------------------------------
    # Iteration
    # ------------------------------------------------------------------

    def __iter__(self):
        """Iterate over valid elements. O(n)."""
        for i in range(self._size):
            yield self._data[i]

    def __repr__(self):
        elements = ", ".join(repr(x) for x in self)
        return f"StaticArray([{elements}], capacity={self._capacity})"

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _normalize_index(self, index):
        """
        Convert negative indices (e.g., -1 for last) to positive ones.
        Raise IndexError on out-of-range.
        """
        if not isinstance(index, int):
            raise TypeError(f"indices must be integers, not {type(index).__name__}")
        if index < 0:
            index += self._size
        if not 0 <= index < self._size:
            raise IndexError(f"index out of range: {index} (size is {self._size})")
        return index


# =========================================================================
# Test the Static Array
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Creating a StaticArray of capacity 5")
    print("=" * 60)
    arr = StaticArray(5)
    print(f"   arr: {arr}")
    print(f"   len:      {len(arr)}")
    print(f"   capacity: {arr.capacity()}")
    print(f"   is_empty: {arr.is_empty()}")
    print(f"   is_full:  {arr.is_full()}")
    print()

    print("Appending 5 elements")
    for x in [10, 20, 30, 40, 50]:
        arr.append(x)
        print(f"   append({x}) -> {arr}")
    print()

    print("Accessing elements (O(1) random access)")
    print(f"   arr[0] = {arr[0]}")
    print(f"   arr[-1] = {arr[-1]}")
    print(f"   arr[2] = {arr[2]}")
    print()

    print("Setting arr[2] = 999")
    arr[2] = 999
    print(f"   arr: {arr}")
    print()

    print("Iterating")
    for x in arr:
        print(f"   {x}", end="  ")
    print("\n")

    print("Trying to append to a FULL array (should raise IndexError)")
    try:
        arr.append(999)
    except IndexError as e:
        print(f"   IndexError: {e}")
    print()

    print("Popping from the end")
    for _ in range(3):
        print(f"   popped {arr.pop()} -> {arr}")
    print()

    print("Popping from EMPTY (should raise IndexError)")
    # keep popping until empty
    while not arr.is_empty():
        arr.pop()
    try:
        arr.pop()
    except IndexError as e:
        print(f"   IndexError: {e}")
    print()

    # Out-of-range access
    print("Out-of-range access")
    arr.append(1)
    arr.append(2)
    try:
        _ = arr[10]
    except IndexError as e:
        print(f"   arr[10] raised: {e}")
    try:
        arr[10] = 99
    except IndexError as e:
        print(f"   arr[10] = 99 raised: {e}")
    print()

    # Wrong type
    print("Wrong-type index")
    try:
        _ = arr["x"]
    except TypeError as e:
        print(f"   arr['x'] raised: {e}")

    # Test cases
    a = StaticArray(10)
    for i in range(10):
        a.append(i * i)

    assert len(a) == 10
    assert a.is_full()
    assert a[0] == 0
    assert a[-1] == 81
    assert a[5] == 25
    assert list(a) == [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

    popped = a.pop()
    assert popped == 81
    assert len(a) == 9
    assert not a.is_full()

    # Setting in range works
    a[0] = -1
    assert a[0] == -1

    # Setting out of range doesn't
    try:
        a[100] = 99
    except IndexError:
        pass
    else:
        raise AssertionError("expected IndexError")

    # Capacity validation
    try:
        StaticArray(0)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for capacity=0")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # What This Shows:
    #
    #   - Arrays are contiguous memory. ctypes gives us that directly.
    #   - Access by index is O(1) — it's just pointer arithmetic +
    #     one memory load.
    #   - "Fixed size" is a REAL constraint at the memory level.
    #     To grow, you'd have to allocate a NEW array and copy — which
    #     is exactly what the dynamic array (dynamic-array.py) does.
    # ---------------------------------------------------------------
