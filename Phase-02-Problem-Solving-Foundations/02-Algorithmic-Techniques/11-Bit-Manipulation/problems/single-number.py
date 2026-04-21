"""
Problem: Single Number

Technique: Bit Manipulation — XOR's "pairs cancel" property
Difficulty: Easy (LeetCode #136)

---------------------------------------------------
Problem Statement:

Given a non-empty array of integers `nums`, every element appears
TWICE except for one, which appears ONCE. Find the single one.

Constraints:
    - O(n) time required.
    - O(1) extra space required.    ← rules out hash sets.

---------------------------------------------------
The XOR Lens:

The naive solution uses a Counter or set — O(n) time, O(n) space.
Fine if you ignore the space constraint, but misses the clever trick.

Recall XOR's properties:

    a ^ a == 0           (self-inverse — pairs cancel)
    a ^ 0 == a           (identity)
    XOR is commutative AND associative

So if we XOR every element in nums together, all the paired elements
cancel out, leaving just the single one.

    [4, 1, 2, 1, 2]
       ^ ^ ^ ^ ^
    = 4 ^ 1 ^ 2 ^ 1 ^ 2
    = 4 ^ (1 ^ 1) ^ (2 ^ 2)
    = 4 ^ 0 ^ 0
    = 4                      ✓

One pass, one accumulator, one XOR per element. Beautiful.

Time Complexity:  O(n)
Space Complexity: O(1)

---------------------------------------------------
Variants — Showcased Here:

    Single Number I  (LC #136):   all others appear 2 times        → XOR all
    Single Number II (LC #137):   all others appear 3 times        → bit-by-bit counting
    Single Number III (LC #260):  TWO singles, others appear 2 times → XOR + split by a bit

Each is a nice generalization of the same XOR insight.

---------------------------------------------------
Example:

    nums = [4, 1, 2, 1, 2]
    -> 4

    nums = [2, 2, 1]
    -> 1

---------------------------------------------------
"""

# -------------------------------------------------
# LC #136 — Single Number (Others Appear Twice)
# -------------------------------------------------

def single_number(nums):
    """
    Return the one element that appears exactly once; every other
    element appears exactly twice.

    Time Complexity:  O(n)
    Space Complexity: O(1)
    """
    out = 0
    for x in nums:
        out ^= x
    return out


# -------------------------------------------------
# LC #137 — Single Number II (Others Appear THREE Times)
# -------------------------------------------------

def single_number_ii(nums):
    """
    Every other element appears THREE times. Find the single one.

    XOR alone doesn't help — XORing three copies leaves one copy, not zero.

    Approach: for each bit position, count how many numbers have that
    bit set. If the count is NOT divisible by 3, that bit belongs to
    the single number.

    Time Complexity:  O(32 * n)  = O(n)
    Space Complexity: O(1)
    """
    result = 0
    for bit in range(32):
        count = sum((x >> bit) & 1 for x in nums)
        if count % 3:
            result |= (1 << bit)
    # Handle sign for 32-bit inputs (LC's constraint; Python ints are arbitrary-precision)
    if result >= (1 << 31):
        result -= (1 << 32)
    return result


# -------------------------------------------------
# LC #260 — Single Number III (TWO Singles, Others Appear Twice)
# -------------------------------------------------

def single_number_iii(nums):
    """
    Exactly two elements appear once; every other appears twice.
    Return both in a list (order doesn't matter).

    Approach:

        1. XOR everything → result is (a ^ b), the two singles XORed.
           Because a ≠ b, result has at least one bit set.
        2. Pick any set bit — call it "diff_bit". Exactly one of a, b
           has this bit set; exactly one doesn't.
        3. Partition nums into two groups by diff_bit. Paired elements
           go to the same group (same value → same bit), so each group
           has one of the singles plus an even number of doubles.
        4. XOR each group → recover each single.

    Time Complexity:  O(n)
    Space Complexity: O(1)
    """
    xor_all = 0
    for x in nums:
        xor_all ^= x

    # isolate ANY set bit of xor_all — this bit distinguishes a from b
    diff_bit = xor_all & -xor_all

    a = b = 0
    for x in nums:
        if x & diff_bit:
            a ^= x
        else:
            b ^= x

    return [a, b]


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    # --- LC #136 ---
    print("=" * 60)
    print("Single Number I (LC #136)")
    print("=" * 60)
    cases = [
        ([2, 2, 1],                1),
        ([4, 1, 2, 1, 2],          4),
        ([1],                      1),
        ([7, 7, 5, 3, 5, 3, 9],    9),
        ([-1, -1, -3, -4, -3],    -4),
    ]
    for nums, expected in cases:
        got = single_number(nums)
        assert got == expected, f"{nums} -> {got}, expected {expected}"
        print(f"   single_number({nums}) = {got}")
    print()

    # --- LC #137 ---
    print("=" * 60)
    print("Single Number II (LC #137) — Others Appear Three Times")
    print("=" * 60)
    cases2 = [
        ([2, 2, 3, 2],          3),
        ([0, 1, 0, 1, 0, 1, 99], 99),
        ([5],                    5),
        ([-2, -2, 1, 1, 1, -2, -3], -3),
    ]
    for nums, expected in cases2:
        got = single_number_ii(nums)
        assert got == expected, f"{nums} -> {got}, expected {expected}"
        print(f"   single_number_ii({nums}) = {got}")
    print()

    # --- LC #260 ---
    print("=" * 60)
    print("Single Number III (LC #260) — Two Singles")
    print("=" * 60)
    cases3 = [
        ([1, 2, 1, 3, 2, 5],           [3, 5]),
        ([-1, 0],                       [-1, 0]),
        ([0, 1],                        [0, 1]),
        ([1, 1, 2, 2, 3, 5, 7, 7, 5, 9], [3, 9]),
    ]
    for nums, expected in cases3:
        got = single_number_iii(nums)
        assert sorted(got) == sorted(expected), (
            f"{nums} -> {got}, expected {expected}"
        )
        print(f"   single_number_iii({nums}) = {sorted(got)}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Why XOR Is So Useful Here:
    #
    #   The "cancellation" property makes XOR the natural tool for
    #   "one odd one out" problems. The three variants above escalate
    #   the complexity:
    #
    #     I:   one single,  pairs everywhere  →  XOR all
    #     II:  one single,  triples everywhere →  bit-by-bit mod-3 counts
    #     III: two singles, pairs everywhere   →  XOR + partition by a bit
    #
    #   Each variant generalizes the same core insight: paired structures
    #   cancel under XOR, and bitwise reasoning unlocks the rest.
    # ---------------------------------------------------------------
