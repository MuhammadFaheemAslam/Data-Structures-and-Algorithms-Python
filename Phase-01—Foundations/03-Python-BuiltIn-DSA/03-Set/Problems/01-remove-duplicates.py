"""
Problem 01: Remove Duplicates from a List

Difficulty: Easy

---------------------------------------------------
Problem Statement:

Given a list of values, return a new list with all duplicates removed.

Provide two versions:
1. A fast version that does NOT preserve original order (uses set()).
2. A fast version that DOES preserve order of first appearance.

This problem highlights the #1 everyday use of sets: deduplication.

---------------------------------------------------
Example:

Input:
    [1, 2, 2, 3, 1, 4, 3, 5]

Output:
    unordered: [1, 2, 3, 4, 5]    # any order
    ordered:   [1, 2, 3, 4, 5]    # first appearance preserved

---------------------------------------------------
"""

# -------------------------------------------------
# Approach 1: Using set() (Simple & Fast, Order Lost)
# -------------------------------------------------

def dedupe_unordered(items):
    """
    Drop the whole list into a set, then convert back to a list.

    Time Complexity: O(n)   – each element hashed once
    Space Complexity: O(n)  – the set + the returned list

    Downside: iteration order of a set is NOT guaranteed.
    If you need the original order, use dedupe_ordered().
    """
    return list(set(items))


# -------------------------------------------------
# Approach 2: Preserve First-Appearance Order (Interview Friendly)
# -------------------------------------------------

def dedupe_ordered(items):
    """
    Walk the list once, keeping a `seen` set for O(1) lookups
    and an output list for order.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    seen = set()
    result = []

    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)

    return result


# -------------------------------------------------
# Approach 3: dict.fromkeys() (Shortest Correct Answer)
# -------------------------------------------------

def dedupe_dict(items):
    """
    Since Python 3.7, dicts preserve insertion order. We can abuse
    that to dedupe while keeping order in one clean line.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    return list(dict.fromkeys(items))


# -------------------------------------------------
# Approach 4: Brute Force – Nested Loop (Anti-Pattern)
# -------------------------------------------------

def dedupe_bruteforce(items):
    """
    For each element, check if it's already in the result list.
    Simple but SLOW – included to show the cost of not using a set.

    Time Complexity: O(n^2)  – `x in list` is O(n) each call
    Space Complexity: O(n)
    """
    result = []
    for item in items:
        if item not in result:           # O(n) linear scan!
            result.append(item)
    return result


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    data = [1, 2, 2, 3, 1, 4, 3, 5]

    print("Input:", data)
    print("dedupe_unordered:  ", sorted(dedupe_unordered(data)), "(sorted for display)")
    print("dedupe_ordered:    ", dedupe_ordered(data))
    print("dedupe_dict:       ", dedupe_dict(data))
    print("dedupe_bruteforce: ", dedupe_bruteforce(data))
    print()

    # Test cases for the order-preserving version
    test_cases = [
        ([1, 2, 2, 3, 1, 4, 3, 5], [1, 2, 3, 4, 5]),
        (["a", "b", "a", "c", "b"], ["a", "b", "c"]),
        ([], []),
        ([7, 7, 7, 7], [7]),
        ([1, 2, 3], [1, 2, 3]),             # already unique
    ]

    for i, (data, expected) in enumerate(test_cases):
        result = dedupe_ordered(data)
        assert result == expected, f"Test {i+1} failed: expected {expected}, got {result}"
        print(f"Test {i+1} passed: {data} -> {result}")

    print("\nAll tests passed!")
