"""
Problem: Climbing Stairs

Difficulty: Easy (LeetCode #70)

---------------------------------------------------
Problem Statement:

You're climbing a staircase of `n` steps. Each move you can take
either 1 step or 2 steps. How many distinct ways can you climb to
the top?

Example:
    n = 2 → 2    (1+1, or 2)
    n = 3 → 3    (1+1+1, 1+2, 2+1)
    n = 5 → 8

---------------------------------------------------
Why It's Fibonacci:

To reach step n, the LAST move was either:
    - a 1-step (from step n-1), contributing dp[n-1] ways
    - a 2-step (from step n-2), contributing dp[n-2] ways

    dp[n] = dp[n-1] + dp[n-2]

Base cases: dp[0] = 1 (one way — do nothing), dp[1] = 1 (one way — one 1-step).

This is literally the Fibonacci recurrence with a different offset:
    dp[0]=1, dp[1]=1, dp[2]=2, dp[3]=3, dp[4]=5, dp[5]=8 …

---------------------------------------------------
Complexity:

    Time:  O(n)
    Space: O(1)     with rolling variables
           O(n)     with the full dp array
"""


# -------- O(1) space — rolling two variables --------

def climb_stairs(n):
    """
    Count the number of distinct ways to climb `n` stairs taking 1 or 2 at a time.

    Time: O(n), Space: O(1).
    """
    if n <= 2:
        return n
    a, b = 1, 2                                     # a = ways(i-2), b = ways(i-1)
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b


# -------- O(n) space — for comparison with the array-based tabulation --------

def climb_stairs_tab(n):
    """
    Tabulated with a full dp array. O(n) time, O(n) space.
    """
    if n <= 2:
        return n
    dp = [0] * (n + 1)
    dp[1], dp[2] = 1, 2
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]


# -------- Generalization: steps of size 1, 2, ..., k --------
#
# Natural follow-up: what if you can take 1, 2, ..., or k steps at a time?
#
#     dp[n] = dp[n-1] + dp[n-2] + ... + dp[n-k]
#
# O(nk) time, O(n) space. Or O(n) time with a rolling sliding-window sum.

def climb_stairs_k(n, k):
    """
    Ways to climb n stairs taking 1..k steps at a time.

    Time: O(n) using a rolling window sum, Space: O(k).
    """
    if n == 0:
        return 1
    if k < 1:
        return 0
    dp = [0] * (n + 1)
    dp[0] = 1
    window = 0                                     # rolling sum of last k dp values
    for i in range(1, n + 1):
        window += dp[i - 1]
        if i - 1 - k >= 0:
            window -= dp[i - 1 - k]
        dp[i] = window
    return dp[n]


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #70 examples
    assert climb_stairs(2) == 2
    assert climb_stairs(3) == 3
    assert climb_stairs(5) == 8

    # Match Fibonacci: climb_stairs(n) == fib(n + 1)
    fib_values = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]  # fib(1..11)
    for n in range(1, 11):
        assert climb_stairs(n) == fib_values[n]
        assert climb_stairs_tab(n) == fib_values[n]

    # Edge cases
    assert climb_stairs(0) == 0
    assert climb_stairs(1) == 1

    # climb_stairs_k(n, 2) is the same as the classic problem
    for n in range(0, 12):
        assert climb_stairs_k(n, 2) == (climb_stairs(n) if n >= 1 else 1)
    # Note: climb_stairs(0) returns 0 by our convention; k-variant returns 1
    # (one "empty" way). Both interpretations are common.

    # k = 1: only one way
    for n in range(0, 10):
        assert climb_stairs_k(n, 1) == 1

    # k = n: 2^(n-1) ways (every "take k" subset that sums to n)
    # For n=4, k=4: [1,1,1,1], [1,1,2], [1,2,1], [2,1,1], [2,2], [1,3], [3,1], [4]
    # That's 8 = 2^3.
    for n in range(1, 10):
        assert climb_stairs_k(n, n) == 2 ** (n - 1)

    # Correctness: O(1) space version matches O(n) tabulation on all inputs
    for n in range(0, 50):
        assert climb_stairs(n) == climb_stairs_tab(n)

    print("All tests passed!")
