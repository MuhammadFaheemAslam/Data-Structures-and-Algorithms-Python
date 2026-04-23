"""
Problem 01: Median of Two Sorted Arrays

Difficulty: Hard (LeetCode #4)

---------------------------------------------------
Problem Statement:

Given two SORTED arrays `nums1` and `nums2` of sizes m and n, return
the MEDIAN of their combined (sorted) contents.

    nums1 = [1, 3], nums2 = [2]       → median = 2
    nums1 = [1, 2], nums2 = [3, 4]    → median = 2.5

Follow-up:
    Can you solve it in **O(log(min(m, n)))** time?

That follow-up is what makes this problem HARD. The naive O(m + n)
merge is easy; the O(log) version is the one that tests algorithmic
maturity.

---------------------------------------------------
The Three Approaches:

    1. Merge then find middle        O(m + n) time, O(m + n) space
    2. Two-pointer walk to middle    O(m + n) time, O(1) space
    3. Binary search on partitions   **O(log(min(m, n)))**   ← THE answer

We'll cover all three. Approach 3 is the interview-defining solution.

---------------------------------------------------
Approach 3 — The Binary-Search-on-Partitions Intuition:

The median of a combined sorted array splits it into two halves of
equal size (or near-equal). The KEY INSIGHT:

    We don't need to MERGE the arrays to find the median — we just
    need to find the CORRECT SPLIT POINT in each one.

Say we take `i` elements from nums1 and `j` elements from nums2,
such that `i + j = (m + n + 1) // 2`. For this split to be the
median's boundary:

    max(nums1[i-1], nums2[j-1])  ≤  min(nums1[i], nums2[j])

i.e., everything on the left is ≤ everything on the right. If the
condition holds:

    median (odd total):  max(nums1[i-1], nums2[j-1])
    median (even total): (max(left) + min(right)) / 2

Binary search `i` on the SHORTER array (size m, say) from 0 to m.
Each iteration adjusts i based on which side of the partition is
out of balance. Total work: O(log(min(m, n))).

This is a brilliantly subtle algorithm — even experienced programmers
struggle with it. It's canonical because it encapsulates the "search
over the ANSWER SPACE, not the input" idea that appears throughout
Phase 02 / 02 / 05-Binary-Search-on-Answer.

---------------------------------------------------
"""

# =========================================================================
# Approach 1: Merge Then Find Middle — O(m + n)
# =========================================================================

def find_median_merge(nums1, nums2):
    """
    Full merge using Python's sorted(), then index the middle.

    Time:  O((m+n) log(m+n)) — sorted() doesn't know the inputs are sorted
    Space: O(m + n)

    Simplest but wasteful. Use two-pointer merge for O(m+n).
    """
    merged = sorted(nums1 + nums2)
    n = len(merged)
    if n == 0:
        return 0.0

    mid = n // 2
    if n % 2 == 1:
        return float(merged[mid])
    return (merged[mid - 1] + merged[mid]) / 2


# =========================================================================
# Approach 2: Two-Pointer Walk — O(m + n) Time, O(1) Space
# =========================================================================

