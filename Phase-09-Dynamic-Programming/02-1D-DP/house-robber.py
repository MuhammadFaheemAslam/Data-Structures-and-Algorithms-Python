"""
Problem: House Robber (I and II)

Difficulty:
    Medium (LeetCode #198 — houses in a row)
    Medium (LeetCode #213 — houses in a circle)

---------------------------------------------------
Problem Statement:

You are a thief and houses are in a line, each with some amount of
cash. You cannot rob two adjacent houses (the police are called).
Maximize the total amount robbed.

    LC #198: houses in a line.
    LC #213: houses in a circle — first and last are adjacent.

---------------------------------------------------
LC #198 — The Classic:

At house i, you either:
    - ROB it: gain houses[i] + dp[i-2]  (can't rob i-1)
    - SKIP it: carry forward dp[i-1]

    dp[i] = max(dp[i-1], houses[i] + dp[i-2])

Base cases: dp[-1] = 0, dp[0] = houses[0].

Only the last two values matter → O(1) space with two rolling variables.

---------------------------------------------------
LC #213 — The Circular Trick:

First and last are now adjacent, so at most one of them is robbed.

SPLIT into two runs of the linear version:
    a. rob houses[0..n-2]     — can include house 0, not last
    b. rob houses[1..n-1]     — can include last, not house 0

Answer = max(a, b). Both sub-problems are LC #198.

Why does this work?
    An optimal circular solution either INCLUDES house 0 or DOESN'T.
    If it includes house 0, it can't include house n-1 → sub-problem (a).
    If it excludes house 0, we're free to consider houses 1..n-1 → sub-problem (b).
    One of these IS optimal.

---------------------------------------------------
Complexity:

    Time:  O(n)
    Space: O(1)
"""


# -------- LC #198: linear --------

def rob_linear(houses):
    """
    Max rob from a LINE of houses.

    Time: O(n), Space: O(1).
    """
    prev2, prev1 = 0, 0                            # dp[i-2], dp[i-1]
    for h in houses:
        prev2, prev1 = prev1, max(prev1, prev2 + h)
    return prev1


# -------- LC #213: circular --------

def rob_circular(houses):
    """
    Max rob from a CIRCLE of houses (first and last are adjacent).

    Time: O(n), Space: O(1).
    """
    n = len(houses)
    if n == 0:
        return 0
    if n == 1:
        return houses[0]
    # Run linear rob twice on the two subarrays:
    #   houses[:-1] — excludes last house
    #   houses[1:]  — excludes first house
    return max(rob_linear(houses[:-1]), rob_linear(houses[1:]))


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #198 examples
    assert rob_linear([1, 2, 3, 1]) == 4                        # rob 1 and 3
    assert rob_linear([2, 7, 9, 3, 1]) == 12                    # rob 2, 9, 1
    assert rob_linear([]) == 0
    assert rob_linear([5]) == 5
    assert rob_linear([2, 1]) == 2
    assert rob_linear([1, 2]) == 2
    assert rob_linear([0, 0, 0]) == 0

    # LC #213 examples
    assert rob_circular([2, 3, 2]) == 3                         # can't rob both ends (value 2)
    assert rob_circular([1, 2, 3, 1]) == 4                      # same as linear since 1 < 4 already
    assert rob_circular([1, 2, 3]) == 3
    assert rob_circular([]) == 0
    assert rob_circular([5]) == 5
    assert rob_circular([2, 1]) == 2

    # Brute-force: enumerate every subset where no two adjacent are chosen
    def brute_linear(houses):
        n = len(houses)
        best = 0
        for mask in range(1 << n):
            # Check no two adjacent bits set
            valid = True
            for i in range(n - 1):
                if (mask >> i) & 1 and (mask >> (i + 1)) & 1:
                    valid = False
                    break
            if not valid:
                continue
            total = sum(houses[i] for i in range(n) if (mask >> i) & 1)
            best = max(best, total)
        return best

    def brute_circular(houses):
        n = len(houses)
        if n == 0:
            return 0
        if n == 1:
            return houses[0]
        best = 0
        for mask in range(1 << n):
            valid = True
            for i in range(n - 1):
                if (mask >> i) & 1 and (mask >> (i + 1)) & 1:
                    valid = False
                    break
            # Circular: first and last are adjacent too
            if (mask >> 0) & 1 and (mask >> (n - 1)) & 1:
                valid = False
            if not valid:
                continue
            total = sum(houses[i] for i in range(n) if (mask >> i) & 1)
            best = max(best, total)
        return best

    # Stress: linear and circular match brute force on small inputs
    import random
    random.seed(42)
    for _ in range(200):
        n = random.randint(0, 12)
        houses = [random.randint(0, 50) for _ in range(n)]
        assert rob_linear(houses) == brute_linear(houses), f"linear({houses})"
        assert rob_circular(houses) == brute_circular(houses), f"circular({houses})"

    print("All tests passed!")
