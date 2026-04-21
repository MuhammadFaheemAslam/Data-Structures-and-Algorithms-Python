"""
fixed-window.py – Sliding Window Template (FIXED size)

Use when the problem asks for "every window of size k" or "the best
window of size k". The window's size never changes — both pointers
advance by 1 at every step.

The template shape:

    1. Prime the first window of size k in O(k).
    2. For each subsequent position, ADD the entering element and
       REMOVE the leaving element — a net O(1) update.
    3. Update the answer at each step.

Total cost: O(n) time, O(1) or O(k) space (depending on window state).

This file shows three canonical fixed-window problems:

    1. Maximum sum of a subarray of size k.
    2. Average of every k-sized subarray.
    3. First negative number in every window of size k.

Run this file to see each template's output.
"""

from collections import deque


# =========================================================================
# Generic Fixed Window Skeleton
# =========================================================================
#
# def fixed_window(arr, k):
#     if len(arr) < k: return ...           # edge case
#
#     # 1. Prime: initialize window state on arr[0..k-1]
#     window = init_state(arr[:k])
#     best = window_answer(window)
#
#     # 2. Slide: advance the window one step at a time
#     for i in range(k, len(arr)):
#         window = add(window, arr[i])       # include entering
#         window = remove(window, arr[i-k])  # exclude leaving
#         best = update(best, window_answer(window))
#
#     return best


# =========================================================================
# Template 1: Maximum Sum of Subarray of Size k
# =========================================================================

def max_sum_subarray_size_k(arr, k):
    """
    Return the maximum sum of any contiguous subarray of length `k`.

    Time Complexity:  O(n)
    Space Complexity: O(1)

    The window STATE is a single int (running sum) — cheapest possible.
    """
    if len(arr) < k:
        return None

    # 1. prime the first window
    window_sum = sum(arr[:k])
    best = window_sum

    # 2. slide
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]         # add new, remove old
        if window_sum > best:
            best = window_sum

    return best


# =========================================================================
# Template 2: Average of Every Subarray of Size k  (LeetCode #643 shape)
# =========================================================================

def average_of_windows(arr, k):
    """
    Return the list of averages of every contiguous subarray of length `k`.

    Time Complexity:  O(n)
    Space Complexity: O(n)  for the output list; O(1) additional

    Same sliding as Template 1, but we emit (window_sum / k) at each step
    rather than tracking a max.
    """
    if len(arr) < k:
        return []

    window_sum = sum(arr[:k])
    results = [window_sum / k]

    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        results.append(window_sum / k)

    return results


# =========================================================================
# Template 3: First Negative Number in Every Window of Size k
# =========================================================================

def first_negative_per_window(arr, k):
    """
    For every contiguous subarray of length `k`, return the FIRST negative
    number in it (or 0 if there's no negative).

    This one uses a DEQUE as window state — an O(1) "next negative" lookup.

    Time Complexity:  O(n)  — each index enters and leaves the deque once
    Space Complexity: O(k)

    Key insight: the queue only ever holds INDICES of negative numbers in
    the current window. The leftmost such index is the answer when present.
    Indices that fall out of the window are removed from the front.
    """
    if len(arr) < k:
        return []

    negs = deque()                                # indices of negatives in window
    results = []

    # 1. prime — populate the deque with negatives from the first window
    for i in range(k):
        if arr[i] < 0:
            negs.append(i)

    # 2. slide
    for end in range(k - 1, len(arr)):
        # drop indices that are outside the window [end-k+1, end]
        while negs and negs[0] < end - k + 1:
            negs.popleft()

        # add the new right-edge index if it's negative
        if arr[end] < 0 and (not negs or negs[-1] != end):
            negs.append(end)

        # emit
        results.append(arr[negs[0]] if negs else 0)

    return results


# =========================================================================
# Demonstration
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Template 1 — Max Sum of Size-k Subarray")
    print("=" * 60)
    cases = [
        ([2, 1, 5, 1, 3, 2], 3,  9),     # [5, 1, 3]
        ([2, 3, 4, 1, 5],    2,  7),     # [3, 4]
        ([5],                1,  5),
        ([5],                2,  None),  # k too big
    ]
    for arr, k, expected in cases:
        got = max_sum_subarray_size_k(arr, k)
        assert got == expected
        print(f"   max_sum_subarray_size_k({arr}, k={k}) = {got}")
    print()

    print("=" * 60)
    print("Template 2 — Averages of Every Size-k Subarray")
    print("=" * 60)
    cases = [
        ([1, 12, -5, -6, 50, 3], 4, [0.5, 12.75, 10.5]),
        ([1, 2, 3, 4, 5], 2, [1.5, 2.5, 3.5, 4.5]),
    ]
    for arr, k, expected in cases:
        got = average_of_windows(arr, k)
        assert got == expected
        print(f"   average_of_windows({arr}, k={k}) = {got}")
    print()

    print("=" * 60)
    print("Template 3 — First Negative in Every Size-k Window")
    print("=" * 60)
    cases = [
        ([-8, 2, 3, -6, 10],     2,  [-8, 0, -6, -6]),
        ([12, -1, -7, 8, -15, 30, 16, 28], 3,
                                    [-1, -1, -7, -15, -15, 0]),
        ([1, 2, 3, 4, 5],        3,  [0, 0, 0]),     # no negatives
    ]
    for arr, k, expected in cases:
        got = first_negative_per_window(arr, k)
        assert got == expected
        print(f"   first_negative_per_window({arr}, k={k}) = {got}")

    print("\nAll tests passed!")
