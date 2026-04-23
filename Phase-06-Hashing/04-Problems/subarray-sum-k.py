"""
Problem: Subarray Sum Equals K

Difficulty: Medium (LeetCode #560)

---------------------------------------------------
Problem Statement:

Given an integer array `nums` and an integer `k`, return the number
of CONTIGUOUS SUBARRAYS whose sum equals `k`.

Example:
    nums = [1, 1, 1], k = 2  → 2       (subarrays [1,1] at indices 0..1 and 1..2)
    nums = [1, 2, 3], k = 3  → 2       ([1,2] and [3])

Values in nums can be negative — so you CANNOT use sliding window
here (the invariant "sum grows monotonically as the window grows"
doesn't hold with negative numbers).

---------------------------------------------------
Why This Problem Is a Hash-Map Gem:

The classical approach is PREFIX SUM + HASH MAP, which looks like
magic the first time you see it:

    Let P[i] = sum of nums[0..i-1], with P[0] = 0.
    A subarray nums[i..j-1] has sum P[j] - P[i] = k.
    So for each j, count how many i < j have P[i] = P[j] - k.

Maintain a running prefix sum `running`. For each index, count how
many times (running - k) has appeared in prefix sums so far. Then
record the current prefix sum.

This reduces from O(n²) brute force to O(n).

---------------------------------------------------
Why Phase 06 Is The Right Place For This Problem:

The algorithm has nothing to do with arrays per se — it's a hash-map
pattern (COUNT occurrences of a transformed quantity). The same
pattern solves:

    - "Subarray sum divisible by K" (LC #974)
      Track prefix sums MOD k.
    - "Continuous subarray sum" (LC #523)
      Track (prefix sum mod k) → earliest index.
    - "Longest subarray sum = k" (LC #325)
      Track (prefix sum → earliest index).
    - "Contiguous array" (LC #525)
      Transform 0→-1, then "longest subarray sum = 0".
    - "Subarrays with exactly K odd numbers" (LC #1248)
      Transform odd→1 even→0; solve as "subarray sum = k".

Each is a one-line transformation layered on top of the prefix-sum
+ hash-map skeleton. Once you see the pattern, five problems collapse
into one.

---------------------------------------------------
Complexity:

    Time:  O(n).
    Space: O(n) for the prefix-sum counter.
"""

from collections import defaultdict


# =========================================================================
# Solution 1: O(n²) Brute Force — establish correctness baseline
# =========================================================================

def subarray_sum_brute(nums, k):
    """Check every contiguous subarray. O(n²)."""
    count = 0
    n = len(nums)
    for i in range(n):
        s = 0
        for j in range(i, n):
            s += nums[j]
            if s == k:
                count += 1
    return count


# =========================================================================
# Solution 2: Prefix Sum + Hash Map — O(n)
# =========================================================================

def subarray_sum(nums, k):
    """
    Count subarrays with sum = k using prefix sums and a hash map of
    prefix-sum frequencies.

    For each index j, the number of valid subarrays ENDING at j is
    the number of prefix sums P[i] (i < j) with P[i] = P[j] - k.

    Time:  O(n).
    Space: O(n).
    """
    # Counts[s] = number of prefix sums equal to s seen so far.
    # Seed with {0: 1} so subarrays starting from index 0 are counted.
    counts = defaultdict(int)
    counts[0] = 1

    total = 0
    running = 0
    for x in nums:
        running += x
        total += counts[running - k]               # all i with P[i] = running - k
        counts[running] += 1

    return total


# =========================================================================
# Related: Subarray Sum Divisible by K (LC #974) — same pattern
# =========================================================================

def subarrays_div_by_k(nums, k):
    """
    Count contiguous subarrays with sum divisible by k.

    Same prefix-sum idea, but we key the map by (running % k).
    Subarray (i..j] is divisible by k iff (P[j] - P[i]) % k == 0,
    i.e. P[j] ≡ P[i] (mod k).

    Python's % returns non-negative, which is perfect here.
    """
    counts = defaultdict(int)
    counts[0] = 1

    total = 0
    running = 0
    for x in nums:
        running = (running + x) % k
        total += counts[running]
        counts[running] += 1

    return total


