"""
Problem: Best Time to Buy and Sell Stock — Unified Family

Difficulty:
    Easy   (LeetCode #121 — at most ONE transaction)
    Medium (LeetCode #122 — unlimited transactions)
    Medium (LeetCode #309 — unlimited + 1-day cooldown after sell)
    Medium (LeetCode #714 — unlimited with a per-transaction fee)
    Hard   (LeetCode #188 — at most K transactions)

---------------------------------------------------
The Unifying Framework — State-Machine DP:

Every stock problem in this family can be modelled as a small finite
state machine. The state represents "what position am I in RIGHT NOW
at this moment in time?":

    Common states:
        FREE      — not holding a share, free to buy
        HOLD      — holding a share, will need to sell
        COOLDOWN  — just sold, can't buy today (LC #309 only)

Transitions move you between states over days; each transition has a
"money change" (buy = -price, sell = +price, hold/free = 0).

The recurrence:

    dp[i][state] = max money you have on day i while in this state

    dp[i][HOLD] = max(
        dp[i-1][HOLD],                          # keep holding
        dp[i-1][FREE] - price[i]                # buy today
    )
    dp[i][FREE] = max(
        dp[i-1][FREE],                          # keep idle
        dp[i-1][HOLD] + price[i]                # sell today (LC #122)
    )

Variants TWEAK the transitions:

    LC #121:  You can only buy ONCE. State dp[i][FREE] doesn't come
              from selling; track "min price seen so far" instead.

    LC #309:  After selling, you must skip a day. Add a COOLDOWN
              state; selling goes to COOLDOWN, not FREE.

    LC #714:  Each sell deducts a fee. Modify the sell transition:
              dp[i][FREE] = dp[i-1][HOLD] + price[i] - fee.

    LC #188:  Track NUMBER OF TRANSACTIONS COMPLETED. Add a k
              dimension: dp[i][k][state]. For large K → reduces to
              LC #122 (since unlimited already).

---------------------------------------------------
Why State-Machine DP Generalizes So Well:

Once you see that every "with cooldown", "with fee", "with limit"
variant is just the same state machine + one tweaked transition, you
stop memorizing algorithms and start DESIGNING them. The same
technique solves:
    - "Max profit with cooldown and fee" — combine both tweaks.
    - "Must wait N days, pay fee F" — cooldown + fee, parameterized.
    - "Can only buy on even-numbered days" — gate the buy transition.

---------------------------------------------------
Complexity:

    LC #121/#122/#309/#714: Time O(n), Space O(1) (rolling two scalars).
    LC #188 (at most K trans): Time O(nK), Space O(K).
"""


# -------- LC #121: at most ONE transaction --------

def max_profit_one(prices):
    """
    Single buy-then-sell. Equivalent to "max (prices[j] - prices[i]) for j > i".

    Time: O(n), Space: O(1).
    """
    if not prices:
        return 0
    min_price = prices[0]
    best = 0
    for p in prices[1:]:
        best = max(best, p - min_price)
        min_price = min(min_price, p)
    return best


# -------- LC #122: unlimited transactions --------

def max_profit_many(prices):
    """
    Sum every upward slope — buy at every local min, sell at every local max.

    Equivalently: on the state-machine framework, FREE and HOLD freely
    exchange. The greedy "sum of positive deltas" is the same answer.

    Time: O(n), Space: O(1).
    """
    profit = 0
    for i in range(1, len(prices)):
        if prices[i] > prices[i - 1]:
            profit += prices[i] - prices[i - 1]
    return profit


# -------- LC #309: unlimited + 1-day cooldown after sell --------

def max_profit_cooldown(prices):
    """
    Three-state machine: HOLD, FREE, COOLDOWN.

    Transitions:
        HOLD    = max(HOLD_prev, FREE_prev - price)      (buy or stay holding)
        COOL    = HOLD_prev + price                      (sell today)
        FREE    = max(FREE_prev, COOL_prev)              (idle or yesterday's cooldown expired)

    Time: O(n), Space: O(1).
    """
    if not prices:
        return 0
    hold = -prices[0]
    cool = float("-inf")
    free = 0
    for i in range(1, len(prices)):
        new_hold = max(hold, free - prices[i])
        new_cool = hold + prices[i]
        new_free = max(free, cool)
        hold, cool, free = new_hold, new_cool, new_free
    # At the end we want NOT holding — max over free/cool
    return max(free, cool, 0)


# -------- LC #714: unlimited with per-transaction fee --------

