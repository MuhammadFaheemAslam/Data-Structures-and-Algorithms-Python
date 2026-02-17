"""
Problem 01: Find Maximum and Minimum in a List

Difficulty: Easy

---------------------------------------------------
Problem Statement:

Given a list of numbers, find:
1. The maximum element
2. The minimum element

You must return both values.

---------------------------------------------------
Example:

Input:
    [3, 5, 1, 9, 2]

Output:
    Maximum = 9
    Minimum = 1

---------------------------------------------------
"""

# -------------------------------------------------
# Approach 1: Using Built-in Functions (Simple)
# -------------------------------------------------

def find_max_min_builtin(arr):
    """
    Uses Python's built-in max() and min() functions.
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    if not arr:
        return None, None

    maximum = max(arr)
    minimum = min(arr)

    return maximum, minimum


# -------------------------------------------------
# Approach 2: Manual Traversal (Interview Friendly)
# -------------------------------------------------

def find_max_min_manual(arr):
    """
    Traverse the list manually and track max and min.
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    """

    if not arr:
        return None, None

    # Assume first element is both max and min
    maximum = arr[0]
    minimum = arr[0]

    # Start checking from second element
    for num in arr[1:]:
        if num > maximum:
            maximum = num

        if num < minimum:
            minimum = num

    return maximum, minimum


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    numbers = [3, 5, 1, 9, 2]

    print("Using Built-in:")
    print(find_max_min_builtin(numbers))

    print("\nUsing Manual Traversal:")
    print(find_max_min_manual(numbers))

    print()
     # Test cases
    test_cases = [
        ([3, 1, 4, 1, 5, 9, 2], (9, 1)),
        ([-5, -2, -10, -1], (-1, -10)),
        ([100], (100, 100)),
        ([], (None, None)),
        ([7, 7, 7, 7], (7, 7))
    ]

    for i, (arr, expected) in enumerate(test_cases):
        result = find_max_min_manual(arr)
        assert result == expected, f"Test {i+1} failed: expected {expected}, got {result}"
        print(f"Test {i+1} passed: {arr} -> {result}")

    print("\nAll tests passed!")