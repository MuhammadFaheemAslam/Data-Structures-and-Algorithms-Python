"""
Unbounded Knapsack — Each Item Can Be Taken Unlimited Times

Given `n` item types with weights `w[i]` and values `v[i]` and a
capacity W, pick items (each reusable) to maximize total value
subject to total weight ≤ W.

---------------------------------------------------
The State And Transition:

    dp[c] = max value achievable with capacity c, items reusable

    for c = 1..W:
        for each item i:
            if w[i] <= c:
                dp[c] = max(dp[c], dp[c - w[i]] + v[i])

---------------------------------------------------
vs 0/1 Knapsack — Loop Direction:

In the 1D implementation of 0/1 knapsack, we iterated capacity
BACKWARDS to prevent re-using an item. Here we iterate FORWARD —
that "reuse" is exactly what we want.

    for item in items:
        for c in w[i]..W:        # FORWARD to reuse
            dp[c] = max(dp[c], dp[c - w_i] + v_i)

---------------------------------------------------
The Loop-Order Relation To LC #322 / #518:

LC #322 coin change (min coins) and LC #518 coin change II (count
combinations) are unbounded-knapsack variants:

    LC #322:    dp[c] = min over coins of (dp[c - coin] + 1)
    LC #518:    dp[c] = sum over coins of dp[c - coin], coins OUTER, c INNER
                (outer order enforces combinations-not-permutations)

Both covered in phase 02 (02-1D-DP/coin-change.py, coin-change-ii.py).

---------------------------------------------------
Complexity:

    Time:  O(n · W)
    Space: O(W)
"""


def unbounded_knapsack(weights, values, W):
    """
    Max value with reusable items and capacity W.

    Time: O(n · W), Space: O(W).
    """
    dp = [0] * (W + 1)
    for i in range(len(weights)):
        w_i, v_i = weights[i], values[i]
        for c in range(w_i, W + 1):                         # FORWARD — allows reuse
            if dp[c - w_i] + v_i > dp[c]:
                dp[c] = dp[c - w_i] + v_i
    return dp[W]


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Classic example
    # items: (w=2,v=3), (w=3,v=4), (w=4,v=5)
    # capacity: 7
    # Unbounded optimal: take item 0 three times (weight 6, value 9) + ??? No, 2+2+3=7, values 3+3+4=10.
    # Or 2 * 2 + 3 = 7, values 3*2 + 4 = 10. Or 2*3 + 0 = 6 value 9. Or 3+4=7 value 9.
    # So max = 10.
    weights = [2, 3, 4]
    values = [3, 4, 5]
    assert unbounded_knapsack(weights, values, 7) == 10

    # Degenerate
    assert unbounded_knapsack([], [], 10) == 0
    assert unbounded_knapsack([5], [10], 0) == 0
    assert unbounded_knapsack([5], [10], 4) == 0                    # can't fit any
    assert unbounded_knapsack([5], [10], 25) == 50                  # 5 copies

    # Single item, multiple taken
    assert unbounded_knapsack([1], [2], 10) == 20                   # 10 copies, value 2 each
    assert unbounded_knapsack([2], [5], 11) == 25                   # floor(11/2) = 5 copies

    # Prefer many cheap items over one big valuable one if they pack better
    assert unbounded_knapsack([1, 10], [1, 9], 20) == 20            # 20 copies of item 0

    # Brute force: try EVERY count of each item
    def brute(weights, values, W):
        n = len(weights)
        best = [0]

        def rec(i, remaining, val):
            if i == n:
                best[0] = max(best[0], val)
                return
            k = 0
            while k * weights[i] <= remaining:
                rec(i + 1, remaining - k * weights[i], val + k * values[i])
                k += 1

        if n > 0:
            rec(0, W, 0)
        return best[0]

    import random
    random.seed(42)
    for _ in range(200):
        n = random.randint(0, 6)
        weights = [random.randint(1, 10) for _ in range(n)]
        values = [random.randint(1, 20) for _ in range(n)]
        W = random.randint(0, 30)
        expected = brute(weights, values, W)
        got = unbounded_knapsack(weights, values, W)
        assert got == expected, f"mismatch: w={weights}, v={values}, W={W}: got {got}, want {expected}"

    print("All tests passed!")
