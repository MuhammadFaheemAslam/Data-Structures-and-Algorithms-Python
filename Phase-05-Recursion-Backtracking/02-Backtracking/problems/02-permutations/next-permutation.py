"""
Problem: Next Permutation

Difficulty: Medium (LeetCode #31)

---------------------------------------------------
Problem Statement:

Given an array `nums`, rearrange it into the LEXICOGRAPHICALLY NEXT
GREATER permutation of numbers. If no such permutation exists (the
array is already the largest permutation), rearrange it as the
LOWEST permutation instead.

Must be done IN PLACE with O(1) extra memory.

    nums = [1, 2, 3]  →  [1, 3, 2]
    nums = [3, 2, 1]  →  [1, 2, 3]           (wrap around)
    nums = [1, 1, 5]  →  [1, 5, 1]

---------------------------------------------------
Why This Problem Is Here:

Unlike most backtracking problems, this one ISN'T backtracking —
it's a clever in-place algorithm on permutations. We include it in
the permutations sub-module because it teaches a DIFFERENT, complementary
skill:

    Backtracking generates ALL permutations (exponential output).
    "Next permutation" advances BETWEEN permutations in O(n) without
    generating the others.

If you need to iterate through permutations one at a time (for
testing, brute-force search, etc.), calling `next_permutation`
repeatedly is dramatically more memory-efficient than generating
all n! upfront.

---------------------------------------------------
The Algorithm (3 Steps):

    1. SCAN FROM THE RIGHT to find the first index `i` where
       nums[i] < nums[i+1]. Call this the "pivot."
       (If no such i exists, the array is the largest permutation;
       just reverse it.)

    2. SCAN FROM THE RIGHT again to find the first index `j` where
       nums[j] > nums[pivot]. (Such a j always exists because
       nums[pivot+1] > nums[pivot] at minimum.)

    3. SWAP nums[pivot] with nums[j].

    4. REVERSE the suffix nums[pivot+1:] to put it in ascending order.

Time:  O(n)
Space: O(1)

---------------------------------------------------
Worked Example:

    nums = [1, 3, 5, 4, 2]

    Step 1: scan right → right. Indices 4→3: 2 < 4 but we want the
            pivot where nums[i] < nums[i+1]. The first such pair
            going RIGHT → LEFT is:
            i=3: 4 > 2 — no
            i=2: 5 > 4 — no
            i=1: 3 < 5 — YES! pivot = 1.

    Step 2: scan right → left for the first j > pivot with nums[j] > nums[pivot]=3.
            i=4: 2 < 3 — no
            i=3: 4 > 3 — YES! j = 3.

    Step 3: swap nums[1] and nums[3]. arr becomes [1, 4, 5, 3, 2].

    Step 4: reverse the suffix nums[2:]. arr becomes [1, 4, 2, 3, 5].

    Answer: [1, 4, 2, 3, 5].
"""


# =========================================================================
# The O(n) Algorithm
# =========================================================================

def next_permutation(nums):
    """
    Rearrange `nums` to its lexicographic NEXT permutation IN PLACE.

    If already the maximum permutation, reset to the minimum.

    Time:  O(n)
    Space: O(1)
    """
    n = len(nums)
    if n <= 1:
        return

    # Step 1: find the pivot — rightmost i such that nums[i] < nums[i+1]
    pivot = n - 2
    while pivot >= 0 and nums[pivot] >= nums[pivot + 1]:
        pivot -= 1

    if pivot == -1:
        # Array is the LARGEST permutation; reset to smallest = reversed
        nums.reverse()
        return

    # Step 2: find rightmost j with nums[j] > nums[pivot]
    j = n - 1
    while nums[j] <= nums[pivot]:
        j -= 1

    # Step 3: swap
    nums[pivot], nums[j] = nums[j], nums[pivot]

    # Step 4: reverse the suffix after `pivot`
    left, right = pivot + 1, n - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1


# =========================================================================
# Previous Permutation (Mirror Algorithm — LC #1053 is a variant)
# =========================================================================

