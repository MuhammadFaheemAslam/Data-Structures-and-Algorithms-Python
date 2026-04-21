"""
Problem: Range Sum Query — Immutable (1D and 2D)

Technique: Prefix Sum
Difficulty: Easy (LeetCode #303 and #304)

---------------------------------------------------
Problem Statement (1D):

Given an array `nums`, implement a class that supports:

    RangeSum(nums)              # constructor
    sumRange(left, right)       # sum of nums[left..right] inclusive

Many calls to sumRange may be made; `nums` never changes after
construction.

Problem Statement (2D):

Given a 2D grid `matrix`, implement a class that supports:

    RangeSum2D(matrix)
    sumRegion(r1, c1, r2, c2)   # sum of the rectangle [r1..r2, c1..c2]

Again, the matrix is immutable after construction.

---------------------------------------------------
The Prefix-Sum Lens:

Brute force is O(n) per query (or O((r2-r1+1)(c2-c1+1)) in 2D). For Q
queries on an n-element array that's O(n·Q) — quickly unusable for
large inputs.

Prefix sum pays a one-time O(n) (or O(m·n) in 2D) cost to preprocess,
then answers every query in O(1).

The 2D version uses inclusion-exclusion during both construction and
querying — see the comments in the code.

Time Complexity:
    1D:  O(n) preprocessing, O(1) per query
    2D:  O(m·n) preprocessing, O(1) per query

Space Complexity:
    1D:  O(n)
    2D:  O(m·n)

---------------------------------------------------
Example (1D):

    nums = [-2, 0, 3, -5, 2, -1]
    sumRange(0, 2) = -2 + 0 + 3   = 1
    sumRange(2, 5) = 3 + (-5) + 2 + (-1) = -1
    sumRange(0, 5) = sum(nums)    = -3

Example (2D):

    matrix = [
        [3, 0, 1, 4, 2],
        [5, 6, 3, 2, 1],
        [1, 2, 0, 1, 5],
        [4, 1, 0, 1, 7],
        [1, 0, 3, 0, 5]
    ]
    sumRegion(2, 1, 4, 3) = 8

---------------------------------------------------
"""

# -------------------------------------------------
# 1D Range Sum Query (Immutable)
# -------------------------------------------------

class NumArray:
    """
    LeetCode #303 shape.

    prefix[i] = sum(nums[0..i-1]), with prefix[0] = 0.
    sumRange(L, R) = prefix[R+1] - prefix[L].
    """

    def __init__(self, nums):
        self.prefix = [0] * (len(nums) + 1)
        for i, x in enumerate(nums):
            self.prefix[i + 1] = self.prefix[i] + x

    def sumRange(self, left, right):
        return self.prefix[right + 1] - self.prefix[left]


# -------------------------------------------------
# 2D Range Sum Query (Immutable)
# -------------------------------------------------

class NumMatrix:
    """
    LeetCode #304 shape.

    prefix[i][j] = sum of matrix[0..i-1, 0..j-1], with a row/column of
    zeros padding index 0 so indices don't underflow.

    Construction uses inclusion-exclusion:
        prefix[i][j] = matrix[i-1][j-1]
                     + prefix[i-1][j]
                     + prefix[i][j-1]
                     - prefix[i-1][j-1]

    A picture:
                                    o---------+
                      +----------+  |         |
                      |          |  |         |
                      |    A     |  |    B    |
                      |          |  |         |
                      +----------o  +---------o
                      +----------+  +---------+
                      |          |  |         |
                      |    C     |  |    X    |   <- new cell at (i-1, j-1)
                      |          |  |         |
                      +----------+  +---------+
                                     (this is what we want)

    The new prefix = A + B + C + X, where:
        prefix[i-1][j]   = A + B
        prefix[i][j-1]   = A + C
        prefix[i-1][j-1] = A       (double-counted; subtract once)
        matrix[i-1][j-1] = X
    """

    def __init__(self, matrix):
        if not matrix or not matrix[0]:
            self.prefix = [[0]]
            return

        m, n = len(matrix), len(matrix[0])
        self.prefix = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m):
            for j in range(n):
                self.prefix[i + 1][j + 1] = (
                    matrix[i][j]
                    + self.prefix[i][j + 1]
                    + self.prefix[i + 1][j]
                    - self.prefix[i][j]
                )

    def sumRegion(self, r1, c1, r2, c2):
        """
        Sum of matrix[r1..r2, c1..c2] (inclusive).

        Inclusion-exclusion on the 2D prefix:
            big rectangle            - top strip            - left strip            + double-subtracted overlap
            prefix[r2+1][c2+1]       - prefix[r1][c2+1]     - prefix[r2+1][c1]      + prefix[r1][c1]
        """
        return (
            self.prefix[r2 + 1][c2 + 1]
            - self.prefix[r1][c2 + 1]
            - self.prefix[r2 + 1][c1]
            + self.prefix[r1][c1]
        )


