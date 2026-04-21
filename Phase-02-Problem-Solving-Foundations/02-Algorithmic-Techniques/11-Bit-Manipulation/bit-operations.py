"""
bit-operations.py – Bit Manipulation Reference

A runnable cheat sheet of the common bit-level primitives and idioms.
Every function here is intentionally tiny — most are one-liners. The
point is to put a NAME on each pattern so you recognize it at 2 AM
three weeks from now.

Organization:

    1. Single-bit operations   — get, set, clear, toggle
    2. Popcount                 — four implementations, increasing speed
    3. Low-bit idioms           — n & (n-1), n & -n
    4. Parity and XOR tricks    — pairs cancel, missing number, swap
    5. Bitmask sets             — union, intersect, iterate bits
    6. Subset enumeration       — all subsets, sub-masks of a mask

Run this file to see every primitive in action on a small example.
"""

# =========================================================================
# 1. Single-Bit Operations
# =========================================================================

def get_bit(n, k):
    """Return bit k of n as 0 or 1."""
    return (n >> k) & 1


def set_bit(n, k):
    """Return n with bit k turned on."""
    return n | (1 << k)


def clear_bit(n, k):
    """Return n with bit k turned off."""
    return n & ~(1 << k)


def toggle_bit(n, k):
    """Return n with bit k flipped."""
    return n ^ (1 << k)


# =========================================================================
# 2. Popcount — Four Ways
# =========================================================================

def popcount_naive(n):
    """
    Count set bits by iterating every bit position.

    Time: O(bit length of n)
    """
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count


def popcount_kernighan(n):
    """
    Brian Kernighan's algorithm: drop the lowest set bit each iteration.

    Time: O(number of set bits in n)   — usually faster than naive.
    """
    count = 0
    while n:
        n &= n - 1                      # clear the lowest set bit
        count += 1
    return count


def popcount_bin(n):
    """Most Pythonic — let the language do it."""
    return bin(n).count("1")


def popcount_builtin(n):
    """Python 3.10+. The fastest option on modern Python."""
    return n.bit_count() if hasattr(n, "bit_count") else popcount_bin(n)


# =========================================================================
# 3. Low-Bit Idioms
# =========================================================================

def clear_lowest_set_bit(n):
    """
    Drop the lowest 1 in n. E.g.  0b1010 -> 0b1000.
    """
    return n & (n - 1)


def isolate_lowest_set_bit(n):
    """
    Return the value of the lowest 1 in n (as a value, not a position).
    E.g.  0b1010 -> 0b0010.
    """
    return n & -n


def is_power_of_two(n):
    """
    A power of two has exactly one bit set — so dropping the lowest bit
    yields zero.
    """
    return n > 0 and (n & (n - 1)) == 0


def lowest_set_bit_position(n):
    """
    Position of the lowest set bit (0-indexed). Returns -1 if n is 0.
    """
    if n == 0:
        return -1
    return (n & -n).bit_length() - 1


# =========================================================================
# 4. Parity and XOR Tricks
# =========================================================================

def find_single_when_others_appear_twice(nums):
    """
    Every element appears twice except one; find the single one via XOR.

    XOR's self-inverse property makes pairs cancel.
    Time: O(n). Space: O(1).
    """
    out = 0
    for x in nums:
        out ^= x
    return out


def find_missing_number(nums):
    """
    Given a permutation of [0, n] with one number missing, find the missing one.

    XOR all numbers AND all indices 0..n. Pairs cancel; the missing
    number survives.

    Time: O(n). Space: O(1).
    """
    n = len(nums)
    result = n                           # start with the "last" index (0..n has n+1 numbers)
    for i, x in enumerate(nums):
        result ^= i ^ x
    return result


def has_opposite_sign(a, b):
    """
    True if a and b have opposite signs. Uses the sign bit's XOR.

    (a ^ b) < 0 iff sign bits differ — i.e., one is negative, the other positive.
    """
    return (a ^ b) < 0


# =========================================================================
# 5. Bitmask Set Operations
# =========================================================================

def mask_union(a, b):
    """Set union on small-universe sets represented as bitmasks."""
    return a | b


def mask_intersection(a, b):
    return a & b


def mask_difference(a, b):
    """Set difference A \\ B."""
    return a & ~b


def mask_symmetric_difference(a, b):
    return a ^ b


