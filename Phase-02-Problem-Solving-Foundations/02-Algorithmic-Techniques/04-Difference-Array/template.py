"""
template.py – Difference Array Reference Template

This file shows the pattern three ways:

    1. 1D Difference Array     — the core trick
    2. 2D Difference Array     — four-corner rectangle updates
    3. Interval-Overlap Counts — a common domain-specific variant

All three share the same shape: record updates cheaply, reconstruct at
the end.

Run this file to see each template's output.
"""

# =========================================================================
# Template 1: 1D Difference Array
# =========================================================================

class DifferenceArray1D:
    """
    Supports O(1) range-add updates and a final O(n) materialization.

    Typical pattern:
        da = DifferenceArray1D(n)
        for (L, R, x) in updates:
            da.update(L, R, x)
        arr = da.build()              # final array, one O(n) pass
    """

    def __init__(self, n):
        # Allocate n+1 slots so update(L, R, x) can safely write diff[R+1]
        # even when R == n-1. The extra slot is discarded during build().
        self.n = n
        self.diff = [0] * (n + 1)

    def update(self, left, right, x):
        """
        Add `x` to every element in arr[left..right] (INCLUSIVE on both ends).
        Cost: O(1).
        """
        self.diff[left] += x
        self.diff[right + 1] -= x

    def build(self):
        """
        Materialize the final array via a running prefix sum over diff.

        Cost: O(n).
        """
        arr = [0] * self.n
        running = 0
        for i in range(self.n):
            running += self.diff[i]
            arr[i] = running
        return arr


# =========================================================================
# Template 2: 2D Difference Array (Rectangle Updates)
# =========================================================================

class DifferenceArray2D:
    """
    Supports O(1) rectangle-add updates on a grid and a final O(m * n)
    materialization.

    To add `x` to every cell in the rectangle (r1, c1) .. (r2, c2)
    inclusive, four corner writes suffice:

        diff[r1  ][c1  ] += x
        diff[r1  ][c2+1] -= x
        diff[r2+1][c1  ] -= x
        diff[r2+1][c2+1] += x

    This is the inclusion-exclusion trick from 2D prefix sum run in
    reverse: the +x starts a contribution extending down and right
    from (r1, c1); the -x corners cancel the contribution outside the
    target rectangle.
    """

    def __init__(self, m, n):
        self.m, self.n = m, n
        # Extra row/column for boundary writes
        self.diff = [[0] * (n + 1) for _ in range(m + 1)]

    def update(self, r1, c1, r2, c2, x):
        """
        Add `x` to every cell in grid[r1..r2, c1..c2] (inclusive).
        Cost: O(1) per update.
        """
        self.diff[r1][c1] += x
        self.diff[r1][c2 + 1] -= x
        self.diff[r2 + 1][c1] -= x
        self.diff[r2 + 1][c2 + 1] += x

    def build(self):
        """
        Materialize the final grid via 2D prefix sum.

        Cost: O(m * n).
        """
        grid = [[0] * self.n for _ in range(self.m)]
        for i in range(self.m):
            for j in range(self.n):
                # cumulative contribution from diff along top + left prefix
                val = self.diff[i][j]
                if i > 0: val += grid[i - 1][j]
                if j > 0: val += grid[i][j - 1]
                if i > 0 and j > 0: val -= grid[i - 1][j - 1]
                grid[i][j] = val
        return grid


# =========================================================================
# Template 3: Count Overlaps at Every Point (Interval-Overlap Profile)
# =========================================================================

def overlap_profile(intervals, size):
    """
    Given a list of intervals [(start, end), ...] (inclusive on both ends),
    return an array `overlap[i]` = how many intervals cover point `i`.

    Classic timeline / scheduling / traffic-count problem.

    Cost:  O(len(intervals) + size)
    Space: O(size)
    """
    diff = [0] * (size + 1)

    for start, end in intervals:
        diff[start] += 1
        diff[end + 1] -= 1

    overlap = [0] * size
    running = 0
    for i in range(size):
        running += diff[i]
        overlap[i] = running

    return overlap


# =========================================================================
# Demonstration
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Template 1 — 1D Difference Array")
    print("=" * 60)
    da = DifferenceArray1D(6)
    print(f"   initial:  {[0] * 6}")

    da.update(1, 3, 3)                       # add 3 to arr[1..3]
    da.update(2, 4, 5)                       # add 5 to arr[2..4]
    print(f"   after two updates:")
    print(f"     update(1, 3, +3)")
    print(f"     update(2, 4, +5)")
    print(f"   result:  {da.build()}")
    print(f"   expected [0, 3, 8, 8, 5, 0]")
    assert da.build() == [0, 3, 8, 8, 5, 0]
    print()

    print("=" * 60)
    print("Template 2 — 2D Difference Array")
    print("=" * 60)
    da2 = DifferenceArray2D(4, 4)
    da2.update(0, 0, 1, 1, 1)                # add 1 to top-left 2x2
    da2.update(1, 1, 3, 3, 2)                # add 2 to bottom-right 3x3
    grid = da2.build()
    print(f"   result grid:")
    for row in grid:
        print(f"     {row}")
    expected_grid = [
        [1, 1, 0, 0],
        [1, 3, 2, 2],
        [0, 2, 2, 2],
        [0, 2, 2, 2],
    ]
    assert grid == expected_grid
    print()

    print("=" * 60)
    print("Template 3 — Interval-Overlap Profile")
    print("=" * 60)
    intervals = [(1, 3), (2, 5), (4, 6), (0, 2)]
    size = 8
    profile = overlap_profile(intervals, size)
    print(f"   intervals: {intervals}")
    print(f"   overlap:   {profile}")
    # brute-force check
    expected = [sum(1 for (s, e) in intervals if s <= i <= e) for i in range(size)]
    assert profile == expected
    print(f"   brute:     {expected}   ✓")

    print("\nAll tests passed!")
