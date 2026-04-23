"""
Problem 01: Find Maximum and Minimum

Difficulty: Easy

---------------------------------------------------
Problem Statement:

Given an array of numbers, find:
    1. The maximum value
    2. The minimum value
    3. Their indices (positions)

Return all four pieces of information.

---------------------------------------------------
Why This Belongs in the Array Module (Not Just "Linear Search"):

Max/min is the canonical "single-pass state-tracking" problem.
Every streaming-array algorithm in your future — Kadane's maximum
subarray, Boyer-Moore voting, sliding-window maximum — is some
variant of "scan once, keep a running state, update at each step".

Master the shape once here; recognize it forever.

---------------------------------------------------
"""

# =========================================================================
# Approach 1: Built-ins
# =========================================================================

def find_max_min_builtin(arr):
    """
    Uses Python's built-in `max` and `min` with `key` to get indices.

    Time:  O(n)  — max and min each scan the array once
    Space: O(1)
    """
    if not arr:
        return None

    n = len(arr)
    max_idx = max(range(n), key=lambda i: arr[i])
    min_idx = min(range(n), key=lambda i: arr[i])
    return {
        "max": arr[max_idx],
        "min": arr[min_idx],
        "max_index": max_idx,
        "min_index": min_idx,
    }


# =========================================================================
# Approach 2: Single-Pass Manual Traversal (Interview-Friendly)
# =========================================================================

def find_max_min_single_pass(arr):
    """
    Walk the array once, tracking max and min simultaneously.

    Time:  O(n)  — one pass instead of two
    Space: O(1)

    One pass is strictly better than two when the array is large or
    living on slow storage. This is the version to write in an interview.
    """
    if not arr:
        return None

    max_val = min_val = arr[0]
    max_idx = min_idx = 0

    for i in range(1, len(arr)):
        if arr[i] > max_val:
            max_val = arr[i]
            max_idx = i
        elif arr[i] < min_val:
            min_val = arr[i]
            min_idx = i

    return {"max": max_val, "min": min_val, "max_index": max_idx, "min_index": min_idx}


# =========================================================================
# Approach 3: Tournament (Fewer Comparisons, Pairwise)
# =========================================================================

def find_max_min_pairs(arr):
    """
    Process elements in PAIRS. Compare the two in the pair first,
    then compare the larger to running max and the smaller to running min.

    Time:  O(n)  — still linear
    Space: O(1)

    Advantage: ~1.5n comparisons instead of 2n — a ~25% reduction.
    Rarely matters in practice, but elegant and useful when comparisons
    are expensive (e.g., long-string comparisons).
    """
    n = len(arr)
    if n == 0:
        return None
    if n == 1:
        return {"max": arr[0], "min": arr[0], "max_index": 0, "min_index": 0}

    # Seed with the first pair
    if arr[0] > arr[1]:
        max_val, max_idx, min_val, min_idx = arr[0], 0, arr[1], 1
    else:
        max_val, max_idx, min_val, min_idx = arr[1], 1, arr[0], 0

    # Process the rest in pairs
    i = 2
    while i + 1 < n:
        # Compare the pair first (1 comparison)
        if arr[i] > arr[i + 1]:
            local_max, local_max_idx = arr[i], i
            local_min, local_min_idx = arr[i + 1], i + 1
        else:
            local_max, local_max_idx = arr[i + 1], i + 1
            local_min, local_min_idx = arr[i], i

        # Compare only the larger to running max (1 comparison)
        if local_max > max_val:
            max_val, max_idx = local_max, local_max_idx

        # Compare only the smaller to running min (1 comparison)
        if local_min < min_val:
            min_val, min_idx = local_min, local_min_idx

        i += 2

    # Handle a leftover odd element
    if i < n:
        if arr[i] > max_val:
            max_val, max_idx = arr[i], i
        if arr[i] < min_val:
            min_val, min_idx = arr[i], i

    return {"max": max_val, "min": min_val, "max_index": max_idx, "min_index": min_idx}


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    arr = [3, 5, 1, 9, 2, 7, 4]
    for fn in (find_max_min_builtin, find_max_min_single_pass, find_max_min_pairs):
        print(f"   {fn.__name__}({arr}) = {fn(arr)}")

    # Test cases
    test_cases = [
        [3, 5, 1, 9, 2, 7, 4],
        [1, 2, 3, 4, 5],                           # sorted — max at end, min at start
        [5, 4, 3, 2, 1],                           # reverse — max at start, min at end
        [42],                                      # single element
        [-1, -5, -3, -8, -2],                      # all negatives
        [7, 7, 7, 7],                              # all equal
        [0, -1, 2, -3, 4, -5],                     # mixed signs
        list(range(100)),                          # longer array
    ]

    for i, data in enumerate(test_cases):
        for fn in (find_max_min_builtin, find_max_min_single_pass, find_max_min_pairs):
            got = fn(data)
            if data:
                assert got["max"] == max(data)
                assert got["min"] == min(data)
                assert data[got["max_index"]] == got["max"]
                assert data[got["min_index"]] == got["min"]
        print(f"Test {i+1} passed: len={len(data)}")

    # Empty input
    for fn in (find_max_min_builtin, find_max_min_single_pass, find_max_min_pairs):
        assert fn([]) is None
    print("\nEmpty input: all three return None")

    # Stress test
    import random
    random.seed(42)
    for _ in range(200):
        n = random.randint(0, 100)
        data = [random.randint(-100, 100) for _ in range(n)]
        results = [fn(data) for fn in (find_max_min_builtin, find_max_min_single_pass, find_max_min_pairs)]
        for r in results[1:]:
            assert r["max"] == results[0]["max"]
            assert r["min"] == results[0]["min"]
    print("\nStress test: 200 random arrays — all three approaches agree")

    print("\nAll tests passed!")
