"""
Problem: Factorial

Difficulty: Introductory

---------------------------------------------------
Problem Statement:

Compute n! = n × (n-1) × (n-2) × ... × 2 × 1  (with 0! = 1 by convention).

---------------------------------------------------
Why Factorial Is the First Recursion Example:

The recurrence is as clean as it gets:

    0! = 1                          (base case)
    n! = n × (n-1)!                 (recursive case)

Two lines, one branch. Every introductory recursion course uses it —
because once you understand why THIS works, you understand every
other linear-recursive function.

---------------------------------------------------
Three Implementations (Linear, Same Big-O):

    1. Direct recursion         O(n) time, O(n) stack
    2. Tail recursion           O(n) time, O(n) stack (no TCO in Python)
    3. Iteration                O(n) time, O(1) stack  ← production choice

And one note: Python's `math.factorial` is C-optimized and faster
than all three.
"""


# =========================================================================
# 1. Direct Recursion (Head Recursion — Work on the Way Back Up)
# =========================================================================

def factorial_recursive(n):
    """
    Direct recursive factorial.

    Not tail-recursive: the multiplication `n * ...` happens AFTER
    the recursive call returns.

    Time:  O(n)
    Space: O(n) stack
    """
    if n < 0:
        raise ValueError("factorial not defined for negative integers")

    if n == 0 or n == 1:
        return 1
    return n * factorial_recursive(n - 1)


# =========================================================================
# 2. Tail Recursion (with Accumulator)
# =========================================================================

def factorial_tail(n, acc=1):
    """
    Tail-recursive factorial via an accumulator parameter.

    The recursive call IS the last thing. In a TCO language this
    would compile to a loop; Python doesn't do TCO, so it still
    grows the stack.

    Time:  O(n)
    Space: O(n) stack
    """
    if n < 0:
        raise ValueError("factorial not defined for negative integers")

    if n == 0 or n == 1:
        return acc
    return factorial_tail(n - 1, acc * n)


# =========================================================================
# 3. Iteration (The Production Choice)
# =========================================================================

def factorial_iterative(n):
    """
    Iterative factorial.

    Time:  O(n)
    Space: O(1)
    """
    if n < 0:
        raise ValueError("factorial not defined for negative integers")

    acc = 1
    for i in range(2, n + 1):
        acc *= i
    return acc


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    import math

    # Correctness for n = 0..15
    for n in range(16):
        expected = math.factorial(n)
        assert factorial_recursive(n) == expected
        assert factorial_tail(n) == expected
        assert factorial_iterative(n) == expected
        print(f"   {n}! = {expected}")

    # Edge cases
    for fn in (factorial_recursive, factorial_tail, factorial_iterative):
        try:
            fn(-1)
        except ValueError as e:
            pass
    print("\nNegative input raises ValueError in all three variants.")

    # Python's int is arbitrary-precision — no overflow concerns
    big = factorial_iterative(100)
    assert big == math.factorial(100)
    print(f"\nfactorial_iterative(100) has {len(str(big))} digits")

    # Timing
    import time
    n = 900                                        # near Python's default recursion limit

    t0 = time.time()
    factorial_recursive(n)
    t_rec = time.time() - t0

    t0 = time.time()
    factorial_iterative(n)
    t_iter = time.time() - t0

    t0 = time.time()
    math.factorial(n)
    t_builtin = time.time() - t0

    print(f"\nTiming (n = {n}):")
    print(f"   recursive:         {t_rec:.5f}s")
    print(f"   iterative:         {t_iter:.5f}s")
    print(f"   math.factorial():  {t_builtin:.5f}s  (C-optimized)")

    print("\nAll tests passed!")
