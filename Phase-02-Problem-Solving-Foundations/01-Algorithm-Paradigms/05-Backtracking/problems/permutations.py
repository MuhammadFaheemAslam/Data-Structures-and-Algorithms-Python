"""
Problem: Permutations

Paradigm: Backtracking — the cleanest demonstration of choose/explore/un-choose
Difficulty: Medium (LeetCode #46 and #47)

---------------------------------------------------
Problem Statement:

Given a list of `nums`, return every possible PERMUTATION (ordering).

Variants:
    1. `nums` contains all distinct values → n! permutations, all unique.
    2. `nums` may contain duplicates       → fewer than n! unique orderings.
                                             We want each unique one exactly once.

---------------------------------------------------
The Backtracking Lens:

This is the purest form of backtracking. The decision tree is:

    Position 0: pick any unused element.
    Position 1: pick any remaining unused element.
    ...
    Position n-1: the only remaining element.

Every leaf of that tree is a complete permutation. No invalid states
— so the only "pruning" we need is the book-keeping to not reuse an
element within the same permutation.

That makes permutations the ideal first problem to see the three-step
backtracking template at its cleanest:

    CHOOSE      → append to the running path, mark as used
    EXPLORE     → recurse
    UN-CHOOSE   → pop from the path, mark as unused

---------------------------------------------------
Example:

    permute([1, 2, 3]) →
        [[1, 2, 3], [1, 3, 2],
         [2, 1, 3], [2, 3, 1],
         [3, 1, 2], [3, 2, 1]]

    permute([1, 1, 2]) →
        [[1, 1, 2], [1, 2, 1], [2, 1, 1]]   ← unique only

---------------------------------------------------
"""

# -------------------------------------------------
# Variant 1: Distinct Elements
# -------------------------------------------------

def permute(nums):
    """
    Return every permutation of `nums` (assumed distinct).

    Time Complexity:  O(n * n!)
        n! permutations, each of length n to copy into the result.
    Space Complexity: O(n) for the recursion stack + O(n * n!) for output.
    """
    result = []
    path = []
    used = [False] * len(nums)

    def backtrack():
        if len(path) == len(nums):
            result.append(path[:])              # SNAPSHOT
            return

        for i in range(len(nums)):
            if used[i]:
                continue

            # CHOOSE
            path.append(nums[i])
            used[i] = True

            # EXPLORE
            backtrack()

            # UN-CHOOSE
            path.pop()
            used[i] = False

    backtrack()
    return result


# -------------------------------------------------
# Variant 2: With Duplicates — Skip Repeats
# -------------------------------------------------

def permute_unique(nums):
    """
    Return every UNIQUE permutation of `nums` (duplicates allowed in input).

    The trick: sort the input so identical values sit adjacent. Then during
    enumeration, skip a candidate if:
        (a) it's the same value as the one immediately preceding it, AND
        (b) the preceding one is NOT currently used in the running path.

    Condition (b) is the subtle part. It means: "we're starting a fresh
    branch with a duplicate value, but a previous branch already covered
    this value at this position. Skip."

    Time Complexity:  O(n * n!)
    Space Complexity: O(n) recursion stack
    """
    result = []
    path = []
    nums = sorted(nums)                         # group duplicates together
    used = [False] * len(nums)

    def backtrack():
        if len(path) == len(nums):
            result.append(path[:])
            return

        for i in range(len(nums)):
            if used[i]:
                continue
            # skip duplicates: if the same value was already explored at
            # this position by the previous branch, don't redo it
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue

            path.append(nums[i])
            used[i] = True

            backtrack()

            path.pop()
            used[i] = False

    backtrack()
    return result


# -------------------------------------------------
# Alternative: Immutable-Path Style (No Un-Choose)
# -------------------------------------------------

def permute_immutable(nums):
    """
    Same output as permute(), but using a CLEANER-LOOKING pattern
    that allocates a new list at each recursive call instead of
    mutating a shared path.

    Pattern B from theory.md — slower, but no un-choose step to forget.

    Time Complexity:  O(n * n!) — plus list-allocation overhead
    Space Complexity: O(n^2) recursion depth with copies
    """
    if len(nums) == 0:
        return [[]]

    result = []
    for i in range(len(nums)):
        rest = nums[:i] + nums[i + 1:]          # everything except nums[i]
        for perm in permute_immutable(rest):    # recurse on rest
            result.append([nums[i]] + perm)
    return result


# -------------------------------------------------
# Test the Functions
# -------------------------------------------------

if __name__ == "__main__":
    import math

    # distinct elements
    for nums in [[1, 2, 3], [1, 2], [1], []]:
        got = permute(nums)
        got_immut = permute_immutable(nums)
        expected_count = math.factorial(len(nums)) if nums else 1

        assert len(got) == expected_count, (
            f"permute({nums}) returned {len(got)} perms, expected {expected_count}"
        )
        # normalize order for comparison
        assert sorted(got) == sorted(got_immut), (
            f"permute / permute_immutable disagreed on {nums}"
        )
        # every permutation should be a reordering of `nums`
        for p in got:
            assert sorted(p) == sorted(nums), (
                f"bad permutation {p} of {nums}"
            )
        print(f"permute({nums}): {len(got)} permutation(s)   ✓")

    print()

    # with duplicates
    dup_tests = [
        ([1, 1, 2], 3),
        ([1, 1, 1], 1),
        ([1, 2, 2], 3),
        ([1, 2, 3], 6),
        ([], 1),                                # one "empty permutation"
    ]
    for nums, expected in dup_tests:
        got = permute_unique(nums)
        assert len(got) == expected, (
            f"permute_unique({nums}) returned {len(got)}, expected {expected}"
        )
        # no duplicates in the result
        assert len(got) == len({tuple(p) for p in got}), (
            f"permute_unique({nums}) returned duplicates: {got}"
        )
        print(f"permute_unique({nums}): {got}   ✓")

    # Show off a larger case
    print()
    n = 4
    perms = permute(list(range(n)))
    print(f"permute(range({n})): got {len(perms)} permutations (expected {math.factorial(n)})")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Why This Problem Matters:
    #
    #   permute() is the CLEANEST showcase of the backtracking template.
    #   Every single line of the solution maps to one of the three steps:
    #
    #       for i in range(len(nums)):       ← candidate loop
    #           if used[i]: continue         ← feasibility pruning
    #           path.append(nums[i])         ← CHOOSE
    #           used[i] = True               ← update state
    #           backtrack()                  ← EXPLORE
    #           path.pop()                   ← UN-CHOOSE
    #           used[i] = False              ← revert state
    #
    #   Once you can write this function from memory, every other
    #   backtracking problem is a variation on the same skeleton.
    # ---------------------------------------------------------------
