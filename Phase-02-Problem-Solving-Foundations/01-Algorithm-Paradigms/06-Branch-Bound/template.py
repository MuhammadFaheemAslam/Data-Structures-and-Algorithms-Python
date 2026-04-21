"""
template.py – Branch & Bound Reference Template

This file demonstrates the SHAPE of a Branch & Bound algorithm.

The ONE change from backtracking is the bound check:

    if bound(state) is worse than best:
        return          # prune — this branch cannot improve on `best`

The bound function is the entire personality of the algorithm — pick it
well and B&B runs in milliseconds where brute force would run for days.

We show the pattern on 0/1 Knapsack:

    Brute force:     O(2^n)  — try every subset
    Backtracking:    O(2^n)  — same; no pruning because everything is "valid"
    Branch & Bound:  O(2^n) worst case; dramatically faster in practice
                     thanks to a fractional-knapsack upper bound.

The B&B version explores far fewer subtrees than brute force on realistic
inputs — we track and print that number at the end so you can see the
effect directly.

Run this file to see the template's output.
"""

# =========================================================================
# Generic Branch & Bound Skeleton
# =========================================================================
#
# best = worst_possible_value          # +inf for min, -inf for max
#
# def branch_and_bound(state):
#     nonlocal best
#
#     if is_complete(state):
#         best = better_of(best, state.cost)
#         return
#
#     if bound(state) is_worse_than best:   # ← the ONE line beyond backtracking
#         return
#
#     for choice in candidate_choices(state):
#         if is_feasible(choice, state):
#             state.apply(choice)
#             branch_and_bound(state)
#             state.unapply(choice)


# =========================================================================
# Template: 0/1 Knapsack (Maximization) via B&B with a Fractional Upper Bound
#
# State: (index_of_next_item, remaining_capacity, value_so_far)
# Goal:  maximize value
# Bound: an UPPER bound on the value achievable from this state.
#        We get it by solving FRACTIONAL knapsack on the remaining items —
#        that always beats any legal 0/1 completion, so it's a safe
#        (admissible) upper bound for maximization.
# =========================================================================

def knapsack_brute_force(weights, values, W):
    """
    Baseline: try every subset. Used to validate B&B's correctness.

    Time Complexity:  O(2^n)
    Space Complexity: O(n)
    """
    n = len(weights)
    best = 0
    for mask in range(1 << n):
        w = sum(weights[i] for i in range(n) if mask & (1 << i))
        v = sum(values[i]  for i in range(n) if mask & (1 << i))
        if w <= W and v > best:
            best = v
    return best


def knapsack_branch_and_bound(weights, values, W):
    """
    Solve 0/1 knapsack with B&B.

    Upper-bound function:
        For any partial state (items selected so far + next item index),
        the UPPER bound on the final value is:

            value_so_far
          + take whole items in value/weight order while they fit
          + take a fraction of the next-best item to fill the remaining capacity

        This is the fractional-knapsack solution on the remaining items,
        which is always >= any legal 0/1 completion.
        So if that upper bound is already <= `best`, this branch is doomed.

    Time Complexity:  O(n log n) for the sort + worst-case O(2^n) branches,
                      in practice MUCH less thanks to pruning.
    Space Complexity: O(n)

    Returns (optimal_value, nodes_explored) so you can see the pruning pay off.
    """
    n = len(weights)

    # sort items by value/weight ratio (descending) — the order that
    # makes the fractional-knapsack bound as tight as possible
    items = sorted(
        zip(weights, values),
        key=lambda wv: wv[1] / wv[0] if wv[0] > 0 else float("inf"),
        reverse=True,
    )
    ws = [w for w, _ in items]
    vs = [v for _, v in items]

    def upper_bound(i, remaining, value_so_far):
        """
        Compute the fractional-knapsack completion value from item index i.
        This is guaranteed to be >= the best 0/1 value from (i, remaining).
        """
        bound = value_so_far
        k = i
        while k < n and ws[k] <= remaining:
            bound += vs[k]
            remaining -= ws[k]
            k += 1
        # partial fraction of the next item, if any
        if k < n and remaining > 0:
            bound += vs[k] * remaining / ws[k]
        return bound

    best = 0
    nodes_explored = 0

    def branch(i, remaining, value_so_far):
        nonlocal best, nodes_explored
        nodes_explored += 1

        if i == n:
            if value_so_far > best:
                best = value_so_far
            return

        # PRUNE: if even the optimistic upper bound can't beat `best`, stop.
        if upper_bound(i, remaining, value_so_far) <= best:
            return

        # Branch 1: TAKE item i (if it fits)
        if ws[i] <= remaining:
            branch(i + 1, remaining - ws[i], value_so_far + vs[i])

        # Branch 2: SKIP item i
        branch(i + 1, remaining, value_so_far)

    branch(0, W, 0)
    return best, nodes_explored


# =========================================================================
# Demonstration
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Template — 0/1 Knapsack with B&B")
    print("=" * 60)

    # Same test cases as the DP module — proves B&B matches DP on correctness
    test_cases = [
        ([1, 2, 3, 8],          [1, 5, 4, 10],          10, 15),
        ([10, 20, 30],          [60, 100, 120],         50, 220),
        ([5],                   [10],                   5,  10),
        ([5],                   [10],                   4,  0),
        ([1, 1, 1],             [100, 100, 100],        2,  200),
        ([2, 3, 4, 5],          [3, 4, 5, 6],           5,  7),
    ]

    # A slightly bigger input to demonstrate the pruning advantage
    big_weights = [4, 2, 7, 3, 1, 5, 6, 8, 2, 9, 3, 4, 6, 1, 5, 2]
    big_values  = [8, 3, 12, 6, 2, 9, 11, 15, 4, 18, 5, 7, 10, 2, 8, 3]
    big_W = 30
    bf_val = knapsack_brute_force(big_weights, big_values, big_W)
    bb_val, nodes = knapsack_branch_and_bound(big_weights, big_values, big_W)

    print(f"\n   Bigger input: n = {len(big_weights)}, W = {big_W}")
    print(f"     brute force value:    {bf_val}")
    print(f"     B&B value:            {bb_val}")
    print(f"     nodes B&B explored:   {nodes}")
    print(f"     full 2^n tree size:   {2 ** len(big_weights)}")
    print(f"     pruning ratio:        {nodes / (2 ** len(big_weights)):.1%}")
    print()

    for i, (w, v, W, expected) in enumerate(test_cases):
        bf = knapsack_brute_force(w, v, W)
        bb, _ = knapsack_branch_and_bound(w, v, W)
        assert bf == expected, f"Test {i+1} (brute force) expected {expected}, got {bf}"
        assert bb == expected, f"Test {i+1} (B&B) expected {expected}, got {bb}"
        print(f"   Test {i+1}: n = {len(w):2}, W = {W:2}, optimal = {expected}   ✓")

    print("\nAll tests passed!")
