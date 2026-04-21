"""
template.py – Prefix Sum Reference Template

This file shows the prefix sum pattern four ways:

    1. 1D prefix sum       — the basic trick
    2. 2D prefix sum       — inclusion-exclusion on a grid
    3. Prefix XOR          — the same pattern, different associative op
    4. Running prefix       — streaming version used for subarray-sum-K

All use the same off-by-one convention: `prefix[0] = 0; prefix[i] =
sum of arr[0..i-1]`. With this convention, `range_sum(L, R)` is always
`prefix[R+1] - prefix[L]` for any inclusive range [L, R].

Run this file to see each template's output.
"""

# =========================================================================
# Template 1: 1D Prefix Sum
# =========================================================================

class RangeSum:
    """
    Precompute once; answer any sumRange(L, R) in O(1).

    Time:  O(n) preprocessing, O(1) per query.
    Space: O(n) prefix array.
    """

    def __init__(self, arr):
        # prefix[i] = sum of arr[0..i-1], so prefix[0] = 0 and prefix[n] = total
        self.prefix = [0] * (len(arr) + 1)
        for i, x in enumerate(arr):
            self.prefix[i + 1] = self.prefix[i] + x

    def range_sum(self, left, right):
        """Sum of arr[left..right] (INCLUSIVE on both ends)."""
        return self.prefix[right + 1] - self.prefix[left]


# =========================================================================
# Template 2: 2D Prefix Sum
# =========================================================================

class RangeSum2D:
    """
    Precompute a 2D prefix on a grid; answer any rectangle sum in O(1).

    Time:  O(m * n) preprocessing, O(1) per query.
    Space: O(m * n) prefix grid.

    Construction uses inclusion-exclusion:
        prefix[i][j] = A[i-1][j-1] + prefix[i-1][j] + prefix[i][j-1]
                       - prefix[i-1][j-1]

    Query (sub-rectangle rows r1..r2, cols c1..c2):
        sum = prefix[r2+1][c2+1]
            - prefix[r1][c2+1]
            - prefix[r2+1][c1]
            + prefix[r1][c1]
    """

    def __init__(self, grid):
        if not grid or not grid[0]:
            self.prefix = [[0]]
            return

        m, n = len(grid), len(grid[0])
        self.prefix = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m):
            for j in range(n):
                self.prefix[i + 1][j + 1] = (
                    grid[i][j]
                    + self.prefix[i][j + 1]
                    + self.prefix[i + 1][j]
                    - self.prefix[i][j]
                )

    def rect_sum(self, r1, c1, r2, c2):
        """Sum of grid[r1..r2, c1..c2] (INCLUSIVE on all sides)."""
        return (
            self.prefix[r2 + 1][c2 + 1]
            - self.prefix[r1][c2 + 1]
            - self.prefix[r2 + 1][c1]
            + self.prefix[r1][c1]
        )


# =========================================================================
# Template 3: Prefix XOR
# =========================================================================

def build_prefix_xor(arr):
    """
    Same pattern as prefix sum, but with XOR instead of addition.

    Works because XOR is associative and self-inverse (a ^ a = 0), so
    `range_xor(L, R) = prefix[R+1] ^ prefix[L]`.

    Time:  O(n)
    Space: O(n)
    """
    prefix = [0] * (len(arr) + 1)
    for i, x in enumerate(arr):
        prefix[i + 1] = prefix[i] ^ x
    return prefix


def range_xor(prefix, left, right):
    """XOR of arr[left..right] (INCLUSIVE)."""
    return prefix[right + 1] ^ prefix[left]


# =========================================================================
# Template 4: Streaming Prefix Sum (for Subarray-Sum-K Type Problems)
# =========================================================================

def count_subarrays_with_sum_k(arr, k):
    """
    Count the number of contiguous subarrays whose sum equals k.

    Uses a STREAMING prefix sum — we don't need the full prefix array,
    just the running total. Combined with a dict counting how many
    times each prefix sum has appeared, this gives O(n).

    Key identity:
        #subarrays ending at i with sum k
          = #prior positions j where prefix[j] == prefix[i+1] - k

    Critical: start with `seen[0] = 1` so subarrays STARTING from index 0
    are counted (empty prefix has value 0, occurring once).

    Time:  O(n)
    Space: O(n)
    """
    seen = {0: 1}                                 # prefix-sum value → count
    running = 0
    count = 0

    for x in arr:
        running += x
        needed = running - k
        if needed in seen:
            count += seen[needed]
        seen[running] = seen.get(running, 0) + 1

    return count


# =========================================================================
# Demonstration
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Template 1 — 1D Prefix Sum")
    print("=" * 60)
    arr = [3, 1, 4, 1, 5, 9, 2, 6]
    rs = RangeSum(arr)
    print(f"   arr = {arr}")
    print(f"   prefix = {rs.prefix}")
    for L, R in [(0, 0), (0, 7), (2, 5), (4, 4)]:
        assert rs.range_sum(L, R) == sum(arr[L:R + 1])
        print(f"   range_sum({L}, {R}) = {rs.range_sum(L, R)}")
    print()

    print("=" * 60)
    print("Template 2 — 2D Prefix Sum")
    print("=" * 60)
    grid = [
        [3, 0, 1, 4, 2],
        [5, 6, 3, 2, 1],
        [1, 2, 0, 1, 5],
        [4, 1, 0, 1, 7],
        [1, 0, 3, 0, 5],
    ]
    rs2 = RangeSum2D(grid)
    test_rects = [(2, 1, 4, 3), (1, 1, 2, 2), (1, 2, 2, 4)]
    for (r1, c1, r2, c2) in test_rects:
        got = rs2.rect_sum(r1, c1, r2, c2)
        expected = sum(grid[r][c] for r in range(r1, r2 + 1) for c in range(c1, c2 + 1))
        assert got == expected
        print(f"   rect_sum({r1},{c1},{r2},{c2}) = {got}  (brute force = {expected})")
    print()

    print("=" * 60)
    print("Template 3 — Prefix XOR")
    print("=" * 60)
    arr = [3, 10, 7, 2, 5, 12]
    pxor = build_prefix_xor(arr)
    for L, R in [(0, 5), (2, 4), (1, 3), (3, 3)]:
        got = range_xor(pxor, L, R)
        expected = 0
        for x in arr[L:R + 1]:
            expected ^= x
        assert got == expected
        print(f"   range_xor({L}, {R}) = {got}")
    print()

    print("=" * 60)
    print("Template 4 — Subarray-Sum-K (Streaming Prefix)")
    print("=" * 60)
    cases = [
        ([1, 1, 1], 2, 2),
        ([1, 2, 3], 3, 2),
        ([1, -1, 1, -1], 0, 4),                # multiple zero-sum subarrays
        ([3, 4, 7, 2, -3, 1, 4, 2], 7, 4),
        ([1], 0, 0),
    ]
    for arr, k, expected in cases:
        got = count_subarrays_with_sum_k(arr, k)
        assert got == expected
        print(f"   count_subarrays_with_sum_k({arr}, {k}) = {got}")

    print("\nAll tests passed!")
