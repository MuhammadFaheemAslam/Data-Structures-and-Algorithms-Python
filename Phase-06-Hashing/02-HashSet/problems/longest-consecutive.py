"""
Problem: Longest Consecutive Sequence

Difficulty: Medium (LeetCode #128)

---------------------------------------------------
Problem Statement:

Given an unsorted array of integers, return the length of the longest
run of CONSECUTIVE integers (order within the array is irrelevant — we
care about the numerical run).

Example:
    nums = [100, 4, 200, 1, 3, 2]
    Longest consecutive run: 1, 2, 3, 4  → length 4

Constraint:
    The solution must run in O(n) time.

---------------------------------------------------
The Obvious (But Wrong) Approach:

    sort(nums); scan to find the longest run

This is O(n log n), which fails the time constraint. So the problem
is specifically asking: "can you do this WITHOUT sorting?"

---------------------------------------------------
The HashSet Trick — O(n):

The insight is that a run is bounded by its SMALLEST element. For
each `x` in the set, check if `x - 1` is in the set:
    - if yes, x is NOT the start of a run — skip
    - if no, x IS the start of a run — walk forward (x, x+1, x+2, ...)
      counting consecutive elements

Each number is visited at most twice (once as a "not a start" check,
once as part of a run), so total work is O(n).

Why this is O(n) overall (not O(n²) as it might look):
    The inner while loop only extends a run for numbers that are
    NOT the start. Each number contributes to at most one inner
    loop iteration across the whole algorithm.

---------------------------------------------------
Complexity:

    Time:  O(n) expected (assumes hash-set ops are O(1))
    Space: O(n) for the set
"""


# =========================================================================
# Solution 1: HashSet (O(n))
# =========================================================================

def longest_consecutive(nums):
    """
    Return the length of the longest run of consecutive integers.

    Time:  O(n).
    Space: O(n).
    """
    if not nums:
        return 0

    num_set = set(nums)
    best = 0

    for x in num_set:
        # Only start counting from a RUN START (x with no predecessor)
        if (x - 1) in num_set:
            continue

        length = 1
        while (x + length) in num_set:
            length += 1

        best = max(best, length)

    return best


# =========================================================================
# Solution 2: Sorting (O(n log n)) — for comparison
# =========================================================================

def longest_consecutive_sort(nums):
    """
    Sort then scan. Violates LC's O(n) requirement but is easier to read.

    Time:  O(n log n).
    Space: O(1) if sort is in-place.
    """
    if not nums:
        return 0

    nums = sorted(set(nums))
    best = 1
    current = 1

    for i in range(1, len(nums)):
        if nums[i] == nums[i - 1] + 1:
            current += 1
            best = max(best, current)
        else:
            current = 1

    return best


# =========================================================================
# Solution 3: Union-Find (academic curiosity)
# =========================================================================

def longest_consecutive_union_find(nums):
    """
    Treat each number as a node; union x with x-1 and x+1 when they exist.
    Largest connected component = longest run.

    Time:  O(n α(n)) ≈ O(n).
    Space: O(n).

    Not necessary for LC, but illustrates the "runs are equivalence
    classes" viewpoint. Covered in detail in Phase-10 (Union-Find).
    """
    if not nums:
        return 0

    parent = {x: x for x in nums}
    size = {x: 1 for x in nums}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]          # path compression
            x = parent[x]
        return x

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx == ry:
            return
        # Union by size
        if size[rx] < size[ry]:
            rx, ry = ry, rx
        parent[ry] = rx
        size[rx] += size[ry]

    num_set = set(nums)
    for x in num_set:
        if (x + 1) in num_set:
            union(x, x + 1)

    return max(size[find(x)] for x in num_set)


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    cases = [
        ([100, 4, 200, 1, 3, 2],             4),    # LC example: 1..4
        ([0, 3, 7, 2, 5, 8, 4, 6, 0, 1],     9),    # LC extended: 0..8
        ([],                                 0),
        ([5],                                1),
        ([1, 2, 0, 1],                       3),    # duplicates don't count extra
        ([-5, -4, -3, 10, 11, 12, 13],       4),    # negative run not longest
        ([-1, 0, 1, 2, 10, 11],              4),    # -1..2
        (list(range(1000)),                  1000), # one big run
        ([i for i in range(1000) if i % 2],  1),    # no two consecutive
    ]

    for nums, expected in cases:
        assert longest_consecutive(nums) == expected, (
            f"hashset: {nums[:10]}... expected {expected}"
        )
        assert longest_consecutive_sort(nums) == expected
        assert longest_consecutive_union_find(nums) == expected

    # Randomized cross-check
    import random
    random.seed(42)
    for _ in range(100):
        nums = [random.randint(-50, 50) for _ in range(random.randint(0, 100))]
        expected = longest_consecutive_sort(nums)
        assert longest_consecutive(nums) == expected
        assert longest_consecutive_union_find(nums) == expected

    print("All tests passed!")

    # ---------------------------------------------------------------
    # Why the Hash-Set Approach Is O(n) — Not O(n²):
    #
    #   At first glance, the nested while loop looks like it could
    #   run to n inside the outer loop, giving O(n²). But the inner
    #   loop ONLY runs for the STARTS of runs, and each run is walked
    #   exactly ONCE. So across the entire outer loop, the total
    #   number of inner iterations is n. Amortized O(1) per number.
    #
    #   This is a classic "argue about total work, not per-iteration"
    #   situation. Similar reasoning appears in:
    #     - two-pointer problems
    #     - monotonic stack problems
    #     - amortized analysis of dynamic arrays
    # ---------------------------------------------------------------
