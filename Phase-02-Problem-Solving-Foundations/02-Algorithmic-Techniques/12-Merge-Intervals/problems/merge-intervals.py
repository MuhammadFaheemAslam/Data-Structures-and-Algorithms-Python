"""
Problem: Merge Intervals

Technique: Merge Intervals (sort + sweep)
Difficulty: Medium (LeetCode #56)

---------------------------------------------------
Problem Statement:

Given a list of intervals, where each interval is `[start, end]`,
merge all OVERLAPPING intervals and return the list of non-overlapping
intervals that cover the same union.

Two intervals overlap if they share at least one point — i.e.,
`[1, 4]` and `[4, 6]` count as overlapping (touching at 4).

---------------------------------------------------
The Merge-Intervals Lens:

Brute force: for each pair of intervals, check if they overlap; merge
if so; repeat until stable. That's O(n²) or worse — the "mark as
merged and rescan" structure rarely terminates cleanly.

Sort + sweep insight:

    1. Sort intervals by START time.
    2. Walk through them in order. Keep a single "running merged"
       interval that represents everything merged so far.
    3. For each new interval:
         - If it overlaps with the running merged interval (its start
           ≤ the merged end), EXTEND the merged end.
         - Otherwise, EMIT the running merged interval and start a
           new one with this interval.

Why this works: after sorting by start, all intervals "after" the
running merged interval have start ≥ its start. The ONLY thing that
can still overlap is an interval whose start ≤ the running end.
If its start > running end, it's completely disjoint — nothing earlier
could overlap with it anymore (they all ended before it started).

Time Complexity:  O(n log n)    — dominated by the sort
Space Complexity: O(n)          — the output list

---------------------------------------------------
Example:

    Input:  [[1,3], [2,6], [8,10], [15,18]]
    Output: [[1,6], [8,10], [15,18]]

    [1,3] and [2,6] overlap → merge to [1,6]
    [1,6] and [8,10] disjoint → emit [1,6], keep [8,10]
    [8,10] and [15,18] disjoint → emit [8,10], keep [15,18]
    End → emit [15,18].

---------------------------------------------------
"""

# -------------------------------------------------
# The Sort + Sweep Solution
# -------------------------------------------------

def merge(intervals):
    """
    Return the merged list of non-overlapping intervals covering the
    same union as the input.

    Time Complexity:  O(n log n)
    Space Complexity: O(n)
    """
    if not intervals:
        return []

    ordered = sorted(intervals, key=lambda iv: iv[0])
    merged = [list(ordered[0])]                   # list, not tuple — we'll mutate

    for start, end in ordered[1:]:
        if start <= merged[-1][1]:                # overlap (touching counts)
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    return merged


# -------------------------------------------------
# Brute Force for Verification — Union-Find / Repeat Until Stable
# -------------------------------------------------

def merge_brute_force(intervals):
    """
    Repeatedly scan for any overlapping pair and merge them. Stop when
    no pair overlaps.

    Time Complexity:  O(n^3) worst case
    Space Complexity: O(n)

    Used for cross-validation on small inputs.
    """
    result = [list(iv) for iv in intervals]
    changed = True
    while changed:
        changed = False
        for i in range(len(result)):
            for j in range(i + 1, len(result)):
                a, b = result[i], result[j]
                # overlap test
                if a[0] <= b[1] and b[0] <= a[1]:
                    a[0] = min(a[0], b[0])
                    a[1] = max(a[1], b[1])
                    result.pop(j)
                    changed = True
                    break
            if changed:
                break
    return sorted(result, key=lambda iv: iv[0])


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
    print(f"Input:  {intervals}")
    print(f"merge:              {merge(intervals)}")
    print(f"merge_brute_force:  {merge_brute_force(intervals)}")
    print()

    # Test cases — (intervals, expected)
    test_cases = [
        ([[1, 3], [2, 6], [8, 10], [15, 18]],     [[1, 6], [8, 10], [15, 18]]),
        ([[1, 4], [4, 5]],                        [[1, 5]]),                     # touching = merged
        ([[1, 4], [5, 6]],                        [[1, 4], [5, 6]]),              # not touching
        ([[1, 4], [0, 4]],                        [[0, 4]]),                      # equal after merge
        ([[1, 4], [2, 3]],                        [[1, 4]]),                      # contained
        ([[1, 10], [2, 3], [4, 5], [6, 7]],       [[1, 10]]),                     # all contained
        ([],                                      []),
        ([[5, 5]],                                [[5, 5]]),                      # zero-length interval
        ([[1, 2], [3, 4], [5, 6]],                [[1, 2], [3, 4], [5, 6]]),      # all disjoint
        ([[1, 4], [2, 5], [7, 9], [3, 6]],        [[1, 6], [7, 9]]),              # unsorted input
    ]

    for i, (data, expected) in enumerate(test_cases):
        got = merge(data)
        assert got == expected, (
            f"Test {i+1} failed on {data}: expected {expected}, got {got}"
        )
        # cross-check with brute force on small inputs
        if len(data) <= 10:
            bf = merge_brute_force(data)
            assert got == bf, (
                f"Test {i+1}: sort-sweep ({got}) disagrees with brute force ({bf})"
            )
        print(f"Test {i+1} passed: {data} -> {got}")

    # Stress test
    import random
    random.seed(12)
    for _ in range(100):
        n = random.randint(0, 15)
        data = []
        for _ in range(n):
            s = random.randint(0, 20)
            e = random.randint(s, s + 10)
            data.append([s, e])

        got = merge(data)
        bf = merge_brute_force(data)
        assert got == bf, f"stress: {data}: sort={got}, brute={bf}"
    print("\nStress test: 100 random inputs matched brute force")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Three-Line Insight:
    #
    #   After sorting by start, the only possible overlap is between
    #   an interval and the RUNNING MERGED interval. That's because:
    #
    #     - Earlier intervals have start ≤ the running one, and they've
    #       all been absorbed already.
    #     - Future intervals have start ≥ the running one.
    #     - If start > running_end, it's disjoint with EVERYTHING so far.
    #
    #   So "does it overlap with the tail?" is the only question you
    #   ever need to ask. Three lines of logic, O(n log n) total.
    # ---------------------------------------------------------------
