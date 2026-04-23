"""
Problem: Count Inversions

Technique: Merge Sort — modifying the merge step to count swaps.
Difficulty: Medium (classic interview / GeeksforGeeks problem)

---------------------------------------------------
Problem Statement:

An INVERSION in an array is a pair of indices (i, j) with:

    i < j    AND    arr[i] > arr[j]

Return the total number of inversions.

    arr = [2, 4, 1, 3, 5]
    inversions: (2,1), (4,1), (4,3)  → count 3

Intuitively, inversions measure "how far from sorted" the array is.
A sorted array has 0 inversions; a reverse-sorted array has n(n-1)/2.

---------------------------------------------------
Why Merge Sort?

Brute force is O(n²): check every pair. Fine for small n.

Merge sort can count inversions in **O(n log n)**. The key insight:

    During the MERGE step, whenever we pick an element from the RIGHT
    half before one from the LEFT half, every remaining element in the
    LEFT half forms an INVERSION with that right-half element.

So we count inversions as a side-effect of sorting. Same Big-O as
merge sort; essentially the same code with one extra counter.

This is the textbook example of "merge sort as a tool for solving
problems OTHER than sorting."

---------------------------------------------------
The Algorithm:

    def count_inversions(arr):
        arr, inv = merge_sort_with_count(arr)
        return inv

    merge_sort_with_count: return (sorted_list, inversion_count)
    merge_with_count: during merge, if right[j] < left[i],
                      accumulate len(left) - i inversions.

---------------------------------------------------
Example:

    arr = [8, 4, 2, 1]
    inversions: (8,4), (8,2), (8,1), (4,2), (4,1), (2,1) → 6
    (This is n(n-1)/2 = 6 for a strictly decreasing array — the maximum.)

---------------------------------------------------
"""

# =========================================================================
# Solution: Merge Sort with Inversion Counting — O(n log n)
# =========================================================================

def count_inversions(arr):
    """
    Return the number of inversions in `arr`.

    Time:   O(n log n)
    Space:  O(n)

    Does not mutate `arr`.
    """
    _, count = _merge_sort_with_count(arr)
    return count


def _merge_sort_with_count(arr):
    """
    Merge sort that also returns the inversion count.

    Returns (sorted_list, inversion_count).
    """
    if len(arr) <= 1:
        return arr[:], 0

    mid = len(arr) // 2
    left,  inv_left  = _merge_sort_with_count(arr[:mid])
    right, inv_right = _merge_sort_with_count(arr[mid:])
    merged, inv_split = _merge_with_count(left, right)

    return merged, inv_left + inv_right + inv_split


def _merge_with_count(left, right):
    """
    Merge two sorted lists and count SPLIT inversions — pairs (i, j)
    where arr[i] is in `left`, arr[j] is in `right`, and left[i] > right[j].

    Whenever we append a right[j] before the left is exhausted, all
    remaining left elements are larger than right[j] (left is sorted),
    so they form `len(left) - i` new inversions.
    """
    merged = []
    i = j = 0
    inversions = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
            inversions += len(left) - i           # the critical accumulator

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, inversions


# =========================================================================
# Brute Force — O(n²) Reference
# =========================================================================

def count_inversions_brute(arr):
    """
    Check every pair.

    Time:   O(n²)
    Space:  O(1)

    Only used to validate the O(n log n) version on small inputs.
    """
    count = 0
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                count += 1
    return count


# =========================================================================
# Test the Functions
# =========================================================================

if __name__ == "__main__":
    # Demo
    for arr in [[2, 4, 1, 3, 5], [8, 4, 2, 1], [1, 2, 3, 4, 5],
                [5, 4, 3, 2, 1], [1], [], [3, 3, 3]]:
        fast = count_inversions(arr)
        brute = count_inversions_brute(arr)
        assert fast == brute, f"{arr}: fast={fast}, brute={brute}"
        print(f"   count_inversions({arr}) = {fast}")
    print()

    # Test cases — (arr, expected)
    test_cases = [
        ([2, 4, 1, 3, 5],          3),
        ([8, 4, 2, 1],             6),               # n(n-1)/2 max
        ([1, 20, 6, 4, 5],         5),
        ([1, 2, 3, 4, 5],          0),               # sorted — zero
        ([5, 4, 3, 2, 1],          10),              # reverse — n(n-1)/2
        ([],                       0),
        ([42],                     0),
        ([3, 3, 3, 3],             0),               # no strict inversions
        ([1, 3, 2, 4, 3],          2),               # (3,2), (4,3)
    ]

    for i, (data, expected) in enumerate(test_cases):
        fast = count_inversions(data)
        brute = count_inversions_brute(data)
        assert fast == expected and brute == expected, (
            f"Test {i+1}: expected {expected}, fast={fast}, brute={brute}"
        )
        print(f"Test {i+1} passed: arr={data} -> {fast}")

    # Stress test
    import random
    random.seed(77)
    for _ in range(200):
        n = random.randint(0, 50)
        data = [random.randint(-100, 100) for _ in range(n)]
        assert count_inversions(data) == count_inversions_brute(data)

    print("\nStress test: 200 random arrays matched brute force")

    # Large-n demo — brute force would take too long
    print()
    big = [random.randint(0, 1000) for _ in range(10_000)]
    print(f"Inversions in a 10_000-element random array: {count_inversions(big)}")
    print("(Brute force O(n²) = 10^8 comparisons; merge sort O(n log n) is instant.)")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Why This Problem Is a Classic:
    #
    #   It's the canonical example of "use a sorting algorithm to solve
    #   a problem that isn't sorting". The merge step has EXACTLY the
    #   information needed to count inversions — no extra data
    #   structures required.
    #
    # Related problems:
    #   - Count Smaller Numbers After Self (LC #315)
    #   - Reverse Pairs (LC #493)
    #   - Count of Range Sum (LC #327)
    #
    # All three use merge sort as their computational engine. Once
    # you've seen the inversion-counting trick, recognizing them is fast.
    # ---------------------------------------------------------------
