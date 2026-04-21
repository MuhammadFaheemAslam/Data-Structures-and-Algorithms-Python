"""
Problem: Insert Interval

Technique: Merge Intervals — single-pass variant for pre-sorted input
Difficulty: Medium (LeetCode #57)

---------------------------------------------------
Problem Statement:

You are given a list of NON-OVERLAPPING intervals `intervals` sorted
by start time, and a new interval `new_interval`.

Insert `new_interval` into `intervals` (still sorted by start time)
and merge any overlapping intervals that result. Return the updated
list.

---------------------------------------------------
Why This Is Harder Than Merge Intervals (LC #56):

The input is ALREADY SORTED and non-overlapping — so we don't need
a full sort. But we need to splice in the new interval correctly, and
the merging only happens around the insertion point.

A lazy approach: "append the new interval and re-merge." That works
and is O(n log n) — fine, but wasteful. The optimal approach is O(n):

    1. Walk the list once. Output every interval that ENDS BEFORE the
       new interval starts — they're entirely to the left of the new
       one and don't overlap.
    2. Merge any interval that overlaps with the new one by extending
       the new interval's bounds.
    3. Output the (possibly-extended) new interval.
    4. Output every interval that STARTS AFTER the new interval ends
       — they're entirely to the right.

Three disjoint phases, each a single forward walk. Total: O(n).

---------------------------------------------------
Example:

    intervals    = [[1, 3], [6, 9]]
    new_interval = [2, 5]
    -> [[1, 5], [6, 9]]
    (Merges [1,3] + [2,5] into [1,5]; [6,9] stays.)

    intervals    = [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]]
    new_interval = [4, 8]
    -> [[1, 2], [3, 10], [12, 16]]
    ([4,8] swallows [3,5], [6,7], [8,10] → [3,10].)

---------------------------------------------------
"""

# -------------------------------------------------
# The Three-Phase Solution — O(n)
# -------------------------------------------------

def insert(intervals, new_interval):
    """
    Insert `new_interval` into a sorted list of non-overlapping
    intervals, merging as needed.

    Time Complexity:  O(n)
    Space Complexity: O(n) for the output
    """
    result = []
    i = 0
    n = len(intervals)
    new_start, new_end = new_interval

    # Phase 1: intervals entirely BEFORE the new one
    while i < n and intervals[i][1] < new_start:
        result.append(intervals[i])
        i += 1

    # Phase 2: intervals that OVERLAP the new one; expand the new bounds
    while i < n and intervals[i][0] <= new_end:
        new_start = min(new_start, intervals[i][0])
        new_end = max(new_end, intervals[i][1])
        i += 1
    result.append([new_start, new_end])

    # Phase 3: intervals entirely AFTER the new one
    while i < n:
        result.append(intervals[i])
        i += 1

    return result


# -------------------------------------------------
# Lazy Alternative: Append and Re-Merge — O(n log n)
# -------------------------------------------------

def insert_by_merging(intervals, new_interval):
    """
    Dumber approach: append + run the full Merge Intervals algorithm.

    Time Complexity:  O(n log n) — because of the sort
    Space Complexity: O(n)

    Correct but wasteful. Included to show both paths.
    """
    combined = intervals + [new_interval]
    combined.sort(key=lambda iv: iv[0])

    merged = [list(combined[0])]
    for start, end in combined[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    return merged


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    print("Example 1:")
    intervals = [[1, 3], [6, 9]]
    new_interval = [2, 5]
    print(f"   intervals    = {intervals}")
    print(f"   new_interval = {new_interval}")
    print(f"   insert:             {insert(intervals, new_interval)}")
    print(f"   insert_by_merging:  {insert_by_merging(intervals, new_interval)}")
    print()

    # Test cases — (intervals, new_interval, expected)
    test_cases = [
        ([[1, 3], [6, 9]],                              [2, 5],    [[1, 5], [6, 9]]),
        ([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]],   [4, 8],    [[1, 2], [3, 10], [12, 16]]),
        ([],                                            [5, 7],    [[5, 7]]),                     # empty existing
        ([[1, 5]],                                      [2, 3],    [[1, 5]]),                     # new is contained
        ([[1, 5]],                                      [6, 8],    [[1, 5], [6, 8]]),              # new is after
        ([[1, 5]],                                      [0, 0],    [[0, 0], [1, 5]]),              # new is before
        ([[1, 5]],                                      [-1, 10],  [[-1, 10]]),                    # new swallows
        ([[1, 5], [10, 15]],                            [5, 10],   [[1, 15]]),                    # new bridges gap (touching)
        ([[3, 5], [12, 15]],                            [6, 6],    [[3, 5], [6, 6], [12, 15]]),   # single-point fit in gap
    ]

    for i, (ivs, ni, expected) in enumerate(test_cases):
        got = insert(ivs, ni)
        got2 = insert_by_merging(ivs, ni)
        assert got == expected, (
            f"Test {i+1} (insert): expected {expected}, got {got}"
        )
        assert got2 == expected, (
            f"Test {i+1} (merge): expected {expected}, got {got2}"
        )
        print(f"Test {i+1} passed: intervals={ivs}, new={ni} -> {expected}")

    # Stress test
    import random
    random.seed(77)
    for _ in range(100):
        n = random.randint(0, 20)
        # build a sorted, non-overlapping interval list
        cursor = 0
        intervals = []
        for _ in range(n):
            gap = random.randint(0, 5)
            length = random.randint(0, 5)
            start = cursor + gap
            end = start + length
            intervals.append([start, end])
            cursor = end + 1

        # pick a new interval with random position/size
        new = [random.randint(-5, 30), 0]
        new[1] = new[0] + random.randint(0, 10)

        a = insert(intervals, new)
        b = insert_by_merging(intervals, new)
        assert a == b, f"stress: intervals={intervals}, new={new}: fast={a}, slow={b}"
    print("\nStress test: 100 random inputs — fast O(n) matches O(n log n)")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Speedup:
    #
    #   Insert + re-sort approach:   O(n log n)
    #   Three-phase walk:            O(n)
    #
    #   For large n (say 10^5 insertions in a loop), this is the
    #   difference between O(n^2 log n) and O(n^2) overall work.
    #
    # The three-phase pattern generalizes to any "splice in a new
    # element and merge with the surrounding block" problem:
    #
    #     - Copy everything fully to the left.
    #     - Merge with everything that overlaps.
    #     - Copy everything fully to the right.
    #
    # Once you see it, you see it everywhere.
    # ---------------------------------------------------------------
