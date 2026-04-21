"""
Problem: Activity Selection

Paradigm: Greedy
Difficulty: Easy-Medium (canonical greedy problem)

---------------------------------------------------
Problem Statement:

Given `n` activities, each with a start and end time, select the
LARGEST possible set of mutually compatible activities.

Two activities are compatible if their time intervals don't overlap.
(Activity A with end time == activity B's start time IS compatible —
they touch but don't overlap.)

---------------------------------------------------
The Greedy Lens:

This is the textbook example of greedy done right. The correct criterion
is non-obvious: several plausible rules LOOK like they should work but
don't. Only one gives a provably optimal answer:

    CORRECT:   pick the activity with the EARLIEST END TIME first.
    WRONG:     earliest start time, shortest duration, fewest conflicts.

Each of the "wrong" criteria has a counter-example where it fails
while "earliest end time" succeeds. We implement all four below and
demonstrate the difference on an adversarial input.

Time Complexity:  O(n log n) — dominated by the sort.
Space Complexity: O(n)       — the chosen set.

---------------------------------------------------
Why Earliest End Time Works (Exchange Argument):

Let G be greedy's solution and O be any optimal solution, each sorted
by end time. If G's first choice g₁ differs from O's first choice o₁,
then by greedy's rule end(g₁) ≤ end(o₁). Swap o₁ for g₁ in O: all
remaining activities in O that were compatible with o₁ remain compatible
with g₁ (which ends no later). The modified O has the same size as before
— still optimal — and now starts with g₁. Induct on the remainder.

Conclusion: greedy always produces an optimal solution.

---------------------------------------------------
Example:

    activities = [(1, 3), (2, 5), (3, 9), (6, 8), (5, 7), (8, 10)]
    Optimal    = 3   — e.g., (1, 3), (5, 7), (8, 10)
                       or   (2, 5), (5, 7), (8, 10)
                       or   (1, 3), (6, 8), (8, 10)
---------------------------------------------------
"""

# -------------------------------------------------
# The Correct Greedy: Earliest End Time
# -------------------------------------------------

def activity_selection(activities):
    """
    Greedy selection by earliest end time.

    Time Complexity:  O(n log n)
    Space Complexity: O(n)

    This is the canonical, provably-optimal greedy algorithm.
    """
    if not activities:
        return []

    # sort by end time (greedy criterion)
    ordered = sorted(activities, key=lambda a: a[1])

    chosen = [ordered[0]]
    last_end = ordered[0][1]

    for start, end in ordered[1:]:
        if start >= last_end:                   # no overlap with last pick
            chosen.append((start, end))
            last_end = end

    return chosen


# -------------------------------------------------
# Three Wrong Greedy Criteria — For Educational Contrast
# -------------------------------------------------

def activity_selection_earliest_start(activities):
    """
    WRONG greedy: pick the earliest STARTING activity first.

    Counter-example: activities = [(0, 100), (1, 2), (3, 4)]
        earliest start  -> [(0, 100)]         (size 1)   ← WRONG
        earliest end    -> [(1, 2), (3, 4)]   (size 2)   ✓

    One very long early activity blocks everything after it.
    """
    if not activities:
        return []

    ordered = sorted(activities, key=lambda a: a[0])    # by start time
    chosen = [ordered[0]]
    last_end = ordered[0][1]

    for start, end in ordered[1:]:
        if start >= last_end:
            chosen.append((start, end))
            last_end = end

    return chosen


def activity_selection_shortest(activities):
    """
    WRONG greedy: pick the shortest activity first.

    Counter-example: activities = [(0, 10), (9, 11), (10, 20)]
        shortest       -> [(9, 11)]                  (size 1)  ← WRONG
        earliest end   -> [(0, 10), (10, 20)]        (size 2)  ✓

    A single short activity sitting in the middle blocks two longer
    ones that could both fit.
    """
    if not activities:
        return []

    ordered = sorted(activities, key=lambda a: a[1] - a[0])    # by duration
    chosen = []

    for act in ordered:
        if all(not _overlap(act, c) for c in chosen):
            chosen.append(act)

    return sorted(chosen, key=lambda a: a[1])


