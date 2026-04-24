"""
Problem: Coin Change (min coins)

Difficulty: Medium (LeetCode #322)

---------------------------------------------------
Problem Statement:

Given coin denominations `coins` and a target `amount`, return the
MINIMUM NUMBER OF COINS to make `amount`, or -1 if impossible.
Each coin can be used UNLIMITED times.

Example:
    coins = [1, 2, 5], amount = 11 → 3    (5 + 5 + 1)
    coins = [2], amount = 3 → -1          (can't make 3 from 2s)
    coins = [1], amount = 0 → 0

---------------------------------------------------
Why It's DP:

Greedy fails. With coins [1, 3, 4] and amount 6:
    greedy would pick 4 + 1 + 1 = 3 coins
    optimal is 3 + 3      = 2 coins
So we can't just take the largest coin first. We need to consider
ALL choices at each step.

State: `dp[a]` = min coins to make amount `a`.
Transition: for each coin `c ≤ a`:
    dp[a] = min(dp[a], dp[a - c] + 1)

Base case: dp[0] = 0. Anything else starts at ∞; stays ∞ if unreachable.

---------------------------------------------------
Complexity:

    Time:  O(amount × |coins|)
    Space: O(amount)

---------------------------------------------------
Why Tabulation, Not Memoization?

Both work. Tabulation is preferred here because:
    1. amount can be up to 10^4; memoization recursion could hit Python's limit.
    2. We fill every state anyway (no sparse search space).
    3. The bottom-up order is natural: dp[1], dp[2], ...

Memoized version is still useful when the state space is "sparse" or
the problem has complex pruning.
"""


def coin_change(coins, amount):
    """
    Min coins to make `amount`, or -1 if impossible.

    Time:  O(amount × |coins|)
    Space: O(amount)
    """
    # dp[a] = min coins to make amount a; use amount+1 as "infinity" sentinel
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0

    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1

    return dp[amount] if dp[amount] <= amount else -1


# -------- Memoized (top-down) version for comparison --------

def coin_change_memo(coins, amount):
    """
    Memoized recursion — same Big-O, different style.

    Time:  O(amount × |coins|)
    Space: O(amount) memo + O(amount) recursion
    """
    from functools import cache

    @cache
    def rec(a):
        if a == 0:
            return 0
        if a < 0:
            return float("inf")
        best = float("inf")
        for c in coins:
            best = min(best, rec(a - c) + 1)
        return best

    result = rec(amount)
    return -1 if result == float("inf") else result


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #322 examples
    assert coin_change([1, 2, 5], 11) == 3
    assert coin_change([2], 3) == -1
    assert coin_change([1], 0) == 0
    assert coin_change([1], 1) == 1
    assert coin_change([1], 2) == 2

    # Greedy-fails trap
    assert coin_change([1, 3, 4], 6) == 2                       # two 3s, not 4+1+1

    # Large amounts
    assert coin_change([186, 419, 83, 408], 6249) == 20         # LC stress test

    # Cross-check: memoized must match tabulated
    import random
    random.seed(42)
    for _ in range(200):
        coins = random.sample(range(1, 50), random.randint(1, 5))
        amount = random.randint(0, 200)
        assert coin_change(coins, amount) == coin_change_memo(coins, amount)

    # Brute-force: BFS by number-of-coins level
    def brute(coins, amount):
        """BFS: layer k contains all sums reachable with k coins."""
        if amount == 0:
            return 0
        from collections import deque
        q = deque([(0, 0)])                         # (current sum, coins used)
        visited = {0}
        while q:
            s, k = q.popleft()
            for c in coins:
                ns = s + c
                if ns == amount:
                    return k + 1
                if ns < amount and ns not in visited:
                    visited.add(ns)
                    q.append((ns, k + 1))
        return -1

    for _ in range(50):
        coins = random.sample(range(1, 10), random.randint(1, 4))
        amount = random.randint(0, 30)
        expected = brute(coins, amount)
        assert coin_change(coins, amount) == expected, (
            f"mismatch: coins={coins}, amount={amount}, brute={expected}"
        )

    print("All tests passed!")

    # ---------------------------------------------------------------
    # Alternative BFS Approach:
    #
    #   Since each coin is a unit "step", BFS finds the min number of
    #   steps to reach `amount` — same O(amount × |coins|) time but
    #   often a bit faster in practice since BFS short-circuits as
    #   soon as it reaches the amount. Worth knowing as a variant.
    # ---------------------------------------------------------------
