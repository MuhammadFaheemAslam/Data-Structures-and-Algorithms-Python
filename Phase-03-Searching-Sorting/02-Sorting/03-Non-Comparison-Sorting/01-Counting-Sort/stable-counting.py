"""
stable-counting.py – Stable Counting Sort (The Textbook Version)

The basic counting sort in `counting-sort.py` loses ordering: it
rewrites the array by walking counts, which doesn't preserve the
input order for satellite data.

The STABLE version — the canonical textbook counting sort — uses a
three-step trick:

    1. COUNT: count[v] = number of occurrences of value v.
    2. PREFIX: count[v] = number of elements with value ≤ v.
               (i.e., the LAST index where v should appear in the output)
    3. BACKWARD WRITE: walk the input from RIGHT to LEFT; for each
       arr[i], place it at output[count[arr[i]] - 1] and decrement.

The backward walk + "count[v] is the last index" invariant means
equal elements land at DECREASING positions in the output — so the
leftmost equal element in the input ends up at the lowest index in
the output. That's stability.

---------------------------------------------------
Time:   O(n + k)
Space:  O(n + k)
Stable: YES

---------------------------------------------------
Why Stability Matters for Counting Sort:

Plain counting sort loses satellite data by construction. But when
sorting RECORDS by a key, you need to preserve each record's
position. Stable counting sort is the only in-family answer.

Even more importantly: **stable counting sort is the required inner
loop for radix sort**. Radix sort's correctness depends on each
digit-level sort being stable — without it, the algorithm just
shuffles digits randomly.

If you only ever care about integers without satellite data, the
simpler `counting_sort()` in the sibling file is fine. For records
or for use inside radix sort, you need this version.

---------------------------------------------------
"""

# =========================================================================
# Stable Counting Sort (the Textbook Version)
# =========================================================================

def stable_counting_sort(arr, key=None):
    """
    Stable counting sort.

    Time:   O(n + k) where k = max key + 1 (keys must be non-negative)
    Space:  O(n + k)
    Stable: Yes

    If `key` is None, the elements themselves are the keys (must be
    non-negative integers). If `key` is a callable, it's applied to
    each element to extract the integer key.

    Returns a NEW sorted list; does not mutate the input.
    """
    if not arr:
        return list(arr)

    # default key is identity
    if key is None:
        key = lambda x: x

    # Step 1: count occurrences of each key
    max_key = max(key(x) for x in arr)
    counts = [0] * (max_key + 1)
    for x in arr:
        counts[key(x)] += 1

    # Step 2: compute prefix sums
    # After this, counts[v] = number of elements with key ≤ v.
    # Equivalently: counts[v] - 1 is the FINAL INDEX for the LAST
    # element with key == v.
    for i in range(1, len(counts)):
        counts[i] += counts[i - 1]

    # Step 3: build the output by walking the input from RIGHT to LEFT.
    # Walking backward is what makes the sort stable: the last occurrence
    # of each key gets the highest slot (preserving original order).
    output = [None] * len(arr)
    for x in reversed(arr):
        k = key(x)
        counts[k] -= 1
        output[counts[k]] = x

    return output


# =========================================================================
# In-Place Stable Counting Sort — For Primitive Int Arrays
# =========================================================================

def stable_counting_sort_in_place(arr):
    """
    Like `stable_counting_sort`, but writes back into `arr` (mutating).
    Works for integer arrays; for records, use the non-mutating version.

    Internally still allocates an O(n) output buffer — "in place from
    the caller's perspective" only.
    """
    if not arr:
        return arr

    out = stable_counting_sort(arr)
    arr[:] = out
    return arr


# =========================================================================
# Demonstrating Stability Matters (Key-Based Sort)
# =========================================================================

def _demonstrate_stability():
    """
    Sort (first_name, age) records by AGE. A stable sort preserves the
    original name order within each age.
    """
    records = [
        ("Alice",   30),
        ("Bob",     25),
        ("Charlie", 30),
        ("Dan",     25),
        ("Eve",     30),
    ]

    sorted_records = stable_counting_sort(records, key=lambda r: r[1])

    # Expected stable output — ages ascending, names within each age in input order
    expected = [
        ("Bob",     25),
        ("Dan",     25),
        ("Alice",   30),
        ("Charlie", 30),
        ("Eve",     30),
    ]

    print("Stability demo — sort by age, names within an age must preserve input order:")
    print(f"   input:    {records}")
    print(f"   sorted:   {sorted_records}")
    assert sorted_records == expected


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    # Basic sort
    arr = [4, 2, 2, 8, 3, 3, 1]
    print(f"Input:  {arr}")
    print(f"Sorted: {stable_counting_sort(arr)}")
    print()

    # Test cases
    test_cases = [
        [4, 2, 2, 8, 3, 3, 1],
        [],
        [5],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5],
        [7] * 20,
        [0, 0, 0, 1],
    ]

    for i, data in enumerate(test_cases):
        expected = sorted(data)
        got = stable_counting_sort(data[:])
        assert got == expected, f"Test {i+1} failed on {data}"
        print(f"Test {i+1} passed: {data} -> {got}")

    # Stability demo
    print()
    _demonstrate_stability()
    print()

    # Extended stability check — sort multiple pairs
    pairs = [(1, "a"), (2, "b"), (1, "c"), (2, "d"), (1, "e")]
    sorted_pairs = stable_counting_sort(pairs, key=lambda p: p[0])
    expected_stable = [(1, "a"), (1, "c"), (1, "e"), (2, "b"), (2, "d")]
    assert sorted_pairs == expected_stable, (
        f"Stability broken: {sorted_pairs} != {expected_stable}"
    )
    print(f"Extended stability check passed: {sorted_pairs}")

    # In-place version
    arr = [4, 2, 2, 8, 3, 3, 1]
    stable_counting_sort_in_place(arr)
    assert arr == [1, 2, 2, 3, 3, 4, 8]
    print(f"In-place version passed: {arr}")

    # Stress test — verify BOTH correctness AND stability using
    # records where we track input order
    import random
    random.seed(42)

    for trial in range(200):
        n = random.randint(0, 50)
        # (key, original_position) — if stable, equal keys retain position order
        records = [(random.randint(0, 5), i) for i in range(n)]
        got = stable_counting_sort(records, key=lambda r: r[0])
        expected = sorted(records, key=lambda r: r[0])   # Python's sorted() is stable
        assert got == expected, (
            f"Stress test trial {trial} failed: "
            f"records={records}, got={got}, expected={expected}"
        )

    print(f"\nStress test: 200 random inputs — stable output verified against Python sorted()")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Three-Step Pattern (Memorize This):
    #
    #   Step 1: counts[v] = number of elements with key == v
    #   Step 2: counts[v] = number of elements with key ≤ v   (prefix sum)
    #   Step 3: walk input BACKWARD; place each element at counts[v] - 1,
    #           then decrement counts[v]
    #
    # This is the exact pattern used inside RADIX SORT for each digit.
    # Master it once; reuse it for every non-comparison sort you'll ever
    # need to write.
    # ---------------------------------------------------------------
