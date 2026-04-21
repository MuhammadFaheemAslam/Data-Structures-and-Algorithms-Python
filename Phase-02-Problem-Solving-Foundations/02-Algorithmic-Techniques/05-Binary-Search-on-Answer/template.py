"""
template.py – Binary Search on Answer Reference Template

This file shows the two templates of BSOA plus one classical example
of each:

    Template A (floor mid)   — find the SMALLEST X such that check(X) is True.
                              Predicate: False on the left, True on the right.

    Template B (ceil mid)    — find the LARGEST X such that check(X) is True.
                              Predicate: True on the left, False on the right.

Classical examples:

    1. Minimum eating speed (Template A — minimum feasible speed).
    2. Maximum min-distance between points (Template B — max feasible distance).

Once you've seen both directions, every BSOA problem reduces to
"which template do I pick, and what is `check(X)`?"

Run this file to see each template's output.
"""

import math


# =========================================================================
# Template A — Minimum X such that check(X) is True
# Predicate pattern: F F F T T T T  →  want the leftmost T
# =========================================================================

def min_feasible(lo, hi, check):
    """
    Generic: binary-search for the smallest integer X in [lo, hi] with
    check(X) == True.

    Precondition: check(hi) == True, and once it flips True it stays True.

    Time Complexity: O(log(hi - lo)) * cost of check
    """
    while lo < hi:
        mid = (lo + hi) // 2                     # FLOOR — no +1
        if check(mid):
            hi = mid                             # mid works — try smaller
        else:
            lo = mid + 1                         # mid fails — must be bigger
    return lo


# =========================================================================
# Template B — Maximum X such that check(X) is True
# Predicate pattern: T T T T F F F  →  want the rightmost T
# =========================================================================

def max_feasible(lo, hi, check):
    """
    Generic: binary-search for the largest integer X in [lo, hi] with
    check(X) == True.

    Precondition: check(lo) == True, and once it flips False it stays False.

    Time Complexity: O(log(hi - lo)) * cost of check

    Note the CEILING mid: without it, the loop can stall when
    hi == lo + 1 because floor(mid) would equal lo, and the branch
    `lo = mid` wouldn't advance.
    """
    while lo < hi:
        mid = (lo + hi + 1) // 2                 # CEIL
        if check(mid):
            lo = mid                             # mid works — try bigger
        else:
            hi = mid - 1                         # mid fails — must be smaller
    return lo


# =========================================================================
# Example 1 (Template A): Minimum eating speed to finish in H hours
# =========================================================================

def minimum_eating_speed(piles, h):
    """
    Koko has `h` hours to eat bananas from given `piles`. At speed k
    she eats k bananas/hour from one pile (but no leftovers spill into
    the next hour). What's the smallest speed k such that she finishes
    in ≤ h hours? (LeetCode #875.)

    check(k) =  total_hours_needed(k)  <=  h
             =  sum(ceil(pile / k) for pile in piles)  <=  h

    This is monotone: larger k → fewer hours → more likely feasible.
    So it's a classic "minimum feasible X" problem — Template A.

    Time Complexity:  O(n log(max(piles)))
    Space Complexity: O(1)
    """
    def check(k):
        return sum(math.ceil(p / k) for p in piles) <= h

    return min_feasible(1, max(piles), check)


# =========================================================================
# Example 2 (Template B): Max min-distance between K points on a line
# =========================================================================

def max_min_distance(positions, k):
    """
    Given sorted `positions` and k cows, place each cow at a position
    to MAXIMIZE the MINIMUM pairwise distance (Aggressive Cows).

    check(d) = can we place k cows such that every pair is >= d apart?
    Greedy: sort positions, place the first cow at positions[0], then
    greedily place the next at the first position >= last + d.

    Monotone: a larger d is harder (fewer placements fit). So this is
    "maximum feasible X" — Template B.

    Time Complexity:  O(n log((max - min)))
    Space Complexity: O(1) (assuming `positions` is already sorted)
    """
    positions = sorted(positions)

    def check(d):
        placed = 1
        last = positions[0]
        for p in positions[1:]:
            if p - last >= d:
                placed += 1
                last = p
                if placed == k:
                    return True
        return placed >= k

    lo = 1                                       # min positive distance
    hi = positions[-1] - positions[0]            # can't exceed total span

    return max_feasible(lo, hi, check)


# =========================================================================
# Demonstration
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Template A — Minimum feasible X")
    print("=" * 60)
    cases = [
        ([3, 6, 7, 11],                 8,  4),
        ([30, 11, 23, 4, 20],           5,  30),
        ([30, 11, 23, 4, 20],           6,  23),
        ([1],                           1,  1),
    ]
    for piles, h, expected in cases:
        got = minimum_eating_speed(piles, h)
        assert got == expected, (
            f"minimum_eating_speed({piles}, h={h}) = {got}, expected {expected}"
        )
        print(f"   minimum_eating_speed({piles}, h={h}) = {got}")
    print()

    print("=" * 60)
    print("Template B — Maximum feasible X")
    print("=" * 60)
    cases = [
        ([1, 2, 4, 8, 9],        3,  3),         # 1, 4, 8  → min dist 3
        ([5, 4, 3, 2, 1, 1000000000], 2, 999999999),
        ([1, 2, 3, 4, 7],        3,  3),
        ([1, 2],                 2,  1),
    ]
    for positions, k, expected in cases:
        got = max_min_distance(positions, k)
        assert got == expected, (
            f"max_min_distance({positions}, k={k}) = {got}, expected {expected}"
        )
        print(f"   max_min_distance({positions}, k={k}) = {got}")

    print("\nAll tests passed!")
