"""
variable-window.py – Sliding Window Template (VARIABLE size)

Use when the window's size changes based on a PREDICATE about its
contents. You typically either:

    A. Find the LONGEST window satisfying the predicate  →  expand always,
       shrink only when predicate breaks, record after shrinking.

    B. Find the SHORTEST window satisfying the predicate →  expand until
       predicate holds, shrink as much as possible while still holding.

This file shows the pattern three ways:

    1. Longest subarray with sum <= target       (LONGEST flavour)
    2. Smallest subarray with sum >= target      (SHORTEST flavour)
    3. Longest substring with at most K distinct characters  (LONGEST flavour, dict state)

These are the three shapes most variable-window problems reduce to.

Run this file to see each template's output.
"""

# =========================================================================
# Generic Variable Window Skeletons
# =========================================================================
#
# LONGEST — expand right, shrink left only when invalid:
#
# def longest_window(arr):
#     left = 0
#     state = empty_state()
#     best = 0
#
#     for right in range(len(arr)):
#         state.add(arr[right])
#         while not valid(state):
#             state.remove(arr[left])
#             left += 1
#         best = max(best, right - left + 1)
#
#     return best
#
#
# SHORTEST — expand right, shrink left as much as possible while valid:
#
# def shortest_window(arr):
#     left = 0
#     state = empty_state()
#     best = INF
#
#     for right in range(len(arr)):
#         state.add(arr[right])
#         while valid(state):
#             best = min(best, right - left + 1)
#             state.remove(arr[left])
#             left += 1
#
#     return best if best != INF else 0


# =========================================================================
# Template 1: Longest Subarray with Sum <= target  (LONGEST flavour)
# =========================================================================

def longest_subarray_sum_at_most(arr, target):
    """
    Return the length of the longest contiguous subarray whose sum is
    <= `target`. Elements assumed non-negative (so the sum is monotone
    as the window grows).

    Time Complexity:  O(n)
    Space Complexity: O(1)

    Pattern: expand `right` each iteration; shrink `left` only when the
    running sum exceeds `target`. The window is valid after every
    iteration, so the length right-left+1 is a candidate for `best`.
    """
    left = 0
    window_sum = 0
    best = 0

    for right in range(len(arr)):
        window_sum += arr[right]

        while window_sum > target and left <= right:
            window_sum -= arr[left]
            left += 1

        best = max(best, right - left + 1)

    return best


# =========================================================================
# Template 2: Smallest Subarray with Sum >= target  (SHORTEST flavour)
# =========================================================================

def smallest_subarray_sum_at_least(arr, target):
    """
    Return the length of the SMALLEST contiguous subarray whose sum is
    >= `target`. Returns 0 if no such subarray exists. (LeetCode #209.)

    Time Complexity:  O(n)
    Space Complexity: O(1)

    Pattern: expand `right` until the window is valid; then shrink
    `left` as far as possible while the window STAYS valid. Each time
    the window is valid, record `right - left + 1` as a candidate.
    """
    left = 0
    window_sum = 0
    best = float("inf")

    for right in range(len(arr)):
        window_sum += arr[right]

        while window_sum >= target:
            best = min(best, right - left + 1)
            window_sum -= arr[left]
            left += 1

    return best if best != float("inf") else 0


# =========================================================================
# Template 3: Longest Substring With At Most K Distinct Characters
# =========================================================================

def longest_substring_k_distinct(s, k):
    """
    Return the length of the longest substring of `s` containing at
    most `k` distinct characters. (LeetCode #340, classic Google question.)

    Time Complexity:  O(n)   — each character enters & leaves dict once
    Space Complexity: O(k)   — dict size bounded by number of distinct chars

    This is a great example of a variable window whose STATE is a dict
    (character → frequency in window) rather than just a number.
    """
    if k == 0 or not s:
        return 0

    left = 0
    freq = {}                                     # char → count in window
    best = 0

    for right in range(len(s)):
        freq[s[right]] = freq.get(s[right], 0) + 1

        # shrink while too many distinct characters
        while len(freq) > k:
            freq[s[left]] -= 1
            if freq[s[left]] == 0:
                del freq[s[left]]                 # important — maintain dict size invariant
            left += 1

        best = max(best, right - left + 1)

    return best


# =========================================================================
# Demonstration
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Template 1 — LONGEST subarray with sum <= target")
    print("=" * 60)
    cases = [
        ([1, 2, 3, 4, 5],    8,   3),   # [1,2,3] = 6 or [3,4,5] too big; [1,2,3,..]; best = 3
        ([1, 1, 1, 1, 1],    3,   3),
        ([5, 5, 5],          4,   0),   # every element > target
        ([],                10,   0),
        ([2, 1, 6, 1, 5, 3], 10,  4),   # [1, 1, 5, 3] or [1, 6, 1, ..]; length 4
    ]
    for arr, target, expected in cases:
        got = longest_subarray_sum_at_most(arr, target)
        assert got == expected, f"{arr} target={target}: expected {expected}, got {got}"
        print(f"   longest_subarray_sum_at_most({arr}, target={target}) = {got}")
    print()

    print("=" * 60)
    print("Template 2 — SHORTEST subarray with sum >= target")
    print("=" * 60)
    cases = [
        ([2, 3, 1, 2, 4, 3],   7,   2),     # [4, 3]
        ([1, 4, 4],            4,   1),
        ([1, 1, 1, 1, 1, 1],   11,  0),     # impossible
        ([],                   5,   0),
        ([1, 2, 3, 4, 5],      11,  3),     # [3, 4, 5]
    ]
    for arr, target, expected in cases:
        got = smallest_subarray_sum_at_least(arr, target)
        assert got == expected, f"{arr} target={target}: expected {expected}, got {got}"
        print(f"   smallest_subarray_sum_at_least({arr}, target={target}) = {got}")
    print()

    print("=" * 60)
    print("Template 3 — LONGEST substring with at most K distinct chars")
    print("=" * 60)
    cases = [
        ("eceba",       2,   3),   # "ece"
        ("aa",          1,   2),
        ("aabbcc",      2,   4),   # "aabb" or "bbcc"
        ("aabbcc",      3,   6),
        ("",            2,   0),
        ("abc",         0,   0),
        ("abaccc",      2,   4),   # "accc" length 4 (chars a, c)
    ]
    for s, k, expected in cases:
        got = longest_substring_k_distinct(s, k)
        assert got == expected, f"{s!r} k={k}: expected {expected}, got {got}"
        print(f"   longest_substring_k_distinct({s!r}, k={k}) = {got}")

    print("\nAll tests passed!")
