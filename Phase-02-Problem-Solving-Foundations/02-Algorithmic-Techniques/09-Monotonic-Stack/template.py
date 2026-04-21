"""
template.py – Monotonic Stack Reference Template

This file demonstrates all FOUR canonical monotonic-stack queries:

    1. next_greater_right      — for each i, first j > i with arr[j] > arr[i]
    2. next_smaller_right      — for each i, first j > i with arr[j] < arr[i]
    3. previous_greater_left   — for each i, last j < i with arr[j] > arr[i]
    4. previous_smaller_left   — for each i, last j < i with arr[j] < arr[i]

All four use the same 5-line skeleton with different comparisons and
walk directions. Once you've seen all four, every monotonic-stack
problem is a fill-in-the-blank.

BONUS: daily_temperatures — the "distance to the next greater" variant.
       sliding_window_max — the deque variant over a fixed window.

Run this file to see each template's output.
"""

from collections import deque


# =========================================================================
# Template 1: Next Greater Element to the Right
# =========================================================================

def next_greater_right(arr):
    """
    For each index i, return the VALUE of the next element to the
    right that is strictly greater, or -1 if none exists.

    Stack invariant: values decreasing from bottom to top.
    When the new element breaks that ordering, we've found its target's
    "next greater".

    Time Complexity:  O(n)
    Space Complexity: O(n)
    """
    n = len(arr)
    result = [-1] * n
    stack = []                                    # holds indices (values decreasing)

    for i in range(n):
        while stack and arr[stack[-1]] < arr[i]:
            j = stack.pop()
            result[j] = arr[i]
        stack.append(i)

    return result


# =========================================================================
# Template 2: Next Smaller Element to the Right
# =========================================================================

def next_smaller_right(arr):
    """
    Mirror of Template 1 with the comparison flipped.

    Stack invariant: values INCREASING from bottom to top.

    Time Complexity:  O(n)
    Space Complexity: O(n)
    """
    n = len(arr)
    result = [-1] * n
    stack = []

    for i in range(n):
        while stack and arr[stack[-1]] > arr[i]:
            j = stack.pop()
            result[j] = arr[i]
        stack.append(i)

    return result


# =========================================================================
# Template 3: Previous Greater Element (to the Left)
# =========================================================================

def previous_greater_left(arr):
    """
    For each index i, return the VALUE of the nearest greater element
    to the left, or -1 if none.

    Approach: walk the array in REVERSE and apply Template 1's logic.
    (Equivalent: walk forward, pop when the top is ≤ current.)

    Time Complexity:  O(n)
    """
    n = len(arr)
    result = [-1] * n
    stack = []

    # walk right-to-left; for each i, the stack holds indices to its
    # right that might be useful
    for i in range(n - 1, -1, -1):
        while stack and arr[stack[-1]] < arr[i]:
            j = stack.pop()
            result[j] = arr[i]
        stack.append(i)

    return result


# =========================================================================
# Template 4: Previous Smaller Element (to the Left)
# =========================================================================

def previous_smaller_left(arr):
    """
    Symmetric to Template 3 with the comparison flipped.
    """
    n = len(arr)
    result = [-1] * n
    stack = []

    for i in range(n - 1, -1, -1):
        while stack and arr[stack[-1]] > arr[i]:
            j = stack.pop()
            result[j] = arr[i]
        stack.append(i)

    return result


# =========================================================================
# Bonus 1: Daily Temperatures — Distance to Next Greater (LC #739)
# =========================================================================

def daily_temperatures(temps):
    """
    For each day i, return how many days you have to wait until a warmer
    temperature. 0 if no warmer day ever comes.

    Same monotonic-stack pattern as next_greater_right, but record
    the INDEX DIFFERENCE (i - j) instead of the value.

    Time Complexity:  O(n)
    Space Complexity: O(n)
    """
    n = len(temps)
    result = [0] * n
    stack = []                                    # indices

    for i in range(n):
        while stack and temps[stack[-1]] < temps[i]:
            j = stack.pop()
            result[j] = i - j                     # distance, not value
        stack.append(i)

    return result


