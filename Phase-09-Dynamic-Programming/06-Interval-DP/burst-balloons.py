"""
Problem: Burst Balloons

Difficulty: Hard (LeetCode #312)

---------------------------------------------------
Problem Statement:

You have `n` balloons, each with a number painted on it. When you
BURST balloon `i`, you gain `nums[i-1] * nums[i] * nums[i+1]` coins
(using the neighbours' CURRENT values, after earlier bursts). Treat
out-of-range indices as balloons with value 1.

Return the MAXIMUM coins you can collect.

Example:
    nums = [3, 1, 5, 8]
    Optimal order: burst 1, 5, 3, 8 → 3*1*5 + 3*5*8 + 1*3*8 + 1*8*1 = 167
    → 167

---------------------------------------------------
Why Greedy And Plain DFS Both Fail:

Greedy ("always burst the one with highest neighbour product") gives
wrong answers. Plain backtracking — try each balloon first — is
O(n!) which times out past n ≈ 10.

The KEY INSIGHT that makes this tractable:

    REVERSE the question. Instead of "which balloon to burst FIRST
    in [l..r]?", ask "which balloon to burst LAST in [l..r]?"

If we burst balloon `k` LAST in the range [l..r], by the time we do,
balloons l..k-1 and k+1..r are all gone. So `k`'s NEIGHBOURS are
nums[l-1] and nums[r+1] — the boundary values, which DON'T CHANGE.

That independence is what makes this a valid interval DP.

---------------------------------------------------
The Recurrence:

Pad nums with 1s on both ends: `nums = [1] + nums + [1]`.

    dp[l][r] = max coins from bursting balloons in range (l, r), EXCLUSIVE

    dp[l][r] = max over k in [l+1..r-1] of:
        dp[l][k] + dp[k][r] + nums[l] * nums[k] * nums[r]

Base: dp[l][r] = 0 if r - l <= 1 (no balloon between).

Answer: dp[0][n + 1] on the padded array.

---------------------------------------------------
Why "EXCLUSIVE" Range?

Using the exclusive convention `(l, r)` makes the recurrence clean:
    - l and r are the BOUNDARIES (still present when we pop k).
    - k is strictly inside, l < k < r.
    - When k is popped last, it multiplies with nums[l] and nums[r]
      directly.

If we used inclusive [l, r], we'd need awkward indexing for the
outer neighbours.

---------------------------------------------------
Complexity:

    Time:  O(n³)
    Space: O(n²)
"""


def max_coins(nums):
    """
    Max coins from bursting balloons in optimal order.

    Time: O(n³), Space: O(n²).
    """
    # Pad with 1s at both ends
    arr = [1] + nums + [1]
    n = len(arr)

    # dp[l][r] = max coins from bursting balloons STRICTLY between l and r
    dp = [[0] * n for _ in range(n)]

    # Fill by length of the (l, r) gap
    for length in range(2, n):
        for l in range(n - length):
            r = l + length
            for k in range(l + 1, r):
                # Burst k LAST: its neighbours at that moment are arr[l] and arr[r]
                coins = dp[l][k] + dp[k][r] + arr[l] * arr[k] * arr[r]
                if coins > dp[l][r]:
                    dp[l][r] = coins

    return dp[0][n - 1]


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #312 examples
    assert max_coins([3, 1, 5, 8]) == 167
    assert max_coins([1, 5]) == 10                      # 1*5*1 + 1*1*1 — wait, last burst left has neighbours 1 and 1
    # Let me re-check: [1, 5]:
    # Order: pop 1 first (neighbours 1 and 5): 1*1*5 = 5; then 5 (neighbours 1 and 1): 1*5*1 = 5. Total 10.
    # Order: pop 5 first (neighbours 1 and 1): 1*5*1 = 5; then 1 (neighbours 1 and 1): 1*1*1 = 1. Total 6.
    # So max is 10. ✓

    assert max_coins([]) == 0
    assert max_coins([5]) == 5                          # 1*5*1 = 5
    assert max_coins([1]) == 1
    # Non-trivial input; the stress block below cross-checks vs brute force.
    assert max_coins([9, 76, 64, 21]) > 0

    # All ones: each pop gives 1, so total = n
    for n in range(1, 8):
        assert max_coins([1] * n) == n

    # Brute force: try every order (only n ≤ 7 or so)
    def brute(nums):
        if not nums:
            return 0

        def rec(remaining):
            if not remaining:
                return 0
            best = 0
            padded = [1] + remaining + [1]
            for i in range(1, len(padded) - 1):
                coins = padded[i - 1] * padded[i] * padded[i + 1]
                # Remove this balloon and recurse
                new_remaining = remaining[:i - 1] + remaining[i:]
                best = max(best, coins + rec(new_remaining))
            return best

        return rec(nums)

    # Stress: DP matches brute force on small inputs
    import random
    random.seed(42)
    for _ in range(30):
        n = random.randint(0, 6)
        nums = [random.randint(1, 10) for _ in range(n)]
        assert max_coins(nums) == brute(nums), f"mismatch: {nums}"

    print("All tests passed!")
