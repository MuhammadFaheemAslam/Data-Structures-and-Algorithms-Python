"""
Problem: Integer Square Root

Technique: Binary Search on the Answer Space
Difficulty: Easy (LeetCode #69)

---------------------------------------------------
Problem Statement:

Given a non-negative integer `x`, compute and return the INTEGER
square root of `x` — that is, the largest integer `r` such that
`r * r <= x`.

Must NOT use any built-in exponentiation or sqrt function.

    sqrt(0)   = 0
    sqrt(4)   = 2
    sqrt(8)   = 2           (truncated; the real sqrt is ~2.83)
    sqrt(16)  = 4
    sqrt(100) = 10

---------------------------------------------------
The Binary-Search Lens:

Brute force: try r = 0, 1, 2, ... until r*r > x. O(sqrt(x)) time.
Works but slow on big x.

Binary search: the answer lies in [0, x]. We seek the LARGEST r with
r*r <= x. This is a MAXIMUM-FEASIBLE search (see Phase-02 / 02 /
05-Binary-Search-on-Answer):

    candidate:  r
    predicate:  r * r <= x    (monotonically True on the left, False right)

We want the RIGHTMOST r where the predicate is True. That's the "max
feasible" binary-search template:

    lo, hi = 0, x
    while lo < hi:
        mid = (lo + hi + 1) // 2           # CEIL mid — see theory
        if mid * mid <= x:
            lo = mid
        else:
            hi = mid - 1
    return lo

Time:  O(log x)
Space: O(1)

---------------------------------------------------
Why Ceil Mid?

With a "maximum feasible" search, the template's `lo = mid` branch
must STRICTLY advance or we loop forever. If mid rounds DOWN
(`(lo + hi) // 2`), then when `hi = lo + 1`, mid == lo, the branch
sets `lo = mid == lo` — no progress, infinite loop.

Ceiling mid (`(lo + hi + 1) // 2`) always rounds up, so `mid > lo`
whenever `hi > lo`. Combined with the `hi = mid - 1` branch, we
always make progress.

Alternative: use exclusive-hi ([lo, hi), with `hi = x + 1`) and
floor mid with a slightly different invariant. Pick whichever you
find clearer.

---------------------------------------------------
Newton's Method — A Faster Alternative:

For floating-point sqrt, Newton's iteration converges in O(log log x)
— much faster than binary search. For integer sqrt, Newton's also
works, with a subtle integer-termination condition:

    r = x
    while r * r > x:
        r = (r + x // r) // 2
    return r

Iteration count is O(log log x) — ~5 steps even for huge x. Included
below for contrast.

---------------------------------------------------
Example:

    int_sqrt(0)   → 0
    int_sqrt(4)   → 2
    int_sqrt(8)   → 2
    int_sqrt(2147483647) → 46340

---------------------------------------------------
"""

# =========================================================================
# Solution 1: Binary Search — O(log x)
# =========================================================================

def int_sqrt_bsearch(x):
    """
    Integer square root via binary search.

    Time Complexity:  O(log x)
    Space Complexity: O(1)
    """
    if x < 2:
        return x

    lo, hi = 1, x

    while lo < hi:
        mid = lo + (hi - lo + 1) // 2              # CEIL mid
        if mid * mid <= x:
            lo = mid                                # mid is feasible — try bigger
        else:
            hi = mid - 1

    return lo


# =========================================================================
# Solution 2: Newton's Method — O(log log x)
# =========================================================================

def int_sqrt_newton(x):
    """
    Integer sqrt via Newton's iteration.

    Time Complexity:  O(log log x) — very few iterations.
    Space Complexity: O(1)

    Why it terminates: Newton's iteration on integer sqrt either
    converges monotonically downward or oscillates near the answer
    by ±1. The `r * r > x` check catches the right fixed point.
    """
    if x < 2:
        return x

    r = x
    while r * r > x:
        r = (r + x // r) // 2
    return r


# =========================================================================
# Solution 3: Brute Force — O(sqrt(x))
# =========================================================================

def int_sqrt_brute(x):
    """
    Count up until r*r exceeds x. Slow but obviously correct.

    Time Complexity:  O(sqrt(x))
    Space Complexity: O(1)
    """
    r = 0
    while (r + 1) * (r + 1) <= x:
        r += 1
    return r


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    # Quick demo
    for x in [0, 1, 4, 8, 16, 99, 100, 2147483647]:
        bs = int_sqrt_bsearch(x)
        nw = int_sqrt_newton(x)
        print(f"   int_sqrt({x:>10}) = {bs}   (newton: {nw})")
    print()

    # Test cases — (x, expected)
    test_cases = [
        (0,             0),
        (1,             1),
        (2,             1),
        (3,             1),
        (4,             2),
        (8,             2),
        (9,             3),
        (15,            3),
        (16,            4),
        (17,            4),
        (99,            9),
        (100,           10),
        (101,           10),
        (10**6,         1000),
        (10**12,        10**6),
        (2147483647,    46340),           # INT_MAX
        (2147395599,    46339),           # LC #69's known edge case
    ]

    for i, (x, expected) in enumerate(test_cases):
        for fn in (int_sqrt_bsearch, int_sqrt_newton, int_sqrt_brute):
            # skip brute force on massive inputs (would take too long)
            if fn is int_sqrt_brute and x > 10**7:
                continue
            got = fn(x)
            assert got == expected, (
                f"Test {i+1} ({fn.__name__}) failed on x={x}: "
                f"expected {expected}, got {got}"
            )
        print(f"Test {i+1} passed: sqrt({x:>10}) = {expected}")

    # Stress test against Python's int(math.sqrt(x))
    import math
    import random
    random.seed(42)
    for _ in range(2000):
        x = random.randint(0, 10**10)
        expected = int(math.isqrt(x))             # Python 3.8+ exact integer sqrt
        assert int_sqrt_bsearch(x) == expected
        assert int_sqrt_newton(x) == expected
    print("\nStress test: 2000 random inputs matched math.isqrt")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Why This Problem Matters:
    #
    #   1. It's the SIMPLEST example of binary-search-on-the-answer:
    #      the candidates are the NUMBERS, not array indices.
    #   2. It introduces the "max-feasible" template (ceiling mid).
    #   3. It contrasts with Newton's method, showing that BS isn't
    #      always optimal — for this specific problem, iterative
    #      refinement converges even faster.
    #
    # Related:
    #   - Koko Eating Bananas (LC #875) — min-feasible BS
    #   - Split Array Largest Sum (LC #410) — BS with greedy check
    #   - Find Peak in a Sequence — BS without a sort order
    # ---------------------------------------------------------------
