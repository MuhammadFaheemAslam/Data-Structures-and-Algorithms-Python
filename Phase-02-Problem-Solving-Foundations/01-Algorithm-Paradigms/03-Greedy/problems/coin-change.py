"""
Problem: Coin Change (Minimum Coins)

Paradigm: Greedy (WHERE IT FAILS) vs Dynamic Programming (WHICH FIXES IT)
Difficulty: Medium (LeetCode #322)

---------------------------------------------------
Problem Statement:

Given coin denominations `coins` and a target amount `amount`, return the
MINIMUM number of coins that sum to `amount`. Each coin may be used any
number of times. Return -1 if no combination sums to `amount`.

---------------------------------------------------
The Greedy Lens — and Why It Is DANGEROUS Here:

The natural greedy approach:

    "Always take the LARGEST coin that doesn't exceed the remaining amount."

This works for SOME coin systems and fails for others:

    - US coins {1, 5, 10, 25}     ← greedy is optimal for any amount
    - EU coins {1, 2, 5, 10, …}   ← greedy is optimal
    - {1, 3, 4}, amount = 6
        - greedy:  4 + 1 + 1  = 3 coins  ← WRONG
        - optimal: 3 + 3      = 2 coins

Why does {1, 3, 4} break greedy? Because committing to the 4 FORCES the
remaining 2 to be made from two 1's. If greedy had "looked ahead" it would
have seen that two 3's beats that. But greedy, by definition, never looks ahead.

This problem is in every DSA curriculum precisely BECAUSE greedy looks right
and quietly produces wrong answers. It's the clearest reminder that greedy
without proof is guesswork.

---------------------------------------------------
The Fix — Dynamic Programming:

Because different choices at one step affect which choices are available
later, we need to try ALL possibilities and keep the best. That's DP.

    dp[i] = minimum coins needed to make amount i
    dp[0] = 0
    dp[i] = min(dp[i - coin] + 1  for each coin where i >= coin)
                                (or ∞ if no coin fits)

This runs in O(amount · len(coins)) time and is provably optimal.

DP is covered properly in Phase-02 / 01 / 04-Dynamic-Programming. We include
a correct DP implementation here to make the comparison concrete.

---------------------------------------------------
Example:

    coins = [1, 3, 4], amount = 6

    greedy   -> 3      (4 + 1 + 1)            ← WRONG
    DP       -> 2      (3 + 3)                ✓

---------------------------------------------------
"""

# -------------------------------------------------
# The Greedy Approach — Only Correct for "Canonical" Coin Systems
# -------------------------------------------------

def coin_change_greedy(coins, amount):
    """
    Always take the largest coin that fits.

    Time Complexity:  O(n log n) – dominated by the sort
    Space Complexity: O(1)

    CAUTION: This is WRONG on non-canonical coin systems. It is included
    here so you can see the exact failure mode on `{1, 3, 4}` with
    amount = 6. Do not ship this for arbitrary denominations.
    """
    if amount == 0:
        return 0

    count = 0
    remaining = amount
    for coin in sorted(coins, reverse=True):
        if coin <= remaining:
            take = remaining // coin
            count += take
            remaining -= coin * take
        if remaining == 0:
            return count

    return -1 if remaining else count


# -------------------------------------------------
# The Correct Approach — Dynamic Programming (Bottom-Up)
# -------------------------------------------------

def coin_change_dp(coins, amount):
    """
    Build up dp[i] = minimum coins needed to make amount `i`.

    Recurrence: dp[i] = min(dp[i - coin] + 1 for coin in coins if coin <= i)
    Base case:  dp[0] = 0

    Time Complexity:  O(amount · len(coins))
    Space Complexity: O(amount)

    This version explores ALL possible choices at each amount, so it can't
    miss the optimal combination the way greedy does.
    """
    if amount < 0:
        return -1

    INF = float("inf")
    dp = [INF] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1

    return dp[amount] if dp[amount] != INF else -1


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    # First, demonstrate the failure mode explicitly
    print("=" * 60)
    print("The Classic Counter-Example: coins={1, 3, 4}, amount=6")
    print("=" * 60)
    coins = [1, 3, 4]
    amount = 6
    g = coin_change_greedy(coins, amount)
    d = coin_change_dp(coins, amount)
    print(f"   greedy -> {g}   (takes 4 + 1 + 1 — WRONG)")
    print(f"   DP     -> {d}   (takes 3 + 3 — optimal)")
    print()

    # Test cases — (coins, amount, expected_optimal)
    test_cases = [
        # Canonical systems where greedy happens to agree with DP
        ([1, 5, 10, 25], 30,  2),               # 25 + 5
        ([1, 5, 10, 25], 41,  4),               # 25 + 10 + 5 + 1
        ([1, 2, 5],      11,  3),               # 5 + 5 + 1
        # Edge cases
        ([1],            0,   0),               # amount 0 — no coins needed
        ([2],            3,   -1),              # impossible
        ([1, 2, 5],      0,   0),
        # Non-canonical — greedy FAILS here, DP still wins
        ([1, 3, 4],      6,   2),               # 3 + 3
        ([1, 3, 4],      8,   2),               # 4 + 4
        # Another non-canonical
        ([3, 5],         11,  3),               # 3 + 3 + 5
    ]

    for i, (coins, amount, expected) in enumerate(test_cases):
        got_dp = coin_change_dp(coins, amount)
        assert got_dp == expected, (
            f"Test {i+1} (DP) failed on coins={coins}, amount={amount}: "
            f"expected {expected}, got {got_dp}"
        )
        print(f"Test {i+1} passed: coins={coins}, amount={amount} -> {expected}")

    # Explicitly catch the cases where greedy disagrees with DP
    print()
    print("Inputs where greedy DISAGREES with DP (greedy is wrong):")
    for coins, amount, _ in test_cases:
        g = coin_change_greedy(coins, amount)
        d = coin_change_dp(coins, amount)
        if g != d:
            print(f"   coins={coins}, amount={amount}: greedy={g}, DP={d}")

    print("\nAll DP tests passed!")

    # ---------------------------------------------------------------
    # The Lesson:
    #
    #   Greedy and DP are *the same family of problems* — both need
    #   optimal substructure. They diverge on whether a single local
    #   rule suffices (greedy) or you must consider all options (DP).
    #
    #   How to tell them apart on a new problem:
    #
    #     1. Try greedy first.
    #     2. Look for a tiny counter-example on a few small inputs.
    #     3. If you can't break greedy AND you can prove the greedy
    #        choice property, ship it.
    #     4. If you can break it — or can't prove it — switch to DP.
    #
    # Coin Change is the clearest reminder of why step 3's PROOF is
    # not optional.
    # ---------------------------------------------------------------
