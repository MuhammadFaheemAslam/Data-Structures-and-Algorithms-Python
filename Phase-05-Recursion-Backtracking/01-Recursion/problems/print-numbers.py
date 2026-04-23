"""
Problem: Print Numbers 1..n and n..1 Recursively

Difficulty: Introductory

---------------------------------------------------
Problem Statement:

Print the numbers from 1 to n (and separately, from n to 1) using
RECURSION, not loops. The challenge isn't the answer — it's
understanding why the SAME function, with the work BEFORE vs AFTER
the recursive call, produces OPPOSITE orderings.

This problem is the clearest demonstration of the head-vs-tail
recursion distinction from `../patterns/`.

---------------------------------------------------
The Four Orderings:

    print_forward(n):    1, 2, 3, ..., n
    print_backward(n):   n, n-1, n-2, ..., 1

Each can be written two ways — with work BEFORE or AFTER the
recursive call. This gives FOUR variants, but two pairs produce
the same output:

    Forward order, tail-style:  do work then recurse DOWN (need accumulator or different parameter)
    Forward order, head-style:  recurse DOWN first, then do work on the way up
    Backward order, tail-style: do work then recurse on n-1
    Backward order, head-style: recurse on n-1 first, then do work (tricky)

---------------------------------------------------
Key Insight:

The RECURSIVE CALL is always on a SMALLER input (to avoid infinite
recursion). What changes between "forward" and "backward" orderings
is:

    - WHEN we do the work (before or after the recursive call)
    - WHAT parameter we use (n itself, or a counter)

This shows that recursion is flexible — you can make it traverse
INDEX-SPACE in either direction regardless of whether your
parameter counts UP or DOWN.
"""


# =========================================================================
# 1. Print Forward (1, 2, 3, ..., n) via Head Recursion
# =========================================================================

def print_forward_head(n):
    """
    Print 1, 2, 3, ..., n using HEAD recursion.

    Strategy: recurse on n-1 FIRST, then print n. The deepest call
    prints 1 first, the outermost prints n last.

    Output: 1, 2, 3, ..., n.
    """
    if n == 0:
        return
    print_forward_head(n - 1)                     # recurse DOWNWARD first
    print(n, end=" ")                             # then print — ordered 1, 2, ..., n


# =========================================================================
# 2. Print Forward via Tail-Style Recursion (with Counter)
# =========================================================================

def print_forward_tail(n, current=1):
    """
    Print 1, 2, 3, ..., n using tail-position recursion with an
    auxiliary counter.

    Strategy: print current FIRST, then recurse on current + 1.
    The counter goes UP from 1 to n.

    Output: 1, 2, 3, ..., n.
    """
    if current > n:
        return
    print(current, end=" ")                       # print FIRST
    print_forward_tail(n, current + 1)            # then recurse


# =========================================================================
# 3. Print Backward (n, n-1, ..., 1) via Tail-Style Recursion
# =========================================================================

def print_backward_tail(n):
    """
    Print n, n-1, ..., 1 using tail-position recursion.

    Strategy: print n FIRST, then recurse on n - 1. Work happens
    before the recursive call, so outputs come in descending order.

    Output: n, n-1, ..., 1.
    """
    if n == 0:
        return
    print(n, end=" ")                             # print FIRST
    print_backward_tail(n - 1)                    # then recurse


# =========================================================================
# 4. Print Backward via Head Recursion (with Counter)
# =========================================================================

def print_backward_head(n, current=None):
    """
    Print n, n-1, ..., 1 using head recursion with a counter.

    Strategy: recurse on current + 1 first, then print current on
    the way back up. The counter goes UP from 1 to n during
    descent; the printing happens in REVERSE order during ascent.

    Output: n, n-1, ..., 1.
    """
    if current is None:
        current = 1
    if current > n:
        return
    print_backward_head(n, current + 1)           # recurse FIRST
    print(current, end=" ")                       # then print — descending order


# =========================================================================
# Bonus: Print Forward via Counting DOWN (Funkier Version)
# =========================================================================

def print_forward_counting_down(n):
    """
    Print 1..n while recursing DOWNWARD (n, n-1, ..., 1) — by doing
    work on the way back up.

    Identical output to print_forward_head; this just shows the
    pattern can be written as:

        recurse → then print n → unwind → print n-1 → unwind → ...

    On the return path, the outermost call prints n last.
    """
    if n == 0:
        return
    print_forward_counting_down(n - 1)
    print(n, end=" ")


# =========================================================================
# Bonus: Print Backward via Counting UP
# =========================================================================

def print_backward_counting_up(n):
    """
    Print n..1 while counting UP a helper from 1 to n.

    Strategy (mirror of print_backward_head): head-recursive with an
    ascending counter.
    """
    def helper(current):
        if current > n:
            return
        helper(current + 1)
        print(current, end=" ")

    helper(1)


# =========================================================================
# Test
# =========================================================================

def _capture_output(fn, *args, **kwargs):
    """Capture what `fn` prints to stdout and return as a string."""
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(*args, **kwargs)
    return buf.getvalue().strip()


if __name__ == "__main__":
    n = 5

    print("1. print_forward_head(5):")
    print("   ", end=""); print_forward_head(n)
    print()

    print("2. print_forward_tail(5):")
    print("   ", end=""); print_forward_tail(n)
    print()

    print("3. print_backward_tail(5):")
    print("   ", end=""); print_backward_tail(n)
    print()

    print("4. print_backward_head(5):")
    print("   ", end=""); print_backward_head(n)
    print()

    print("Bonus:")
    print("   print_forward_counting_down(5):  ", end="")
    print_forward_counting_down(n); print()
    print("   print_backward_counting_up(5):   ", end="")
    print_backward_counting_up(n); print()

    # Verify outputs
    for n in [0, 1, 5, 10]:
        forward_expected = " ".join(str(i) for i in range(1, n + 1))
        backward_expected = " ".join(str(i) for i in range(n, 0, -1))

        assert _capture_output(print_forward_head, n) == forward_expected
        assert _capture_output(print_forward_tail, n) == forward_expected
        assert _capture_output(print_forward_counting_down, n) == forward_expected

        assert _capture_output(print_backward_tail, n) == backward_expected
        assert _capture_output(print_backward_head, n) == backward_expected
        assert _capture_output(print_backward_counting_up, n) == backward_expected

    print("\nAll outputs verified for n = 0, 1, 5, 10.")
    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Lesson:
    #
    #   Recursion direction ("does n count up or down?") is
    #   INDEPENDENT of output direction ("do we print 1 or n first?").
    #
    #   Any combination works, depending on whether the useful work
    #   (the print) happens BEFORE or AFTER the recursive call.
    #
    #   This is the cleanest, smallest example of that distinction —
    #   use it whenever explaining recursion order to someone for
    #   the first time.
    # ---------------------------------------------------------------
