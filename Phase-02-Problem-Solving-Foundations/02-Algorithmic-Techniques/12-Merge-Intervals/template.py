"""
template.py – Merge Intervals Reference Template

This file demonstrates the interval technique five ways:

    1. merge_intervals       — the canonical "sort + sweep" merge
    2. intervals_overlap     — overlap detection and intersection
    3. meeting_rooms_i       — can a single person attend them all?
    4. meeting_rooms_ii      — min rooms needed (heap-based sweep)
    5. interval_intersections — two-pointer walk over two sorted lists

Together these cover the canonical interval-technique skeletons.

Run this file to see each template's output.
"""

import heapq


# =========================================================================
# Template 1: Merge Intervals (LC #56) — The Canonical Sort + Sweep
# =========================================================================

def merge_intervals(intervals):
    """
    Given overlapping intervals, return the list of merged
    non-overlapping intervals (maximal).

    Time Complexity:  O(n log n) — dominated by the sort
    Space Complexity: O(n)
    """
    if not intervals:
        return []

    ordered = sorted(intervals, key=lambda iv: iv[0])
    merged = [list(ordered[0])]

    for start, end in ordered[1:]:
        if start <= merged[-1][1]:                # overlap (touching = overlap)
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    return merged


# =========================================================================
# Template 2: Overlap Detection and Intersection
# =========================================================================

def intervals_overlap(a, b):
    """
    Return True iff the two intervals overlap (including touching at an endpoint).

    Overlap iff: neither ends strictly before the other starts.
        not (a.end < b.start)    AND    not (b.end < a.start)
    <=> a.start <= b.end         AND    b.start <= a.end
    """
    return a[0] <= b[1] and b[0] <= a[1]


def intervals_intersection(a, b):
    """
    Return the intersection of two intervals, or None if they don't overlap.

    intersection = [max(starts), min(ends)]
    """
    lo = max(a[0], b[0])
    hi = min(a[1], b[1])
    return [lo, hi] if lo <= hi else None


# =========================================================================
# Template 3: Meeting Rooms I (LC #252) — Can One Person Attend All?
# =========================================================================

def can_attend_all(meetings):
    """
    Return True iff a single person can attend every meeting —
    i.e., no two meetings overlap.

    Sort by start, then check each consecutive pair.

    Time Complexity:  O(n log n)
    Space Complexity: O(1) additional beyond the sort
    """
    if not meetings:
        return True

    ordered = sorted(meetings, key=lambda m: m[0])
    for i in range(1, len(ordered)):
        if ordered[i][0] < ordered[i - 1][1]:     # strict overlap (end == start OK)
            return False

    return True


# =========================================================================
# Template 4: Meeting Rooms II (LC #253) — Minimum Rooms Needed
# =========================================================================

def min_meeting_rooms(meetings):
    """
    Return the minimum number of rooms needed so that every meeting
    happens at its scheduled time.

    Approach: sort by start; maintain a min-heap of currently-occupied
    rooms' END times. For each new meeting:
        - If the earliest-ending active room is already free (its end
          ≤ this meeting's start), reuse it (pop it off the heap).
        - Push this meeting's end time (new or reused room).

    The heap's size at any moment is the number of CONCURRENTLY busy
    rooms. The maximum over the scan is the answer — and conveniently,
    it's simply the heap's final size.

    Time Complexity:  O(n log n)
    Space Complexity: O(n)
    """
    if not meetings:
        return 0

    ordered = sorted(meetings, key=lambda m: m[0])
    active = []                                   # min-heap of end times

    for start, end in ordered:
        if active and active[0] <= start:
            heapq.heappop(active)                 # reuse a freed room
        heapq.heappush(active, end)

    return len(active)


# =========================================================================
# Template 5: Interval List Intersections (LC #986) — Two-Pointer Walk
# =========================================================================

def intersect_interval_lists(a, b):
    """
    Given two lists of non-overlapping intervals, each sorted by start,
    return the list of intersection intervals.

    Time Complexity:  O(n + m)
    Space Complexity: O(n + m) for the output

    Two-pointer trick: whichever interval ends first gets advanced.
    That's because intervals in each list don't overlap with each
    other, so the lower endpoint can't contribute again.
    """
    i = j = 0
    result = []

    while i < len(a) and j < len(b):
        lo = max(a[i][0], b[j][0])
        hi = min(a[i][1], b[j][1])
        if lo <= hi:
            result.append([lo, hi])
        # advance the interval with the smaller end
        if a[i][1] < b[j][1]:
            i += 1
        else:
            j += 1

    return result


# =========================================================================
# Demonstration
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Template 1 — Merge Intervals (LC #56)")
    print("=" * 60)
    tests = [
        ([[1, 3], [2, 6], [8, 10], [15, 18]],  [[1, 6], [8, 10], [15, 18]]),
        ([[1, 4], [4, 5]],                     [[1, 5]]),         # touching = merged
        ([[1, 4], [5, 6]],                     [[1, 4], [5, 6]]),  # not touching
        ([],                                   []),
        ([[1, 5]],                             [[1, 5]]),
        ([[1, 4], [2, 3]],                     [[1, 4]]),          # fully contained
    ]
    for intervals, expected in tests:
        got = merge_intervals(intervals)
        assert got == expected, f"{intervals}: expected {expected}, got {got}"
        print(f"   merge_intervals({intervals}) = {got}")
    print()

    print("=" * 60)
    print("Template 2 — Overlap / Intersection")
    print("=" * 60)
    for a, b in [([1, 5], [3, 7]), ([1, 3], [5, 9]), ([1, 5], [5, 8]), ([0, 10], [3, 7])]:
        ov = intervals_overlap(a, b)
        inter = intervals_intersection(a, b)
        print(f"   overlap({a}, {b}) = {ov},  intersection = {inter}")
    print()

    print("=" * 60)
    print("Template 3 — Meeting Rooms I")
    print("=" * 60)
    tests = [
        ([[0, 30], [5, 10], [15, 20]],         False),            # overlapping
        ([[7, 10], [2, 4]],                    True),
        ([],                                   True),
        ([[1, 5], [5, 10]],                    True),              # touching OK
    ]
    for meetings, expected in tests:
        got = can_attend_all(meetings)
        assert got == expected
        print(f"   can_attend_all({meetings}) = {got}")
    print()

    print("=" * 60)
    print("Template 4 — Meeting Rooms II (Minimum Rooms)")
    print("=" * 60)
    tests = [
        ([[0, 30], [5, 10], [15, 20]],         2),
        ([[7, 10], [2, 4]],                    1),
        ([[1, 5], [1, 5], [1, 5]],             3),
        ([],                                   0),
        ([[0, 1], [1, 2], [2, 3]],             1),                # sequential
    ]
    for meetings, expected in tests:
        got = min_meeting_rooms(meetings)
        assert got == expected
        print(f"   min_meeting_rooms({meetings}) = {got}")
    print()

    print("=" * 60)
    print("Template 5 — Interval List Intersections")
    print("=" * 60)
    a = [[0, 2], [5, 10], [13, 23], [24, 25]]
    b = [[1, 5], [8, 12], [15, 24], [25, 26]]
    expected = [[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]]
    got = intersect_interval_lists(a, b)
    print(f"   intersect_interval_lists(A, B) = {got}")
    assert got == expected
    print()

    print("All tests passed!")
