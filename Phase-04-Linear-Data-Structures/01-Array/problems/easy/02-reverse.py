"""
Problem 02: Reverse an Array

Difficulty: Easy

---------------------------------------------------
Problem Statement:

Reverse an array — i.e., the last element becomes first, the
first becomes last, and so on.

    [1, 2, 3, 4, 5]  →  [5, 4, 3, 2, 1]

---------------------------------------------------
Why This Problem Matters:

Reversing an array is trivial on its own, but the TWO-POINTER SWAP
technique it introduces is one of the most reused patterns in all of
linear data structures:

    - Reverse linked list in place
    - Check if a string is a palindrome
    - Rotate array (one of the elegant algorithms uses 3 reverses)
    - Sort Colors / Dutch National Flag
    - Partition around a pivot

This file covers three approaches — from the "wrong" idiomatic one
to the right-but-not-best one to the standard O(1)-space answer.

---------------------------------------------------
"""

# =========================================================================
# Approach 1: Python Built-In Slice Reverse
# =========================================================================

def reverse_slice(arr):
    """
    The Pythonic one-liner. Creates a NEW reversed list.

    Time:  O(n)
    Space: O(n) — not in place; allocates a new list

    Fine for one-shot use; violates "in place" constraints in interview
    problems that demand O(1) space.
    """
    return arr[::-1]


# =========================================================================
# Approach 2: Using a Second Array (Naive)
# =========================================================================

def reverse_new_array(arr):
    """
    Walk the input backward, appending to a new list.

    Time:  O(n)
    Space: O(n)

    Same complexity as slice but more explicit. Useful for teaching
    the concept; in practice the slice form is shorter.
    """
    result = []
    for i in range(len(arr) - 1, -1, -1):
        result.append(arr[i])
    return result


# =========================================================================
# Approach 3: Two-Pointer Swap (In Place) — THE Answer
# =========================================================================

def reverse_in_place(arr):
    """
    Swap from both ends inward.

    Time:  O(n)   — exactly n/2 swaps
    Space: O(1)   — mutates the input; no new allocation

    This is the interview-standard version. The two-pointer swap
    pattern generalizes to many other problems.
    """
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
    return arr


# =========================================================================
# Approach 4: Recursive (Educational)
# =========================================================================

def reverse_recursive(arr, left=0, right=None):
    """
    Recursive reversal. Swap the ends, then recurse on the inner range.

    Time:  O(n)
    Space: O(n) — recursion stack

    Strictly worse than the iterative two-pointer approach in Python
    (stack overhead, recursion limit). Shown for completeness.
    """
    if right is None:
        right = len(arr) - 1

    if left >= right:
        return arr

    arr[left], arr[right] = arr[right], arr[left]
    return reverse_recursive(arr, left + 1, right - 1)


# =========================================================================
# Bonus: Reverse a SUBARRAY (Useful for the "rotate" medium problem)
# =========================================================================

def reverse_subarray(arr, left, right):
    """
    Reverse arr[left..right] (INCLUSIVE) in place.

    Used as a building block in array rotation — see
    problems/medium/01-rotate.py.
    """
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
    return arr


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    data = [1, 2, 3, 4, 5]
    print(f"Input:  {data}")
    print(f"   slice reverse:      {reverse_slice(data)}")
    print(f"   new-array reverse:  {reverse_new_array(data)}")

    mut = data[:]
    reverse_in_place(mut)
    print(f"   in-place two-ptr:   {mut}")

    mut = data[:]
    reverse_recursive(mut)
    print(f"   recursive:          {mut}")
    print()

    # Test cases — (input, expected_after_reverse)
    test_cases = [
        [1, 2, 3, 4, 5],
        [],
        [42],
        [1, 2],
        [5, 4, 3, 2, 1],                           # already reversed
        [1, 1, 1, 1],                              # all equal
        [-3, -1, 2, 4],
    ]

    for i, data in enumerate(test_cases):
        expected = list(reversed(data))

        assert reverse_slice(data) == expected
        assert reverse_new_array(data) == expected

        mut = data[:]
        reverse_in_place(mut)
        assert mut == expected

        mut = data[:]
        reverse_recursive(mut)
        assert mut == expected

        print(f"Test {i+1} passed: {data} -> {expected}")

    # Reverse subarray
    print()
    print("Reverse-subarray bonus:")
    arr = [1, 2, 3, 4, 5, 6, 7]
    reverse_subarray(arr, 2, 5)
    print(f"   reverse_subarray([1..7], 2, 5) = {arr}")
    assert arr == [1, 2, 6, 5, 4, 3, 7]

    # Stress test
    import random
    random.seed(42)
    for _ in range(200):
        n = random.randint(0, 30)
        data = [random.randint(-100, 100) for _ in range(n)]
        expected = list(reversed(data))
        mut = data[:]
        reverse_in_place(mut)
        assert mut == expected

    print("\nStress test: 200 random arrays reversed correctly")

    print("\nAll tests passed!")
