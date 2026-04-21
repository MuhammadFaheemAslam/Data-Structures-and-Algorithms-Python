"""
Problem: 0/1 Knapsack

Paradigm: Dynamic Programming — the canonical 2D DP problem
Difficulty: Medium

---------------------------------------------------
Problem Statement:

You have a knapsack of capacity `W` and `n` items. Item `i` has weight
`weights[i]` and value `values[i]`. You can either take an item WHOLE or
leave it (you may NOT take fractions — that's fractional knapsack, a
different problem).

Return the maximum total value you can fit in the knapsack.

---------------------------------------------------
Why This Problem Matters:

Knapsack is the prototype for an entire family of DP problems:

    - Subset Sum        ("can we make sum T?")            — same structure
    - Partition Equal Subset Sum                           — subset sum in disguise
    - Coin Change (count ways / min coins)                 — unbounded knapsack
    - Target Sum                                           — subset sum with signs
    - Last Stone Weight II                                 — subset sum (minimize difference)

If you can recognize "knapsack shape", you immediately know how to solve
each of these. That pattern-matching is half of DP practice.

---------------------------------------------------
The Recurrence:

    State: dp[i][w] = max value using first i items, capacity w.

    Transitions (for each item i):
        DON'T take item i-1:  dp[i][w]  =  dp[i-1][w]
        DO take item i-1:     dp[i][w]  =  dp[i-1][w - weights[i-1]] + values[i-1]
                                           (only if weights[i-1] <= w)

    dp[i][w] = max of the two.

    Base case: dp[0][w] = 0   (no items → zero value)

    Answer: dp[n][W]

---------------------------------------------------
The Greedy Trap:

A natural greedy approach is "take the highest value-per-weight ratio first."
This IS optimal for FRACTIONAL knapsack (see 03-Greedy/template.py) but
fails for 0/1 because you can't shave off a fraction to fit the capacity.

    Counter-example:
        weights = [10, 20, 30]
        values  = [60, 100, 120]
        W = 50

    Ratios: 6.0, 5.0, 4.0.
    Greedy 0/1: take items 0 and 1 (w=30, v=160). Can't take item 2 (30 > 20 left).
    DP optimal: take items 1 and 2 (w=50, v=220).                 ← wins

That one-word constraint change — "fractional" to "0/1" — flips the
right paradigm from greedy to DP.

---------------------------------------------------
Example:

    weights = [1, 2, 3, 8]
    values  = [1, 5, 4, 10]
    W = 10

    Optimal: take items 1, 2, 3  (weights 2+3+8=13)  → too heavy
    Optimal: take items 0, 1, 3  (weights 1+2+8=11)  → too heavy
    Optimal: take items 0, 1, 2  (weights 1+2+3=6, values 1+5+4=10)
    Optimal: take items 1, 3     (weights 2+8=10, values 5+10=15) ✓

    Answer: 15

---------------------------------------------------
"""

from functools import cache


# -------------------------------------------------
# Approach 1: Top-Down DP (Memoization)
# -------------------------------------------------

def knapsack_topdown(weights, values, W):
    """
    Classical memoized recursion on (index_of_item, remaining_capacity).

    Time Complexity:  O(n * W)
    Space Complexity: O(n * W)   — memo + recursion stack

    Closest to the mathematical recurrence. Good for understanding.
    """
    n = len(weights)

    @cache
    def dp(i, w):
        # base case: no more items to consider
        if i == n:
            return 0

        # option A: skip item i
        best = dp(i + 1, w)

        # option B: take item i — only if it fits
        if weights[i] <= w:
            best = max(best, dp(i + 1, w - weights[i]) + values[i])

        return best

    return dp(0, W)


# -------------------------------------------------
# Approach 2: Bottom-Up DP (Tabulation)
# -------------------------------------------------

def knapsack_bottomup(weights, values, W):
    """
    Build a 2D table dp[i][w] iteratively.

    Time Complexity:  O(n * W)
    Space Complexity: O(n * W)

    Exactly the recurrence, filled in a loop. Good for performance;
    no recursion overhead, no stack concerns.
    """
    n = len(weights)
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        weight_i = weights[i - 1]
        value_i = values[i - 1]
        for w in range(W + 1):
            dp[i][w] = dp[i - 1][w]              # skip item i
            if weight_i <= w:
                dp[i][w] = max(
                    dp[i][w],
                    dp[i - 1][w - weight_i] + value_i,  # take item i
                )

    return dp[n][W]