def max_profit_fee(prices, fee):
    """
    Same state machine as LC #122, with `fee` deducted on every sell.

    Time: O(n), Space: O(1).
    """
    if not prices:
        return 0
    hold = -prices[0]
    free = 0
    for i in range(1, len(prices)):
        hold, free = max(hold, free - prices[i]), max(free, hold + prices[i] - fee)
    return free


# -------- LC #188: at most K transactions --------

def max_profit_k(prices, k):
    """
    Two-dimensional DP: dp[j][state] where j = completed transactions.

    If k >= n/2, unlimited transactions is already optimal → LC #122.

    Time: O(n·k), Space: O(k).
    """
    n = len(prices)
    if n < 2 or k == 0:
        return 0
    if k >= n // 2:
        return max_profit_many(prices)

    # hold[j] = max cash if holding a share AFTER j-th buy
    # free[j] = max cash if free AFTER j-th sell
    # Initialize: no transaction yet → hold[0] would need a buy; skip
    INF = float("-inf")
    hold = [INF] * (k + 1)
    free = [0] * (k + 1)

    for p in prices:
        for j in range(1, k + 1):
            hold[j] = max(hold[j], free[j - 1] - p)           # buy for the j-th time
            free[j] = max(free[j], hold[j] + p)               # sell for the j-th time

    return max(free)


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #121
    assert max_profit_one([7, 1, 5, 3, 6, 4]) == 5                # buy 1, sell 6
    assert max_profit_one([7, 6, 4, 3, 1]) == 0                   # monotone down
    assert max_profit_one([]) == 0
    assert max_profit_one([5]) == 0

    # LC #122
    assert max_profit_many([7, 1, 5, 3, 6, 4]) == 7               # (5-1) + (6-3)
    assert max_profit_many([1, 2, 3, 4, 5]) == 4
    assert max_profit_many([7, 6, 4, 3, 1]) == 0

    # LC #309
    assert max_profit_cooldown([1, 2, 3, 0, 2]) == 3              # buy 1 sell 3; buy 0 sell 2
    assert max_profit_cooldown([1]) == 0
    assert max_profit_cooldown([]) == 0

    # LC #714
    assert max_profit_fee([1, 3, 2, 8, 4, 9], 2) == 8             # (8-1-2) + (9-4-2) = 5+3
    assert max_profit_fee([1, 3, 7, 5, 10, 3], 3) == 6

    # LC #188
    assert max_profit_k([2, 4, 1], 2) == 2                        # one transaction 2→4
    assert max_profit_k([3, 2, 6, 5, 0, 3], 2) == 7               # (6-2) + (3-0)
    assert max_profit_k([1, 2, 3, 4, 5], 100) == 4                # k >> n/2 → LC #122

    # Unification sanity check: k=1 and k=∞
    prices = [3, 2, 6, 5, 0, 3]
    assert max_profit_k(prices, 1) == max_profit_one(prices)
    assert max_profit_k(prices, len(prices)) == max_profit_many(prices)

    # Brute force for LC #309 cooldown
    def brute_cooldown(prices):
        n = len(prices)
        best = [0]
        # state 0 = free, 1 = holding, 2 = cooldown
        def rec(i, state, cash):
            if i == n:
                best[0] = max(best[0], cash)
                return
            if state == 0:                                   # free: can buy or idle
                rec(i + 1, 1, cash - prices[i])
                rec(i + 1, 0, cash)
            elif state == 1:                                 # holding: can sell or hold
                rec(i + 1, 2, cash + prices[i])
                rec(i + 1, 1, cash)
            else:                                            # cooldown: must become free
                rec(i + 1, 0, cash)
        rec(0, 0, 0)
        return best[0]

    import random
    random.seed(42)
    for _ in range(50):
        n = random.randint(0, 8)
        prices = [random.randint(0, 10) for _ in range(n)]
        assert max_profit_cooldown(prices) == brute_cooldown(prices), (
            f"cooldown mismatch on {prices}"
        )

    # Brute force for LC #714 fee
    def brute_fee(prices, fee):
        n = len(prices)
        best = [0]
        def rec(i, holding, cash):
            if i == n:
                best[0] = max(best[0], cash)
                return
            if holding:
                rec(i + 1, False, cash + prices[i] - fee)   # sell
                rec(i + 1, True, cash)                       # hold
            else:
                rec(i + 1, True, cash - prices[i])           # buy
                rec(i + 1, False, cash)                      # idle
        rec(0, False, 0)
        return best[0]

    for _ in range(50):
        n = random.randint(0, 7)
        prices = [random.randint(0, 10) for _ in range(n)]
        fee = random.randint(0, 5)
        assert max_profit_fee(prices, fee) == brute_fee(prices, fee)

    print("All tests passed!")
