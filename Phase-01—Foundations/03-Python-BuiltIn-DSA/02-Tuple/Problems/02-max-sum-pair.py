"""
Problem 02: Find the Pair with the Maximum Sum

Difficulty: Easy

---------------------------------------------------
Problem Statement:

Given a list of tuples, where each tuple is a pair (a, b),
return the pair whose sum (a + b) is the largest.

If the input list is empty, return None.

This problem highlights how tuples are used as fixed, heterogeneous
records, and how tuple unpacking makes iteration clean and readable.

---------------------------------------------------
Example:

Input:
    [(1, 2), (3, 4), (5, 1), (2, 8)]

Output:
    (2, 8)     # because 2 + 8 = 10 is the largest sum

---------------------------------------------------
"""

# -------------------------------------------------
# Approach 1: Using max() with a Key Function (Pythonic)
# -------------------------------------------------

def max_sum_pair_builtin(pairs):
    """
    Use the built-in max() with key=sum so the largest sum wins.

    Time Complexity: O(n)   – one pass, computing sum per pair
    Space Complexity: O(1)  – no extra list created
    """
    if not pairs:
        return None

    return max(pairs, key=sum)


# -------------------------------------------------
# Approach 2: Manual Traversal with Unpacking (Interview Friendly)
# -------------------------------------------------

def max_sum_pair_manual(pairs):
    """
    Traverse the list, unpack each tuple, and track the best pair.

    Notice how `for a, b in pairs` unpacks each tuple directly into
    two named variables — this is one of the biggest readability wins
    of using tuples for structured records.

    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    if not pairs:
        return None

    # Assume the first pair is the best
    best_pair = pairs[0]
    best_sum = best_pair[0] + best_pair[1]

    for a, b in pairs[1:]:
        current_sum = a + b
        if current_sum > best_sum:
            best_sum = current_sum
            best_pair = (a, b)

    return best_pair


# -------------------------------------------------
# Approach 3: Sort by Sum, Pick the Last (Brute Force)
# -------------------------------------------------

def max_sum_pair_sorted(pairs):
    """
    Sort the list by each pair's sum, then return the last element.

    Works but is strictly worse than O(n) — included to show the
    tradeoff between a clean one-liner and actual efficiency.

    Time Complexity: O(n log n)
    Space Complexity: O(n)   – sorted() returns a new list
    """
    if not pairs:
        return None

    return sorted(pairs, key=sum)[-1]


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    pairs = [(1, 2), (3, 4), (5, 1), (2, 8)]

    print("Input pairs:", pairs)
    print("max_sum_pair_builtin: ", max_sum_pair_builtin(pairs))
    print("max_sum_pair_manual:  ", max_sum_pair_manual(pairs))
    print("max_sum_pair_sorted:  ", max_sum_pair_sorted(pairs))
    print()

    # Test cases – (input, expected)
    test_cases = [
        ([(1, 2), (3, 4), (5, 1), (2, 8)], (2, 8)),
        ([(10, 20)], (10, 20)),
        ([(-1, -2), (-3, -4), (0, 0)], (0, 0)),
        ([(1, 1), (2, 0), (0, 2)], (1, 1)),   # ties: first max wins (max() behavior)
        ([], None),
    ]

    for i, (data, expected) in enumerate(test_cases):
        result = max_sum_pair_manual(data)
        assert result == expected, f"Test {i+1} failed: expected {expected}, got {result}"
        print(f"Test {i+1} passed: {data} -> {result}")

    print("\nAll tests passed!")
