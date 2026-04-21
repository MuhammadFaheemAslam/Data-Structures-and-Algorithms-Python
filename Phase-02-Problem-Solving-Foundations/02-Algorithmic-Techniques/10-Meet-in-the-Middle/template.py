"""
template.py – Meet in the Middle Reference Template

This file demonstrates the MITM pattern three ways:

    1. all_subset_sums       — enumerate all 2^n subset sums in O(n * 2^n)
    2. exists_subset_sum     — MITM: exists subset of nums summing to target?  O(n * 2^(n/2))
    3. count_pairs_with_sum  — MITM: count pairs (a, b) in two halves with a + b == target

The core trick: enumerate each half independently, then combine.

Run this file to see each template's output.
"""

from bisect import bisect_left, insort


# =========================================================================
# Utility: Enumerate all subset sums (helper for MITM)
# =========================================================================

def all_subset_sums(nums):
    """
    Return a sorted list of ALL subset sums of `nums` (including the
    empty subset with sum 0). Contains 2^n entries.

    Time Complexity:  O(2^n * n)
    Space Complexity: O(2^n)
    """
    sums = [0]
    for x in nums:
        sums = sums + [s + x for s in sums]       # doubles the list each step
    return sorted(sums)


# =========================================================================
# Template 1: Brute Force (For Contrast)
# =========================================================================

def exists_subset_sum_brute_force(nums, target):
    """
    Check every subset via bitmask.

    Time Complexity:  O(n * 2^n)
    Space Complexity: O(1)

    Usable up to n ~ 25. Included here to cross-verify the MITM version.
    """
    n = len(nums)
    for mask in range(1 << n):
        s = 0
        for k in range(n):
            if mask & (1 << k):
                s += nums[k]
        if s == target:
            return True
    return False


# =========================================================================
# Template 2: Meet in the Middle — Exists a Subset Summing to Target?
# =========================================================================

def exists_subset_sum(nums, target):
    """
    Return True iff some subset of `nums` sums to exactly `target`.

    Meet-in-the-middle implementation:
        - Split nums in half.
        - Enumerate all subset sums of each half (2^(n/2) each).
        - For each sum `sb` in the right half, check whether `target - sb`
          was produced by the left half (hash set lookup).

    Time Complexity:  O(n * 2^(n/2))
    Space Complexity: O(2^(n/2))

    Practical up to n ~ 40–50 depending on memory. This is the range
    where brute force fails but MITM still breezes through.
    """
    n = len(nums)
    if n == 0:
        return target == 0

    mid = n // 2
    left, right = nums[:mid], nums[mid:]

    # enumerate left subset sums into a set for O(1) lookup
    left_sums = {0}
    for x in left:
        left_sums |= {s + x for s in left_sums}

    # for each right subset sum, ask "did the left produce the complement?"
    right_sums = [0]
    for x in right:
        right_sums = right_sums + [s + x for s in right_sums]

    for sb in right_sums:
        if (target - sb) in left_sums:
            return True

    return False


# =========================================================================
# Template 3: Meet in the Middle — Count Pairs with Given Sum
# =========================================================================

def count_pairs_with_sum(nums, target):
    """
    Return the number of subsets of `nums` whose sum equals `target`.

    Same MITM structure, but we COUNT matches rather than stopping at
    the first one. Uses a dict: {left_sum: count_of_subsets_producing_it}.

    Time Complexity:  O(n * 2^(n/2))
    Space Complexity: O(2^(n/2))
    """
    from collections import Counter

    n = len(nums)
    mid = n // 2
    left, right = nums[:mid], nums[mid:]

    # all subset sums of the left half (WITH multiplicity — two different
    # subsets can produce the same sum, and each counts)
    left_sums = [0]
    for x in left:
        left_sums = left_sums + [s + x for s in left_sums]
    left_counter = Counter(left_sums)

    right_sums = [0]
    for x in right:
        right_sums = right_sums + [s + x for s in right_sums]

    # pair each right_sum with the count of complementing left_sums
    total = 0
    for sb in right_sums:
        total += left_counter.get(target - sb, 0)

    return total


# =========================================================================
# Template 4: MITM with Sort + Binary Search — Closest Subset Sum
# =========================================================================

