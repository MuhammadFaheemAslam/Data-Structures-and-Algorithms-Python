"""
template.py – Two Pointers Reference Template

This file demonstrates the three flavours of the two-pointer technique:

    1. Converging (opposite direction)  – both pointers move inward.
    2. Same direction (slow/fast)       – both pointers walk rightward.
    3. Two arrays                       – one pointer per input.

Each demo is a minimal, canonical example of that flavour so you can
recognise the shape in the wild.

Run this file to see each template's output.
"""

# =========================================================================
# Generic Skeletons
# =========================================================================
#
# Converging:
#     left, right = 0, n - 1
#     while left < right:
#         if ok(a[left], a[right]):
#             record_or_return()
#             left += 1; right -= 1
#         elif too_small(a[left], a[right]):
#             left += 1
#         else:
#             right -= 1
#
# Same-direction:
#     slow = 0
#     for fast in range(n):
#         if keep(a[fast]):
#             a[slow] = a[fast]
#             slow += 1
#     return slow
#
# Two arrays:
#     i = j = 0
#     while i < n and j < m:
#         if a[i] <= b[j]:
#             out.append(a[i]); i += 1
#         else:
#             out.append(b[j]); j += 1
#     out.extend(a[i:]); out.extend(b[j:])


# =========================================================================
# Template 1: Converging — Valid Palindrome
# =========================================================================

def is_palindrome(s):
    """
    True iff `s` is a palindrome (case- and non-alphanumeric-insensitive).

    The classic converging two-pointer pattern:
        left starts at 0, right at n-1, both step inward on a match,
        and we return False the moment they disagree.

    Time Complexity:  O(n)
    Space Complexity: O(1)
    """
    left, right = 0, len(s) - 1

    while left < right:
        # skip non-alphanumerics (common variant of this problem)
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1

        if s[left].lower() != s[right].lower():
            return False

        left += 1
        right -= 1

    return True


# =========================================================================
# Template 2: Same-Direction — In-Place Dedup on Sorted Array
# =========================================================================

def remove_duplicates_sorted(nums):
    """
    Remove duplicates in place from a SORTED list.
    Return the length of the deduplicated prefix.

    Pattern: `slow` is the write pointer, `fast` is the scan pointer.
    When `fast` sees a new value, copy it to `slow` and advance.

    Time Complexity:  O(n)
    Space Complexity: O(1)

    Returns the new length; the first `len` elements of `nums` are the
    unique values in order (matching LeetCode #26's interface).
    """
    if not nums:
        return 0

    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]

    return slow + 1                              # new length


# =========================================================================
# Template 3: Two-Array — Merge Two Sorted Arrays
# =========================================================================

def merge_sorted(a, b):
    """
    Merge two sorted lists into a single sorted list.

    Pattern: one pointer per array; at each step take the smaller head
    and advance that pointer. When one array is exhausted, extend with
    whatever's left of the other.

    This is literally the combine step of merge sort (see Phase-02 / 01 /
    02-Divide-Conquer / problems / merge-sort.py).

    Time Complexity:  O(n + m)
    Space Complexity: O(n + m) for the output
    """
    i, j = 0, 0
    out = []

    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1

    out.extend(a[i:])
    out.extend(b[j:])

    return out


# =========================================================================
# Template 4: Converging on a Computed Quantity — Reverse a List In-Place
# =========================================================================

def reverse_in_place(nums):
    """
    Reverse `nums` in place by swapping from both ends inward.

    A classic O(1)-space two-pointer operation. Same idea as palindrome
    check, but we swap instead of compare.

    Time Complexity:  O(n)
    Space Complexity: O(1)
    """
    left, right = 0, len(nums) - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1
    return nums


# =========================================================================
# Demonstration
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Template 1 — Converging (Palindrome Check)")
    print("=" * 60)
    for s in ["racecar", "hello", "A man a plan a canal Panama", "", "a"]:
        print(f"   is_palindrome({s!r:35}) = {is_palindrome(s)}")
    print()

    print("=" * 60)
    print("Template 2 — Same-Direction (In-Place Dedup)")
    print("=" * 60)
    for data in [[1, 1, 2], [0, 0, 1, 1, 1, 2, 2, 3, 3, 4], [], [5, 5, 5, 5]]:
        original = data[:]
        new_len = remove_duplicates_sorted(data)
        print(f"   input:  {original}")
        print(f"   dedup:  {data[:new_len]}   (new length = {new_len})")
        print()

    print("=" * 60)
    print("Template 3 — Two-Array Merge")
    print("=" * 60)
    for a, b in [([1, 3, 5], [2, 4, 6]), ([1, 2, 3], []), ([], [7]), ([1, 1], [1, 1])]:
        print(f"   merge_sorted({a}, {b}) = {merge_sorted(a, b)}")
    print()

    print("=" * 60)
    print("Template 4 — Converging In-Place Swap (Reverse)")
    print("=" * 60)
    for data in [[1, 2, 3, 4, 5], [42], [], [1, 2]]:
        original = data[:]
        reverse_in_place(data)
        print(f"   reverse_in_place({original}) -> {data}")