# =========================================================================
# Related: Longest Subarray With Sum = K (LC #325) — same skeleton, different return
# =========================================================================

def longest_subarray_with_sum(nums, k):
    """
    Return the length of the longest subarray with sum = k.

    Instead of counting, record the EARLIEST index each prefix-sum
    value was seen. Longest subarray ending at j = j - first_seen[P[j] - k].

    Time:  O(n).
    """
    first_seen = {0: -1}                           # prefix sum 0 before any element
    running = 0
    best = 0

    for j, x in enumerate(nums):
        running += x
        if (running - k) in first_seen:
            best = max(best, j - first_seen[running - k])
        # Only record the FIRST time we see each prefix sum
        if running not in first_seen:
            first_seen[running] = j

    return best


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #560 examples
    cases_sum = [
        ([1, 1, 1],                2, 2),
        ([1, 2, 3],                3, 2),
        ([1, -1, 0],               0, 3),           # [1,-1], [-1,0+wait... actually [-1,1]? Let's recount]
    ]
    # Manually verified: [1, -1, 0], k=0 → subarrays [1,-1], [0], [1,-1,0] → 3
    for nums, k, expected in cases_sum:
        assert subarray_sum(nums, k) == expected
        assert subarray_sum_brute(nums, k) == expected

    # Randomized: O(n) matches O(n²) on hundreds of cases
    import random
    random.seed(42)
    for _ in range(500):
        n = random.randint(0, 40)
        nums = [random.randint(-5, 5) for _ in range(n)]
        k = random.randint(-10, 10)
        assert subarray_sum(nums, k) == subarray_sum_brute(nums, k), (
            f"mismatch: nums={nums}, k={k}"
        )

    print("subarray_sum: 500 random cases match brute force")

    # Subarray sum divisible by k (LC #974)
    # Example: [4,5,0,-2,-3,1], k=5 → 7
    assert subarrays_div_by_k([4, 5, 0, -2, -3, 1], 5) == 7
    assert subarrays_div_by_k([5], 9) == 0
    assert subarrays_div_by_k([5], 5) == 1
    print("subarrays_div_by_k: LC #974 examples pass")

    # Longest subarray with sum k (LC #325)
    assert longest_subarray_with_sum([1, -1, 5, -2, 3], 3) == 4       # [1,-1,5,-2]
    assert longest_subarray_with_sum([-2, -1, 2, 1], 1) == 2          # [-1,2]
    assert longest_subarray_with_sum([1, 2, 3], 7) == 0               # no such subarray
    print("longest_subarray_with_sum: LC #325 examples pass")

    # Randomized cross-check for longest subarray
    def longest_brute(nums, k):
        best = 0
        for i in range(len(nums)):
            s = 0
            for j in range(i, len(nums)):
                s += nums[j]
                if s == k:
                    best = max(best, j - i + 1)
        return best

    for _ in range(200):
        n = random.randint(0, 30)
        nums = [random.randint(-5, 5) for _ in range(n)]
        k = random.randint(-10, 10)
        assert longest_subarray_with_sum(nums, k) == longest_brute(nums, k)

    print("longest_subarray_with_sum: 200 random cases match brute force")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Pattern, Once More:
    #
    #     1. Define a PREFIX-SUM-LIKE running quantity.
    #     2. The property you're counting is some algebraic identity
    #        between two prefix values (equal, differ by k, differ
    #        by a multiple of k, etc.).
    #     3. Store prefix values in a hash map.
    #        - Map value → count: for "how many subarrays?"
    #        - Map value → earliest index: for "longest subarray?"
    #
    # This pattern underlies easily 20% of the "medium" difficulty
    # subarray problems on LeetCode. Recognize the shape — you'll
    # see it everywhere.
    # ---------------------------------------------------------------
