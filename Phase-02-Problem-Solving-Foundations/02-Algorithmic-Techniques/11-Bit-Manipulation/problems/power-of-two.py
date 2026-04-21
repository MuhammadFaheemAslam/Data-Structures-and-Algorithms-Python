"""
Problem: Power of Two

Technique: Bit Manipulation — the `n & (n-1)` idiom
Difficulty: Easy (LeetCode #231)

---------------------------------------------------
Problem Statement:

Given an integer `n`, return True if it is a power of two (i.e., there
exists some integer x such that n == 2^x). Otherwise return False.

    1   is 2^0 → True
    16  is 2^4 → True
    3   = 2 + 1 → False
    0   → False    (there is no x with 2^x == 0)
    -16 → False    (negatives are not powers of two)

---------------------------------------------------
The Bit-Manipulation Lens:

A number is a power of two iff its binary representation has exactly
ONE set bit:

    1    = 0b0001 ← one set bit ✓
    2    = 0b0010 ← one set bit ✓
    4    = 0b0100 ← one set bit ✓
    8    = 0b1000 ← one set bit ✓
    16   = 0b10000 ← one set bit ✓

    3    = 0b0011 ← two set bits ✗
    12   = 0b1100 ← two set bits ✗

So "is power of two" == "exactly one set bit" == "popcount == 1".

There are several ways to test this. The most elegant:

    n > 0 and (n & (n - 1)) == 0

Why? For any positive `n`, subtracting 1:

    - flips the lowest set bit to 0
    - flips all bits below it to 1

    n     = 0b...X100        (some bits, then 1, then zeros)
    n - 1 = 0b...X011

ANDing `n` with `n - 1` clears the lowest set bit. If `n` had ONLY
that one bit set, the result is 0.

    n = 8   = 0b1000
    n-1 = 7 = 0b0111
    n & (n-1) = 0b0000 → 0 ✓

    n = 12  = 0b1100
    n-1 = 11= 0b1011
    n & (n-1) = 0b1000 → nonzero ✗

The guard `n > 0` is necessary because 0 would pass the bit test
vacuously (0 & -1 = 0), but 0 is not 2^anything.

---------------------------------------------------
Time Complexity:  O(1)
Space Complexity: O(1)

Compare to the "divide by 2 until 1" approach: that's O(log n) and
involves a loop. The bit trick is a single comparison.

---------------------------------------------------
"""

# -------------------------------------------------
# Approach 1: n & (n - 1)  (THE Answer)
# -------------------------------------------------

def is_power_of_two(n):
    """
    Return True iff n is a power of two (1, 2, 4, 8, …).

    Time Complexity:  O(1)
    Space Complexity: O(1)
    """
    return n > 0 and (n & (n - 1)) == 0


# -------------------------------------------------
# Approach 2: n & -n (Isolate Lowest Set Bit)
# -------------------------------------------------

def is_power_of_two_lowbit(n):
    """
    Alternative: the lowest set bit IS n iff exactly one bit is set.

    `n & -n` isolates the lowest set bit (as a value). For a power of
    two, that lowest set bit equals n itself.

    Time Complexity:  O(1)
    Space Complexity: O(1)
    """
    return n > 0 and (n & -n) == n


# -------------------------------------------------
# Approach 3: Popcount == 1
# -------------------------------------------------

def is_power_of_two_popcount(n):
    """
    Count set bits; power of two iff exactly one.

    Time Complexity:  O(1) in Python 3.10+ (uses .bit_count())
                      O(bit length of n) otherwise
    Space Complexity: O(1)
    """
    if n <= 0:
        return False
    return bin(n).count("1") == 1


# -------------------------------------------------
# Approach 4: Divide-by-2 Loop (For Contrast)
# -------------------------------------------------

def is_power_of_two_loop(n):
    """
    Classical approach — keep dividing by 2 while even; succeed iff we end at 1.

    Time Complexity:  O(log n)
    Space Complexity: O(1)

    Works, but O(log n) is strictly worse than the bit tricks' O(1).
    """
    if n <= 0:
        return False
    while n % 2 == 0:
        n //= 2
    return n == 1


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    # Test cases — (n, expected)
    test_cases = [
        (1,             True),           # 2^0
        (2,             True),
        (4,             True),
        (8,             True),
        (16,            True),
        (1024,          True),           # 2^10
        (1 << 30,       True),
        (0,             False),          # zero is not a power of 2
        (-1,            False),          # negatives are not powers of 2
        (-16,           False),
        (3,             False),
        (6,             False),
        (15,            False),
        (1023,          False),          # 2^10 - 1
        (12345,         False),
        (1 << 30 | 1,   False),          # 2^30 + 1
    ]

    for i, (n, expected) in enumerate(test_cases):
        for fn in (
            is_power_of_two,
            is_power_of_two_lowbit,
            is_power_of_two_popcount,
            is_power_of_two_loop,
        ):
            got = fn(n)
            assert got == expected, (
                f"Test {i+1} ({fn.__name__}) failed on n={n}: "
                f"expected {expected}, got {got}"
            )
        print(f"Test {i+1} passed: n={n:<15} -> {expected}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Pattern Family:
    #
    #   Related "one-bit" queries all use variations of the same trick:
    #
    #     is power of 2          n > 0 and (n & (n - 1)) == 0
    #     is power of 4          n > 0 and (n & (n - 1)) == 0 and n % 3 == 1
    #                            (4^k mod 3 == 1, but 2^(odd k) mod 3 == 2)
    #     popcount               Brian Kernighan's n & (n-1) loop
    #     lowest set bit         n & -n
    #     next larger perm       "Gosper's hack" — beyond this module
    #
    #   Each of these is a one-line incantation with O(1) cost once
    #   you've seen it. They don't teach themselves; you have to
    #   memorize them. But there aren't many, and they're all useful.
    # ---------------------------------------------------------------
