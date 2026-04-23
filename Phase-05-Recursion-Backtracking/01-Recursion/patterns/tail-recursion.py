"""
tail-recursion.py – Tail Recursion

A function is **tail-recursive** if the recursive call is the LAST
thing it does — no further computation happens after the call returns.

    def tail_recursive(n, acc):
        if base_case(n):
            return acc
        return tail_recursive(reduce(n), combine(acc, n))
                ^^^^^^^^^^^^^^^
                        │
                  returned DIRECTLY — no "+ something" after it

vs non-tail-recursive:

    def not_tail(n):
        if base_case(n):
            return 0
        return n + not_tail(n - 1)
               ^^^^
               │
         work happens AFTER the call — not a tail call

---------------------------------------------------
Why Tail Recursion Matters (Outside Python):

Languages with **tail-call optimization (TCO)** — Scheme, ML,
Haskell, some Scala — rewrite tail-recursive functions as LOOPS at
compile time. No stack growth. No recursion-depth limit.

Python does NOT have TCO. Tail recursion in Python still grows the
stack and still crashes at depth 1000. Guido van Rossum has
explicitly rejected TCO for Python (he prefers explicit loops).

So in Python, the lesson is different:

    **If your function is tail-recursive, it can usually be
    rewritten as a while loop with no functional change.**

That iterative version avoids the stack-depth risk. For linear tail
recursion (sum, length, gcd), always prefer the iterative form in
production Python.

This file demonstrates the concept on three canonical examples,
each paired with its iterative equivalent.
"""


# =========================================================================
# 1. Sum of 1..n
# =========================================================================

def sum_to_tail(n, acc=0):
    """
    Tail-recursive sum 1..n.

    The RECURSIVE CALL is the last thing. An accumulator parameter
    (`acc`) carries the running total forward.

    Time:  O(n)
    Space: O(n) stack in Python (would be O(1) with TCO)
    """
    if n == 0:
        return acc
    return sum_to_tail(n - 1, acc + n)


def sum_to_iterative(n):
    """
    Iterative equivalent — same algorithm, no stack growth.

    Time:  O(n)
    Space: O(1)
    """
    acc = 0
    while n > 0:
        acc += n
        n -= 1
    return acc


# =========================================================================
# 2. GCD (Euclid's Algorithm) — Naturally Tail-Recursive
# =========================================================================

def gcd_tail(a, b):
    """
    Greatest common divisor via Euclid's algorithm — tail-recursive.

    gcd(a, b) = gcd(b, a mod b), with gcd(a, 0) = a.

    Time:  O(log(min(a, b)))    — Euclid's bound
    Space: O(log ...) stack (iterative version uses O(1))
    """
    if b == 0:
        return a
    return gcd_tail(b, a % b)


def gcd_iterative(a, b):
    """Iterative equivalent."""
    while b != 0:
        a, b = b, a % b
    return a


# =========================================================================
# 3. Factorial with an Accumulator — Tail-Recursive Variant
# =========================================================================

def factorial_tail(n, acc=1):
    """
    Factorial using an accumulator so the recursive call is tail position.

    Contrast with the standard factorial:
        def factorial(n): return 1 if n == 0 else n * factorial(n - 1)
    That version is NOT tail-recursive — the multiplication happens
    AFTER the recursive call returns.

    Time:  O(n)
    Space: O(n) stack in Python
    """
    if n == 0:
        return acc
    return factorial_tail(n - 1, acc * n)


def factorial_iterative(n):
    """Iterative equivalent."""
    acc = 1
    for i in range(1, n + 1):
        acc *= i
    return acc


# =========================================================================
# Trampoline — Simulating TCO in Python (Rarely Needed)
# =========================================================================
#
# If you REALLY need to tail-recurse deeply in Python without blowing
# the stack, a "trampoline" is a pattern: the tail-recursive function
# returns a THUNK (a zero-argument function) representing the next
# call, and a driver loop repeatedly unwraps thunks until a final
# value appears.
#
# It works, but it's ugly and slow. Better option: just write the
# loop.

def trampoline(result):
    """
    Repeatedly call `result` if it's callable; otherwise return it.

    Usage: return a thunk (no-arg function) instead of recursing directly,
    and call `trampoline(initial_thunk)` from the outside.
    """
    while callable(result):
        result = result()
    return result


def _sum_to_thunked(n, acc=0):
    """Return a thunk representing the next recursive step."""
    if n == 0:
        return acc
    return lambda: _sum_to_thunked(n - 1, acc + n)


def sum_to_trampolined(n):
    """Deep sum without stack growth — using a trampoline."""
    return trampoline(_sum_to_thunked(n))


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    # Correctness
    for n in [0, 1, 5, 10, 100]:
        expected = n * (n + 1) // 2
        assert sum_to_tail(n) == expected
        assert sum_to_iterative(n) == expected
        assert sum_to_trampolined(n) == expected
        print(f"   sum_to({n:3}) = {expected}")
    print()

    import math
    for n in [0, 1, 5, 10, 15]:
        expected = math.factorial(n)
        assert factorial_tail(n) == expected
        assert factorial_iterative(n) == expected
        print(f"   factorial({n:3}) = {expected}")
    print()

    gcd_cases = [
        (12, 8, 4),
        (100, 75, 25),
        (48, 18, 6),
        (17, 5, 1),
        (100, 0, 100),
        (0, 100, 100),
    ]
    for a, b, expected in gcd_cases:
        assert gcd_tail(a, b) == expected
        assert gcd_iterative(a, b) == expected
        print(f"   gcd({a}, {b}) = {expected}")
    print()

    # Demonstrate the depth limit — iterative handles what tail-recursive can't
    import sys
    big = 5_000

    # Tail recursive WILL hit the recursion limit
    sys.setrecursionlimit(10_000)                 # bump it up for this test
    print(f"sum_to_tail({big}) = {sum_to_tail(big)}")
    print(f"sum_to_iterative({big}) = {sum_to_iterative(big)}")
    print(f"sum_to_trampolined({big}) = {sum_to_trampolined(big)}")
    assert sum_to_tail(big) == sum_to_iterative(big) == sum_to_trampolined(big)

    # Reset limit
    sys.setrecursionlimit(1000)

    # At Python's default limit (1000), the tail-recursive version would
    # crash at n > ~990. The iterative version works for any n.
    print(f"\nsum_to_iterative(1_000_000) = {sum_to_iterative(1_000_000)}")
    # (Tail-recursive version would crash immediately.)

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Lesson for Python Programmers:
    #
    #   Tail recursion is a beautiful theoretical concept — but
    #   Python ignores it. Every tail-recursive function should be
    #   rewritten as a `while` loop for production use.
    #
    #   The trampoline pattern exists but is rarely worth it. Just
    #   write the loop.
    # ---------------------------------------------------------------
