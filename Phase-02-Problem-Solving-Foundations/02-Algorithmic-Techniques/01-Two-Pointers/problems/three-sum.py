"""
Problem: 3Sum

Technique: Two Pointers (converging) + outer loop + duplicate skipping
Difficulty: Medium (LeetCode #15)

---------------------------------------------------
Problem Statement:

Given an array `nums`, return all UNIQUE triples `(a, b, c)` such that
a + b + c == 0 and the indices are all distinct.

The returned triples themselves must be unique — no triple appears twice.

---------------------------------------------------
The Two-Pointer Lens:

Brute force is O(n^3): check every triple. That's unusable past
n ~ 1000. The two-pointer insight is:

    "Fix the outermost element a. Then we need b + c = -a. On a SORTED
    array, that's just a two-pointer pair search — O(n). Repeating over
    all choices of a gives O(n^2)."

So the overall structure is:

    Sort input                             O(n log n)
    For each `a`:                          n iterations
        Two-pointer search for b + c       O(n) each
    Total:                                 O(n^2)

The subtle parts are all in the DEDUPLICATION. There are three places
where duplicates would otherwise creep into the result:

    1. The outer `a` loop: if nums[i] == nums[i-1] and we already ran
       the two-pointer search for that value, skip.
    2. After a successful match, ADVANCE left past any equal neighbours
       (so the same `b` value isn't reused).
    3. Similarly for the right pointer.

Get any of these wrong and you'll return duplicate triples.

Time Complexity:  O(n^2)
Space Complexity: O(1) beyond the output (sort can be in place)

---------------------------------------------------
Example:

    nums = [-1, 0, 1, 2, -1, -4]
    Output (order-independent):
        [[-1, -1, 2], [-1, 0, 1]]

---------------------------------------------------
"""

# -------------------------------------------------
# The Two-Pointer Solution
# -------------------------------------------------

def three_sum(nums):
    """
    Return all unique triples (a, b, c) from nums with a + b + c == 0.

    Approach:
        1. Sort.
        2. Fix each `a = nums[i]`; two-pointer search the tail nums[i+1:]
           for a pair summing to -a.
        3. Skip duplicates at i, left, and right to avoid repeat triples.

    Time Complexity:  O(n^2)
    Space Complexity: O(1) beyond the output
    """
    nums = sorted(nums)
    n = len(nums)
    result = []

    for i in range(n - 2):
        # outer duplicate skip: we've already handled this value of `a`
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        # small optimization: if a > 0 we can never sum to 0 with b, c ≥ a
        if nums[i] > 0:
            break

        target = -nums[i]
        left, right = i + 1, n - 1

        while left < right:
            s = nums[left] + nums[right]

            if s == target:
                result.append([nums[i], nums[left], nums[right]])

                # advance past duplicates on BOTH sides
                left += 1
                right -= 1
                while left < right and nums[left] == nums[left - 1]:
                    left += 1
                while left < right and nums[right] == nums[right + 1]:
                    right -= 1
            elif s < target:
                left += 1
            else:
                right -= 1

    return result


# -------------------------------------------------
# Brute Force for Verification
# -------------------------------------------------

def three_sum_brute_force(nums):
    """
    O(n^3) reference — used only to verify the two-pointer result on
    small inputs.
    """
    n = len(nums)
    seen = set()
    result = []
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if nums[i] + nums[j] + nums[k] == 0:
                    triple = tuple(sorted([nums[i], nums[j], nums[k]]))
                    if triple not in seen:
                        seen.add(triple)
                        result.append(list(triple))
    return result


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    nums = [-1, 0, 1, 2, -1, -4]
    print(f"nums = {nums}")
    print(f"three_sum:             {sorted(three_sum(nums))}")
    print(f"three_sum_brute_force: {sorted(three_sum_brute_force(nums))}")
    print()

    # Test cases — (nums, expected_normalized_result)
    test_cases = [
        (
            [-1, 0, 1, 2, -1, -4],
            [[-1, -1, 2], [-1, 0, 1]],
        ),
        (
            [0, 1, 1],
            [],
        ),
        (
            [0, 0, 0],
            [[0, 0, 0]],
        ),
        (
            [0, 0, 0, 0],
            [[0, 0, 0]],
        ),
        (
            [],
            [],
        ),
        (
            [1, 2, 3],
            [],
        ),
        (
            [-2, 0, 1, 1, 2],
            [[-2, 0, 2], [-2, 1, 1]],
        ),
        (
            [-1, -1, -1, 2, 2],
            [[-1, -1, 2]],
        ),
    ]

    for i, (data, expected) in enumerate(test_cases):
        got = sorted(three_sum(data))
        exp = sorted(expected)
        assert got == exp, (
            f"Test {i+1} failed on {data}: expected {exp}, got {got}"
        )
        # cross-check with brute force
        bf = sorted(three_sum_brute_force(data))
        assert got == bf, (
            f"Test {i+1}: two-pointer ({got}) disagrees with brute force ({bf})"
        )
        print(f"Test {i+1} passed: {data} -> {got}")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Why 3Sum Is Worth Learning Cold:
    #
    #   The "fix one, two-pointer the rest" pattern generalizes:
    #
    #     K-Sum for any fixed K:
    #         recursively fix (K-2) elements, then two-pointer the remaining pair.
    #         Time: O(n^(K-1))
    #         Same deduplication rules apply at each nesting level.
    #
    #     Closest Three Sum:
    #         Same shape, track the triple whose sum is closest to target.
    #
    #     Three Sum With Multiplicity:
    #         Count triples rather than enumerate them.
    #
    # Master the 3Sum skeleton and you've mastered a family of problems.
    # ---------------------------------------------------------------