def previous_permutation(nums):
    """
    Rearrange `nums` to its lexicographic PREVIOUS permutation.

    Symmetric to next_permutation, with ≤ flipped to ≥ etc.

    Time:  O(n)
    Space: O(1)
    """
    n = len(nums)
    if n <= 1:
        return

    # Step 1: find rightmost pivot where nums[pivot] > nums[pivot + 1]
    pivot = n - 2
    while pivot >= 0 and nums[pivot] <= nums[pivot + 1]:
        pivot -= 1

    if pivot == -1:
        # Already the smallest — reset to the largest
        nums.reverse()
        return

    # Step 2: find rightmost j with nums[j] < nums[pivot]
    j = n - 1
    while nums[j] >= nums[pivot]:
        j -= 1

    # Step 3: swap
    nums[pivot], nums[j] = nums[j], nums[pivot]

    # Step 4: reverse the suffix
    left, right = pivot + 1, n - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1


# =========================================================================
# Bonus: Iterate All Permutations via Repeated `next_permutation`
# =========================================================================

def all_permutations_via_next(nums):
    """
    Generate all permutations by starting with the SMALLEST (sorted)
    and repeatedly calling `next_permutation` until we wrap.

    Useful as a memory-efficient alternative to generating all n!
    permutations at once.

    Time:  O(n · n!)
    Space: O(n) for the rolling array
    """
    nums = sorted(nums)                           # start at the smallest
    seen = []
    while True:
        seen.append(nums[:])
        next_permutation(nums)
        if nums == sorted(nums):                  # we've wrapped back to the start
            break

    # If there was only one permutation (all-same array), we stopped immediately.
    return seen


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    cases = [
        # (input, expected after next_permutation)
        ([1, 2, 3],                [1, 3, 2]),
        ([3, 2, 1],                [1, 2, 3]),         # wraps around
        ([1, 1, 5],                [1, 5, 1]),
        ([1],                      [1]),
        ([],                       []),
        ([1, 2],                   [2, 1]),
        ([2, 1],                   [1, 2]),
        ([1, 3, 5, 4, 2],          [1, 4, 2, 3, 5]),   # worked example
        ([1, 5, 1],                [5, 1, 1]),
        ([2, 3, 1],                [3, 1, 2]),
        ([1, 1, 1],                [1, 1, 1]),         # only one permutation
    ]

    for nums, expected in cases:
        arr = list(nums)
        next_permutation(arr)
        assert arr == expected, f"next_permutation({nums}) = {arr}, expected {expected}"
        print(f"   next({nums}) = {arr}")
    print()

    # previous_permutation — mirror
    prev_cases = [
        ([1, 3, 2],                [1, 2, 3]),
        ([3, 2, 1],                [3, 1, 2]),
        ([1, 2, 3],                [3, 2, 1]),         # wraps around
        ([1],                      [1]),
    ]

    for nums, expected in prev_cases:
        arr = list(nums)
        previous_permutation(arr)
        assert arr == expected, f"previous({nums}) = {arr}, expected {expected}"
        print(f"   previous({nums}) = {arr}")
    print()

    # Iterate all permutations via next
    for nums in [[1, 2, 3], [1, 1, 2]]:
        all_perms = all_permutations_via_next(nums)
        from itertools import permutations
        expected = sorted(set(permutations(nums)))
        got = sorted(tuple(p) for p in all_perms)
        assert got == expected, f"mismatch on {nums}: {got} vs {expected}"
        print(f"   all permutations of {nums} (via repeated next): {len(got)}")

    # next then previous should return to the original (when not at an edge)
    import random
    random.seed(42)
    for _ in range(100):
        n = random.randint(2, 8)
        original = sorted(random.sample(range(100), n))
        # Move forward, then back — should equal original
        arr = list(original)
        if arr != sorted(arr, reverse=True):          # not at the top
            next_permutation(arr)
            previous_permutation(arr)
            assert arr == original

    print("\nStress test: 100 random arrays — next+previous is the identity (at non-edge positions)")

    print("\nAll tests passed!")

    # ---------------------------------------------------------------
    # Why `next_permutation` Is Beautiful:
    #
    #   Three observations:
    #
    #     1. The SUFFIX after the pivot is always in DESCENDING order.
    #        (Otherwise we'd have found a later pivot.)
    #     2. We want to SWAP the pivot with the SMALLEST value in the
    #        suffix that's still GREATER than the pivot — this gives
    #        the "least change" that increases the number.
    #     3. After the swap, the suffix is still DESCENDING, so
    #        REVERSING it gives us the smallest possible suffix —
    #        the "next" permutation.
    #
    # Four O(1) steps + one O(n) reverse = O(n) total. It's the
    # algorithm behind C++'s `std::next_permutation` and Python's
    # `itertools.permutations` (which internally yields one at a
    # time via this exact logic).
    # ---------------------------------------------------------------
