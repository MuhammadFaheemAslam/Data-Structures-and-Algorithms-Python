"""
Problem: Coin Change II (count combinations)

Difficulty: Medium (LeetCode #518)

---------------------------------------------------
Problem Statement:

Given coin denominations `coins` and target `amount`, return the
NUMBER OF DISTINCT COMBINATIONS that sum to `amount`. Each coin can
be used UNLIMITED times. Ordering doesn't matter — {1,1,2} and
{1,2,1} are the same combination.

Example:
    amount = 5, coins = [1, 2, 5] → 4
    Combinations:
        5
        2 + 2 + 1
        2 + 1 + 1 + 1
        1 + 1 + 1 + 1 + 1

---------------------------------------------------
The Counting Trap:

If you loop "amount outside, coins inside", you count PERMUTATIONS,
not COMBINATIONS:

    for a in 1..amount:
        for c in coins:
            dp[a] += dp[a - c]       # WRONG for combinations

With coins=[1,2] and amount=3 this gives:
    dp[3] = dp[2] + dp[1] = 2 + 1 = 3     but only {1,1,1} and {1,2} exist = 2

The fix: put COINS OUTER, AMOUNT INNER. This enforces "use each coin
type in the order they appear", eliminating permutations of the same
combination.

    for c in coins:
        for a in c..amount:
            dp[a] += dp[a - c]       # CORRECT for combinations

Subtle, important, frequently trips people up. The order of loops
IS the algorithm here.

---------------------------------------------------
Complexity:

    Time:  O(amount × |coins|)
    Space: O(amount)
"""


def count_combinations(amount, coins):
    """
    Number of distinct combinations of coins that sum to amount.

    Time:  O(amount × |coins|).
    Space: O(amount).
    """
    dp = [0] * (amount + 1)
    dp[0] = 1                                      # one way to make 0 (empty combo)

    for c in coins:
        for a in range(c, amount + 1):
            dp[a] += dp[a - c]

    return dp[amount]


# -------- "What not to do" — permutations version --------

def count_permutations(amount, coins):
    """
    NUMBER OF ORDERED SEQUENCES of coins summing to amount (permutations).
    Included here to contrast with the combinations version.

    This is the LC #377 "Combination Sum IV" problem, despite its name.

    Time:  O(amount × |coins|).
    """
    dp = [0] * (amount + 1)
    dp[0] = 1
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] += dp[a - c]
    return dp[amount]


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #518 examples
    assert count_combinations(5, [1, 2, 5]) == 4
    assert count_combinations(3, [2]) == 0                     # can't make 3 from 2s
    assert count_combinations(10, [10]) == 1
    assert count_combinations(0, [1, 2, 3]) == 1               # one way — empty

    # Edge cases
    assert count_combinations(0, []) == 1                       # empty combo is the only way
    assert count_combinations(5, []) == 0                       # no coins, can't make 5

    # Demonstrate the permutations vs combinations distinction
    #   amount=3, coins=[1, 2]
    #   Combinations: {1,1,1}, {1,2} → 2
    #   Permutations: 1+1+1, 1+2, 2+1 → 3
    assert count_combinations(3, [1, 2]) == 2
    assert count_permutations(3, [1, 2]) == 3

    # Brute force for combinations: enumerate every multiset
    def brute_combinations(amount, coins):
        """Count multisets of coins summing to amount."""
        if amount == 0:
            return 1
        if not coins or amount < 0:
            return 0
        count = 0
        c0 = coins[0]
        # Take 0, 1, 2, ... of c0
        k = 0
        while k * c0 <= amount:
            count += brute_combinations(amount - k * c0, coins[1:])
            k += 1
        return count

    # Stress: fast vs brute
    import random
    random.seed(42)
    for _ in range(100):
        amount = random.randint(0, 25)
        coins = random.sample(range(1, 10), random.randint(0, 4))
        assert count_combinations(amount, coins) == brute_combinations(amount, coins), (
            f"mismatch: amount={amount}, coins={coins}"
        )

    print("All tests passed!")

    # ---------------------------------------------------------------
    # The Loop Order Takeaway:
    #
    #   Coins OUTER, amount INNER  → COMBINATIONS (unordered).
    #   Amount OUTER, coins INNER  → PERMUTATIONS (ordered sequences).
    #
    # Same recurrence `dp[a] += dp[a-c]`; the LOOP NESTING determines
    # whether ordering matters. This subtle distinction appears in
    # many "count ways" DP problems — always ask yourself which
    # version the problem wants.
    # ---------------------------------------------------------------
