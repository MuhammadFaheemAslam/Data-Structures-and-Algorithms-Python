"""
template.py – Greedy Reference Template

This file demonstrates the SHAPE of a greedy algorithm, then shows two
concrete instances of it:

    1. Fractional Knapsack – greedy by value-per-weight ratio; provably optimal.
    2. Minimum Platforms   – greedy by earliest event time (classic schedule/interval problem).

Every greedy algorithm follows the same four-step recipe:

    (1) Define the greedy criterion (the rule that picks "the obvious next move").
    (2) Sort / prioritize items by that criterion.
    (3) Walk them, committing to each feasible choice.
    (4) Return the accumulated solution.

The subtle part is ALWAYS step 1: picking the right criterion so that the
greedy algorithm is provably optimal. See theory.md for the proof pattern
(exchange arguments).

Run this file to see each template's output.
"""

import heapq


# =========================================================================
# Generic Greedy Skeleton
# =========================================================================
#
# def greedy(items):
#     items = sorted(items, key=greedy_criterion, reverse=maximizing)
#
#     solution = []
#     for item in items:
#         if feasible(item, solution):
#             solution.append(item)
#             commit(item)
#
#     return solution
#
# The work is in `greedy_criterion` and `feasible`. Everything else is boilerplate.


# =========================================================================
# Template 1: Fractional Knapsack
# Complexity: O(n log n)  (dominated by the sort)
# Greedy criterion: highest value-to-weight ratio first
# =========================================================================

def fractional_knapsack(items, capacity):
    """
    Given items, each with (value, weight), fill a knapsack of the given
    `capacity` to maximize total value. You may take FRACTIONS of an item.

    Greedy: take items in decreasing order of value/weight ratio. If the
    last item doesn't fit whole, take a fraction of it.

    This is PROVABLY optimal by an exchange argument — swapping any pair
    of ratio-ordered picks for a non-greedy pair can only reduce the total.

    *Important:* fractional knapsack is greedy-solvable; 0/1 knapsack
    (no fractions) is NOT — it needs DP. This is a great example of a
    one-word constraint change flipping the right paradigm.

    Time Complexity:  O(n log n)
    Space Complexity: O(n)

    Returns (total_value, chosen) where `chosen` is a list of
    (value, weight, fraction_taken) triples.
    """
    # (1) + (2) prioritize by the greedy criterion: value / weight
    ranked = sorted(items, key=lambda vw: vw[0] / vw[1], reverse=True)

    # (3) commit, one item at a time, until the knapsack is full
    total_value = 0.0
    remaining = capacity
    chosen = []

    for value, weight in ranked:
        if remaining == 0:
            break

        if weight <= remaining:                 # take the whole item
            chosen.append((value, weight, 1.0))
            total_value += value
            remaining -= weight
        else:                                   # take a fraction to fill up
            fraction = remaining / weight
            chosen.append((value, weight, fraction))
            total_value += value * fraction
            remaining = 0

    return total_value, chosen


# =========================================================================
# Template 2: Minimum Platforms (Interval Scheduling)
# Complexity: O(n log n) for the sort + O(n log n) for the heap ops
# Greedy criterion: process events in order; reuse a platform if possible
# =========================================================================

def min_platforms(trains):
    """
    Given a list of (arrival, departure) times for trains at a station,
    return the minimum number of platforms needed so that no train waits.

    Greedy: sort by arrival time. For each train, check the EARLIEST train
    currently occupying a platform — if it's already departed, reuse that
    platform; otherwise open a new one. A min-heap of active departure
    times implements this in O(log n) per step.

    This is a classic "events on a timeline" greedy.

    Time Complexity:  O(n log n)
    Space Complexity: O(n)
    """
    if not trains:
        return 0

    # (1) + (2) sort by arrival time so we process events in order
    ordered = sorted(trains, key=lambda t: t[0])

    # Active departures of platforms in use — the smallest one is the
    # candidate to be freed up first.
    active = []  # min-heap of departure times

    for arrival, departure in ordered:
        # (3) can we reuse an already-freed platform?
        if active and active[0] <= arrival:
            heapq.heappop(active)
        # open a new (or reused) platform by scheduling its departure
        heapq.heappush(active, departure)

    # The peak number of platforms ever in use is the heap's final size.
    return len(active)


# =========================================================================
# Demonstration
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Template 1 — Fractional Knapsack  (O(n log n))")
    print("=" * 60)
    items = [                                    # (value, weight)
        (60, 10),                                # ratio 6.0
        (100, 20),                               # ratio 5.0
        (120, 30),                               # ratio 4.0
    ]
    capacity = 50
    total, chosen = fractional_knapsack(items, capacity)
    print(f"   items = {items}")
    print(f"   capacity = {capacity}")
    print(f"   total value   = {total}")
    print(f"   chosen (v, w, frac):")
    for pick in chosen:
        print(f"      {pick}")
    print()

    print("=" * 60)
    print("Template 2 — Minimum Platforms  (O(n log n))")
    print("=" * 60)
    trains = [
        (900,  910),
        (940, 1200),
        (950, 1120),
        (1100, 1130),
        (1500, 1900),
        (1800, 2000),
    ]
    print(f"   trains (arrive, depart): {trains}")
    print(f"   minimum platforms needed = {min_platforms(trains)}")
