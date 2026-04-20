"""
Problem 03: Count Unique Coordinates

Difficulty: Easy

---------------------------------------------------
Problem Statement:

Given a list of (x, y) coordinate tuples, possibly with duplicates,
return:
1. The number of UNIQUE coordinates.
2. The list of unique coordinates (order of first appearance preserved).

This problem highlights the MOST IMPORTANT tuple property:
tuples are HASHABLE, so they can live inside sets and act as dict keys.
A list could never be used this way.

---------------------------------------------------
Example:

Input:
    [(1, 2), (3, 4), (1, 2), (5, 6), (3, 4)]

Output:
    unique_count = 3
    unique_points = [(1, 2), (3, 4), (5, 6)]

---------------------------------------------------
"""

# -------------------------------------------------
# Approach 1: Using a set() (Simple & Fast, Order NOT Preserved)
# -------------------------------------------------

def unique_count_set(points):
    """
    Convert the list to a set – duplicates vanish because tuples are hashable.

    Time Complexity: O(n)   – each insert is O(1) average
    Space Complexity: O(n)  – the set of unique points
    """
    return len(set(points))


# -------------------------------------------------
# Approach 2: Preserve First-Appearance Order
# -------------------------------------------------

def unique_points_ordered(points):
    """
    Walk the list once, keeping a `seen` set for O(1) lookups and
    an output list in original order.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    seen = set()
    result = []

    for p in points:
        if p not in seen:
            seen.add(p)
            result.append(p)

    return result


# -------------------------------------------------
# Approach 3: Count Each Coordinate's Occurrences (Dict as Counter)
# -------------------------------------------------

def count_occurrences(points):
    """
    Build a dict mapping each coordinate -> how many times it appeared.
    Again, this only works because tuples are hashable.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    counts = {}
    for p in points:
        counts[p] = counts.get(p, 0) + 1
    return counts


# -------------------------------------------------
# Why This Would FAIL With Lists
# -------------------------------------------------
#
# If the points were represented as lists instead of tuples:
#     set([[1, 2], [3, 4]])  -> TypeError: unhashable type: 'list'
#     { [1, 2]: "origin" }   -> TypeError: unhashable type: 'list'
#
# Tuples are the standard choice when a small fixed-size record
# needs to be used as a set element or dict key.


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    points = [(1, 2), (3, 4), (1, 2), (5, 6), (3, 4)]

    print("Input:", points)
    print("unique_count_set:      ", unique_count_set(points))
    print("unique_points_ordered: ", unique_points_ordered(points))
    print("count_occurrences:     ", count_occurrences(points))
    print()

    # Test cases – (input, expected_count, expected_ordered)
    test_cases = [
        (
            [(1, 2), (3, 4), (1, 2), (5, 6), (3, 4)],
            3,
            [(1, 2), (3, 4), (5, 6)],
        ),
        (
            [(0, 0), (0, 0), (0, 0)],
            1,
            [(0, 0)],
        ),
        (
            [(1, 1), (2, 2), (3, 3)],
            3,
            [(1, 1), (2, 2), (3, 3)],
        ),
        (
            [],
            0,
            [],
        ),
    ]

    for i, (data, expected_count, expected_ordered) in enumerate(test_cases):
        count = unique_count_set(data)
        ordered = unique_points_ordered(data)
        assert count == expected_count, (
            f"Test {i+1} (count) failed: expected {expected_count}, got {count}"
        )
        assert ordered == expected_ordered, (
            f"Test {i+1} (order) failed: expected {expected_ordered}, got {ordered}"
        )
        print(f"Test {i+1} passed: {data} -> count={count}, unique={ordered}")

    print("\nAll tests passed!")