def mask_contains(mask, k):
    """Is element k in the set mask?"""
    return (mask >> k) & 1 == 1


def iterate_set_bits(mask):
    """Yield each 0-indexed position of a set bit in `mask`."""
    while mask:
        low = mask & -mask               # lowest set bit (as a value)
        yield low.bit_length() - 1
        mask ^= low                      # clear it


# =========================================================================
# 6. Subset Enumeration
# =========================================================================

def all_subsets_as_masks(n):
    """
    Yield each integer in 0 .. 2^n - 1; each encodes one subset of
    the universe {0, 1, ..., n-1}.

    Time: O(2^n)
    """
    yield from range(1 << n)


def enumerate_sub_masks(mask):
    """
    Yield every non-empty subset of the set bits in `mask`, plus the
    mask itself. Standard bitmask-DP trick.

    Time: O(2^k) where k = popcount(mask).

    Does NOT yield 0 (the empty subset). Prepend 0 yourself if you need it.
    """
    sub = mask
    while sub:
        yield sub
        sub = (sub - 1) & mask


# =========================================================================
# Demonstration
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("1. Single-Bit Operations")
    print("=" * 60)
    n = 0b10110           # decimal 22
    print(f"   n = {bin(n)} ({n})")
    print(f"   get_bit(n, 1)    = {get_bit(n, 1)}    (bit 1 is {'set' if get_bit(n, 1) else 'unset'})")
    print(f"   set_bit(n, 0)    = {bin(set_bit(n, 0))}")
    print(f"   clear_bit(n, 2)  = {bin(clear_bit(n, 2))}")
    print(f"   toggle_bit(n, 4) = {bin(toggle_bit(n, 4))}")
    print()

    print("=" * 60)
    print("2. Popcount")
    print("=" * 60)
    for n in [0, 1, 0b1010, 0b11111111, 0xDEADBEEF]:
        naive = popcount_naive(n)
        kern = popcount_kernighan(n)
        b = popcount_bin(n)
        bu = popcount_builtin(n)
        assert naive == kern == b == bu
        print(f"   n = {bin(n):<36}  popcount = {naive}")
    print()

    print("=" * 60)
    print("3. Low-Bit Idioms")
    print("=" * 60)
    for n in [0b1010, 0b1000, 0b1111, 16]:
        print(f"   n = {bin(n):<10}  "
              f"clear_lowest = {bin(clear_lowest_set_bit(n)):<10}  "
              f"isolate_lowest = {bin(isolate_lowest_set_bit(n)):<10}  "
              f"is_pow2 = {is_power_of_two(n)}")
    print()

    print("=" * 60)
    print("4. Parity and XOR Tricks")
    print("=" * 60)
    print(f"   find_single([2,3,4,3,2]) = {find_single_when_others_appear_twice([2, 3, 4, 3, 2])}")
    print(f"   find_missing([3, 0, 1])  = {find_missing_number([3, 0, 1])}")
    print(f"   has_opposite_sign(-3, 7) = {has_opposite_sign(-3, 7)}")
    print(f"   has_opposite_sign(3, 7)  = {has_opposite_sign(3, 7)}")
    print()

    print("=" * 60)
    print("5. Bitmask Sets")
    print("=" * 60)
    a = 0b1010     # {1, 3}
    b = 0b0110     # {1, 2}
    print(f"   a = {bin(a)}  (elements {{1, 3}})")
    print(f"   b = {bin(b)}  (elements {{1, 2}})")
    print(f"   a | b = {bin(mask_union(a, b))}  (union)")
    print(f"   a & b = {bin(mask_intersection(a, b))}  (intersection)")
    print(f"   a & ~b = {bin(mask_difference(a, b) & 0b1111)}  (a \\ b, in 4-bit view)")
    print(f"   a ^ b = {bin(mask_symmetric_difference(a, b))}  (symmetric difference)")
    print(f"   iterate_set_bits(0b10110101) = {list(iterate_set_bits(0b10110101))}")
    print()

    print("=" * 60)
    print("6. Subset Enumeration")
    print("=" * 60)
    print(f"   all_subsets_as_masks(3) = {list(all_subsets_as_masks(3))}")
    mask = 0b1101
    subs = list(enumerate_sub_masks(mask))
    print(f"   enumerate_sub_masks({bin(mask)}) = {[bin(s) for s in subs]}")

    print("\nAll operations demonstrated.")