def closest_subset_sum(nums, target):
    """
    Return the subset sum closest to `target` (ties broken towards lower).

    Uses sort + binary search combine (instead of hash set), because we
    need range queries — specifically "the sum in left_sums closest to X".

    Time Complexity:  O(n * 2^(n/2))
    Space Complexity: O(2^(n/2))
    """
    if not nums:
        return 0

    n = len(nums)
    mid = n // 2
    left, right = nums[:mid], nums[mid:]

    left_sums = all_subset_sums(left)            # sorted
    right_sums = all_subset_sums(right)

    best = float("inf")
    best_val = 0

    for sb in right_sums:
        # we want the left_sum CLOSEST to (target - sb)
        want = target - sb
        idx = bisect_left(left_sums, want)
        candidates = []
        if idx < len(left_sums):
            candidates.append(left_sums[idx])
        if idx > 0:
            candidates.append(left_sums[idx - 1])
        for sa in candidates:
            total = sa + sb
            diff = abs(total - target)
            if diff < best:
                best = diff
                best_val = total

    return best_val


# =========================================================================
# Demonstration
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Template 1 — all_subset_sums (helper)")
    print("=" * 60)
    nums = [1, 2, 3]
    print(f"   nums = {nums}")
    print(f"   all_subset_sums = {all_subset_sums(nums)}")
    # 2^3 = 8 subsets: sums {0, 1, 2, 3, 3, 4, 5, 6}
    assert all_subset_sums(nums) == [0, 1, 2, 3, 3, 4, 5, 6]
    print()

    print("=" * 60)
    print("Template 2 — exists_subset_sum (MITM)")
    print("=" * 60)
    tests = [
        ([3, 34, 4, 12, 5, 2],   9,   True),     # 4 + 5
        ([3, 34, 4, 12, 5, 2],   30,  False),
        ([1, 2, 3],              7,   False),
        ([1, 2, 3],              6,   True),     # all three
        ([],                     0,   True),     # empty subset
        ([5],                    5,   True),
        ([5],                    3,   False),
        ([2, 4, 6],              0,   True),     # empty subset again
    ]
    for nums, target, expected in tests:
        got = exists_subset_sum(nums, target)
        bf = exists_subset_sum_brute_force(nums, target)
        assert got == expected, f"{nums}, target={target}: expected {expected}, got {got}"
        assert bf == expected
        print(f"   exists_subset_sum({nums}, {target}) = {got}")
    print()

    print("=" * 60)
    print("Template 3 — count_pairs_with_sum")
    print("=" * 60)
    tests = [
        ([1, 2, 3, 4],          5,   3),         # {1,4},{2,3},{1,4}? let's verify via brute:
                                                  # subsets of [1,2,3,4] with sum 5:
                                                  # {1,4}, {2,3}, {1,4}? no, only one {1,4}. let me recount:
                                                  # actually all subsets with sum 5: {1,4}, {2,3}. So count is 2.
    ]
    # quickly verify by brute force
    def brute_count(nums, target):
        n = len(nums)
        cnt = 0
        for mask in range(1 << n):
            s = sum(nums[i] for i in range(n) if mask & (1 << i))
            if s == target:
                cnt += 1
        return cnt

    for nums, target, _expected in tests:
        got = count_pairs_with_sum(nums, target)
        bf = brute_count(nums, target)
        assert got == bf, f"count_pairs_with_sum({nums}, {target}) = {got}, brute = {bf}"
        print(f"   count_pairs_with_sum({nums}, {target}) = {got}")

    # extra count tests via brute force only (self-consistent)
    for nums in [[1, 2, 3, 4, 5], [1, 1, 1, 1], [2, 4, 6, 8]]:
        for target in range(sum(nums) + 1):
            got = count_pairs_with_sum(nums, target)
            bf = brute_count(nums, target)
            assert got == bf, f"count_pairs_with_sum({nums}, {target}) = {got}, brute = {bf}"
    print("   (additional count stress tests passed)")
    print()

    print("=" * 60)
    print("Template 4 — closest_subset_sum")
    print("=" * 60)
    tests = [
        ([5, -3, 8, 2],   4,   4),                # subset {2, 5, -3} → 4 exactly
        ([5, -3, 8, 2],   10,  10),               # {2, 8}
        ([1, 2, 4, 8],    7,   7),                # {1, 2, 4}
        ([1, 2, 4, 8],    100, 15),               # farthest feasible is the total
    ]
    for nums, target, expected in tests:
        got = closest_subset_sum(nums, target)
        assert got == expected, f"{nums}, target={target}: expected {expected}, got {got}"
        print(f"   closest_subset_sum({nums}, target={target}) = {got}")

    print("\nAll tests passed!")