def activity_selection_fewest_conflicts(activities):
    """
    WRONG greedy: pick the activity with the FEWEST conflicts first.

    Has known counter-examples in the literature. Kept here as another
    example of a plausible-but-wrong greedy criterion.
    """
    if not activities:
        return []

    def conflicts(a, pool):
        return sum(1 for b in pool if a is not b and _overlap(a, b))

    ordered = sorted(activities, key=lambda a: conflicts(a, activities))
    chosen = []

    for act in ordered:
        if all(not _overlap(act, c) for c in chosen):
            chosen.append(act)

    return sorted(chosen, key=lambda a: a[1])


def _overlap(a, b):
    """Two intervals overlap if each starts before the other ends."""
    return a[0] < b[1] and b[0] < a[1]


# -------------------------------------------------
# Brute Force (for verifying greedy's optimality on small inputs)
# -------------------------------------------------

def activity_selection_brute_force(activities):
    """
    Exhaustive: enumerate every subset, keep the largest mutually-compatible one.

    Time Complexity:  O(2^n * n^2)
    Space Complexity: O(n)

    Useful ONLY to cross-check that greedy produces an answer of the
    same size as the true optimum on small inputs.
    """
    from itertools import combinations

    best = []
    n = len(activities)
    for r in range(n + 1):
        for subset in combinations(activities, r):
            ok = all(
                not _overlap(subset[i], subset[j])
                for i in range(len(subset)) for j in range(i + 1, len(subset))
            )
            if ok and len(subset) > len(best):
                best = list(subset)
    return best


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    activities = [(1, 3), (2, 5), (3, 9), (6, 8), (5, 7), (8, 10)]
    print(f"activities: {activities}")
    print(f"greedy (earliest end time): {activity_selection(activities)}")
    print()

    # Demonstrate the wrong greedies losing on adversarial inputs
    print("Demonstrating why criterion matters:")
    print()

    adv1 = [(0, 100), (1, 2), (3, 4)]
    print(f"   activities = {adv1}")
    print(f"   earliest end    -> {activity_selection(adv1)}")
    print(f"   earliest start  -> {activity_selection_earliest_start(adv1)}   (wrong)")
    print()

    adv2 = [(0, 10), (9, 11), (10, 20)]
    print(f"   activities = {adv2}")
    print(f"   earliest end    -> {activity_selection(adv2)}")
    print(f"   shortest        -> {activity_selection_shortest(adv2)}   (wrong)")
    print()

    # Test cases – optimal set SIZES verified against brute force
    test_cases = [
        # (activities, optimal_size)
        ([(1, 3), (2, 5), (3, 9), (6, 8), (5, 7), (8, 10)],    3),
        ([],                                                    0),
        ([(5, 10)],                                             1),
        ([(1, 2), (3, 4), (5, 6)],                              3),  # all compatible
        ([(1, 10), (2, 3), (4, 5)],                             2),  # the long one is a trap
        ([(0, 100), (1, 2), (3, 4)],                            2),
        ([(0, 10), (9, 11), (10, 20)],                          2),
    ]

    for i, (acts, expected_size) in enumerate(test_cases):
        got = activity_selection(acts)
        assert len(got) == expected_size, (
            f"Test {i+1} failed: on {acts}, expected size {expected_size}, "
            f"got {len(got)} ({got})"
        )
        # validate pairwise compatibility of the chosen activities
        for i1, a in enumerate(got):
            for b in got[i1 + 1:]:
                assert not _overlap(a, b), (
                    f"Test {i+1}: overlapping activities in result: {a}, {b}"
                )
        # cross-check against brute force on every test case
        bf = activity_selection_brute_force(acts)
        assert len(got) == len(bf), (
            f"Test {i+1}: greedy found {len(got)}, brute force found {len(bf)}"
        )
        print(f"Test {i+1} passed: {acts} -> size {expected_size}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Why This Problem Is the Canonical Greedy Example:
    #
    #   1. Multiple plausible greedy criteria exist.
    #   2. Only ONE of them (earliest end time) is provably optimal.
    #   3. The exchange argument for why that one works is clean enough
    #      to write on a whiteboard.
    #   4. The wrong criteria have tiny, elegant counter-examples.
    #
    # Together these make activity selection the best problem for
    # learning why greedy DEMANDS proof — not just intuition.
    # ---------------------------------------------------------------
