"""
Problem: Next Greater Element

Technique: Monotonic Stack
Difficulty: Easy-Medium (LeetCode #496 + #503)

---------------------------------------------------
Problem Statement:

Given an array `nums`, return an array `ans` where `ans[i]` is the NEXT
GREATER ELEMENT of `nums[i]` — the first element to the right of `i`
that is strictly greater. If no such element exists, ans[i] = -1.

Variant (LC #503 — circular):
    The array is treated as CIRCULAR — once you reach the end, keep
    looking from the start. Stop when you've gone around once.

---------------------------------------------------
The Monotonic-Stack Lens:

Brute force: for each i, scan i+1..n-1 (or wrap around) until you find
a greater value. O(n²).

Monotonic-stack insight: as we walk the array left-to-right, maintain
a stack of indices whose answer is still unresolved. The stack holds
values in DECREASING order (top is smallest) — because the moment a
new element is greater than the top, the top's answer is found, and
we pop it. The new element is then either smaller than the new top
(push it, still decreasing) or greater (keep popping).

Each index is pushed once and popped at most once → amortized O(n).

---------------------------------------------------
The Circular Variant (LC #503):

Simulate two full passes over the array. The stack carries over — so
on the second pass we only POP (we don't need to push again; every
index already went on the stack during the first pass).

A common idiom:

    for i in range(2 * n):
        idx = i % n
        while stack and nums[stack[-1]] < nums[idx]:
            ...
        if i < n:                 # only push during the FIRST pass
            stack.append(idx)

Still O(n) — 2n iterations of O(1) amortized each.

---------------------------------------------------
Example:

    nums = [2, 1, 2, 4, 3]
    -> [4, 2, 4, -1, -1]

    nums = [1, 2, 1], circular
    -> [2, -1, 2]             # the last 1 wraps around to the 2

---------------------------------------------------
"""

# -------------------------------------------------
# Approach 1: Monotonic Stack — O(n)
# -------------------------------------------------

def next_greater(nums):
    """
    Return, for each index, the next strictly greater element to the right.

    Time Complexity:  O(n)
    Space Complexity: O(n)
    """
    n = len(nums)
    result = [-1] * n
    stack = []                                    # stack of indices; values decreasing

    for i in range(n):
        while stack and nums[stack[-1]] < nums[i]:
            j = stack.pop()
            result[j] = nums[i]
        stack.append(i)

    # whatever remains on the stack has no next-greater → already -1
    return result


# -------------------------------------------------
# Approach 2: Circular Next Greater — O(n) (LC #503)
# -------------------------------------------------

def next_greater_circular(nums):
    """
    Same question, but with circular wraparound.

    Technique: simulate two passes. In the second pass we only pop
    (not push), because every index was already put on the stack
    during the first pass.

    Time Complexity:  O(n)
    Space Complexity: O(n)
    """
    n = len(nums)
    result = [-1] * n
    stack = []

    for i in range(2 * n):
        idx = i % n
        while stack and nums[stack[-1]] < nums[idx]:
            j = stack.pop()
            result[j] = nums[idx]
        if i < n:                                 # only push during first pass
            stack.append(idx)

    return result


# -------------------------------------------------
# Approach 3: Brute Force — O(n²)
# -------------------------------------------------

def next_greater_brute_force(nums):
    """
    For each i, scan the right side until you find a greater value.

    Time Complexity:  O(n²)
    Space Complexity: O(1) beyond the output
    """
    n = len(nums)
    result = [-1] * n
    for i in range(n):
        for j in range(i + 1, n):
            if nums[j] > nums[i]:
                result[i] = nums[j]
                break
    return result


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    nums = [2, 1, 2, 4, 3]

    print(f"nums = {nums}")
    print(f"next_greater:                {next_greater(nums)}")
    print(f"next_greater_brute_force:    {next_greater_brute_force(nums)}")
    print(f"next_greater_circular(nums): {next_greater_circular(nums)}")
    print()

    # Test cases — (nums, expected_linear, expected_circular)
    test_cases = [
        ([2, 1, 2, 4, 3],        [4, 2, 4, -1, -1],          [4, 2, 4, -1, 4]),
        ([1, 2, 3, 4, 5],        [2, 3, 4, 5, -1],           [2, 3, 4, 5, -1]),
        ([5, 4, 3, 2, 1],        [-1, -1, -1, -1, -1],       [-1, 5, 5, 5, 5]),       # strictly decreasing — wrap around finds the 5
        ([1, 2, 1],              [2, -1, -1],                [2, -1, 2]),
        ([],                     [],                         []),
        ([7],                    [-1],                       [-1]),
        ([1, 1, 1],              [-1, -1, -1],               [-1, -1, -1]),           # ties → no strictly greater
        ([3, 8, 4, 1, 2],        [8, -1, -1, 2, -1],         [8, -1, 8, 2, 3]),
    ]

    for i, (data, expected, expected_c) in enumerate(test_cases):
        got = next_greater(data)
        got_bf = next_greater_brute_force(data)
        got_c = next_greater_circular(data)

        assert got == expected, (
            f"Test {i+1} (linear): expected {expected}, got {got}"
        )
        assert got_bf == expected, (
            f"Test {i+1} (brute force): expected {expected}, got {got_bf}"
        )
        assert got_c == expected_c, (
            f"Test {i+1} (circular): expected {expected_c}, got {got_c}"
        )
        print(f"Test {i+1} passed: {data}")
        print(f"   linear:   {got}")
        print(f"   circular: {got_c}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Speedup:
    #
    #   Brute force:         O(n^2)
    #   Monotonic stack:     O(n)
    #
    # For n = 10_000 that's 10^8 vs 10^4 ops — a 10000× speedup.
    #
    # The pattern also underlies:
    #   - Daily Temperatures  (distance instead of value)
    #   - Stock Span          (previous greater)
    #   - Sliding Window Max  (monotonic deque variant)
    #   - Largest Rectangle   (next/previous smaller — histogram.py)
    # ---------------------------------------------------------------
