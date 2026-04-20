"""
Problem 03: Detect if a List Contains Any Duplicate

Difficulty: Easy (variant: LeetCode 217 – Contains Duplicate)

---------------------------------------------------
Problem Statement:

Given a list of values, return True if ANY value appears at least twice.
Return False if every element is distinct.

This is the canonical "O(n^2) brute force becomes O(n) with a set"
problem. The optimization is the core technique you'll reuse in
dozens of interview problems (Two Sum, Happy Number, Contains
Duplicate II, Longest Substring Without Repeating Characters, …).

---------------------------------------------------
Example:

Input:   [1, 2, 3, 1]
Output:  True

Input:   [1, 2, 3, 4]
Output:  False

---------------------------------------------------
"""

# -------------------------------------------------
# Approach 1: Compare Lengths with a set (Shortest)
# -------------------------------------------------

def has_duplicate_short(nums):
    """
    If turning the list into a set changes the length, there was a duplicate.

    Time Complexity: O(n)   – one pass to build the set
    Space Complexity: O(n)  – the set itself

    Downside: always allocates the full set, even if a duplicate
    is found on the very first pair. See Approach 2 for early exit.
    """
    return len(nums) != len(set(nums))


# -------------------------------------------------
# Approach 2: Early-Exit Traversal (Interview Friendly)
# -------------------------------------------------

def has_duplicate_early_exit(nums):
    """
    Walk the list once; bail the moment a repeat is spotted.

    Time Complexity: O(n) worst case, much faster on average
                     – stops as soon as the first duplicate appears.
    Space Complexity: O(n) worst case – the `seen` set can grow to n.

    This is the version to write in an interview: same big-O as
    Approach 1, but tangibly faster on "contains a duplicate early"
    inputs because it avoids hashing the tail of the list.
    """
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False


# -------------------------------------------------
# Approach 3: Brute Force – Nested Loop (Anti-Pattern)
# -------------------------------------------------

def has_duplicate_bruteforce(nums):
    """
    Compare every pair of elements.

    Time Complexity: O(n^2)
    Space Complexity: O(1)

    Included to show the before/after. For n = 10,000 this does
    ~50 million comparisons; the set-based versions do 10,000 hashes.
    """
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] == nums[j]:
                return True
    return False


# -------------------------------------------------
# Approach 4: Sort First, Then Check Adjacent Pairs
# -------------------------------------------------

def has_duplicate_sort(nums):
    """
    If the list is sorted, any duplicates must be adjacent.

    Time Complexity: O(n log n) – dominated by sorting
    Space Complexity: O(n)      – sorted() returns a new list

    Worse than the set-based approaches, but doesn't need a hash
    table – useful when memory is very tight or elements aren't
    hashable but ARE comparable.
    """
    ordered = sorted(nums)
    for i in range(1, len(ordered)):
        if ordered[i] == ordered[i - 1]:
            return True
    return False


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    samples = [
        [1, 2, 3, 1],                     # True
        [1, 2, 3, 4],                     # False
        [],                               # False
        [7],                              # False
        [1, 1, 1, 1],                     # True
        ["a", "b", "c", "a"],             # True
    ]

    for sample in samples:
        print(f"{sample!r:30} -> {has_duplicate_early_exit(sample)}")
    print()

    # Test cases – (input, expected)
    test_cases = [
        ([1, 2, 3, 1],        True),
        ([1, 2, 3, 4],        False),
        ([],                  False),
        ([7],                 False),
        ([1, 1],              True),
        ([1, 2, 3, 4, 5],     False),
        (["a", "b", "a"],     True),
    ]

    for i, (data, expected) in enumerate(test_cases):
        for fn in (
            has_duplicate_short,
            has_duplicate_early_exit,
            has_duplicate_bruteforce,
            has_duplicate_sort,
        ):
            got = fn(data)
            assert got == expected, (
                f"Test {i+1} ({fn.__name__}) failed on {data}: "
                f"expected {expected}, got {got}"
            )
        print(f"Test {i+1} passed: {data} -> {expected}")

    print("\nAll tests passed!")