# -------------------------------------------------
# Brute Force for Verification
# -------------------------------------------------

class NumArrayBrute:
    def __init__(self, nums): self.nums = nums
    def sumRange(self, L, R): return sum(self.nums[L:R + 1])


class NumMatrixBrute:
    def __init__(self, matrix): self.matrix = matrix
    def sumRegion(self, r1, c1, r2, c2):
        return sum(self.matrix[r][c] for r in range(r1, r2 + 1) for c in range(c1, c2 + 1))


# -------------------------------------------------
# Test the Classes
# -------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("1D Range Sum Query")
    print("=" * 60)
    nums = [-2, 0, 3, -5, 2, -1]
    fast = NumArray(nums)
    brute = NumArrayBrute(nums)
    print(f"   nums = {nums}")
    for L, R in [(0, 2), (2, 5), (0, 5), (1, 3), (4, 4)]:
        got = fast.sumRange(L, R)
        expected = brute.sumRange(L, R)
        assert got == expected, f"sumRange({L},{R}): expected {expected}, got {got}"
        print(f"   sumRange({L}, {R}) = {got}")
    print()

    print("=" * 60)
    print("2D Range Sum Query")
    print("=" * 60)
    matrix = [
        [3, 0, 1, 4, 2],
        [5, 6, 3, 2, 1],
        [1, 2, 0, 1, 5],
        [4, 1, 0, 1, 7],
        [1, 0, 3, 0, 5],
    ]
    fast2 = NumMatrix(matrix)
    brute2 = NumMatrixBrute(matrix)
    print(f"   matrix is 5x5")
    tests2 = [(2, 1, 4, 3), (1, 1, 2, 2), (1, 2, 2, 4), (0, 0, 4, 4), (3, 3, 3, 3)]
    for r1, c1, r2, c2 in tests2:
        got = fast2.sumRegion(r1, c1, r2, c2)
        expected = brute2.sumRegion(r1, c1, r2, c2)
        assert got == expected, (
            f"sumRegion({r1},{c1},{r2},{c2}): expected {expected}, got {got}"
        )
        print(f"   sumRegion({r1},{c1},{r2},{c2}) = {got}")
    print()

    # Stress test — many random queries to confirm the classes agree
    import random
    random.seed(0)
    random_arr = [random.randint(-100, 100) for _ in range(100)]
    fast = NumArray(random_arr)
    brute = NumArrayBrute(random_arr)
    for _ in range(1000):
        L = random.randint(0, len(random_arr) - 1)
        R = random.randint(L, len(random_arr) - 1)
        assert fast.sumRange(L, R) == brute.sumRange(L, R)
    print("1D stress test: 1000 random queries matched brute force")

    random_grid = [[random.randint(-50, 50) for _ in range(20)] for _ in range(20)]
    fast2 = NumMatrix(random_grid)
    brute2 = NumMatrixBrute(random_grid)
    for _ in range(500):
        r1 = random.randint(0, 19)
        r2 = random.randint(r1, 19)
        c1 = random.randint(0, 19)
        c2 = random.randint(c1, 19)
        assert fast2.sumRegion(r1, c1, r2, c2) == brute2.sumRegion(r1, c1, r2, c2)
    print("2D stress test: 500 random queries matched brute force")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Speedup:
    #
    #   Naive:  O(n) per query on 1D, O(m·n) per query on 2D.
    #   Prefix: O(1) per query on both, after the preprocess.
    #
    #   For 10_000 queries on a 1_000-element array:
    #       naive:  10_000_000 operations
    #       prefix: ~1_000 for setup + 10_000 for queries = 11_000 ops
    #
    #   That's a ~1000× speedup — the kind of difference that moves an
    #   algorithm from "times out" to "instant".
    # ---------------------------------------------------------------