def find_median_two_pointers(nums1, nums2):
    """
    Merge-style walk, but stop at the median position. No full merge.

    Time:  O(m + n)  — walk halfway
    Space: O(1)
    """
    m, n = len(nums1), len(nums2)
    total = m + n
    if total == 0:
        return 0.0

    # We need to find positions (total - 1) // 2 and total // 2
    i = j = 0
    prev = curr = 0

    for _ in range(total // 2 + 1):
        prev = curr
        if i < m and (j >= n or nums1[i] <= nums2[j]):
            curr = nums1[i]
            i += 1
        else:
            curr = nums2[j]
            j += 1

    if total % 2 == 1:
        return float(curr)
    return (prev + curr) / 2


# =========================================================================
# Approach 3: Binary Search on Partitions — O(log(min(m, n)))
# =========================================================================

def find_median(nums1, nums2):
    """
    Find the median in O(log(min(m, n))) by binary-searching the
    partition point in the SHORTER array.

    Time:  O(log(min(m, n)))
    Space: O(1)

    The key insight: we find the partition `i` in nums1 and
    `j = half_length - i` in nums2 such that:

        nums1_left_max  ≤  nums2_right_min
        nums2_left_max  ≤  nums1_right_min

    When both hold, the partition boundary is the median.
    """
    # Always binary-search the SHORTER array for min log factor
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    total = m + n
    half = (total + 1) // 2                       # size of the LEFT half

    lo, hi = 0, m
    while lo <= hi:
        i = (lo + hi) // 2                         # take i elements from nums1
        j = half - i                               # take j elements from nums2

        # boundaries of the four regions, using ±∞ for out-of-range
        nums1_left  = nums1[i - 1] if i > 0 else float("-inf")
        nums1_right = nums1[i]     if i < m else float("inf")
        nums2_left  = nums2[j - 1] if j > 0 else float("-inf")
        nums2_right = nums2[j]     if j < n else float("inf")

        # correct partition: every left element ≤ every right element
        if nums1_left <= nums2_right and nums2_left <= nums1_right:
            if total % 2 == 1:
                return float(max(nums1_left, nums2_left))
            return (max(nums1_left, nums2_left) + min(nums1_right, nums2_right)) / 2

        # adjust
        if nums1_left > nums2_right:
            hi = i - 1                             # take fewer from nums1
        else:
            lo = i + 1                             # take more from nums1

    # unreachable given valid input
    raise RuntimeError("Input arrays are not sorted")


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    # Canonical examples
    examples = [
        ([1, 3],         [2],             2.0),
        ([1, 2],         [3, 4],          2.5),
        ([0, 0],         [0, 0],          0.0),
        ([],             [1],             1.0),
        ([1],            [],              1.0),
        ([1, 3],         [2, 7],          2.5),
    ]
    print("Canonical examples:")
    for a, b, expected in examples:
        for fn in (find_median_merge, find_median_two_pointers, find_median):
            got = fn(a, b)
            assert abs(got - expected) < 1e-9, (
                f"{fn.__name__}({a}, {b}) = {got}, expected {expected}"
            )
        print(f"   find_median({a}, {b}) = {expected}")
    print()

    # Edge cases
    edge_cases = [
        ([1, 2, 3, 4, 5],      [6, 7, 8, 9, 10],     5.5),   # one entirely below the other
        ([6, 7, 8, 9, 10],     [1, 2, 3, 4, 5],      5.5),   # the reverse
        ([1],                  [2, 3, 4, 5, 6],      3.5),   # one much smaller
        ([1, 2, 3, 4, 5],      [6],                  3.5),
        ([-10, -5, 0, 5, 10],  [-8, -3, 2, 7],       0.0),   # negatives
        ([1, 1, 1],            [1, 1, 1],            1.0),   # all equal
        ([1, 2, 3],            [4, 5, 6, 7],         4.0),   # odd total
    ]

    for i, (a, b, expected) in enumerate(edge_cases):
        for fn in (find_median_merge, find_median_two_pointers, find_median):
            got = fn(a, b)
            assert abs(got - expected) < 1e-9, (
                f"Test {i+1} ({fn.__name__}): expected {expected}, got {got}"
            )
        print(f"Test {i+1} passed: median({a}, {b}) = {expected}")

    # Stress test — compare all three against Python's sorted
    import random
    random.seed(42)
    for _ in range(500):
        m = random.randint(0, 30)
        n = random.randint(0, 30)
        if m + n == 0:
            continue
        a = sorted(random.sample(range(-100, 100), m))
        b = sorted(random.sample(range(-100, 100), n))

        merged = sorted(a + b)
        total = m + n
        if total % 2 == 1:
            expected = float(merged[total // 2])
        else:
            expected = (merged[total // 2 - 1] + merged[total // 2]) / 2

        for fn in (find_median_merge, find_median_two_pointers, find_median):
            got = fn(a, b)
            assert abs(got - expected) < 1e-9, (
                f"stress: a={a}, b={b}: {fn.__name__}={got}, expected={expected}"
            )

    print("\nStress test: 500 random sorted-array pairs — all three approaches agree")

    # Timing — show the binary search version is actually log
    import time
    random.seed(0)
    big_a = sorted(random.sample(range(-10**6, 10**6), 500_000))
    big_b = sorted(random.sample(range(-10**6, 10**6), 500_000))

    t0 = time.time()
    find_median_two_pointers(big_a, big_b)
    t_linear = time.time() - t0

    t0 = time.time()
    find_median(big_a, big_b)
    t_log = time.time() - t0

    print(f"\nTiming on 500k + 500k sorted arrays:")
    print(f"   two-pointer O(m+n):           {t_linear:.4f}s")
    print(f"   binary search O(log min):     {t_log:.6f}s")
    print(f"   speedup:                      {t_linear / max(t_log, 1e-6):.0f}×")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Why This Problem Is Hard:
    #
    #   1. The O(m + n) solution is "too easy" — anyone can merge.
    #   2. The O(log) solution requires seeing the problem through
    #      a completely different lens: not "merge the arrays" but
    #      "find the partition point".
    #   3. The partition invariants are easy to state, hard to get
    #      right under interview pressure. The ±∞ edge cases trip
    #      up most first attempts.
    #
    # Worth spending time on. If you can derive the O(log) version
    # from scratch, you've genuinely internalized "binary search
    # on the answer space" from Phase-02 / 02 / 05.
    # ---------------------------------------------------------------