# =========================================================================
# Bonus 2: Sliding Window Maximum — Monotonic DEQUE (LC #239)
# =========================================================================

def sliding_window_max(arr, k):
    """
    Return the maximum of every contiguous subarray of size k.

    Uses a monotonic DEQUE keyed by indices. Invariant: values at
    those indices are DECREASING from front to back.

    For each new index i:
        1. Drop from the FRONT any index that fell out of the window.
        2. Drop from the BACK any index whose value is ≤ arr[i]
           (they can never be the max while arr[i] is in the window).
        3. Push i to the back.
        4. The front of the deque is the max of the current window.

    Time Complexity:  O(n) — each index enters and leaves the deque once.
    Space Complexity: O(k)
    """
    if not arr or k == 0:
        return []

    dq = deque()                                  # indices
    result = []

    for i, v in enumerate(arr):
        # 1. drop indices outside the window [i - k + 1, i]
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        # 2. drop smaller-or-equal values from the back
        while dq and arr[dq[-1]] <= v:
            dq.pop()
        # 3. push the new index
        dq.append(i)
        # 4. record the current window's max, once we have a full window
        if i >= k - 1:
            result.append(arr[dq[0]])

    return result


# =========================================================================
# Demonstration
# =========================================================================

if __name__ == "__main__":
    arr = [2, 1, 2, 4, 3, 1]

    print("=" * 60)
    print("Template 1 — Next Greater to the Right")
    print("=" * 60)
    print(f"   arr = {arr}")
    print(f"   next_greater_right(arr) = {next_greater_right(arr)}")
    # expected: [4, 2, 4, -1, -1, -1]
    assert next_greater_right(arr) == [4, 2, 4, -1, -1, -1]
    print()

    print("=" * 60)
    print("Template 2 — Next Smaller to the Right")
    print("=" * 60)
    print(f"   next_smaller_right(arr) = {next_smaller_right(arr)}")
    # expected: [1, -1, 1, 3, 1, -1]
    assert next_smaller_right(arr) == [1, -1, 1, 3, 1, -1]
    print()

    print("=" * 60)
    print("Template 3 — Previous Greater to the Left")
    print("=" * 60)
    print(f"   previous_greater_left(arr) = {previous_greater_left(arr)}")
    # at each i: the closest value to its LEFT that is greater
    # arr = [2, 1, 2, 4, 3, 1]
    # i=0: none → -1
    # i=1: 2 > 1 → 2
    # i=2: 2 == 2 → not strictly greater, so -1
    # i=3: nothing greater → -1
    # i=4: 4 > 3 → 4
    # i=5: 3 > 1 → 3
    assert previous_greater_left(arr) == [-1, 2, -1, -1, 4, 3]
    print()

    print("=" * 60)
    print("Template 4 — Previous Smaller to the Left")
    print("=" * 60)
    print(f"   previous_smaller_left(arr) = {previous_smaller_left(arr)}")
    # arr = [2, 1, 2, 4, 3, 1]
    # i=0: -1
    # i=1: no smaller to left of 1 → -1
    # i=2: 1 < 2 → 1
    # i=3: 2 < 4 → 2
    # i=4: 2 < 3 → 2
    # i=5: no smaller than 1 to its left (values 2, 1, 2, 4, 3) → -1
    assert previous_smaller_left(arr) == [-1, -1, 1, 2, 2, -1]
    print()

    print("=" * 60)
    print("Bonus 1 — Daily Temperatures")
    print("=" * 60)
    temps = [73, 74, 75, 71, 69, 72, 76, 73]
    print(f"   temps  = {temps}")
    print(f"   result = {daily_temperatures(temps)}")
    assert daily_temperatures(temps) == [1, 1, 4, 2, 1, 1, 0, 0]
    print()

    print("=" * 60)
    print("Bonus 2 — Sliding Window Maximum (Monotonic Deque)")
    print("=" * 60)
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    print(f"   nums = {nums}")
    print(f"   sliding_window_max(nums, k=3) = {sliding_window_max(nums, 3)}")
    assert sliding_window_max(nums, 3) == [3, 3, 5, 5, 6, 7]

    print("\nAll tests passed!")
