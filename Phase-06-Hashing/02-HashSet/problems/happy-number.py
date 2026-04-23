"""
Problem: Happy Number

Difficulty: Easy (LeetCode #202)

---------------------------------------------------
Problem Statement:

A number is HAPPY if you can reach 1 by repeatedly replacing it with
the sum of the squares of its digits. If the process instead enters a
cycle (never reaching 1), the number is not happy.

Return True iff `n` is happy.

Examples:
    n = 19
        1² + 9²                  = 82
        8² + 2²                  = 68
        6² + 8²                  = 100
        1² + 0² + 0²             = 1                 → happy

    n = 2
        2² = 4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4 → ... (cycle)
                                                             → not happy

---------------------------------------------------
Why This Problem Is a HashSet Classic:

The question "does this sequence enter a cycle?" has two canonical
solutions:

    Approach A — HASH SET:  store every number we've seen; if we see one
                            twice, there's a cycle.
                            Time: O(log n) per step (digit extraction),
                                  O(k) total where k = cycle length
                            Space: O(k)

    Approach B — FLOYD'S TORTOISE & HARE:  two pointers, one advancing
                            one step, the other two. They meet inside
                            any cycle.
                            Time: O(k)
                            Space: O(1)

Approach A is easier to write and equally fast in practice — 4 lines
once you have the digit-sum helper. Approach B uses constant extra
memory but requires the cycle-detection insight.

Both are worth knowing — and we show both.

---------------------------------------------------
Key Mathematical Fact:

The digit-square-sum of any number has a known upper bound. For any
`n`, squaring each digit and summing CAN'T exceed ~810 (if n has 10
digits of all 9s: 10 × 81 = 810). So the sequence quickly enters a
SMALL range, which means a cycle — if there is one — must be reached
quickly. Hence the algorithm always terminates.
"""


# =========================================================================
# Helper: digit-square sum
# =========================================================================

def _sum_of_digit_squares(n):
    total = 0
    while n > 0:
        d = n % 10
        total += d * d
        n //= 10
    return total


# =========================================================================
# Solution 1: HashSet (iterative)
# =========================================================================

def is_happy_set(n):
    """
    Walk the sequence. If we revisit a number, there's a cycle — return False.
    If we reach 1, return True.

    Time:  O(k log n) where k is sequence length (small in practice).
    Space: O(k).
    """
    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = _sum_of_digit_squares(n)
    return n == 1


# =========================================================================
# Solution 2: Floyd's Tortoise and Hare (O(1) space)
# =========================================================================

def is_happy_floyd(n):
    """
    Treat the sequence as a "linked list" where next(x) = digit-square-sum(x).
    If 1 is ever produced, next(1) = 1 (self-loop at 1) — so we detect the
    happy case as tortoise == hare == 1.

    Time:  O(k).
    Space: O(1).
    """
    slow = n
    fast = _sum_of_digit_squares(n)
    while fast != 1 and slow != fast:
        slow = _sum_of_digit_squares(slow)
        fast = _sum_of_digit_squares(_sum_of_digit_squares(fast))
    return fast == 1


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # Known happy numbers from OEIS A007770 (up to 100):
    happy_up_to_100 = {
        1, 7, 10, 13, 19, 23, 28, 31, 32, 44, 49, 68, 70, 79,
        82, 86, 91, 94, 97, 100,
    }

    for n in range(1, 101):
        expected = n in happy_up_to_100
        assert is_happy_set(n) == expected, f"set: n={n} expected {expected}"
        assert is_happy_floyd(n) == expected, f"floyd: n={n} expected {expected}"

    # Targeted cases from LC examples
    assert is_happy_set(19) is True
    assert is_happy_set(2) is False

    # Cross-check on random inputs
    import random
    random.seed(42)
    for _ in range(500):
        n = random.randint(1, 10 ** 6)
        assert is_happy_set(n) == is_happy_floyd(n), f"disagreement on n={n}"

    print("All tests passed!")
    print()
    print("Happy numbers from 1 to 100:")
    print(" ", sorted(happy_up_to_100))

    # ---------------------------------------------------------------
    # Why Floyd's Works Even for the Happy Case:
    #
    #   If n is happy, the sequence is ..., 1, 1, 1, 1, ...
    #   — a self-loop at 1. Floyd's algorithm detects cycles in any
    #   "next-function" sequence, so the happy case is just a trivial
    #   cycle of length 1 where slow and fast both land on 1.
    #
    #   If n is UNHAPPY, we enter some cycle that doesn't include 1.
    #   slow and fast meet INSIDE that cycle, not at 1 — so we return
    #   False.
    # ---------------------------------------------------------------
