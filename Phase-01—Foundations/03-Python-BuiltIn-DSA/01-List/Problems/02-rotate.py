"""
Problem 02: Rotate a List

Difficulty: Easy

---------------------------------------------------
Problem Statement:

Given a list of numbers and a number k,
rotate the list by k positions.

You should support:
1. Left rotation
2. Right rotation

---------------------------------------------------
Example:

Input:
    arr = [1, 2, 3, 4, 5]
    k = 2

Left Rotation:
    [3, 4, 5, 1, 2]

Right Rotation:
    [4, 5, 1, 2, 3]

---------------------------------------------------
"""

# -------------------------------------------------
# Approach 1: Using Slicing (Simple & Optimal)
# -------------------------------------------------

def rotate_left(arr, k):
    """
    Rotate list to the left by k positions.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """

    if not arr:
        return []

    n = len(arr)
    k = k % n   # Handle k > n

    return arr[k:] + arr[:k]


def rotate_right(arr, k):
    """
    Rotate list to the right by k positions.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """

    if not arr:
        return []

    n = len(arr)
    k = k % n

    return arr[-k:] + arr[:-k]


# -------------------------------------------------
# Approach 2: One-by-One Rotation (Brute Force)
# -------------------------------------------------

def rotate_left_bruteforce(arr, k):
    """
    Rotate left by shifting elements one by one.

    Time Complexity: O(n * k)
    Space Complexity: O(1)
    """

    if not arr:
        return []

    n = len(arr)
    k = k % n
    arr = arr[:]  # copy to avoid modifying original

    for _ in range(k):
        first = arr.pop(0)   # remove first element
        arr.append(first)    # add it at the end

    return arr


def rotate_right_bruteforce(arr, k):
    """
    Rotate right by shifting elements one by one.

    Time Complexity: O(n * k)
    Space Complexity: O(1)
    """

    if not arr:
        return []

    n = len(arr)
    k = k % n
    arr = arr[:]

    for _ in range(k):
        last = arr.pop()      # remove last element
        arr.insert(0, last)   # insert at beginning

    return arr


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]
    k = 2

    print("Original:", numbers)

    print("\nLeft Rotation (Slicing):")
    print(rotate_left(numbers, k))

    print("\nRight Rotation (Slicing):")
    print(rotate_right(numbers, k))

    print("\nLeft Rotation (Brute Force):")
    print(rotate_left_bruteforce(numbers, k))

    print("\nRight Rotation (Brute Force):")
    print(rotate_right_bruteforce(numbers, k))
