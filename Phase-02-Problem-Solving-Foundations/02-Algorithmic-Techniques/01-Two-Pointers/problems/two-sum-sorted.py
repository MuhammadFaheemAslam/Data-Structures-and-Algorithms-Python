"""
Problem: Two Sum II — Input Array Is Sorted

Technique: Two Pointers (converging)
Difficulty: Easy-Medium (LeetCode #167)

---------------------------------------------------
Problem Statement:

Given a 1-indexed SORTED array `numbers` and an integer `target`, find
two distinct indices (1-indexed) whose values sum to `target`. You may
assume exactly one solution exists, and you may not use the same element
twice.

Return them as a tuple (i, j) with i < j.

---------------------------------------------------
The Two-Pointer Lens:

Contrast with the unsorted version of Two Sum (Phase-02 / 01 /
01-Brute-Force / problems / two-sum.py), where we reach for hashing
to get O(n) time at the cost of O(n) space.

When the input is SORTED, two pointers wins:
    - Still O(n) time
    - O(1) space (just two integers — no hash map)

The invariant: the answer, if it exists, lies in arr[left..right]. Each
move RULES OUT one position forever:

    - If the current sum is too small, the smallest element can no
      longer participate — advance `left`.
    - If too large, the largest can't participate — retract `right`.

When neither is true, we have the pair. Return immediately.

Time Complexity:  O(n)
Space Complexity: O(1)

---------------------------------------------------
Example:

    numbers = [2, 7, 11, 15],  target = 9
    Answer (1-indexed): (1, 2)         # numbers[1] + numbers[2] = 2 + 7

---------------------------------------------------
"""

# -------------------------------------------------
# The Two-Pointer Solution
# -------------------------------------------------

def two_sum_sorted(numbers, target):
    """
    Two-pointer pair search on a sorted array.

    Returns the 1-indexed pair (i, j) such that
    numbers[i-1] + numbers[j-1] == target, or None if no pair exists.
    """
    left, right = 0, len(numbers) - 1

    while left < right:
        current = numbers[left] + numbers[right]

        if current == target:
            return (left + 1, right + 1)          # LeetCode is 1-indexed
        elif current < target:
            left += 1                              # need a bigger sum
        else:
            right -= 1                             # need a smaller sum

    return None


# -------------------------------------------------
# For Contrast: Binary Search Per Element — O(n log n)
# -------------------------------------------------

def two_sum_sorted_binary(numbers, target):
    """
    For each element at index i, binary-search for (target - numbers[i])
    in the suffix numbers[i+1:].

    Time Complexity:  O(n log n) — n binary searches
    Space Complexity: O(1)

    Strictly worse than the two-pointer version for this problem.
    Included to show WHY two pointers wins when you can use it: same
    space, better asymptotics.
    """
    from bisect import bisect_left

    n = len(numbers)
    for i in range(n):
        complement = target - numbers[i]
        j = bisect_left(numbers, complement, lo=i + 1)
        if j < n and numbers[j] == complement:
            return (i + 1, j + 1)

    return None


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    numbers = [2, 7, 11, 15]
    target = 9
    print(f"numbers = {numbers}, target = {target}")
    print(f"two_sum_sorted:        {two_sum_sorted(numbers, target)}")
    print(f"two_sum_sorted_binary: {two_sum_sorted_binary(numbers, target)}")
    print()

    # Test cases — (numbers, target, expected)
    test_cases = [
        ([2, 7, 11, 15],     9,   (1, 2)),
        ([2, 3, 4],          6,   (1, 3)),
        ([-1, 0],           -1,   (1, 2)),
        ([1, 2, 3, 4, 5],    9,   (4, 5)),
        ([1, 2, 3, 4, 5],    3,   (1, 2)),
        ([5, 25, 75],       100,  (2, 3)),
        ([1, 2, 3],          7,   None),          # no solution
        ([1],                1,   None),          # single element
        ([],                 0,   None),          # empty
    ]

    for i, (data, tgt, expected) in enumerate(test_cases):
        for fn in (two_sum_sorted, two_sum_sorted_binary):
            got = fn(data, tgt)
            assert got == expected, (
                f"Test {i+1} ({fn.__name__}) failed on {data} target={tgt}: "
                f"expected {expected}, got {got}"
            )
        print(f"Test {i+1} passed: numbers={data}, target={tgt} -> {expected}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Comparison:
    #
    #                     time       space    key feature
    #   brute force       O(n^2)     O(1)     works on anything
    #   hash map (Two Sum)O(n)       O(n)     works on unsorted input
    #   two pointers      O(n)       O(1)     wins when already sorted
    #   binary search     O(n log n) O(1)     beats brute force, not two pointers
    #
    # Rule of thumb: if the input is sorted, use two pointers. If it
    # isn't and sorting would lose information (e.g., you need original
    # indices), use hashing.
    # ---------------------------------------------------------------
