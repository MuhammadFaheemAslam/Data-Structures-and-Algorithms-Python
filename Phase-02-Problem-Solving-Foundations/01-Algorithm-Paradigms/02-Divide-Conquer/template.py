"""
template.py – Divide & Conquer Reference Template

This file demonstrates the SHAPE of a Divide & Conquer algorithm, then
shows two concrete instances of it:

    1. Binary Search   – O(log n), one subproblem, trivial combine.
    2. Maximum Element – O(n),     two subproblems, O(1) combine.

Every D&C algorithm you'll ever write follows this three-step recipe:

    (1) Divide   — split the problem into smaller versions of itself.
    (2) Conquer  — recurse on each subproblem.
    (3) Combine  — merge the subproblem answers.

Run this file to see each template's output.
"""

# =========================================================================
# Generic Divide & Conquer Skeleton
# =========================================================================
#
# A literal, generic D&C function. You'd never call this directly — it's
# here as a TEMPLATE showing the three-step shape. The problem-specific
# functions below instantiate this shape concretely.
#
# def divide_and_conquer(problem):
#     if is_base_case(problem):
#         return solve_directly(problem)
#
#     subproblems    = divide(problem)
#     sub_solutions  = [divide_and_conquer(p) for p in subproblems]
#     return combine(sub_solutions)


# =========================================================================
# Template 1: Binary Search
# Complexity: O(log n), one subproblem, O(1) combine
# Recurrence: T(n) = T(n/2) + O(1)
# =========================================================================

def binary_search(arr, target):
    """
    Find the index of `target` in a SORTED array, or -1 if it isn't present.

    Divide:  compare target to the middle element.
    Conquer: recurse into the half that could still contain target.
    Combine: nothing – the recursive call's answer IS the answer.

    Time Complexity:  O(log n)
    Space Complexity: O(log n) for the call stack (O(1) if written iteratively)
    """
    def search(lo, hi):
        # base case: empty range
        if lo > hi:
            return -1

        mid = (lo + hi) // 2

        if arr[mid] == target:
            return mid                          # solve directly
        if arr[mid] < target:
            return search(mid + 1, hi)          # recurse right
        return search(lo, mid - 1)              # recurse left

    return search(0, len(arr) - 1)


# =========================================================================
# Template 2: Maximum Element via D&C
# Complexity: O(n), two subproblems, O(1) combine
# Recurrence: T(n) = 2*T(n/2) + O(1)  →  O(n) (leaf work dominates)
# =========================================================================

def max_element(arr):
    """
    Find the maximum value in an array using divide & conquer.

    This is an EDUCATIONAL example — a simple linear scan is clearly
    simpler in practice. The point is to see the three-step shape on
    the smallest possible problem.

    Divide:  split the array in half.
    Conquer: recursively find the max of each half.
    Combine: return the larger of the two halves' answers.

    Time Complexity:  O(n)
    Space Complexity: O(log n) for the call stack
    """
    def helper(lo, hi):
        # base case: single element
        if lo == hi:
            return arr[lo]

        # divide
        mid = (lo + hi) // 2

        # conquer
        left_max = helper(lo, mid)
        right_max = helper(mid + 1, hi)

        # combine
        return max(left_max, right_max)

    if not arr:
        raise ValueError("max_element requires a non-empty array")
    return helper(0, len(arr) - 1)


# =========================================================================
# Template 3: Power Function via D&C (a^n in O(log n))
# Complexity: O(log n), one recursive call re-used, O(1) combine
# Recurrence: T(n) = T(n/2) + O(1)
# =========================================================================

def power(a, n):
    """
    Compute a^n using divide & conquer.

    The trick: a^n == (a^(n/2))^2 if n is even,
                     a * (a^(n/2))^2 if n is odd.

    Crucially, we compute a^(n/2) ONCE and square it — not twice.
    (Calling `power(a, n//2) * power(a, n//2)` would be O(n), not O(log n).)

    Time Complexity:  O(log n)
    Space Complexity: O(log n) call stack
    """
    if n == 0:
        return 1
    if n == 1:
        return a

    half = power(a, n // 2)                     # ONE recursive call, reused
    squared = half * half                       # combine

    if n % 2 == 0:
        return squared
    return a * squared


# =========================================================================
# Demonstration
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Template 1 — Binary Search  (O(log n))")
    print("=" * 60)
    arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    print(f"   arr = {arr}")
    for target in [7, 20, 1, 19, 4]:
        print(f"   binary_search(arr, {target:2}) -> {binary_search(arr, target)}")
    print()

    print("=" * 60)
    print("Template 2 — Maximum Element  (O(n))")
    print("=" * 60)
    for data in [[3, 1, 4, 1, 5, 9, 2, 6], [42], [-5, -2, -10, -1]]:
        print(f"   max_element({data}) -> {max_element(data)}")
    print()

    print("=" * 60)
    print("Template 3 — Power Function  (O(log n))")
    print("=" * 60)
    for (a, n) in [(2, 10), (3, 4), (5, 0), (7, 1), (2, 20)]:
        print(f"   power({a}, {n:2}) = {power(a, n):>10}   (check: {a ** n})")
