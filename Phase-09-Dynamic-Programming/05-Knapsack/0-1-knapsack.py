"""
0-1 Knapsack — The Classic Formulation

Given `n` items with weights `w[i]` and values `v[i]` and a capacity W,
pick a subset maximizing total value subject to total weight ≤ W.
Each item is taken AT MOST ONCE.

---------------------------------------------------
State:

    dp[i][c] = max value using items 0..i-1, with capacity c

Transition:

    dp[i][c] = max(
        dp[i-1][c],                              # skip item i-1
        dp[i-1][c - w[i-1]] + v[i-1]             # take item i-1 (if c >= w[i-1])
    )

Base: dp[0][*] = 0 (no items → zero value).

---------------------------------------------------
The 1D Rolling-Array Trick:

The 2D dp[n][W] can be rolled into a 1D dp[W] if we iterate capacity
from W DOWN TO w[i]. Backward iteration ensures we're reading the
PREVIOUS ROW's dp[c - w[i]] (= "item not yet taken") rather than the
current row (= "item taken in THIS iteration", which would double-count).

Forward iteration would give us the UNBOUNDED knapsack — see the
other file.

---------------------------------------------------
Complexity:

    Time:  O(n · W)
    Space: O(n · W)  or  O(W) with rolling
"""


# -------- Full 2D DP --------

def knapsack_01_2d(weights, values, W):
    """
    Max value of items whose total weight ≤ W, each item at most once.

    Time:  O(n · W)
    Space: O(n · W)
    """
    n = len(weights)
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w_i, v_i = weights[i - 1], values[i - 1]
        for c in range(W + 1):
            dp[i][c] = dp[i - 1][c]                         # skip
            if c >= w_i:
                dp[i][c] = max(dp[i][c], dp[i - 1][c - w_i] + v_i)

    return dp[n][W]


# -------- Space-optimized 1D --------

def knapsack_01(weights, values, W):
    """
    Same answer, O(W) space.

    The crucial detail: iterate `c` BACKWARDS. If we went forward, we'd
    use dp[c - w_i] that was ALREADY updated in THIS iteration (= item
    i taken multiple times), not the previous row's.

    Time: O(n · W), Space: O(W).
    """
    n = len(weights)
    dp = [0] * (W + 1)

    for i in range(n):
        w_i, v_i = weights[i], values[i]
        for c in range(W, w_i - 1, -1):                     # BACKWARDS: W, W-1, ..., w_i
            dp[c] = max(dp[c], dp[c - w_i] + v_i)

    return dp[W]


# -------- Reconstruction: which items were chosen? --------

def knapsack_01_items(weights, values, W):
    """
    Return (max_value, list_of_indices_chosen).

    Requires the full 2D table to backtrack.

    Time: O(n · W), Space: O(n · W).
    """
    n = len(weights)
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w_i, v_i = weights[i - 1], values[i - 1]
        for c in range(W + 1):
            dp[i][c] = dp[i - 1][c]
            if c >= w_i:
                dp[i][c] = max(dp[i][c], dp[i - 1][c - w_i] + v_i)

    # Backtrack
    chosen = []
    c = W
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i - 1][c]:                        # item i-1 WAS taken
            chosen.append(i - 1)
            c -= weights[i - 1]
    chosen.reverse()
    return dp[n][W], chosen


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Classic example
    #   items: (w=2,v=3), (w=3,v=4), (w=4,v=5), (w=5,v=6)
    #   capacity: 5
    #   Optimal: take items 0 and 1 → weight 2+3=5, value 3+4=7
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    W = 5
    assert knapsack_01(weights, values, W) == 7
    assert knapsack_01_2d(weights, values, W) == 7
    max_v, items = knapsack_01_items(weights, values, W)
    assert max_v == 7
    assert sum(weights[i] for i in items) <= W
    assert sum(values[i] for i in items) == 7

    # Empty / trivial
    assert knapsack_01([], [], 10) == 0
    assert knapsack_01([5], [10], 0) == 0                   # no capacity
    assert knapsack_01([5], [10], 4) == 0                   # can't fit
    assert knapsack_01([5], [10], 5) == 10                  # fits exactly

    # All items take, nothing left
    assert knapsack_01([1, 1, 1], [5, 5, 5], 3) == 15

    # Single heavy item that dominates
    assert knapsack_01([1, 1, 10], [1, 1, 100], 10) == 100

    # Brute force: enumerate subsets (only for small n)
    def brute(weights, values, W):
        n = len(weights)
        best = 0
        for mask in range(1 << n):
            wt = vt = 0
            for i in range(n):
                if (mask >> i) & 1:
                    wt += weights[i]
                    vt += values[i]
            if wt <= W:
                best = max(best, vt)
        return best

    import random
    random.seed(42)
    for _ in range(200):
        n = random.randint(0, 12)
        weights = [random.randint(1, 20) for _ in range(n)]
        values = [random.randint(1, 50) for _ in range(n)]
        W = random.randint(0, 50)
        expected = brute(weights, values, W)
        assert knapsack_01(weights, values, W) == expected
        assert knapsack_01_2d(weights, values, W) == expected
        v, items = knapsack_01_items(weights, values, W)
        assert v == expected
        assert sum(weights[i] for i in items) <= W
        assert sum(values[i] for i in items) == v

    print("All tests passed!")
