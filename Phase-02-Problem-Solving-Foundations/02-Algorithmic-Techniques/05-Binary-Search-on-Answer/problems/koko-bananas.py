"""
Problem: Koko Eating Bananas

Technique: Binary Search on Answer
Difficulty: Medium (LeetCode #875)

---------------------------------------------------
Problem Statement:

Koko loves bananas. There are `n` piles, where pile `i` contains
`piles[i]` bananas. The guards will return in `h` hours.

Koko decides her eating speed `k` (bananas/hour). Each hour, she picks
a pile and eats up to `k` bananas from it:

    - If the pile has fewer than k bananas, she eats them all and
      stops for this hour (no leftover time carries over).
    - If the pile has more, she eats exactly k and moves to the next
      hour.

Find the MINIMUM integer speed `k` such that Koko finishes all piles
within `h` hours.

---------------------------------------------------
The Binary-Search-on-Answer Lens:

The brute-force approach is to try k = 1, 2, 3, ... and stop at the
first feasible speed. That's O(max(piles) * n) — way too slow when
piles contain up to 10^9 bananas.

Observation — MONOTONICITY:

    If Koko can finish at speed k, she can also finish at any speed > k.
    (Eating faster never helps miss a deadline.)

That's the precondition for BSOA:

    speed:     1 2 3 4 5 6 7 8 9 10 …
    feasible:  F F F F F T T T T T  …
                       ↑
                       smallest feasible k — the answer.

We binary-search for the boundary. Given a candidate speed k, the
feasibility check is:

    hours_needed(k) = sum(ceil(p / k) for p in piles)
    feasible(k)     = hours_needed(k) <= h

This is O(n) per candidate. Binary search over [1, max(piles)] has
log(max(piles)) ≈ 30 iterations. Total: O(n log(max(piles))).

---------------------------------------------------
Template: MINIMUM feasible X — floor mid, shrink from the right.

---------------------------------------------------
Example:

    piles = [3, 6, 7, 11], h = 8
    -> 4
    (At k=4: 1 + 2 + 2 + 3 = 8 hours exactly. At k=3: 1 + 2 + 3 + 4 = 10, too slow.)

---------------------------------------------------
"""

import math


# -------------------------------------------------
# The Binary-Search-on-Answer Solution
# -------------------------------------------------

def min_eating_speed(piles, h):
    """
    Return the minimum integer eating speed such that Koko finishes
    all piles in at most `h` hours.

    Time Complexity:  O(n * log(max(piles)))
    Space Complexity: O(1)
    """
    def hours_needed(k):
        """How many hours does Koko take at speed k?"""
        return sum(math.ceil(pile / k) for pile in piles)

    # search range: at least 1 banana/hour; at most the biggest pile
    # (any k beyond that wastes capacity — one pile per hour regardless)
    lo, hi = 1, max(piles)

    # Template A (FLOOR mid): want the smallest k with hours_needed(k) <= h
    while lo < hi:
        mid = (lo + hi) // 2
        if hours_needed(mid) <= h:               # mid works — try smaller
            hi = mid
        else:                                    # mid fails — must be bigger
            lo = mid + 1

    return lo


# -------------------------------------------------
# Brute Force for Verification — O(max(piles) * n)
# -------------------------------------------------

def min_eating_speed_brute_force(piles, h):
    """
    Try every k from 1 upward; return the first that works.

    Time Complexity:  O(max(piles) * n)
    Space Complexity: O(1)

    Used only to validate the BSOA solution on small inputs.
    """
    for k in range(1, max(piles) + 1):
        if sum(math.ceil(p / k) for p in piles) <= h:
            return k
    return max(piles)                             # fallback (unreachable for valid input)


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    piles, h = [3, 6, 7, 11], 8
    print(f"piles = {piles}, h = {h}")
    print(f"min_eating_speed:             {min_eating_speed(piles, h)}")
    print(f"min_eating_speed_brute_force: {min_eating_speed_brute_force(piles, h)}")
    print()

    # Test cases — (piles, h, expected)
    test_cases = [
        ([3, 6, 7, 11],               8,   4),       # canonical
        ([30, 11, 23, 4, 20],         5,   30),      # tight deadline → must eat whole biggest pile per hour
        ([30, 11, 23, 4, 20],         6,   23),
        ([1],                         1,   1),
        ([1, 1, 1, 1],                4,   1),
        ([1000000000],                2,   500000000),  # big value, enforce BSOA is used (not iteration)
        ([312884470],                 968709470,   1),  # plenty of time — speed 1 suffices
    ]

    for i, (p, hh, expected) in enumerate(test_cases):
        got = min_eating_speed(p, hh)
        assert got == expected, (
            f"Test {i+1}: piles={p}, h={hh} → expected {expected}, got {got}"
        )
        # cross-check brute force only on small inputs
        if max(p) <= 100:
            bf = min_eating_speed_brute_force(p, hh)
            assert got == bf, f"Test {i+1}: BSOA ({got}) disagrees with brute force ({bf})"
        print(f"Test {i+1} passed: piles={p}, h={hh} -> {expected}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Speedup:
    #
    #   Brute force:   O(max(piles) * n)      up to 10^9 * 10^4 = 10^13  (unusable)
    #   BSOA:          O(n log(max(piles)))   up to ~30 * 10^4 = 3·10^5  (instant)
    #
    # That's a 30-million-fold speedup by replacing linear scan over
    # candidate speeds with binary search.
    # ---------------------------------------------------------------
