"""
template.py – Brute Force Reference Template

This file demonstrates the SHAPE of a brute-force algorithm in three
canonical search-space flavors. Every brute-force problem you'll ever
write is a variation on one of these three.

    1. All pairs        O(n^2)
    2. All subsets      O(2^n)
    3. All permutations O(n!)

Each template uses the same three-step recipe:
    (a) Define the search space.
    (b) Enumerate every candidate.
    (c) Validate each candidate and track the best.

Run this file to see each template's output on a small example.
"""

from itertools import combinations, permutations


# =========================================================================
# Template 1: Search Space = All Pairs
# Complexity: O(n^2) to enumerate, times O(c) to validate each pair
# =========================================================================

def brute_force_pairs(arr, is_better=max):
    """
    Find the pair (i, j) with i < j that maximizes some score.
    Here we score a pair by its SUM — swap in any scoring function.

    Time Complexity: O(n^2)
    Space Complexity: O(1)
    """
    n = len(arr)
    best_score = None
    best_pair = None

    # (a) + (b) enumerate every valid pair of indices
    for i in range(n):
        for j in range(i + 1, n):
            score = arr[i] + arr[j]             # scoring function
            # (c) keep the best candidate seen so far
            if best_score is None or is_better(score, best_score) == score:
                best_score = score
                best_pair = (i, j)

    return best_pair, best_score


# =========================================================================
# Template 2: Search Space = All Subsets
# Complexity: O(2^n) to enumerate, times O(c) to validate each subset
# =========================================================================

def brute_force_subsets(items):
    """
    Visit every subset of `items` and return the one with the largest sum
    under the constraint that its sum is at most `capacity`. This is
    exactly the shape of the 0/1 knapsack brute force.

    Time Complexity: O(2^n * n)   — 2^n subsets, each scored in O(n)
    Space Complexity: O(n)        — at most one subset at a time
    """
    best_subset = ()
    best_score = 0

    # itertools.combinations(items, r) for r in 0..n enumerates every subset
    # (a) + (b) all subsets of all sizes
    for r in range(len(items) + 1):
        for subset in combinations(items, r):
            # (c) score the candidate
            score = sum(subset)
            if score > best_score:
                best_score = score
                best_subset = subset

    return best_subset, best_score


# Equivalent bitmask enumeration — often faster and more "brute" in spirit.
# Every integer mask from 0 to 2^n - 1 encodes a subset:
#   bit k set in mask  <->  items[k] is IN the subset.
def brute_force_subsets_bitmask(items):
    """
    Same as brute_force_subsets, but enumerated via bitmasks.

    Time Complexity: O(2^n * n)
    Space Complexity: O(n)
    """
    n = len(items)
    best_subset = ()
    best_score = 0

    for mask in range(1 << n):                  # 0 .. 2^n - 1
        subset = tuple(items[k] for k in range(n) if mask & (1 << k))
        score = sum(subset)
        if score > best_score:
            best_score = score
            best_subset = subset

    return best_subset, best_score


# =========================================================================
# Template 3: Search Space = All Permutations
# Complexity: O(n! * c) where c is the per-permutation validation cost
# =========================================================================

def brute_force_permutations(cities, distance):
    """
    Classic Traveling Salesman brute force: try every permutation of
    cities and return the one with the smallest total tour distance.

    Args:
        cities:   list of city labels  (e.g. ["A", "B", "C"])
        distance: callable (a, b) -> number; distance between two cities

    Time Complexity: O(n! * n)
    Space Complexity: O(n)
    """
    best_tour = None
    best_cost = None

    # (a) + (b) every permutation of the cities
    for tour in permutations(cities):
        # (c) score: sum the distances around the tour, returning to start
        cost = sum(
            distance(tour[i], tour[(i + 1) % len(tour)])
            for i in range(len(tour))
        )
        if best_cost is None or cost < best_cost:
            best_cost = cost
            best_tour = tour

    return best_tour, best_cost


# =========================================================================
# Demonstration
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Template 1 — All Pairs")
    print("=" * 60)
    arr = [1, 5, 3, 8, 2, 9, 4]
    pair, score = brute_force_pairs(arr)
    print(f"   arr   = {arr}")
    print(f"   best pair of indices -> {pair}")
    print(f"   values               -> ({arr[pair[0]]}, {arr[pair[1]]})")
    print(f"   sum                  -> {score}")
    print()

    print("=" * 60)
    print("Template 2 — All Subsets")
    print("=" * 60)
    items = [3, 1, 4, 1, 5, 9, 2, 6]
    subset, score = brute_force_subsets(items)
    subset_bm, score_bm = brute_force_subsets_bitmask(items)
    print(f"   items                    = {items}")
    print(f"   best subset (combinations) -> {subset} (sum = {score})")
    print(f"   best subset (bitmask)      -> {subset_bm} (sum = {score_bm})")
    print()

    print("=" * 60)
    print("Template 3 — All Permutations (TSP)")
    print("=" * 60)
    cities = ["A", "B", "C", "D"]
    dist_map = {
        ("A", "B"): 1, ("A", "C"): 4, ("A", "D"): 3,
        ("B", "C"): 2, ("B", "D"): 5,
        ("C", "D"): 1,
    }

    def distance(a, b):
        if a == b:
            return 0
        return dist_map.get((a, b), dist_map.get((b, a)))

    tour, cost = brute_force_permutations(cities, distance)
    print(f"   cities = {cities}")
    print(f"   best tour  -> {' -> '.join(tour)} -> {tour[0]}")
    print(f"   total cost -> {cost}")
