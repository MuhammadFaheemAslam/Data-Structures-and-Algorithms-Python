"""
Problem: Majority Element

Technique: Frequency Counting — with a surprise O(1)-space algorithm
Difficulty: Easy (LeetCode #169)

---------------------------------------------------
Problem Statement:

Given an array `nums` of size n, return the majority element — the
element that appears MORE than ⌊n/2⌋ times.

You may assume a majority element exists in the input.

---------------------------------------------------
Why This Problem Matters:

On the surface, it's a classic frequency-counting problem — build a
Counter, pick the max. That works in O(n) time, O(n) space.

But there's a classical O(n)-time, **O(1)-space** algorithm:
**Boyer-Moore Voting**. It's the canonical reminder that when a
problem *looks* like frequency counting, there might be a slicker
approach that avoids the counter entirely.

We show four approaches side by side:

    1. Hash counter             — O(n) time, O(n) space
    2. Sort, take middle        — O(n log n) time, O(1) space (or O(n))
    3. Bit-by-bit voting        — O(32n) = O(n) time, O(1) space (bitwise voting)
    4. Boyer-Moore Voting       — O(n) time, O(1) space  ← the right answer

---------------------------------------------------
Why Boyer-Moore Works:

Invariant: at any point in the scan, `candidate` is a value that
"survives" against everything seen so far; `count` is the surplus of
candidate votes over non-candidate votes.

When count == 0, no single value is currently "winning" — so pick the
next element as the new candidate and start counting again.

When the scan ends, since the majority appears MORE than n/2 times,
it necessarily wins the tournament against every other element paired
off — so `candidate` holds the majority.

Note: this algorithm REQUIRES a majority to exist. If not, it will
return some arbitrary element. A second pass can verify.

---------------------------------------------------
Example:

    nums = [2, 2, 1, 1, 1, 2, 2]
    -> 2       (appears 4 times out of 7)

---------------------------------------------------
"""

from collections import Counter


# -------------------------------------------------
# Approach 1: Hash Counter (The "Obvious" Solution)
# -------------------------------------------------

def majority_element_counter(nums):
    """
    Build a Counter, return its most-common element.

    Time Complexity:  O(n)
    Space Complexity: O(n)
    """
    return Counter(nums).most_common(1)[0][0]


# -------------------------------------------------
# Approach 2: Sort, Return Middle
# -------------------------------------------------

def majority_element_sort(nums):
    """
    Since the majority appears > n/2 times, sorting places it at the
    middle regardless of where duplicates land.

    Time Complexity:  O(n log n)
    Space Complexity: O(n) (sorted() returns a new list; use list.sort()
                             in place for O(1) extra space).
    """
    return sorted(nums)[len(nums) // 2]


# -------------------------------------------------
# Approach 3: Boyer-Moore Voting (The Good Answer)
# -------------------------------------------------

def majority_element_boyer_moore(nums):
    """
    Boyer-Moore Voting — O(n) time, O(1) space.

    candidate:  the current "leader"
    count:      net surplus of leader votes over non-leader votes

    When count == 0, we haven't seen a net majority yet — pick the next
    element as the fresh candidate. When the scan ends, the majority
    (if one exists) survives as the candidate.

    Time Complexity:  O(n)
    Space Complexity: O(1)

    Note: this assumes a majority EXISTS. If not, it returns whichever
    element happened to be the final candidate. For problem inputs
    guaranteeing a majority (LC #169), that's a non-issue.
    """
    candidate = None
    count = 0

    for x in nums:
        if count == 0:
            candidate = x
        count += 1 if x == candidate else -1

    return candidate


# -------------------------------------------------
# Approach 4: Bit-by-Bit Voting (Educational)
# -------------------------------------------------

def majority_element_bitwise(nums):
    """
    For each bit position, count how many numbers have that bit set.
    If more than half do, the majority element also has that bit set.

    Time Complexity:  O(32 * n) = O(n) (for 32-bit ints)
    Space Complexity: O(1)

    Educational only — Boyer-Moore is simpler and has a smaller constant.
    Assumes 32-bit non-negative ints.
    """
    result = 0
    n = len(nums)
    for bit in range(32):
        mask = 1 << bit
        count = sum(1 for x in nums if x & mask)
        if count > n // 2:
            result |= mask
    return result


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    nums = [2, 2, 1, 1, 1, 2, 2]
    print(f"nums = {nums}")
    print(f"majority_element_counter:     {majority_element_counter(nums)}")
    print(f"majority_element_sort:        {majority_element_sort(nums)}")
    print(f"majority_element_boyer_moore: {majority_element_boyer_moore(nums)}")
    print(f"majority_element_bitwise:     {majority_element_bitwise(nums)}")
    print()

    # Test cases — (nums, expected)
    # All inputs guarantee a majority element exists.
    test_cases = [
        ([3, 2, 3],                  3),
        ([2, 2, 1, 1, 1, 2, 2],      2),
        ([1],                        1),
        ([6, 6, 6, 6, 6, 1, 2, 3, 4], 6),
        ([4, 4, 4, 5, 4],            4),
        ([0, 0, 1],                  0),
        ([1, 1, 2, 2, 1],            1),
    ]

    for i, (data, expected) in enumerate(test_cases):
        for fn in (
            majority_element_counter,
            majority_element_sort,
            majority_element_boyer_moore,
            majority_element_bitwise,
        ):
            got = fn(data)
            assert got == expected, (
                f"Test {i+1} ({fn.__name__}) failed on {data}: "
                f"expected {expected}, got {got}"
            )
        print(f"Test {i+1} passed: {data} -> {expected}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # The Four Approaches Summary:
    #
    #                              time          space    notes
    #   Counter                    O(n)          O(n)     obvious; uses extra memory
    #   Sort                       O(n log n)    O(n)     short; slower than necessary
    #   Boyer-Moore                O(n)          O(1)     ← classic answer
    #   Bit-by-bit                 O(n)          O(1)     elegant but limited to ints
    #
    # Boyer-Moore is the "textbook" answer. When an interview asks
    # "can you do it in O(1) space?", this is what they want.
    # ---------------------------------------------------------------
