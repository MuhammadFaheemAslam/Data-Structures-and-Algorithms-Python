"""
Problem 02: Intersection and Union of Two Lists

Difficulty: Easy

---------------------------------------------------
Problem Statement:

Given two lists, return:
1. Their intersection – elements that appear in BOTH (unique).
2. Their union        – elements that appear in EITHER (unique).

Duplicates within a single list should not appear twice in the output.

This problem highlights the other headline feature of sets:
built-in mathematical set algebra with O(n + m) cost.

---------------------------------------------------
Example:

Input:
    a = [1, 2, 2, 3, 4]
    b = [3, 4, 4, 5, 6]

Output:
    intersection = [3, 4]
    union        = [1, 2, 3, 4, 5, 6]

---------------------------------------------------
"""

# -------------------------------------------------
# Approach 1: Using Set Operators (Pythonic)
# -------------------------------------------------

def intersection_sets(a, b):
    """
    Convert both lists to sets and use the `&` operator.

    Time Complexity: O(n + m)
        O(n + m) to build the sets, then O(min(n, m)) for the
        intersection itself (Python iterates the smaller set).
    Space Complexity: O(n + m)
    """
    return sorted(set(a) & set(b))       # sorted() only so tests are stable


def union_sets(a, b):
    """
    Convert both lists to sets and use the `|` operator.

    Time Complexity: O(n + m)
    Space Complexity: O(n + m)
    """
    return sorted(set(a) | set(b))


# -------------------------------------------------
# Approach 2: Using Set Methods (Accept Any Iterable)
# -------------------------------------------------

def intersection_methods(a, b):
    """
    Equivalent to Approach 1 but using the method forms.

    Note: `set(a).intersection(b)` works even if `b` is a list;
    the method form accepts any iterable. The `&` operator would
    require both sides to be sets.
    """
    return sorted(set(a).intersection(b))


def union_methods(a, b):
    return sorted(set(a).union(b))


# -------------------------------------------------
# Approach 3: Brute Force (Anti-Pattern)
# -------------------------------------------------

def intersection_bruteforce(a, b):
    """
    For each element in `a`, linearly scan `b`.
    Also has to manually dedupe the output.

    Time Complexity: O(n * m)
    Space Complexity: O(min(n, m))

    Included to highlight the dramatic win from using a set.
    """
    result = []
    for x in a:
        if x in b and x not in result:   # both `in` calls are O(k) linear scans
            result.append(x)
    return sorted(result)


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    a = [1, 2, 2, 3, 4]
    b = [3, 4, 4, 5, 6]

    print(f"a = {a}")
    print(f"b = {b}")
    print()
    print("intersection (set ops):     ", intersection_sets(a, b))
    print("intersection (methods):     ", intersection_methods(a, b))
    print("intersection (brute force): ", intersection_bruteforce(a, b))
    print()
    print("union (set ops):            ", union_sets(a, b))
    print("union (methods):            ", union_methods(a, b))
    print()

    # Test cases – (a, b, expected_intersection, expected_union)
    test_cases = [
        ([1, 2, 2, 3, 4], [3, 4, 4, 5, 6], [3, 4],    [1, 2, 3, 4, 5, 6]),
        ([1, 2, 3],       [4, 5, 6],       [],        [1, 2, 3, 4, 5, 6]),
        ([1, 1, 1],       [1, 1, 1],       [1],       [1]),
        ([],              [1, 2, 3],       [],        [1, 2, 3]),
        ([],              [],              [],        []),
    ]

    for i, (lst_a, lst_b, exp_inter, exp_union) in enumerate(test_cases):
        got_inter = intersection_sets(lst_a, lst_b)
        got_union = union_sets(lst_a, lst_b)
        assert got_inter == exp_inter, (
            f"Test {i+1} intersection failed: expected {exp_inter}, got {got_inter}"
        )
        assert got_union == exp_union, (
            f"Test {i+1} union failed: expected {exp_union}, got {got_union}"
        )
        print(f"Test {i+1} passed: inter={got_inter}, union={got_union}")

    print("\nAll tests passed!")
