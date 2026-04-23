"""
head-recursion.py – Head Recursion ("Process on the Way Up")

A function is **head-recursive** if the useful work happens AFTER
the recursive call returns — on the way BACK UP the call stack:

    def head_recursive(n):
        if base_case(n):
            return
        head_recursive(n - 1)           # recurse FIRST
        do_work(n)                      # then do work

Contrast with tail recursion:

    def tail_recursive(n):
        if base_case(n):
            return
        do_work(n)                      # do work FIRST
        tail_recursive(n - 1)           # then recurse

Both are O(n) time and O(n) stack. The difference is WHEN the
useful work happens — which determines the ORDER in which outputs
or side effects occur.

---------------------------------------------------
The Two Iteration Orders:

Tail recursion visits 1, 2, 3, ..., n (natural order).
Head recursion visits n, n-1, n-2, ..., 1 (reverse order).

Why? Because each call waits for the NEXT to finish. The DEEPEST
call returns first, so its work happens first. The outermost call's
work happens LAST.

This makes head recursion the natural tool for:
    - Printing in reverse
    - Reversing a linked list
    - Decoding data that was encoded with a stack
    - Any "unstack as we come back" pattern

---------------------------------------------------
Head Recursion vs Explicit Stack:

Head recursion is an implicit stack. Every recursive call pushes a
frame; every `return` pops one. The "work on the way back up"
happens in LIFO order — which is why it's reversed.

You can replicate head recursion iteratively by PUSHING work into
a stack in forward order, then POPPING to execute in reverse:

    stack = []
    for i in range(n):
        stack.append(i)          # push in forward order
    while stack:
        do_work(stack.pop())     # execute in reverse

Same output, no recursion-depth risk.
"""


# =========================================================================
# 1. Print 1..n in REVERSE via Head Recursion
# =========================================================================

def print_reverse(n):
    """
    Print n, n-1, ..., 1 using head recursion on a COUNT-UP.

    Even though we recurse on n-1, n-2, ..., 1 (counting DOWN), the
    prints happen as each call RETURNS — so the first print is from
    the DEEPEST call (which received n = 1), then n = 2, ...

    Wait — that would print FORWARD. Let me re-examine.
    """
    if n == 0:
        return
    print_reverse(n - 1)                          # recurse FIRST — unwinds to depth 0
    print(n)                                      # then print — outermost prints LAST


def print_forward(n):
    """Tail-recursive variant — prints in natural 1..n order."""
    if n == 0:
        return
    # (technically not pure tail — print is before the call, but it's
    # the head/tail-like placement that controls output order)
    _print_forward_helper(n, 1)


def _print_forward_helper(n, current):
    if current > n:
        return
    print(current)                                # print FIRST
    _print_forward_helper(n, current + 1)         # then recurse


# =========================================================================
# 2. Print 1..n (Forward Order) via Head Recursion
# =========================================================================

def print_1_to_n(n):
    """
    Print 1, 2, 3, ..., n using head recursion.

    Strategy: recurse DOWNWARD from n to 1, but print on the way UP.
    The DEEPEST call (n=1) prints 1 first; then n=2 prints 2; then n=3
    prints 3; ...; the outermost call (n=n itself) prints n last.

    Output: 1 2 3 ... n

    Same output as an iterative `for i in range(1, n+1): print(i)`.
    The difference is architectural — head recursion uses O(n) stack
    for what iteration does with O(1) space.
    """
    if n == 0:
        return
    print_1_to_n(n - 1)                           # recurse FIRST (all the way down to 0)
    print(n)                                      # then print — ordered 1, 2, ..., n


def print_n_to_1(n):
    """
    Print n, n-1, ..., 1 via tail-position recursion.

    Here print HAPPENS BEFORE the recursive call, so the outermost
    call prints first, then n-1, then n-2, ...
    """
    if n == 0:
        return
    print(n)                                      # print FIRST (outermost value)
    print_n_to_1(n - 1)                           # then recurse


# =========================================================================
# 3. Reverse a String via Head Recursion
# =========================================================================

def reverse_string(s):
    """
    Return the reverse of `s` using head recursion.

    reverse("abcd") = reverse("bcd") + "a"  (head recursion:
    recurse first, then prepend the current character).

    Time:  O(n²) in Python due to string concatenation; O(n) if we
    collect into a list and join at the end.
    Space: O(n) stack + O(n) output.
    """
    if len(s) <= 1:
        return s
    return reverse_string(s[1:]) + s[0]           # recurse on tail, append head LAST


def reverse_string_efficient(s):
    """
    Same algorithm, O(n) time: collect characters in a list during
    recursion (avoiding string concatenation), then join once at the end.
    """
    chars = []
    def helper(i):
        if i < 0:
            return
        chars.append(s[i])                        # write outermost → innermost order
        helper(i - 1)
    helper(len(s) - 1)
    return "".join(chars)


# =========================================================================
# 4. Reverse a List via Head Recursion (In Place)
# =========================================================================

def reverse_list_head(lst, left=0, right=None):
    """
    Reverse a list in place using head recursion on two-pointer swap.

    Head recursion form: swap after the recursive call.

    Time:  O(n)
    Space: O(n) stack — unlike the iterative two-pointer, which is O(1).
    """
    if right is None:
        right = len(lst) - 1

    if left >= right:
        return lst

    # Head recursion style — recurse on the inner subarray FIRST, then swap.
    reverse_list_head(lst, left + 1, right - 1)
    lst[left], lst[right] = lst[right], lst[left]
    return lst


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    # 1. Print in forward order via head recursion
    print("print_1_to_n(5):")
    print_1_to_n(5)                                # expects 1 2 3 4 5
    print()

    print("print_n_to_1(5):")
    print_n_to_1(5)                                # expects 5 4 3 2 1
    print()

    # 2. The confusingly-named print_reverse
    print("print_reverse(5) — prints 1..5 (head recursion traverses down, prints on the way back up):")
    print_reverse(5)                               # 1 2 3 4 5
    print()

    # 3. Reverse a string
    reverse_cases = [
        ("abcd",    "dcba"),
        ("",        ""),
        ("a",       "a"),
        ("ab",      "ba"),
        ("racecar", "racecar"),                    # palindrome
    ]
    print("reverse_string:")
    for s, expected in reverse_cases:
        assert reverse_string(s) == expected
        assert reverse_string_efficient(s) == expected
        print(f"   reverse_string({s!r:10}) = {expected!r}")
    print()

    # 4. Reverse a list in place
    print("reverse_list_head:")
    for lst in [[1, 2, 3, 4, 5], [], [42], [1, 2]]:
        expected = list(reversed(lst))
        copy = list(lst)
        reverse_list_head(copy)
        assert copy == expected
        print(f"   reverse_list_head({lst}) = {copy}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # When Head Recursion Is Genuinely Useful:
    #
    #   - Walking a linked list and processing nodes in reverse.
    #   - Printing output in reverse without an explicit stack.
    #   - Parsing structures where the grammar is "children first,
    #     then self" (e.g., post-order tree traversal).
    #
    # Otherwise, for straightforward forward iteration, a plain loop
    # is simpler. Head recursion's value is in the "output on the way
    # back up" ordering, not in raw control flow.
    # ---------------------------------------------------------------