# -------------------------------------------------
# Approach 3: Space-Optimized (1D Array)
# -------------------------------------------------

def knapsack_space_optimized(weights, values, W):
    """
    dp[i][w] only ever reads dp[i-1][*]. Roll the 2D table into a 1D array.

    Time Complexity:  O(n * W)
    Space Complexity: O(W)

    CRITICAL: iterate w from HIGH to LOW.

    Why? dp[w - weight_i] on the left side of the recurrence must still
    contain the PREVIOUS row's value when we read it. If we iterated
    left-to-right, we'd overwrite dp[w - weight_i] with the current row's
    value before using it — that would (incorrectly) allow item i to be
    used multiple times (which is the UNBOUNDED knapsack, not 0/1).

    Iterating right-to-left means dp[w - weight_i] is always from the
    previous iteration, which is the 0/1 constraint.
    """
    n = len(weights)
    dp = [0] * (W + 1)

    for i in range(n):
        weight_i = weights[i]
        value_i = values[i]
        # iterate w from W down to weight_i
        for w in range(W, weight_i - 1, -1):
            dp[w] = max(dp[w], dp[w - weight_i] + value_i)

    return dp[W]


# -------------------------------------------------
# Approach 4: Brute Force (Verification Only)
# -------------------------------------------------

def knapsack_brute_force(weights, values, W):
    """
    Try every subset. Used ONLY to cross-check the DP versions on
    small inputs.

    Time Complexity:  O(2^n)
    Space Complexity: O(n)
    """
    n = len(weights)
    best = 0
    for mask in range(1 << n):
        total_weight = 0
        total_value = 0
        for i in range(n):
            if mask & (1 << i):
                total_weight += weights[i]
                total_value += values[i]
        if total_weight <= W and total_value > best:
            best = total_value
    return best


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    weights = [1, 2, 3, 8]
    values  = [1, 5, 4, 10]
    W = 10

    print(f"weights = {weights}")
    print(f"values  = {values}")
    print(f"W       = {W}")
    print()
    print(f"top-down DP:        {knapsack_topdown(weights, values, W)}")
    print(f"bottom-up DP (2D):  {knapsack_bottomup(weights, values, W)}")
    print(f"space-optimized:    {knapsack_space_optimized(weights, values, W)}")
    print(f"brute force (check): {knapsack_brute_force(weights, values, W)}")
    print()

    # Test cases – (weights, values, W, expected)
    test_cases = [
        ([1, 2, 3, 8],      [1, 5, 4, 10],    10, 15),   # example above
        ([10, 20, 30],      [60, 100, 120],   50, 220),  # the greedy counter-example
        ([],                [],               10, 0),    # no items
        ([5],               [10],             4,  0),    # item doesn't fit
        ([5],               [10],             5,  10),   # item exactly fits
        ([1, 1, 1],         [100, 100, 100],  2,  200),  # take any 2 of 3
        ([2, 3, 4, 5],      [3, 4, 5, 6],     5,  7),    # 2 + 3 = 5, values 3 + 4 = 7
        ([3, 2, 4, 1],      [5, 3, 5, 2],     5,  8),   # items 0+1: weights 3+2=5, values 5+3=8
    ]

    for i, (ws, vs, W, expected) in enumerate(test_cases):
        for fn in (knapsack_topdown, knapsack_bottomup, knapsack_space_optimized):
            got = fn(ws, vs, W)
            assert got == expected, (
                f"Test {i+1} ({fn.__name__}) failed on W={W}, "
                f"weights={ws}, values={vs}: expected {expected}, got {got}"
            )
        # cross-check with brute force
        assert knapsack_brute_force(ws, vs, W) == expected
        print(f"Test {i+1} passed: W={W}, expected {expected}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The DP Arc for 0/1 Knapsack:
    #
    #   top-down       O(n*W) time    O(n*W) space   clearest code
    #   bottom-up 2D   O(n*W) time    O(n*W) space   no recursion
    #   1D rolling     O(n*W) time    O(W)   space   production-ready
    #
    # All three are the same algorithm; the last is the version you'd
    # ship. The right-to-left iteration is the subtle invariant that
    # enforces the "each item used at most once" constraint.
    # ---------------------------------------------------------------
