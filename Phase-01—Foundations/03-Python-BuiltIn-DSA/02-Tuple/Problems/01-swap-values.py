"""
Problem 01: Swap Two Values Using a Tuple

Difficulty: Easy

---------------------------------------------------
Problem Statement:

Given two values (a, b), return them swapped as (b, a).

Also demonstrate the Pythonic, tuple‑based swap idiom that avoids
using a temporary variable.

This problem highlights one of the core strengths of tuples:
packing and unpacking multiple values in a single expression.

---------------------------------------------------
Example:

Input:
    a = 1, b = 2

Output:
    (2, 1)

---------------------------------------------------
"""

# -------------------------------------------------
# Approach 1: Return a New Tuple (Simple)
# -------------------------------------------------

def swap_return(a, b):
    """
    Build a new tuple with the values reversed.

    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    return (b, a)


# -------------------------------------------------
# Approach 2: Pythonic Tuple Swap (Without Temp)
# -------------------------------------------------

def swap_pythonic(a, b):
    """
    Use tuple packing + unpacking in a single statement.

    The right-hand side `b, a` builds a temporary tuple (b, a);
    Python then unpacks it into the left-hand side names.

    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    a, b = b, a
    return (a, b)


# -------------------------------------------------
# Approach 3: Using a Temp Variable (Classical)
# -------------------------------------------------

def swap_with_temp(a, b):
    """
    The traditional swap that most other languages require.
    Shown for contrast — Python's tuple swap is preferred.

    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    temp = a
    a = b
    b = temp
    return (a, b)


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    print("swap_return(1, 2):   ", swap_return(1, 2))
    print("swap_pythonic(1, 2): ", swap_pythonic(1, 2))
    print("swap_with_temp(1, 2):", swap_with_temp(1, 2))
    print()

    # Test cases – (a, b, expected)
    test_cases = [
        (1, 2, (2, 1)),
        (-5, 10, (10, -5)),
        (0, 0, (0, 0)),
        ("x", "y", ("y", "x")),
        ([1, 2], [3, 4], ([3, 4], [1, 2])),   # works for any types
    ]

    for i, (a, b, expected) in enumerate(test_cases):
        result = swap_pythonic(a, b)
        assert result == expected, f"Test {i+1} failed: expected {expected}, got {result}"
        print(f"Test {i+1} passed: ({a!r}, {b!r}) -> {result}")

    print("\nAll tests passed!")
