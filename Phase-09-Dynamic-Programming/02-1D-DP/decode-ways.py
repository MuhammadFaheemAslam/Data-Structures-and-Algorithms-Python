"""
Problem: Decode Ways

Difficulty: Medium (LeetCode #91)

---------------------------------------------------
Problem Statement:

A message of digits is encoded under the mapping:

    'A' → "1"    'B' → "2"   ...   'Z' → "26"

Given a string `s` of digits, return the number of ways to decode it.

Examples:
    "12"     → 2    ("AB" = 1,2  or  "L" = 12)
    "226"    → 3    ("BZ", "VF", "BBF")
    "06"     → 0    (leading zero — 6 alone is fine but 06 isn't a valid code)
    "10"     → 1    ("J")
    "0"      → 0    (no valid decoding)

---------------------------------------------------
The State:

`dp[i]` = number of ways to decode `s[0..i-1]` (first i characters).
Base: `dp[0] = 1` (empty string has ONE decoding — the empty message).

Transition:
    At position i, we just decoded either:
        - ONE char   s[i-1]     (must be '1'..'9')    → dp[i] += dp[i-1]
        - TWO chars  s[i-2..i-1] (must be "10".."26") → dp[i] += dp[i-2]

Edge cases:
    '0' alone can't be decoded.
    "30", "40"..."90" can't be decoded (30+ is out of range AND 0 alone is invalid).
    "10" and "20" are the only "X0" valid decodings.

---------------------------------------------------
Complexity:

    Time:  O(n)
    Space: O(1)     with rolling variables
           O(n)     with the full dp array
"""


# -------- O(1) space, rolling two variables --------

def num_decodings(s):
    """
    Number of ways to decode the digit string `s`.

    Time: O(n), Space: O(1).
    """
    if not s or s[0] == "0":
        return 0

    # dp[0] = 1 (empty), dp[1] = 1 if s[0] != '0' else 0
    prev2, prev1 = 1, 1

    for i in range(2, len(s) + 1):
        cur = 0

        # Single digit s[i-1]
        if s[i - 1] != "0":
            cur += prev1

        # Two digits s[i-2..i-1] — must be "10".."26"
        two_digit = int(s[i - 2:i])
        if 10 <= two_digit <= 26:
            cur += prev2

        prev2, prev1 = prev1, cur

    return prev1


# -------- O(n) tabulation — for comparison / clarity --------

def num_decodings_tab(s):
    """O(n) time, O(n) space. Verbose but easier to step through."""
    n = len(s)
    if n == 0 or s[0] == "0":
        return 0
    dp = [0] * (n + 1)
    dp[0] = 1                                      # empty prefix
    dp[1] = 1                                      # s[0] is already validated non-zero

    for i in range(2, n + 1):
        if s[i - 1] != "0":
            dp[i] += dp[i - 1]
        two_digit = int(s[i - 2:i])
        if 10 <= two_digit <= 26:
            dp[i] += dp[i - 2]

    return dp[n]


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #91 examples
    assert num_decodings("12") == 2
    assert num_decodings("226") == 3
    assert num_decodings("06") == 0
    assert num_decodings("10") == 1
    assert num_decodings("0") == 0
    assert num_decodings("1") == 1
    assert num_decodings("27") == 1                             # only "B,G" (2 + 7)
    assert num_decodings("101") == 1                            # "10","1" = J,A
    assert num_decodings("100") == 0                            # "10","0" invalid
    assert num_decodings("2101") == 1                           # "2","10","1" = B,J,A
    assert num_decodings("2611055971756562") == 4               # random LC stress

    # Empty
    assert num_decodings("") == 0

    # All ones — fib-like
    #   "1"     = 1 way
    #   "11"    = 2 ways
    #   "111"   = 3 ways
    #   "1111"  = 5 ways (fib(5))
    #   "11111" = 8 ways (fib(6))
    fib = [1, 1, 2, 3, 5, 8, 13]
    for k in range(1, 7):
        assert num_decodings("1" * k) == fib[k]

    # Cross-check: rolling vs tabulation
    import random
    random.seed(42)
    for _ in range(500):
        L = random.randint(0, 15)
        s = "".join(random.choice("0123456789") for _ in range(L))
        assert num_decodings(s) == num_decodings_tab(s)

    # Brute-force: enumerate every split
    def brute(s):
        if not s:
            return 1

        def rec(i):
            if i == len(s):
                return 1
            count = 0
            # take 1 digit
            if s[i] != "0":
                count += rec(i + 1)
            # take 2 digits
            if i + 2 <= len(s):
                two = int(s[i:i + 2])
                if 10 <= two <= 26:
                    count += rec(i + 2)
            return count

        if s[0] == "0":
            return 0
        return rec(0)

    for _ in range(200):
        L = random.randint(1, 12)
        s = "".join(random.choice("0123456789") for _ in range(L))
        assert num_decodings(s) == brute(s)

    print("All tests passed!")
